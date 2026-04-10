from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Computer(db.Model):
    __tablename__ = 'computers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ip = db.Column(db.String(50))
    location = db.Column(db.String(100))
    remarks = db.Column(db.Text)
    status = db.Column(db.String(20), default='online')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    cpus = db.relationship('CPU', backref='computer', lazy=True, cascade='all, delete-orphan')
    rams = db.relationship('RAM', backref='computer', lazy=True, cascade='all, delete-orphan')
    disks = db.relationship('Disk', backref='computer', lazy=True, cascade='all, delete-orphan')
    os_instances = db.relationship('OsInstance', backref='computer', lazy=True, cascade='all, delete-orphan')

    def to_dict(self, include_details=False):
        data = {
            'id': self.id,
            'name': self.name,
            'ip': self.ip,
            'location': self.location,
            'remarks': self.remarks,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        if include_details:
            data['cpus'] = [cpu.to_dict() for cpu in self.cpus]
            data['rams'] = [ram.to_dict() for ram in self.rams]
            data['disks'] = [disk.to_dict() for disk in self.disks]
            data['os_instances'] = [os.to_dict(include_details=True) for os in self.os_instances]
            data['cpuIds'] = [cpu.id for cpu in self.cpus]
            data['ramIds'] = [ram.id for ram in self.rams]
            data['diskIds'] = [disk.id for disk in self.disks]
            data['osInstanceIds'] = [os.id for os in self.os_instances]
            data['total_ram'] = sum(r.capacity_gb for r in self.rams)
            data['total_disk'] = sum(d.capacity_gb for d in self.disks)
            data['vm_count'] = len(self.os_instances)
        return data


class CPU(db.Model):
    __tablename__ = 'cpus'

    id = db.Column(db.Integer, primary_key=True)
    computer_id = db.Column(db.Integer, db.ForeignKey('computers.id'), nullable=True)
    model = db.Column(db.String(100))
    cores = db.Column(db.Integer)
    clock_speed = db.Column(db.Float)
    purchase_date = db.Column(db.String(20))
    remarks = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'computer_id': self.computer_id,
            'model': self.model,
            'cores': self.cores,
            'clock_speed': self.clock_speed,
            'purchase_date': self.purchase_date,
            'remarks': self.remarks
        }


class RAM(db.Model):
    __tablename__ = 'rams'

    id = db.Column(db.Integer, primary_key=True)
    computer_id = db.Column(db.Integer, db.ForeignKey('computers.id'), nullable=True)
    brand = db.Column(db.String(50))
    model = db.Column(db.String(50))
    capacity_gb = db.Column(db.Integer)
    ram_type = db.Column(db.String(20))
    slots_occupied = db.Column(db.String(20))
    purchase_date = db.Column(db.String(20))
    remarks = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'computer_id': self.computer_id,
            'brand': self.brand,
            'model': self.model,
            'capacity_gb': self.capacity_gb,
            'ram_type': self.ram_type,
            'slots_occupied': self.slots_occupied,
            'purchase_date': self.purchase_date,
            'remarks': self.remarks
        }


class Disk(db.Model):
    __tablename__ = 'disks'

    id = db.Column(db.Integer, primary_key=True)
    computer_id = db.Column(db.Integer, db.ForeignKey('computers.id'), nullable=True)
    brand = db.Column(db.String(50))
    model = db.Column(db.String(50))
    capacity_gb = db.Column(db.Integer)
    interface = db.Column(db.String(20))
    file_system = db.Column(db.String(20))
    purpose = db.Column(db.String(50))
    slot_info = db.Column(db.String(20))
    is_boot_disk = db.Column(db.Boolean, default=False)
    purchase_date = db.Column(db.String(20))
    remarks = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'computer_id': self.computer_id,
            'brand': self.brand,
            'model': self.model,
            'capacity_gb': self.capacity_gb,
            'interface': self.interface,
            'file_system': self.file_system,
            'purpose': self.purpose,
            'slot_info': self.slot_info,
            'is_boot_disk': self.is_boot_disk,
            'purchase_date': self.purchase_date,
            'remarks': self.remarks
        }


class OsInstance(db.Model):
    __tablename__ = 'os_instances'

    id = db.Column(db.Integer, primary_key=True)
    computer_id = db.Column(db.Integer, db.ForeignKey('computers.id'), nullable=False)
    parent_os_id = db.Column(db.Integer, db.ForeignKey('os_instances.id'))
    name = db.Column(db.String(100), nullable=False)
    os_type = db.Column(db.String(20))
    ip_address = db.Column(db.String(50))
    mac_address = db.Column(db.String(50))
    port = db.Column(db.Integer)
    pcie_passthrough = db.Column(db.String(100))
    notes = db.Column(db.Text)

    services = db.relationship('Service', backref='os_instance', lazy=True, cascade='all, delete-orphan')
    children = db.relationship('OsInstance', backref=db.backref('parent', remote_side=[id]), lazy=True)

    def to_dict(self, include_details=False):
        data = {
            'id': self.id,
            'computer_id': self.computer_id,
            'parent_os_id': self.parent_os_id,
            'name': self.name,
            'os_type': self.os_type,
            'ip_address': self.ip_address,
            'mac_address': self.mac_address,
            'port': self.port,
            'pcie_passthrough': self.pcie_passthrough,
            'notes': self.notes,
            'computer_name': self.computer.name if self.computer else None
        }
        if include_details:
            data['services'] = [s.to_dict() for s in self.services]
            data['children'] = [c.to_dict(include_details=True) for c in self.children]
        return data


class Service(db.Model):
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
    os_instance_id = db.Column(db.Integer, db.ForeignKey('os_instances.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    protocol = db.Column(db.String(10))
    ip_address = db.Column(db.String(50))
    port = db.Column(db.Integer)
    description = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'os_instance_id': self.os_instance_id,
            'name': self.name,
            'protocol': self.protocol,
            'ip_address': self.ip_address,
            'port': self.port,
            'description': self.description,
            'os_instance': {'id': self.os_instance.id, 'name': self.os_instance.name} if self.os_instance else None
        }


class IpGroup(db.Model):
    __tablename__ = 'ip_groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    subnet = db.Column(db.String(20))
    start_ip = db.Column(db.String(20))
    end_ip = db.Column(db.String(20))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'subnet': self.subnet,
            'startIp': self.start_ip,
            'endIp': self.end_ip
        }


class TypeConfig(db.Model):
    __tablename__ = 'type_configs'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(20), nullable=False)  # 'os_type' or 'protocol'
    name = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(20), default='#409EFF')

    def to_dict(self):
        return {
            'id': self.id,
            'category': self.category,
            'name': self.name,
            'color': self.color
        }
