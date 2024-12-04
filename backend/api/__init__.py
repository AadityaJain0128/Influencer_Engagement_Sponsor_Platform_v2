from flask import Blueprint
from .auth import auth
from .admin import admin
from .influencer import influencer
from .sponsor import sponsor


api = Blueprint("api", __name__)
api.register_blueprint(auth, url_prefix="/auth/")
api.register_blueprint(admin, url_prefix="/admin/")
api.register_blueprint(influencer, url_prefix="/influencer/")
api.register_blueprint(sponsor, url_prefix="/sponsor/")