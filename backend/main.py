import os
import sys

# Ensure backend/ is in path whether running via `python main.py` or gunicorn
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from models import db


def create_app():
    app = Flask(__name__)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(base_dir)  # go up from backend/ to project root
    frontend_dir = os.path.join(project_dir, 'dist')  # Vite build 输出在根目录 dist/
    db_path = os.path.join(base_dir, 'data', 'hardware.db')
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    CORS(app)

    from routes.computers import computers_bp
    from routes.os_instances import os_instances_bp
    from routes.services import services_bp
    from routes.search import search_bp
    from routes.ip_groups import ip_groups_bp
    from routes.type_configs import type_configs_bp

    app.register_blueprint(computers_bp, url_prefix='/api')
    app.register_blueprint(os_instances_bp, url_prefix='/api')
    app.register_blueprint(services_bp, url_prefix='/api')
    app.register_blueprint(search_bp, url_prefix='/api')
    app.register_blueprint(ip_groups_bp, url_prefix='/api')
    app.register_blueprint(type_configs_bp, url_prefix='/api')

    @app.route('/')
    def index():
        return send_from_directory(frontend_dir, 'index.html')

    @app.route('/<path:path>')
    def static_files(path):
        # Serve Vue static assets
        static_path = os.path.join(frontend_dir, path)
        if os.path.exists(static_path):
            return send_from_directory(frontend_dir, path)
        # Fallback to index.html for SPA routing
        return send_from_directory(frontend_dir, 'index.html')

    with app.app_context():
        db.create_all()
        seed_data_if_empty()

    return app


def seed_data_if_empty():
    """如果数据库为空，加载完整的示例数据"""
    from models import Computer
    if Computer.query.first() is None:
        from init_db import load_example_data
        load_example_data()
        print('Example data loaded.')


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
