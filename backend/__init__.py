from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from .models import db
from .config import Config
from . import worker
from .caching import cache
import os


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    create_db(app)

    jwt = JWTManager(app)

    CORS(app)

    from .api import api
    app.register_blueprint(api, url_prefix="/api/")


    cache.init_app(app)

    celery = worker.celery
    celery.conf.update(
        broker_url = app.config["CELERY_BROKER_URL"],
        result_backend = app.config["CELERY_RESULT_BACKEND"],
        broker_connection_retry_on_startup = True,
        timezone = "Asia/Kolkata"
    )
    celery.Task = worker.ContextTask
    app.app_context().push()
    return app, celery


def create_db(app):
    if not os.path.exists(os.path.join(app.instance_path, "database.db")):
        with app.app_context():
            db.create_all()

            from .models import Category, User, Admin
            
            categories = ["Technology", "Education", "Entertainment", "Fashion", "Skincare", "Finance", "Healthcare", "Media", "Travel", "Sports", "Gaming"]
            for i in categories:
                c = Category(name=i)
                db.session.add(c)

            from werkzeug.security import generate_password_hash
            user = User(username="admin", email="admin@gmail.com", role="admin", password=generate_password_hash("admin"))
            admin = Admin(username="admin", name="Aaditya Jain")
            db.session.add(user)
            db.session.add(admin)

            db.session.commit()