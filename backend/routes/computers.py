from flask import Blueprint, request, jsonify
from backend.models import db, Computer, CPU, RAM, Disk, OsInstance

computers_bp = Blueprint('computers', __name__)


# Global hardware endpoints (no computer_id required)
@computers_bp.route('/cpus', methods=['GET'])
def get_all_cpus():
    cpus = CPU.query.all()
    return jsonify([c.to_dict() for c in cpus])

@computers_bp.route('/cpus', methods=['POST'])
def create_cpu_global():
    data = request.get_json()
    cpu = CPU(
        computer_id=data.get('computer_id'),
        model=data.get('model'),
        cores=data.get('cores'),
        clock_speed=data.get('clock_speed') or data.get('clockSpeed'),
        purchase_date=data.get('purchase_date') or data.get('purchaseDate'),
        remarks=data.get('remarks')
    )
    db.session.add(cpu)
    db.session.commit()
    return jsonify(cpu.to_dict()), 201

@computers_bp.route('/cpus/<int:id>', methods=['PUT'])
def update_cpu(id):
    cpu = CPU.query.get_or_404(id)
    data = request.get_json()
    if 'computer_id' in data: cpu.computer_id = data['computer_id']
    if 'model' in data: cpu.model = data['model']
    if 'cores' in data: cpu.cores = data['cores']
    if 'clock_speed' in data or 'clockSpeed' in data: cpu.clock_speed = data.get('clock_speed') or data.get('clockSpeed')
    if 'purchase_date' in data or 'purchaseDate' in data: cpu.purchase_date = data.get('purchase_date') or data.get('purchaseDate')
    if 'remarks' in data: cpu.remarks = data['remarks']
    db.session.commit()
    return jsonify(cpu.to_dict())

@computers_bp.route('/rams', methods=['GET'])
def get_all_rams():
    rams = RAM.query.all()
    return jsonify([r.to_dict() for r in rams])

@computers_bp.route('/rams', methods=['POST'])
def create_ram_global():
    data = request.get_json()
    ram = RAM(
        computer_id=data.get('computer_id'),
        brand=data.get('brand'),
        model=data.get('model'),
        capacity_gb=data.get('capacity_gb'),
        ram_type=data.get('ram_type'),
        slots_occupied=data.get('slots_occupied'),
        purchase_date=data.get('purchase_date'),
        remarks=data.get('remarks')
    )
    db.session.add(ram)
    db.session.commit()
    return jsonify(ram.to_dict()), 201

@computers_bp.route('/rams/<int:id>', methods=['PUT'])
def update_ram(id):
    ram = RAM.query.get_or_404(id)
    data = request.get_json()
    ram.computer_id = data.get('computer_id', ram.computer_id)
    ram.brand = data.get('brand', ram.brand)
    ram.model = data.get('model', ram.model)
    ram.capacity_gb = data.get('capacity_gb', ram.capacity_gb)
    ram.ram_type = data.get('ram_type', ram.ram_type)
    ram.slots_occupied = data.get('slots_occupied', ram.slots_occupied)
    ram.purchase_date = data.get('purchase_date', ram.purchase_date)
    ram.remarks = data.get('remarks', ram.remarks)
    db.session.commit()
    return jsonify(ram.to_dict())

@computers_bp.route('/disks', methods=['GET'])
def get_all_disks():
    disks = Disk.query.all()
    return jsonify([d.to_dict() for d in disks])

@computers_bp.route('/disks', methods=['POST'])
def create_disk_global():
    data = request.get_json()
    disk = Disk(
        computer_id=data.get('computer_id'),
        brand=data.get('brand'),
        model=data.get('model'),
        capacity_gb=data.get('capacity_gb'),
        interface=data.get('interface'),
        file_system=data.get('file_system'),
        purpose=data.get('purpose'),
        slot_info=data.get('slot_info'),
        is_boot_disk=data.get('is_boot_disk', False),
        purchase_date=data.get('purchase_date'),
        remarks=data.get('remarks')
    )
    db.session.add(disk)
    db.session.commit()
    return jsonify(disk.to_dict()), 201

@computers_bp.route('/disks/<int:id>', methods=['PUT'])
def update_disk(id):
    disk = Disk.query.get_or_404(id)
    data = request.get_json()
    disk.computer_id = data.get('computer_id', disk.computer_id)
    disk.brand = data.get('brand', disk.brand)
    disk.model = data.get('model', disk.model)
    disk.capacity_gb = data.get('capacity_gb', disk.capacity_gb)
    disk.interface = data.get('interface', disk.interface)
    disk.file_system = data.get('file_system', disk.file_system)
    disk.purpose = data.get('purpose', disk.purpose)
    disk.slot_info = data.get('slot_info', disk.slot_info)
    disk.is_boot_disk = data.get('is_boot_disk', disk.is_boot_disk)
    disk.purchase_date = data.get('purchase_date', disk.purchase_date)
    disk.remarks = data.get('remarks', disk.remarks)
    db.session.commit()
    return jsonify(disk.to_dict())


@computers_bp.route('/computers', methods=['GET'])
def get_computers():
    computers = Computer.query.all()
    return jsonify([c.to_dict(include_details=True) for c in computers])


@computers_bp.route('/computers/<int:id>', methods=['GET'])
def get_computer(id):
    computer = Computer.query.get_or_404(id)
    return jsonify(computer.to_dict(include_details=True))


@computers_bp.route('/computers', methods=['POST'])
def create_computer():
    data = request.get_json()
    computer = Computer(
        name=data.get('name'),
        ip=data.get('ip'),
        location=data.get('location'),
        remarks=data.get('remarks'),
        status=data.get('status', 'online')
    )
    db.session.add(computer)
    db.session.commit()
    return jsonify(computer.to_dict()), 201


@computers_bp.route('/computers/<int:id>', methods=['PUT'])
def update_computer(id):
    computer = Computer.query.get_or_404(id)
    data = request.get_json()
    computer.name = data.get('name', computer.name)
    computer.ip = data.get('ip', computer.ip)
    computer.location = data.get('location', computer.location)
    computer.remarks = data.get('remarks', computer.remarks)
    computer.status = data.get('status', computer.status)
    db.session.commit()
    return jsonify(computer.to_dict())


@computers_bp.route('/computers/<int:id>', methods=['DELETE'])
def delete_computer(id):
    computer = Computer.query.get_or_404(id)
    db.session.delete(computer)
    db.session.commit()
    return '', 204


@computers_bp.route('/computers/<int:computer_id>/cpus', methods=['GET'])
def get_cpus(computer_id):
    Computer.query.get_or_404(computer_id)
    cpus = CPU.query.filter_by(computer_id=computer_id).all()
    return jsonify([c.to_dict() for c in cpus])


@computers_bp.route('/computers/<int:computer_id>/cpus', methods=['POST'])
def create_cpu(computer_id):
    Computer.query.get_or_404(computer_id)
    data = request.get_json()
    cpu = CPU(
        computer_id=computer_id,
        model=data.get('model'),
        cores=data.get('cores'),
        clock_speed=data.get('clock_speed'),
        purchase_date=data.get('purchase_date'),
        remarks=data.get('remarks')
    )
    db.session.add(cpu)
    db.session.commit()
    return jsonify(cpu.to_dict()), 201


@computers_bp.route('/cpus/<int:id>', methods=['DELETE'])
def delete_cpu(id):
    cpu = CPU.query.get_or_404(id)
    db.session.delete(cpu)
    db.session.commit()
    return '', 204


@computers_bp.route('/computers/<int:computer_id>/rams', methods=['GET'])
def get_rams(computer_id):
    Computer.query.get_or_404(computer_id)
    rams = RAM.query.filter_by(computer_id=computer_id).all()
    return jsonify([r.to_dict() for r in rams])


@computers_bp.route('/computers/<int:computer_id>/rams', methods=['POST'])
def create_ram(computer_id):
    Computer.query.get_or_404(computer_id)
    data = request.get_json()
    ram = RAM(
        computer_id=computer_id,
        brand=data.get('brand'),
        model=data.get('model'),
        capacity_gb=data.get('capacity_gb'),
        ram_type=data.get('ram_type'),
        slots_occupied=data.get('slots_occupied'),
        purchase_date=data.get('purchase_date'),
        remarks=data.get('remarks')
    )
    db.session.add(ram)
    db.session.commit()
    return jsonify(ram.to_dict()), 201


@computers_bp.route('/rams/<int:id>', methods=['DELETE'])
def delete_ram(id):
    ram = RAM.query.get_or_404(id)
    db.session.delete(ram)
    db.session.commit()
    return '', 204


@computers_bp.route('/computers/<int:computer_id>/disks', methods=['GET'])
def get_disks(computer_id):
    Computer.query.get_or_404(computer_id)
    disks = Disk.query.filter_by(computer_id=computer_id).all()
    return jsonify([d.to_dict() for d in disks])


@computers_bp.route('/computers/<int:computer_id>/disks', methods=['POST'])
def create_disk(computer_id):
    Computer.query.get_or_404(computer_id)
    data = request.get_json()
    disk = Disk(
        computer_id=computer_id,
        brand=data.get('brand'),
        model=data.get('model'),
        capacity_gb=data.get('capacity_gb'),
        interface=data.get('interface'),
        file_system=data.get('file_system'),
        purpose=data.get('purpose'),
        slot_info=data.get('slot_info'),
        is_boot_disk=data.get('is_boot_disk', False),
        purchase_date=data.get('purchase_date'),
        remarks=data.get('remarks')
    )
    db.session.add(disk)
    db.session.commit()
    return jsonify(disk.to_dict()), 201


@computers_bp.route('/disks/<int:id>', methods=['DELETE'])
def delete_disk(id):
    disk = Disk.query.get_or_404(id)
    db.session.delete(disk)
    db.session.commit()
    return '', 204


@computers_bp.route('/computers/<int:computer_id>/os-instances', methods=['GET'])
def get_os_instances(computer_id):
    Computer.query.get_or_404(computer_id)
    instances = OsInstance.query.filter_by(computer_id=computer_id).all()
    return jsonify([i.to_dict(include_details=True) for i in instances])


@computers_bp.route('/computers/<int:computer_id>/os-instances', methods=['POST'])
def create_os_instance(computer_id):
    Computer.query.get_or_404(computer_id)
    data = request.get_json()
    instance = OsInstance(
        computer_id=computer_id,
        parent_os_id=data.get('parent_os_id'),
        name=data.get('name'),
        os_type=data.get('os_type'),
        ip_address=data.get('ip_address'),
        mac_address=data.get('mac_address'),
        port=data.get('port'),
        pcie_passthrough=data.get('pcie_passthrough'),
        notes=data.get('notes')
    )
    db.session.add(instance)
    db.session.commit()
    return jsonify(instance.to_dict()), 201


@computers_bp.route('/os-instances/<int:id>', methods=['DELETE'])
def delete_os_instance(id):
    instance = OsInstance.query.get_or_404(id)
    db.session.delete(instance)
    db.session.commit()
    return '', 204
