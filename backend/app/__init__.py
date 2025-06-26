from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_migrate import Migrate
from .config import Config

db = SQLAlchemy()
migrate = Migrate()
socketio = SocketIO(cors_allowed_origins='*')

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app, message_queue=app.config.get('REDIS_URL'))

    from . import routes, sockets
    app.register_blueprint(routes.bp)
    sockets.register_socketio_events(socketio)

    return app
