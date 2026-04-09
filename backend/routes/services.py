from flask import Blueprint, request, jsonify
from models import db, Service

services_bp = Blueprint('services', __name__)


@services_bp.route('/services/<int:id>', methods=['GET'])
def get_service(id):
    service = Service.query.get_or_404(id)
    return jsonify(service.to_dict())


@services_bp.route('/services/<int:id>', methods=['PUT'])
def update_service(id):
    service = Service.query.get_or_404(id)
    data = request.get_json()
    service.name = data.get('name', service.name)
    service.protocol = data.get('protocol', service.protocol)
    service.ip_address = data.get('ip_address', service.ip_address)
    service.port = data.get('port', service.port)
    service.description = data.get('description', service.description)
    db.session.commit()
    return jsonify(service.to_dict())


@services_bp.route('/services/<int:id>', methods=['DELETE'])
def delete_service(id):
    service = Service.query.get_or_404(id)
    db.session.delete(service)
    db.session.commit()
    return '', 204
