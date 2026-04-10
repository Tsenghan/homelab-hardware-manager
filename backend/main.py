import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from backend.models import db


def create_app():
    app = Flask(__name__)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(base_dir)  # go up from backend/ to project root
    frontend_dir = os.path.join(project_dir, 'dist')  # Vite build 输出在根目录 dist/
    db_path = os.path.join(base_dir, 'data', 'hardware.db')
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    CORS(app)

    from routes.computers import computers_bp
    from routes.os_instances import os_instances_bp
    from routes.services import services_bp
    from routes.search import search_bp
    from routes.ip_groups import ip_groups_bp
    from routes.type_configs import type_configs_bp

    app.register_blueprint(computers_bp, url_prefix='/api')
    app.register_blueprint(os_instances_bp, url_prefix='/api')
    app.register_blueprint(services_bp, url_prefix='/api')
    app.register_blueprint(search_bp, url_prefix='/api')
    app.register_blueprint(ip_groups_bp, url_prefix='/api')
    app.register_blueprint(type_configs_bp, url_prefix='/api')

    @app.route('/')
    def index():
        return send_from_directory(frontend_dir, 'index.html')

    @app.route('/<path:path>')
    def static_files(path):
        # Serve Vue static assets
        static_path = os.path.join(frontend_dir, path)
        if os.path.exists(static_path):
            return send_from_directory(frontend_dir, path)
        # Fallback to index.html for SPA routing
        return send_from_directory(frontend_dir, 'index.html')

    with app.app_context():
        db.create_all()
        seed_data_if_empty()

    return app


def seed_data_if_empty():
    from backend.models import Computer, CPU, RAM, Disk, OsInstance, Service, IpGroup, TypeConfig

    if IpGroup.query.first() is None:
        groups = [
            IpGroup(name='网络设备', subnet='192.168.1.0/24', start_ip='192.168.1.1', end_ip='192.168.1.30'),
            IpGroup(name='物理服务器', subnet='192.168.1.0/24', start_ip='192.168.1.100', end_ip='192.168.1.150'),
            IpGroup(name='虚拟机/LXC', subnet='192.168.1.0/24', start_ip='192.168.1.50', end_ip='192.168.1.99'),
            IpGroup(name='预留地址', subnet='192.168.1.0/24', start_ip='192.168.1.240', end_ip='192.168.1.254')
        ]
        db.session.add_all(groups)

    if TypeConfig.query.first() is None:
        type_configs = [
            # OS types
            TypeConfig(category='os_type', name='PVE', color='#E6A23C'),
            TypeConfig(category='os_type', name='LXC', color='#909399'),
            TypeConfig(category='os_type', name='VM', color='#409EFF'),
            TypeConfig(category='os_type', name='Linux', color='#67C23A'),
            TypeConfig(category='os_type', name='Windows', color='#F56C6C'),
            # Protocols
            TypeConfig(category='protocol', name='http', color='#409EFF'),
            TypeConfig(category='protocol', name='https', color='#67C23A'),
            TypeConfig(category='protocol', name='ssh', color='#909399'),
            TypeConfig(category='protocol', name='tcp', color='#E6A23C'),
            TypeConfig(category='protocol', name='udp', color='#F56C6C'),
        ]
        db.session.add_all(type_configs)
        db.session.commit()

    if Computer.query.first() is None:
        c1 = Computer(name='PVE-Server-1', ip='192.168.1.100', location='机柜A-3U', remarks='主要虚拟化主机')
        db.session.add(c1)
        db.session.flush()

        cpu1 = CPU(computer_id=c1.id, model='Intel Xeon E-2286G', cores=12, clock_speed=4.0, purchase_date='2023-06-15', remarks='服务器专用')
        cpu2 = CPU(computer_id=c1.id, model='Intel Xeon E-2286G', cores=12, clock_speed=4.0, purchase_date='2023-06-15', remarks='服务器专用')
        db.session.add_all([cpu1, cpu2])

        ram1 = RAM(computer_id=c1.id, brand='Samsung', model='M393A8G40AB2', capacity_gb=64, ram_type='DDR4')
        ram2 = RAM(computer_id=c1.id, brand='Samsung', model='M393A8G40AB2', capacity_gb=64, ram_type='DDR4')
        db.session.add_all([ram1, ram2])

        disk1 = Disk(computer_id=c1.id, brand='Samsung', model='PM983', capacity_gb=960, interface='NVMe', file_system='ext4', purpose='系统盘', is_boot_disk=True, remarks='PVE系统')
        disk2 = Disk(computer_id=c1.id, brand='Intel', model='SSDPFKNQ960TZY', capacity_gb=960, interface='NVMe', file_system='ext4', purpose='数据盘', is_boot_disk=False, remarks='数据库')
        db.session.add_all([disk1, disk2])

        os1 = OsInstance(computer_id=c1.id, name='Proxmox VE 8.1', os_type='PVE', ip_address='192.168.1.100', port=8006, notes='主控节点')
        db.session.add(os1)
        db.session.flush()

        os2 = OsInstance(computer_id=c1.id, parent_os_id=os1.id, name='OpenWrt-主路由', os_type='LXC', ip_address='192.168.1.1', port=80)
        os3 = OsInstance(computer_id=c1.id, parent_os_id=os1.id, name='HomeAssistant VM', os_type='VM', ip_address='192.168.1.50', port=8123)
        os4 = OsInstance(computer_id=c1.id, parent_os_id=os1.id, name='Nextcloud LXC', os_type='LXC', ip_address='192.168.1.51', port=443)
        db.session.add_all([os2, os3, os4])
        db.session.flush()

        s1 = Service(os_instance_id=os2.id, name='OpenClash', protocol='http', ip_address='192.168.1.1', port=9090, description='Clash dashboard')
        s2 = Service(os_instance_id=os2.id, name='AdGuard Home', protocol='http', ip_address='192.168.1.1', port=3000, description='DNS过滤服务')
        s3 = Service(os_instance_id=os3.id, name='HomeAssistant', protocol='https', ip_address='192.168.1.50', port=8123, description='智能家居平台')
        s4 = Service(os_instance_id=os4.id, name='Nextcloud', protocol='https', ip_address='192.168.1.51', port=443, description='私有云存储')
        s5 = Service(os_instance_id=os1.id, name='PVE控制台', protocol='https', ip_address='192.168.1.100', port=8006, description='Proxmox Web界面')
        db.session.add_all([s1, s2, s3, s4, s5])

        db.session.commit()
        print('Seed data inserted.')


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
