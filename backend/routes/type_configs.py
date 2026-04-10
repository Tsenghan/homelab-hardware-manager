from flask import Blueprint, request, jsonify
from models import db, TypeConfig

type_configs_bp = Blueprint('type_configs', __name__)


@type_configs_bp.route('/type-configs', methods=['GET'])
def get_type_configs():
    configs = TypeConfig.query.all()
    return jsonify([c.to_dict() for c in configs])


@type_configs_bp.route('/type-configs', methods=['POST'])
def create_type_config():
    data = request.get_json()
    config = TypeConfig(
        category=data.get('category'),
        name=data.get('name'),
        color=data.get('color', '#409EFF')
    )
    db.session.add(config)
    db.session.commit()
    return jsonify(config.to_dict()), 201


@type_configs_bp.route('/type-configs/<int:id>', methods=['PUT'])
def update_type_config(id):
    config = TypeConfig.query.get_or_404(id)
    data = request.get_json()
    config.name = data.get('name', config.name)
    config.color = data.get('color', config.color)
    db.session.commit()
    return jsonify(config.to_dict())


@type_configs_bp.route('/type-configs/<int:id>', methods=['DELETE'])
def delete_type_config(id):
    config = TypeConfig.query.get_or_404(id)
    db.session.delete(config)
    db.session.commit()
    return '', 204
