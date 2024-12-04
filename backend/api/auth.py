from flask import Blueprint, jsonify, request, url_for
from ..models import db, User, Influencer, Sponsor, Category
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import timedelta
import os
from ..caching import cache


auth = Blueprint("auth", __name__)


@auth.route("/login", methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"status" : "fail", "error" : "Username does not exists !"})
    
    if not check_password_hash(user.password, password):
        return jsonify({"status" : "fail", "error" : "Incorrect Password !"})

    if user.role == "influencer":
        cache.delete("influencers")
    
    authToken = create_access_token(identity=username, expires_delta=timedelta(days=5))
    return jsonify({"status" : "success", "authToken" : authToken, "role" : user.role, "username" : user.username, "email" : user.email})



@auth.route("/signup", methods=['POST'])
def signup():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")

    if User.query.filter_by(email=email).first():
        return jsonify({"status" : "fail", "error" : "Email ID already exists !"})
    
    if User.query.filter_by(username=username).first():
        return jsonify({"status" : "fail", "error" : "Username already exists !"})


    if role == "influencer":
        name = data.get("full_name")
        niche = data.get("niche")

        user = User(username=username, email=email, password=generate_password_hash(password), role=role)

        influencer = Influencer(username=username, name=name, niche=niche)

        db.session.add(user)
        db.session.add(influencer)

    
    else:
        name = data.get("company_name")
        industry = data.get("industry")

        user = User(username=username, email=email, password=generate_password_hash(password), role=role)
        
        sponsor = Sponsor(username=username, name=name, industry=industry)

        db.session.add(user)
        db.session.add(sponsor)


    db.session.commit()
    return jsonify({"status" : "success"})



@auth.route("/categories")
@cache.cached()
def categories():
    categories = [{"id" : category.id, "name" : category.name} for category in Category.query.all()]
    return jsonify(categories)



@auth.route("/profile-image")
@jwt_required()
def profile_image():
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()
    SERVER = "http://127.0.0.1:5000"
    return jsonify({"status" : "success", "url" : SERVER + (url_for("static", filename=user.profile_picture))})



@auth.route("/flagged")
@jwt_required()
def flagged():
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()
    
    return jsonify(user.flagged)



@auth.route("/profile_image_update", methods=['PUT', 'DELETE'])
@jwt_required()
def profile_image_update():
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()
    
    path = user.profile_picture
    if path != "profile_pictures/dpp.png":
        try:
            os.remove(rf"backend/static/{path}")
        except FileNotFoundError:
            pass

    if request.method == "PUT":
        profile = request.files.get("profile")
        ext = profile.filename.split(".")[-1]

        if ext.lower() not in ["png", "jpg", "jpeg", "webp", "svg", "gif"]:
            return jsonify({"status" : "error", "message" : "File format not supported !"})
        
        path = rf"profile_pictures/{user.username}.{ext}"
        profile.save(os.path.join("backend/static", path))
        user.profile_picture = path
        db.session.commit()
        return jsonify({"status" : "success", "message" : "Profile picture updated !", "url" : user.profile_picture})

    else:
        user.profile_picture = "profile_pictures/dpp.png"
        db.session.commit()
        return jsonify({"status" : "success", "message" : "Profile picture removed !", "url" : user.profile_picture})