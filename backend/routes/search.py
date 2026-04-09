from flask import Blueprint, request, jsonify
from models import Computer, OsInstance, Service

search_bp = Blueprint('search', __name__)


@search_bp.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify([])

    q_lower = query.lower()
    results = []

    computers = Computer.query.filter(
        Computer.name.ilike(f'%{query}%') |
        Computer.ip.ilike(f'%{query}%') |
        Computer.location.ilike(f'%{query}%') |
        Computer.remarks.ilike(f'%{query}%')
    ).all()
    for c in computers:
        results.append({
            'type': 'computer',
            'id': c.id,
            'name': c.name,
            'ip': c.ip,
            'location': c.location
        })

    os_instances = OsInstance.query.filter(
        OsInstance.name.ilike(f'%{query}%') |
        OsInstance.ip_address.ilike(f'%{query}%') |
        OsInstance.notes.ilike(f'%{query}%')
    ).all()
    for os in os_instances:
        results.append({
            'type': 'os_instance',
            'id': os.id,
            'name': os.name,
            'os_type': os.os_type,
            'ip_address': os.ip_address,
            'computer_id': os.computer_id,
            'computer_name': os.computer.name if os.computer else None
        })

    services = Service.query.filter(
        Service.name.ilike(f'%{query}%') |
        Service.url.ilike(f'%{query}%') |
        Service.description.ilike(f'%{query}%')
    ).all()
    for s in services:
        results.append({
            'type': 'service',
            'id': s.id,
            'name': s.name,
            'protocol': s.protocol,
            'url': s.url,
            'port': s.port,
            'os_instance_id': s.os_instance_id,
            'os_instance_name': s.os_instance.name if s.os_instance else None
        })

    return jsonify(results)


@search_bp.route('/export', methods=['GET'])
def export_data():
    from models import Computer
    import json

    computers = Computer.query.all()
    data = {
        'computers': [c.to_dict(include_details=True) for c in computers]
    }

    response = jsonify(data)
    response.headers['Content-Disposition'] = 'attachment; filename=hardware_data.json'
    return response


@search_bp.route('/import', methods=['POST'])
def import_data():
    from models import Computer, CPU, RAM, Disk, StoragePool, VirtualDisk, OsInstance, Service
    import json

    data = request.get_json()

    Computer.query.delete()
    CPU.query.delete()
    RAM.query.delete()
    Disk.query.delete()
    StoragePool.query.delete()
    VirtualDisk.query.delete()
    OsInstance.query.delete()
    Service.query.delete()
    db.session.commit()

    computer_map = {}

    for c_data in data.get('computers', []):
        c = Computer(
            name=c_data['name'],
            ip=c_data.get('ip'),
            location=c_data.get('location'),
            remarks=c_data.get('remarks'),
            status=c_data.get('status', 'online')
        )
        db.session.add(c)
        db.session.flush()
        computer_map[c_data['id']] = c.id

        for cpu_data in c_data.get('cpus', []):
            cpu = CPU(computer_id=c.id, model=cpu_data['model'], cores=cpu_data['cores'],
                      clock_speed=cpu_data.get('clock_speed'), purchase_date=cpu_data.get('purchase_date'),
                      remarks=cpu_data.get('remarks'))
            db.session.add(cpu)

        for ram_data in c_data.get('rams', []):
            ram = RAM(computer_id=c.id, brand=ram_data.get('brand'), model=ram_data.get('model'),
                      capacity_gb=ram_data.get('capacity_gb'), ram_type=ram_data.get('ram_type'),
                      slots_occupied=ram_data.get('slots_occupied'), purchase_date=ram_data.get('purchase_date'),
                      remarks=ram_data.get('remarks'))
            db.session.add(ram)

        for disk_data in c_data.get('disks', []):
            disk = Disk(computer_id=c.id, brand=disk_data.get('brand'), model=disk_data.get('model'),
                        capacity_gb=disk_data.get('capacity_gb'), interface=disk_data.get('interface'),
                        file_system=disk_data.get('file_system'), purpose=disk_data.get('purpose'),
                        slot_info=disk_data.get('slot_info'), is_boot_disk=disk_data.get('is_boot_disk', False),
                        purchase_date=disk_data.get('purchase_date'), remarks=disk_data.get('remarks'))
            db.session.add(disk)

        for sp_data in c_data.get('storage_pools', []):
            sp = StoragePool(computer_id=c.id, name=sp_data['name'], pool_type=sp_data.get('pool_type'),
                             total_capacity_gb=sp_data.get('total_capacity_gb'),
                             used_capacity_gb=sp_data.get('used_capacity_gb', 0))
            db.session.add(sp)

        for os_data in c_data.get('os_instances', []):
            os = OsInstance(computer_id=c.id, parent_os_id=os_data.get('parent_os_id'),
                            name=os_data['name'], os_type=os_data.get('os_type'),
                            ip_address=os_data.get('ip_address'), mac_address=os_data.get('mac_address'),
                            port=os_data.get('port'), pcie_passthrough=os_data.get('pcie_passthrough'),
                            notes=os_data.get('notes'))
            db.session.add(os)

    db.session.commit()
    return jsonify({'message': 'Import successful'}), 201
