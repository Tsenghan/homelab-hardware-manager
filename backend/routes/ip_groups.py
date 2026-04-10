from flask import Blueprint, request, jsonify
from backend.models import db, IpGroup

ip_groups_bp = Blueprint('ip_groups', __name__)


@ip_groups_bp.route('/ip-groups', methods=['GET'])
def get_ip_groups():
    groups = IpGroup.query.all()
    return jsonify([g.to_dict() for g in groups])


@ip_groups_bp.route('/ip-groups', methods=['POST'])
def create_ip_group():
    data = request.get_json()
    group = IpGroup(
        name=data.get('name'),
        subnet=data.get('subnet'),
        start_ip=data.get('startIp'),
        end_ip=data.get('endIp')
    )
    db.session.add(group)
    db.session.commit()
    return jsonify(group.to_dict()), 201


@ip_groups_bp.route('/ip-groups/<int:id>', methods=['PUT'])
def update_ip_group(id):
    group = IpGroup.query.get_or_404(id)
    data = request.get_json()
    group.name = data.get('name', group.name)
    group.subnet = data.get('subnet', group.subnet)
    group.start_ip = data.get('startIp', group.start_ip)
    group.end_ip = data.get('endIp', group.end_ip)
    db.session.commit()
    return jsonify(group.to_dict())


@ip_groups_bp.route('/ip-groups/<int:id>', methods=['DELETE'])
def delete_ip_group(id):
    group = IpGroup.query.get_or_404(id)
    db.session.delete(group)
    db.session.commit()
    return '', 204
