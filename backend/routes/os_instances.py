from flask import Blueprint, request, jsonify
from models import db, OsInstance, Service

os_instances_bp = Blueprint('os_instances', __name__)


@os_instances_bp.route('/os-instances/<int:id>', methods=['GET'])
def get_os_instance(id):
    instance = OsInstance.query.get_or_404(id)
    return jsonify(instance.to_dict(include_details=True))


@os_instances_bp.route('/os-instances/<int:os_instance_id>/services', methods=['GET'])
def get_services(os_instance_id):
    OsInstance.query.get_or_404(os_instance_id)
    services = Service.query.filter_by(os_instance_id=os_instance_id).all()
    return jsonify([s.to_dict() for s in services])


@os_instances_bp.route('/os-instances/<int:os_instance_id>/services', methods=['POST'])
def create_service(os_instance_id):
    OsInstance.query.get_or_404(os_instance_id)
    data = request.get_json()
    service = Service(
        os_instance_id=os_instance_id,
        name=data.get('name'),
        protocol=data.get('protocol'),
        ip_address=data.get('ip_address'),
        port=data.get('port'),
        description=data.get('description')
    )
    db.session.add(service)
    db.session.commit()
    return jsonify(service.to_dict()), 201
