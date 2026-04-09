from flask import Blueprint, request, jsonify
from models import db, StoragePool, VirtualDisk

storage_bp = Blueprint('storage', __name__)


@storage_bp.route('/storage-pools/<int:id>', methods=['GET'])
def get_storage_pool(id):
    pool = StoragePool.query.get_or_404(id)
    return jsonify(pool.to_dict(include_disks=True))


@storage_bp.route('/storage-pools/<int:id>/trace', methods=['GET'])
def get_storage_trace(id):
    pool = StoragePool.query.get_or_404(id)
    trace = {
        'storage_pool': pool.to_dict(),
        'computer': pool.computer.to_dict(),
        'physical_disks': [d.to_dict() for d in pool.computer.disks],
        'virtual_disks': [vd.to_dict() for vd in pool.virtual_disks]
    }
    return jsonify(trace)


@storage_bp.route('/storage-pools/<int:pool_id>/virtual-disks', methods=['GET'])
def get_virtual_disks(pool_id):
    StoragePool.query.get_or_404(pool_id)
    vdisks = VirtualDisk.query.filter_by(storage_pool_id=pool_id).all()
    return jsonify([v.to_dict() for v in vdisks])


@storage_bp.route('/storage-pools/<int:pool_id>/virtual-disks', methods=['POST'])
def create_virtual_disk(pool_id):
    StoragePool.query.get_or_404(pool_id)
    data = request.get_json()
    vdisk = VirtualDisk(
        storage_pool_id=pool_id,
        os_instance_id=data.get('os_instance_id'),
        name=data.get('name'),
        format=data.get('format'),
        size_gb=data.get('size_gb')
    )
    db.session.add(vdisk)
    db.session.commit()
    return jsonify(vdisk.to_dict()), 201


@storage_bp.route('/virtual-disks/<int:id>', methods=['GET'])
def get_virtual_disk(id):
    vdisk = VirtualDisk.query.get_or_404(id)
    return jsonify(vdisk.to_dict())
