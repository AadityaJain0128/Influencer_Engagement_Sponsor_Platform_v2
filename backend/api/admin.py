from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from .utils import check_role
from ..models import db, Admin, User, Sponsor, Influencer, Campaign, Request, Transaction, Category


admin = Blueprint("admin", __name__)


@admin.route("/getDetails")
@jwt_required()
def getDetails():
    username = get_jwt_identity()
    if not check_role(username, "admin"):
        return jsonify({"status" : "fail", "error" : "Invalid Token"})

    admin = Admin.query.filter_by(username=username).first()

    return jsonify({"status" : "success", "id" : admin.id, "name" : admin.name})


@admin.route("/getData")
@jwt_required()
def dashboard():
    username = get_jwt_identity()
    if not check_role(username, "admin"):
        return jsonify({"status" : "fail", "error" : "Invalid Token"})

    admin = Admin.query.filter_by(username=username).first()

    users = User.query
    user_labels = ["Admin", "Sponsor", "Influencer"]
    user_values = [len(users.filter_by(role="admin").all()), len(users.filter_by(role="sponsor").all()), len(users.filter_by(role="influencer").all())]

    campaigns = Campaign.query
    active_campaigns = campaigns.filter(Campaign.completed == False, Campaign.influencer_id.isnot(None)).all()
    pending_campaigns = campaigns.filter(Campaign.completed == False, Campaign.influencer_id.is_(None)).all()
    completed_campaigns = campaigns.filter_by(completed=True).all()
    campaign_labels = ["Active Campaigns", "Pending Campaigns", "Completed Campaigns"]
    campaign_values = [len(active_campaigns), len(pending_campaigns), len(completed_campaigns)]

    campaign_ids = [c.id for c in Campaign.query.filter_by(paid=True).all()]
    transactions = Transaction.query.filter(Transaction.campaign_id.in_(campaign_ids)).all()
    transaction_labels = [t.campaign.name for t in transactions]
    transaction_values = [t.amount for t in transactions]

    flagged_labels = ["Flagged Campaigns", "UnFlagged Campaigns"]
    flagged_values = [len(campaigns.filter_by(flagged=True).all()), len(campaigns.filter_by(flagged=False).all())]

    categories = Category.query.all()
    category_labels = [c.name for c in categories]

    i = Influencer.query
    i_values = [len(i.filter_by(niche=c.name).all()) for c in categories]

    s = Sponsor.query
    s_values = [len(s.filter_by(industry=c.name).all()) for c in categories]

    req = Request.query
    request_labels = ["Influencer", "Sponsor"]
    request_values = [len(req.filter_by(sent_by="influencer").all()), len(req.filter_by(sent_by="sponsor").all())]

    status_labels = ["Public", "Private"]
    status_values = [len(campaigns.filter_by(visibility="public").all()), len(campaigns.filter_by(visibility="private").all())]

    return jsonify({"status" : "success", "user_labels" : user_labels, "user_values" : user_values, "campaign_labels" : campaign_labels, "campaign_values" : campaign_values, "transaction_labels" : transaction_labels, "transaction_values" : transaction_values, "flagged_labels" : flagged_labels, "flagged_values" : flagged_values, "category_labels" : category_labels, "i_values" : i_values, "s_values" : s_values, "request_labels" : request_labels, "request_values" : request_values, "status_labels" : status_labels, "status_values" : status_values})



@admin.route("/sponsors")
@jwt_required()
def sponsors():
    username = get_jwt_identity()
    if not check_role(username, "admin"):
        return jsonify({"status" : "fail", "error" : "Invalid Token"})

    admin = Admin.query.filter_by(username=username).first()

    uname = request.args.get("username", "")
    sponsors = Sponsor.query.filter_by(verified=False)
    if uname:
        sponsors = sponsors.filter(Sponsor.username.contains(uname) | Sponsor.name.contains(uname))
    sponsors = sponsors.all()

    sponsors_json = []
    for s in sponsors:
        profile_picture = User.query.filter_by(username=s.username).first().profile_picture
        sp = {
            "id" : s.id,
            "username" : s.username,
            "name" : s.name,
            "industry" : s.industry,
            "verified" : s.verified,
            "profile_picture" : profile_picture
        }
        sponsors_json.append(sp)

    return jsonify({"status" : "success", "sponsors" : sponsors_json})


@admin.route("/verify", methods=['POST'])
@jwt_required()
def verify():
    username = get_jwt_identity()
    if not check_role(username, "admin"):
        return jsonify({"status" : "fail", "error" : "Invalid Token"})

    admin = Admin.query.filter_by(username=username).first()

    id = request.json.get("id", "")
    sponsor = Sponsor.query.filter_by(id=id).first()
    sponsor.verified = True
    db.session.commit()

    return jsonify({"status" : "success"})


@admin.route("/campaigns", methods=['GET', 'POST'])
@jwt_required()
def campaigns():
    username = get_jwt_identity()
    if not check_role(username, "admin"):
        return jsonify({"status" : "fail", "error" : "Invalid Token"})

    admin = Admin.query.filter_by(username=username).first()

    if request.method == "POST":
        id = request.json.get("id")
        campaign = Campaign.query.filter_by(id=id).first()
        campaign.flagged = True
        db.session.commit()
        return jsonify({"status" : "success"})
    
    cname = request.args.get("cname", "")
    sname = request.args.get("sname", "")
    campaigns = Campaign.query.filter_by(completed=False, flagged=False)
    if cname:
        campaigns = campaigns.filter(Campaign.name.contains(cname))
    if sname:
        campaigns = campaigns.filter(Campaign.sponsor.has(Sponsor.name.contains(sname)) | Campaign.sponsor.has(Sponsor.username.contains(sname)))
    campaigns = campaigns.all()

    campaigns_json = []
    for c in campaigns:
        inf = None
        if c.influencer_id:
            i = Influencer.query.filter_by(id=c.influencer_id).first()
            inf = {"id" : i.id, "username" : i.username, "name" : i.name, "niche" : i.niche}
        cam = {
            "id" : c.id,
            "name" : c.name,
            "description" : c.description,
            "start_date" : c.start_date.strftime("%d %B, %Y"),
            "end_date" : c.end_date.strftime("%d %B, %Y"),
            "budget" : c.budget,
            "visibility" : c.visibility,
            "influencer" : inf,
            "sponsor" : {"id" : c.sponsor.id, "username" : c.sponsor.username, "name" : c.sponsor.name, "industry" : c.sponsor.industry}
        }
        campaigns_json.append(cam)

    return jsonify({"status" : "success", "campaigns" : campaigns_json})


@admin.route("/flagged_campaigns", methods=['GET', 'POST'])
@jwt_required()
def flagged_campaigns():
    username = get_jwt_identity()
    if not check_role(username, "admin"):
        return jsonify({"status" : "fail", "error" : "Invalid Token"})

    admin = Admin.query.filter_by(username=username).first()

    if request.method == "POST":
        id = request.json.get("id")
        campaign = Campaign.query.filter_by(id=id).first()
        campaign.flagged = False
        db.session.commit()
        return jsonify({"status" : "success"})

    cname = request.args.get("cname", "")
    sname = request.args.get("sname", "")
    campaigns = Campaign.query.filter_by(flagged=True)
    if cname:
        campaigns = campaigns.filter(Campaign.name.contains(cname))
    if sname:
        campaigns = campaigns.filter(Campaign.sponsor.has(Sponsor.name.contains(sname)) | Campaign.sponsor.has(Sponsor.username.contains(sname)))
    
    campaigns = campaigns.all()
    campaigns_json = []
    for c in campaigns:
        inf = None
        if c.influencer_id:
            i = Influencer.query.filter_by(id=c.influencer_id).first()
            inf = {"id" : i.id, "username" : i.username, "name" : i.name, "niche" : i.niche}
        cam = {
            "id" : c.id,
            "name" : c.name,
            "description" : c.description,
            "start_date" : c.start_date.strftime("%d %B, %Y"),
            "end_date" : c.end_date.strftime("%d %B, %Y"),
            "budget" : c.budget,
            "visibility" : c.visibility,
            "influencer" : inf,
            "sponsor" : {"id" : c.sponsor.id, "username" : c.sponsor.username, "name" : c.sponsor.name, "industry" : c.sponsor.industry}
        }
        campaigns_json.append(cam)

    return jsonify({"status" : "success", "campaigns" : campaigns_json})


@admin.route("/users", methods=['GET', 'POST'])
@jwt_required()
def users():
    username = get_jwt_identity()
    if not check_role(username, "admin"):
        return jsonify({"status" : "fail", "error" : "Invalid Token"})

    admin = Admin.query.filter_by(username=username).first()

    if request.method == "POST":
        username = request.json.get("username")
        user = User.query.filter_by(username=username).first()
        user.flagged = True
        db.session.commit()
        return jsonify({"status" : "success"})


    uname = request.args.get("uname")
    role = request.args.get("role")

    users = User.query.filter((User.flagged==False) & (User.role != "admin"))
    if uname:
        users = users.filter(User.username.contains(uname) | User.email.contains(uname))
    if role:
        users = users.filter_by(role=role)
    users = users.all()

    users_json = []
    for user in users:
        u = {
            "username" : user.username,
            "email" : user.email,
            "role" : user.role,
            "profile_picture" : user.profile_picture
        }
        users_json.append(u)

    return jsonify({"status" : "success", "users" : users_json})


@admin.route("/flagged_users", methods=['GET', 'POST'])
@jwt_required()
def flagged_users():
    username = get_jwt_identity()
    if not check_role(username, "admin"):
        return jsonify({"status" : "fail", "error" : "Invalid Token"})

    admin = Admin.query.filter_by(username=username).first()

    if request.method == "POST":
        username = request.json.get("username")
        user = User.query.filter_by(username=username).first()
        user.flagged = False
        db.session.commit()
        return jsonify({"status" : "success"})


    uname = request.args.get("uname")
    role = request.args.get("role")

    users = User.query.filter((User.flagged==True) & (User.role != "admin"))
    if uname:
        users = users.filter(User.username.contains(uname) | User.email.contains(uname))
    if role:
        users = users.filter_by(role=role)
    users = users.all()

    users_json = []
    for user in users:
        u = {
            "username" : user.username,
            "email" : user.email,
            "role" : user.role,
            "profile_picture" : user.profile_picture
        }
        users_json.append(u)

    return jsonify({"status" : "success", "users" : users_json})