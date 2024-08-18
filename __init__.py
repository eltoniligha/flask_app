from flask import Flask
from app.models import db
from app.routes import api
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    
    app.register_blueprint(api)
    
    with app.app_context():
        db.create_all()  # Create database tables
    
    return app
