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
from models import db, Computer, CPU, RAM, Disk, OsInstance, Service, IpGroup, TypeConfig


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
    """Load comprehensive example data into the database."""

    # ==================== Type Configs ====================
    # OS Types
    os_types = [
        TypeConfig(category='os_type', name='PVE', color='#E6A23C'),
        TypeConfig(category='os_type', name='LXC', color='#909399'),
        TypeConfig(category='os_type', name='VM', color='#409EFF'),
        TypeConfig(category='os_type', name='Linux', color='#67C23A'),
        TypeConfig(category='os_type', name='Windows', color='#F56C6C'),
        TypeConfig(category='os_type', name='Docker', color='#2496ED'),
    ]
    db.session.add_all(os_types)

    # Protocols
    protocols = [
        TypeConfig(category='protocol', name='http', color='#409EFF'),
        TypeConfig(category='protocol', name='https', color='#67C23A'),
        TypeConfig(category='protocol', name='ssh', color='#909399'),
        TypeConfig(category='protocol', name='tcp', color='#E6A23C'),
        TypeConfig(category='protocol', name='udp', color='#F56C6C'),
        TypeConfig(category='protocol', name='rdp', color='#0078D4'),
        TypeConfig(category='protocol', name='vnc', color='#44B78B'),
    ]
    db.session.add_all(protocols)

    # Service Types
    service_types = [
        TypeConfig(category='service_type', name='Web服务', color='#409EFF'),
        TypeConfig(category='service_type', name='存储服务', color='#67C23A'),
        TypeConfig(category='service_type', name='智能家居', color='#E6A23C'),
        TypeConfig(category='service_type', name='网络工具', color='#909399'),
        TypeConfig(category='service_type', name='开发工具', color='#F56C6C'),
        TypeConfig(category='service_type', name='监控系统', color='#2496ED'),
        TypeConfig(category='service_type', name='媒体服务', color='#9012FE'),
        TypeConfig(category='service_type', name='安全工具', color='#F56C6C'),
    ]
    db.session.add_all(service_types)

    # Disk Interface Types
    disk_interfaces = [
        TypeConfig(category='disk_interface', name='NVMe PCIe 3.0'),
        TypeConfig(category='disk_interface', name='NVMe PCIe 4.0'),
        TypeConfig(category='disk_interface', name='SATA'),
        TypeConfig(category='disk_interface', name='USB'),
        TypeConfig(category='disk_interface', name='RDM'),
        TypeConfig(category='disk_interface', name='控制器直通'),
    ]
    db.session.add_all(disk_interfaces)

    # Disk File System Types
    disk_file_systems = [
        TypeConfig(category='disk_file_system', name='ext4'),
        TypeConfig(category='disk_file_system', name='ZFS'),
        TypeConfig(category='disk_file_system', name='NTFS'),
        TypeConfig(category='disk_file_system', name='Btrfs'),
        TypeConfig(category='disk_file_system', name='XFS'),
    ]
    db.session.add_all(disk_file_systems)

    # Disk Mount Method Types
    disk_mount_methods = [
        TypeConfig(category='disk_mount_method', name='本地路径挂载'),
        TypeConfig(category='disk_mount_method', name='NFS共享'),
        TypeConfig(category='disk_mount_method', name='CIFS/SMB共享'),
        TypeConfig(category='disk_mount_method', name='iSCSI'),
        TypeConfig(category='disk_mount_method', name='ZFS数据集'),
    ]
    db.session.add_all(disk_mount_methods)

    db.session.commit()

    # ==================== IP Groups ====================
    ip_groups = [
        IpGroup(name='网络设备', subnet='192.168.1.0/24', start_ip='192.168.1.1', end_ip='192.168.1.20'),
        IpGroup(name='物理服务器', subnet='192.168.1.0/24', start_ip='192.168.1.50', end_ip='192.168.1.80'),
        IpGroup(name='宿主机', subnet='192.168.1.0/24', start_ip='192.168.1.100', end_ip='192.168.1.110'),
        IpGroup(name='虚拟机/LXC', subnet='192.168.1.0/24', start_ip='192.168.1.120', end_ip='192.168.1.200'),
        IpGroup(name='Docker容器', subnet='192.168.1.0/24', start_ip='192.168.1.201', end_ip='192.168.1.230'),
        IpGroup(name='预留地址', subnet='192.168.1.0/24', start_ip='192.168.1.240', end_ip='192.168.1.254'),
    ]
    db.session.add_all(ip_groups)
    db.session.commit()

    # ==================== Physical Server 1: PVE-Server-1 ====================
    pve1 = Computer(name='示例-PVE-Server-1', location='机柜A-3U', remarks='主要虚拟化宿主机，承担80%虚拟化负载')
    db.session.add(pve1)
    db.session.flush()

    # CPU for PVE1
    cpus_pve1 = [
        CPU(computer_id=pve1.id, model='Intel Xeon E-2286G', cores=12, clock_speed=4.0, purchase_date='2024-01-15', remarks='服务器级处理器'),
    ]
    db.session.add_all(cpus_pve1)

    # RAM for PVE1
    rams_pve1 = [
        RAM(computer_id=pve1.id, brand='Samsung', model='M393A8G40AB2', capacity_gb=64, ram_type='DDR4', purchase_date='2024-01-15'),
        RAM(computer_id=pve1.id, brand='Samsung', model='M393A8G40AB2', capacity_gb=64, ram_type='DDR4', purchase_date='2024-01-15'),
    ]
    db.session.add_all(rams_pve1)

    # Disks for PVE1
    disks_pve1 = [
        Disk(computer_id=pve1.id, brand='Samsung', model='PM983', capacity_gb=960, interface='NVMe PCIe 4.0', file_system='ext4', mount_method='本地路径挂载', purpose='PVE系统盘', is_boot_disk=True, purchase_date='2024-01-15'),
        Disk(computer_id=pve1.id, brand='Samsung', model='PM983', capacity_gb=1920, interface='NVMe PCIe 4.0', file_system='ZFS', mount_method='ZFS数据集', purpose='数据存储池', is_boot_disk=False, purchase_date='2024-01-15', remarks='1.92TB NVMe 用于ZFS存储池'),
        Disk(computer_id=pve1.id, brand='WD', model='WD40EFPX', capacity_gb=4000, interface='SATA', file_system='ext4', mount_method='本地路径挂载', purpose='备份盘', is_boot_disk=False, purchase_date='2023-06-01', remarks='4TB 红盘，用于备份'),
    ]
    db.session.add_all(disks_pve1)

    # ==================== Physical Server 2: PVE-Server-2 ====================
    pve2 = Computer(name='示例-PVE-Server-2', location='机柜A-4U', remarks='辅助虚拟化宿主机')
    db.session.add(pve2)
    db.session.flush()

    cpus_pve2 = [
        CPU(computer_id=pve2.id, model='AMD Ryzen 9 5950X', cores=16, clock_speed=3.4, purchase_date='2024-03-20'),
    ]
    db.session.add_all(cpus_pve2)

    rams_pve2 = [
        RAM(computer_id=pve2.id, brand='G.Skill', model='F4-3600C16D-32GTZN', capacity_gb=32, ram_type='DDR4', purchase_date='2024-03-20'),
        RAM(computer_id=pve2.id, brand='G.Skill', model='F4-3600C16D-32GTZN', capacity_gb=32, ram_type='DDR4', purchase_date='2024-03-20'),
        RAM(computer_id=pve2.id, brand='G.Skill', model='F4-3600C16D-32GTZN', capacity_gb=32, ram_type='DDR4', purchase_date='2024-03-20'),
        RAM(computer_id=pve2.id, brand='G.Skill', model='F4-3600C16D-32GTZN', capacity_gb=32, ram_type='DDR4', purchase_date='2024-03-20'),
    ]
    db.session.add_all(rams_pve2)

    disks_pve2 = [
        Disk(computer_id=pve2.id, brand='Samsung', model='980 PRO', capacity_gb=500, interface='NVMe PCIe 4.0', file_system='ext4', mount_method='本地路径挂载', purpose='系统盘', is_boot_disk=True, purchase_date='2024-03-20'),
        Disk(computer_id=pve2.id, brand='Seagate', model='IronWolf 8T', capacity_gb=8000, interface='SATA', file_system='ZFS', mount_method='ZFS数据集', purpose='NAS存储', is_boot_disk=False, purchase_date='2024-03-25', remarks='8TB NAS专用盘'),
    ]
    db.session.add_all(disks_pve2)

    db.session.commit()

    # ==================== OS Instances for PVE1 ====================
    # PVE Host OS
    os_pve1_host = OsInstance(
        computer_id=pve1.id,
        name='Proxmox VE 8.2',
        os_type='PVE',
        ip_address='192.168.1.100',
        mac_address='BC:30:5B:ED:33:4A',
        port=8006,
        notes='主控节点，通过web界面管理所有VM和LXC'
    )
    db.session.add(os_pve1_host)
    db.session.flush()

    # Router LXC
    os_router = OsInstance(
        computer_id=pve1.id,
        parent_os_id=os_pve1_host.id,
        name='OpenWrt-主路由',
        os_type='LXC',
        ip_address='192.168.1.1',
        mac_address='BC:30:5B:ED:33:4B',
        port=80,
        notes='主路由器，运行OpenWrt系统'
    )
    db.session.add(os_router)
    db.session.flush()

    # Home Assistant VM
    os_ha = OsInstance(
        computer_id=pve1.id,
        parent_os_id=os_pve1_host.id,
        name='HomeAssistant',
        os_type='VM',
        ip_address='192.168.1.50',
        mac_address='BC:30:5B:ED:33:4C',
        port=8123,
        notes='智能家居控制中心'
    )
    db.session.add(os_ha)
    db.session.flush()

    # Nextcloud LXC
    os_nextcloud = OsInstance(
        computer_id=pve1.id,
        parent_os_id=os_pve1_host.id,
        name='Nextcloud',
        os_type='LXC',
        ip_address='192.168.1.51',
        mac_address='BC:30:5B:ED:33:4D',
        port=443,
        notes='私有云存储'
    )
    db.session.add(os_nextcloud)
    db.session.flush()

    # Ubuntu Server (Development)
    os_ubuntu = OsInstance(
        computer_id=pve1.id,
        parent_os_id=os_pve1_host.id,
        name='Ubuntu-Server',
        os_type='Linux',
        ip_address='192.168.1.60',
        mac_address='BC:30:5B:ED:33:4E',
        port=22,
        notes='开发测试服务器'
    )
    db.session.add(os_ubuntu)
    db.session.flush()

    # Windows VM
    os_win = OsInstance(
        computer_id=pve1.id,
        parent_os_id=os_pve1_host.id,
        name='Windows-VM',
        os_type='VM',
        ip_address='192.168.1.70',
        mac_address='BC:30:5B:ED:33:4F',
        port=3389,
        notes='Windows开发测试环境'
    )
    db.session.add(os_win)
    db.session.flush()

    db.session.commit()

    # ==================== OS Instances for PVE2 ====================
    os_pve2_host = OsInstance(
        computer_id=pve2.id,
        name='Proxmox VE 8.2',
        os_type='PVE',
        ip_address='192.168.1.101',
        port=8006,
        notes='辅助宿主机'
    )
    db.session.add(os_pve2_host)
    db.session.flush()

    # Docker Host
    os_docker = OsInstance(
        computer_id=pve2.id,
        parent_os_id=os_pve2_host.id,
        name='Docker-Host',
        os_type='Linux',
        ip_address='192.168.1.102',
        port=22,
        notes='Docker容器宿主机'
    )
    db.session.add(os_docker)
    db.session.flush()

    # Jellyfin Media Server
    os_jellyfin = OsInstance(
        computer_id=pve2.id,
        parent_os_id=os_pve2_host.id,
        name='Jellyfin',
        os_type='LXC',
        ip_address='192.168.1.110',
        port=8096,
        notes='媒体服务器，存储家庭照片和视频'
    )
    db.session.add(os_jellyfin)
    db.session.flush()

    db.session.commit()

    # ==================== Services ====================
    # Router Services
    services_router = [
        Service(
            os_instance_id=os_router.id,
            name='OpenClash',
            type='网络工具',
            protocol='http',
            ip_address='192.168.1.1',
            port=9090,
            description='Clash Dashboard，透明代理控制面板'
        ),
        Service(
            os_instance_id=os_router.id,
            name='AdGuard Home',
            type='安全工具',
            protocol='https',
            ip_address='192.168.1.1',
            port=3053,
            description='DNS过滤，拦截广告和恶意域名'
        ),
        Service(
            os_instance_id=os_router.id,
            name='OpenWrt Web',
            type='网络工具',
            protocol='http',
            ip_address='192.168.1.1',
            port=80,
            description='OpenWrt LuCI管理界面'
        ),
        Service(
            os_instance_id=os_router.id,
            name='WireGuard',
            type='网络工具',
            protocol='udp',
            ip_address='192.168.1.1',
            port=51820,
            description='VPN服务器，支持远程接入'
        ),
    ]
    db.session.add_all(services_router)

    # Home Assistant Services
    services_ha = [
        Service(
            os_instance_id=os_ha.id,
            name='HomeAssistant',
            type='智能家居',
            protocol='https',
            ip_address='192.168.1.50',
            port=8123,
            description='智能家居核心平台'
        ),
        Service(
            os_instance_id=os_ha.id,
            name='HASS SSH',
            type='开发工具',
            protocol='ssh',
            ip_address='192.168.1.50',
            port=22,
            description='HomeAssistant SSH访问'
        ),
    ]
    db.session.add_all(services_ha)

    # Nextcloud Services
    services_nextcloud = [
        Service(
            os_instance_id=os_nextcloud.id,
            name='Nextcloud',
            type='存储服务',
            protocol='https',
            ip_address='192.168.1.51',
            port=443,
            description='私有云存储，支持文件同步和分享'
        ),
        Service(
            os_instance_id=os_nextcloud.id,
            name='Nextcloud AIO',
            type='存储服务',
            protocol='http',
            ip_address='192.168.1.51',
            port=8080,
            description='Nextcloud All-in-One管理面板'
        ),
    ]
    db.session.add_all(services_nextcloud)

    # Ubuntu Server Services
    services_ubuntu = [
        Service(
            os_instance_id=os_ubuntu.id,
            name='SSH',
            type='开发工具',
            protocol='ssh',
            ip_address='192.168.1.60',
            port=22,
            description='服务器SSH访问'
        ),
        Service(
            os_instance_id=os_ubuntu.id,
            name='Docker Registry',
            type='开发工具',
            protocol='https',
            ip_address='192.168.1.60',
            port=5000,
            description='私有Docker镜像仓库'
        ),
        Service(
            os_instance_id=os_ubuntu.id,
            name='Portainer',
            type='开发工具',
            protocol='http',
            ip_address='192.168.1.60',
            port=9000,
            description='Docker容器管理界面'
        ),
        Service(
            os_instance_id=os_ubuntu.id,
            name='Gitea',
            type='开发工具',
            protocol='http',
            ip_address='192.168.1.60',
            port=3000,
            description='自建Git代码仓库'
        ),
    ]
    db.session.add_all(services_ubuntu)

    # PVE Host Services
    services_pve1 = [
        Service(
            os_instance_id=os_pve1_host.id,
            name='Proxmox Web',
            type='Web服务',
            protocol='https',
            ip_address='192.168.1.100',
            port=8006,
            description='Proxmox VE Web管理界面'
        ),
        Service(
            os_instance_id=os_pve1_host.id,
            name='SSH',
            type='开发工具',
            protocol='ssh',
            ip_address='192.168.1.100',
            port=22,
            description='Proxmox主机SSH'
        ),
    ]
    db.session.add_all(services_pve1)

    # Jellyfin Services
    services_jellyfin = [
        Service(
            os_instance_id=os_jellyfin.id,
            name='Jellyfin',
            type='媒体服务',
            protocol='http',
            ip_address='192.168.1.110',
            port=8096,
            description='媒体服务器，播放电影、音乐'
        ),
        Service(
            os_instance_id=os_jellyfin.id,
            name='Jellyfin Admin',
            type='媒体服务',
            protocol='https',
            ip_address='192.168.1.110',
            port=8920,
            description='Jellyfin管理后台'
        ),
    ]
    db.session.add_all(services_jellyfin)

    # Docker Host Services
    services_docker = [
        Service(
            os_instance_id=os_docker.id,
            name='Portainer Agent',
            type='监控系统',
            protocol='https',
            ip_address='192.168.1.102',
            port=9443,
            description='Docker主机管理'
        ),
        Service(
            os_instance_id=os_docker.id,
            name='Nginx Proxy',
            type='Web服务',
            protocol='http',
            ip_address='192.168.1.102',
            port=80,
            description='反向代理入口'
        ),
        Service(
            os_instance_id=os_docker.id,
            name='Watchtower',
            type='监控系统',
            protocol='http',
            ip_address='192.168.1.102',
            port=8080,
            description='自动更新Docker容器'
        ),
    ]
    db.session.add_all(services_docker)

    # Windows VM Services
    services_win = [
        Service(
            os_instance_id=os_win.id,
            name='RDP',
            type='开发工具',
            protocol='rdp',
            ip_address='192.168.1.70',
            port=3389,
            description='Windows远程桌面'
        ),
        Service(
            os_instance_id=os_win.id,
            name='SMB Share',
            type='存储服务',
            protocol='tcp',
            ip_address='192.168.1.70',
            port=445,
            description='文件共享服务'
        ),
    ]
    db.session.add_all(services_win)

    db.session.commit()
    print("Example data committed to database.")


if __name__ == '__main__':
    init_database()
