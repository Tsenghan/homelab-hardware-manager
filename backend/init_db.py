"""
Database initialization script.
Run this manually to set up or reset the database with example data.

Usage: python init_db.py
"""
import os
import sys

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import create_app
from models import db, Computer, CPU, RAM, Disk, StoragePool, OsInstance, Service, IpGroup, TypeConfig


def init_database():
    """Initialize database with tables and example data."""
    app = create_app()

    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database tables created.")

        # Check if data already exists
        if Computer.query.first() is not None:
            response = input("Database already has data. Reset and load example data? (y/N): ")
            if response.lower() != 'y':
                print("Aborted.")
                return
            # Clear existing data
            db.drop_all()
            db.create_all()
            print("Database reset.")

        # Load example data
        load_example_data()
        print("Example data loaded successfully.")


def load_example_data():
    """Load example data into the database."""
    # IP Groups
    ip_groups = [
        IpGroup(name='网络设备', subnet='192.168.1.0/24', start_ip='192.168.1.1', end_ip='192.168.1.30'),
        IpGroup(name='物理服务器', subnet='192.168.1.0/24', start_ip='192.168.1.100', end_ip='192.168.1.150'),
        IpGroup(name='虚拟机/LXC', subnet='192.168.1.0/24', start_ip='192.168.1.50', end_ip='192.168.1.99'),
        IpGroup(name='预留地址', subnet='192.168.1.0/24', start_ip='192.168.1.240', end_ip='192.168.1.254')
    ]
    db.session.add_all(ip_groups)

    # Type Configs
    type_configs = [
        TypeConfig(category='os_type', name='PVE', color='#E6A23C'),
        TypeConfig(category='os_type', name='LXC', color='#909399'),
        TypeConfig(category='os_type', name='VM', color='#409EFF'),
        TypeConfig(category='os_type', name='Linux', color='#67C23A'),
        TypeConfig(category='os_type', name='Windows', color='#F56C6C'),
        TypeConfig(category='protocol', name='http', color='#409EFF'),
        TypeConfig(category='protocol', name='https', color='#67C23A'),
        TypeConfig(category='protocol', name='ssh', color='#909399'),
        TypeConfig(category='protocol', name='tcp', color='#E6A23C'),
        TypeConfig(category='protocol', name='udp', color='#F56C6C'),
    ]
    db.session.add_all(type_configs)
    db.session.commit()

    # Main Proxmox server
    c1 = Computer(name='PVE-Server-1', ip='192.168.1.100', location='机柜A-3U', remarks='主要虚拟化主机')
    db.session.add(c1)
    db.session.flush()

    # CPUs
    cpus = [
        CPU(computer_id=c1.id, model='Intel Xeon E-2286G', cores=12, clock_speed=4.0, purchase_date='2023-06-15', remarks='服务器专用'),
        CPU(computer_id=c1.id, model='Intel Xeon E-2286G', cores=12, clock_speed=4.0, purchase_date='2023-06-15', remarks='服务器专用'),
    ]
    db.session.add_all(cpus)

    # RAMs
    rams = [
        RAM(computer_id=c1.id, brand='Samsung', model='M393A8G40AB2', capacity_gb=64, ram_type='DDR4'),
        RAM(computer_id=c1.id, brand='Samsung', model='M393A8G40AB2', capacity_gb=64, ram_type='DDR4'),
    ]
    db.session.add_all(rams)

    # Disks
    disks = [
        Disk(computer_id=c1.id, brand='Samsung', model='PM983', capacity_gb=960, interface='NVMe', file_system='ext4', purpose='系统盘', is_boot_disk=True, remarks='PVE系统'),
        Disk(computer_id=c1.id, brand='Intel', model='SSDPFKNQ960TZY', capacity_gb=960, interface='NVMe', file_system='ext4', purpose='数据盘', is_boot_disk=False, remarks='数据库'),
    ]
    db.session.add_all(disks)

    # Storage Pools
    pools = [
        StoragePool(computer_id=c1.id, name='local-lvm', pool_type='LVM', total_capacity_gb=800, used_capacity_gb=400),
        StoragePool(computer_id=c1.id, name='local-zfs', pool_type='ZFS', total_capacity_gb=1800, used_capacity_gb=900),
    ]
    db.session.add_all(pools)

    # OS Instances
    os1 = OsInstance(computer_id=c1.id, name='Proxmox VE 8.1', os_type='PVE', ip_address='192.168.1.100', port=8006, notes='主控节点')
    db.session.add(os1)
    db.session.flush()

    os_instances = [
        OsInstance(computer_id=c1.id, parent_os_id=os1.id, name='OpenWrt-主路由', os_type='LXC', ip_address='192.168.1.1', port=80),
        OsInstance(computer_id=c1.id, parent_os_id=os1.id, name='HomeAssistant VM', os_type='VM', ip_address='192.168.1.50', port=8123),
        OsInstance(computer_id=c1.id, parent_os_id=os1.id, name='Nextcloud LXC', os_type='LXC', ip_address='192.168.1.51', port=443),
    ]
    db.session.add_all(os_instances)
    db.session.flush()

    # Services
    services = [
        Service(os_instance_id=os_instances[0].id, name='OpenClash', protocol='http', ip_address='192.168.1.1', port=9090, description='Clash dashboard'),
        Service(os_instance_id=os_instances[0].id, name='AdGuard Home', protocol='http', ip_address='192.168.1.1', port=3000, description='DNS过滤服务'),
        Service(os_instance_id=os_instances[1].id, name='HomeAssistant', protocol='https', ip_address='192.168.1.50', port=8123, description='智能家居平台'),
        Service(os_instance_id=os_instances[2].id, name='Nextcloud', protocol='https', ip_address='192.168.1.51', port=443, description='私有云存储'),
        Service(os_instance_id=os1.id, name='PVE控制台', protocol='https', ip_address='192.168.1.100', port=8006, description='Proxmox Web界面'),
    ]
    db.session.add_all(services)

    db.session.commit()
    print("Example data committed to database.")


if __name__ == '__main__':
    init_database()