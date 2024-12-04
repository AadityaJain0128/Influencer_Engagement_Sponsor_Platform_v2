from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from .utils import check_role
from ..models import db, User, Sponsor, Influencer, Campaign, Request, Rating, Transaction
from datetime import datetime
from ..caching import cache


sponsor = Blueprint("sponsor", __name__)


@sponsor.route("/verified")
@jwt_required()
def verified():
    username = get_jwt_identity()
    if not check_role(username, "sponsor"):
        return jsonify({"status" : "fail", "error" : "Invalid Token"})
    
    sponsor = Sponsor.query.filter_by(username=username).first()
    return jsonify(sponsor.verified)


@sponsor.route("/getDetails", methods=['GET'])
@jwt_required()
def getDetails():
    username = get_jwt_identity()
    if not check_role(username, "sponsor"):
        return jsonify({"status" : "fail", "error" : "Invalid Token"})

    sponsor = Sponsor.query.filter_by(username=username).first()
    
    return jsonify({"status" : "success", "id" : sponsor.id, "name" : sponsor.name, "category" : sponsor.industry})



@sponsor.route("/dashboard")
@jwt_required()
def dashboard():
    username = get_jwt_identity()
    if not check_role(username, "sponsor"):
        return jsonify({"status" : "fail", "error" : "Invalid Token"})
    
    sponsor = Sponsor.query.filter_by(username=username).first()
    active_campaigns = Campaign.query.filter(Campaign.sponsor_id==sponsor.id, Campaign.completed==False, Campaign.influencer_id.isnot(None)).all()
    active_campaigns_json = []
    for campaign in active_campaigns:
        c = {
            "id" : campaign.id,
            "name" : campaign.name,
            "description" : campaign.description,
            "sponsor" : {"id" : campaign.sponsor.id, "name" : campaign.sponsor.name},
            "start_date" : campaign.start_date.strftime("%d %b, %Y"),
            "end_date" : campaign.end_date.strftime("%d %b, %Y"),
            "budget" : campaign.budget,
            "visibility" : campaign.visibility,
            "flagged" : campaign.flagged,
            "influencer" : {"id" : campaign.influencer_id, "name" : Influencer.query.filter_by(id=campaign.influencer_id).first().name, "username" : Influencer.query.filter_by(id=campaign.influencer_id).first().username}
        }
        active_campaigns_json.append(c)

    campaign_ids = Campaign.query.filter(Campaign.sponsor_id==sponsor.id, Campaign.influencer_id.is_(None)).with_entities(Campaign.id)
    recieved_requests = Request.query.filter(Request.campaign_id.in_(campaign_ids), Request.sent_by=="influencer", Request.status=="pending").all()

    recieved_requests_json = []
    for req in recieved_requests:
        inf = Influencer.query.filter_by(id=req.influencer_id).first()
        r = {
            "id" : req.id,
            "campaign" : {"id" : req.campaign_id, "name" : req.campaign.name, "budget" : req.campaign.budget},
            "messages" : req.messages,
            "requirements" : req.requirements,
            "budget" : req.budget,
            "status" : req.status,
            "influencer" : {"id" : req.influencer_id, "name" : inf.name, "username" : inf.username}
        }
        recieved_requests_json.append(r)

    return jsonify({"status" : "success", "active_campaigns" : active_campaigns_json[::-1], "recieved_requests" : recieved_requests_json[::-1]})


@sponsor.route("/getCampaigns")
@jwt_required()
def getCampaigns():
    username = get_jwt_identity()
    if not check_role(username, "sponsor"):
        return jsonify({"status" : "fail", "error" : "Invalid Token"})
    
    sponsor = Sponsor.query.filter_by(username=username).first()

    campaigns = Campaign.query.filter_by(sponsor_id=sponsor.id)
    active_campaigns = campaigns.filter(Campaign.completed == False, Campaign.influencer_id.isnot(None)).all()
    pending_campaigns = campaigns.filter(Campaign.completed == False, Campaign.influencer_id.is_(None)).all()
    completed_campaigns = campaigns.filter_by(completed=True).all()

    active_campaigns_json = []
    for campaign in active_campaigns:
        c = {
            "id" : campaign.id,
            "name" : campaign.name,
            "description" : campaign.description,
            "sponsor" : {"id" : campaign.sponsor.id, "name" : campaign.sponsor.name},
            "start_date" : campaign.start_date.strftime("%d %b, %Y"),
            "end_date" : campaign.end_date.strftime("%d %b, %Y"),
            "budget" : campaign.budget,
            "visibility" : campaign.visibility,
            "flagged" : campaign.flagged,
            "influencer" : {"id" : campaign.influencer_id, "name" : Influencer.query.filter_by(id=campaign.influencer_id).first().name, "username" : Influencer.query.filter_by(id=campaign.influencer_id).first().username}
        }
        active_campaigns_json.append(c)

    pending_campaigns_json = []
    for campaign in pending_campaigns:
        c = {
            "id" : campaign.id,
            "name" : campaign.name,
            "description" : campaign.description,
            "sponsor" : {"id" : campaign.sponsor.id, "name" : campaign.sponsor.name},
            "start_date" : campaign.start_date.strftime("%d %b, %Y"),
            "end_date" : campaign.end_date.strftime("%d %b, %Y"),
            "budget" : campaign.budget,
            "visibility" : campaign.visibility,
            "flagged" : campaign.flagged
        }
        pending_campaigns_json.append(c)

    completed_campaigns_json = []
    for campaign in completed_campaigns:
        c = {
            "id" : campaign.id,
            "name" : campaign.name,
            "description" : campaign.description,
            "sponsor" : {"id" : campaign.sponsor.id, "name" : campaign.sponsor.name},
            "start_date" : campaign.start_date.strftime("%d %b, %Y"),
            "end_date" : campaign.end_date.strftime("%d %b, %Y"),
            "budget" : campaign.budget,
            "visibility" : campaign.visibility,
            "flagged" : campaign.flagged,
            "influencer" : {"id" : campaign.influencer_id, "name" : Influencer.query.filter_by(id=campaign.influencer_id).first().name, "username" : Influencer.query.filter_by(id=campaign.influencer_id).first().username}
        }
        completed_campaigns_json.append(c)


    return jsonify({"status" : "success", "active_campaigns" : active_campaigns_json[::-1], "pending_campaigns" : pending_campaigns_json[::-1], "completed_campaigns" : completed_campaigns_json[::-1]})


@sponsor.route("/addCampaign", methods=['POST'])
@jwt_required()
def addCampaign():
    username = get_jwt_identity()
    if not check_role(username, "sponsor"):
        return jsonify({"status" : "fail", "error" : "Invalid Token"})
    
    sponsor = Sponsor.query.filter_by(username=username).first()

    data = request.json
    name = data.get("name")
    description = data.get("description")
    start_date = datetime.strptime(data.get("start_date"), "%Y-%m-%d")
    end_date = datetime.strptime(data.get("end_date"), "%Y-%m-%d")
    budget = float(data.get("budget"))
    visibility = data.get("visibility")

    campaign = Campaign(name=name, description=description, start_date=start_date, end_date=end_date, budget=budget, visibility=visibility, sponsor_id=sponsor.id)
    db.session.add(campaign)
    db.session.commit()

    cache.delete("campaigns")
    return jsonify({"status" : "success"})


@sponsor.route("/campaigns/<int:id>", methods=['GET', 'PUT', 'POST', 'DELETE'])
@jwt_required()
def campaignDetails(id):
    username = get_jwt_identity()
    if not check_role(username, "sponsor"):
        return jsonify({"status" : "fail", "error" : "Invalid Token"})
    
    sponsor = Sponsor.query.filter_by(username=username).first()
    campaign = Campaign.query.filter_by(id=id, sponsor_id=sponsor.id).first()
    if not campaign:
        return jsonify({"status" : "fail", "message" : "Invalid Campaign !"})


    if request.method == "PUT":
        data = request.json
        campaign.name, campaign.description, campaign.start_date, campaign.end_date, campaign.budget, campaign.visibility = data.get("cname"), data.get("description"), datetime.strptime(data.get("start_date"), "%Y-%m-%d"), datetime.strptime(data.get("end_date"), "%Y-%m-%d"), data.get("budget"), data.get("visibility")

        db.session.commit()
        return jsonify({"status" : "success"})
    
    if request.method == "POST":
        if campaign.flagged:
            return jsonify({"status" : "error", "message" : "Campaign has been flagged by Admin !"})

        influencer = Influencer.query.filter_by(id=campaign.influencer_id).first()
        transaction = Transaction(influencer_id=influencer.id, campaign_id=campaign.id, amount=campaign.budget, date=datetime.now())
        campaign.paid = True
        campaign.completed = True
        db.session.add(transaction)
        db.session.commit()
        return jsonify({"status" : "success", "message" : "Campaign has been marked as completed !"})
    
    if request.method == "DELETE":
        for r in campaign.requests:
            db.session.delete(r)
        db.session.delete(campaign)
        db.session.commit()
        return jsonify({"status" : "success", "message" : "Campaign has been deleted !"})
        
        
    recieved_requests = Request.query.filter_by(campaign_id=id, sent_by="influencer").all()
    sent_requests = Request.query.filter_by(campaign_id=id, sent_by="sponsor").all()

    recieved_requests_json = []
    sent_requests_json = []

    for req in recieved_requests:
        inf = Influencer.query.filter_by(id=req.influencer_id).first()
        r = {
            "id" : req.id,
            "campaign" : {"id" : req.campaign_id, "name" : req.campaign.name, "budget" : req.campaign.budget},
            "messages" : req.messages,
            "requirements" : req.requirements,
            "budget" : req.budget,
            "status" : req.status,
            "influencer" : {"id" : req.influencer_id, "name" : inf.name, "username" : inf.username}
        }
        recieved_requests_json.append(r)

    for req in sent_requests:
        inf = Influencer.query.filter_by(id=req.influencer_id).first()
        r = {
            "id" : req.id,
            "campaign" : {"id" : req.campaign_id, "name" : req.campaign.name, "budget" : req.campaign.budget},
            "messages" : req.messages,
            "requirements" : req.requirements,
            "budget" : req.budget,
            "status" : req.status,
            "influencer" : {"id" : req.influencer_id, "name" : inf.name, "username" : inf.username}
        }
        sent_requests_json.append(r)

    inf = None
    if campaign.influencer_id:
        inf = {"id" : campaign.influencer_id, "name" : Influencer.query.filter_by(id=campaign.influencer_id).first().name, "username" : Influencer.query.filter_by(id=campaign.influencer_id).first().username}
    r = None
    rating = Rating.query.filter_by(campaign_id=campaign.id).first()
    if rating:
        r = {"rating" : rating.rating}

    campaign_json = {
        "id" : campaign.id,
        "name" : campaign.name,
        "description" : campaign.description,
        "start_date" : campaign.start_date.strftime("%Y-%m-%d"),
        "end_date" : campaign.end_date.strftime("%Y-%m-%d"),
        "budget" : campaign.budget,
        "visibility" : campaign.visibility,
        "flagged" : campaign.flagged,
        "influencer" : inf,
        "rating" : r,
        "completed" : campaign.completed
    }

    return jsonify({"status" : "success", "sent_requests" : sent_requests_json[::-1], "recieved_requests" : recieved_requests_json[::-1], "campaign" : campaign_json})


@sponsor.route("/request", methods=['POST', 'PUT'])
@jwt_required()
def handle_request():
    username = get_jwt_identity()
    if not check_role(username, "sponsor"):
        return jsonify({"status" : "fail", "error" : "Invalid Token"})
    
    sponsor = Sponsor.query.filter_by(username=username).first()

    id = request.json.get("id")
    req = Request.query.filter_by(id=id).first()
    campaign = req.campaign

    if campaign.flagged:
        return jsonify({"status" : "fail", "message" : f"Request failed as the campaign is flagged by admin !"})

    if request.method == "PUT":
        messages = request.json.get("messages")
        requirements = request.json.get("requirements")
        budget = request.json.get("budget")

        req.messages = messages
        req.requirements = requirements
        req.budget = budget
        db.session.commit()
        return jsonify({"status" : "success", "message" : "Request has been updated !"})


    type = request.json.get("type")
    if type == "accept":
        if campaign.completed or campaign.influencer_id:
            return jsonify({"status" : "fail", "message" : "Invalid Request !"})
        
        for r in campaign.requests:
            r.status = "expired"
        req.status = "accepted"
        campaign.budget = req.budget
        campaign.influencer_id = req.influencer_id
    else:
        req.status = "rejected"
    
    db.session.commit()
    return jsonify({"status" : "success", "message" : f"Request {type}ed !"})


@sponsor.route("/rating", methods=['POST'])
@jwt_required()
def rating():
    username = get_jwt_identity()
    if not check_role(username, "sponsor"):
        return jsonify({"status" : "error", "error" : "Invalid Token"})
    
    sponsor = Sponsor.query.filter_by(username=username).first()

    id = request.json.get("id")
    rating = request.json.get("rating")
    campaign = Campaign.query.filter_by(id=id, sponsor_id=sponsor.id).first()
    if not campaign:
        return jsonify({"status" : "error", "message" : "Invalid Campaign !"})
    
    if campaign.flagged:
        return jsonify({"status" : "error", "message" : "Campaign has been flagged by Admin !"})
    
    if Rating.query.filter_by(campaign_id=campaign.id).first():
        return jsonify({"status" : "error", "message" : "Rating has already been submitted !"})

    r = Rating(campaign_id=campaign.id, influencer_id=campaign.influencer_id, rating=rating)
    db.session.add(r)
    db.session.commit()
    return jsonify({"status" : "success", "message" : "Rating has been submitted !"})


@sponsor.route("/find")
@cache.cached(key_prefix="influencers")
@jwt_required()
def find():
    username = get_jwt_identity()
    if not check_role(username, "sponsor"):
        return jsonify({"status" : "fail", "error" : "Invalid Token"})
    
    sponsor = Sponsor.query.filter_by(username=username).first()

    campaigns = Campaign.query.filter(Campaign.sponsor_id==sponsor.id, Campaign.completed == False, Campaign.influencer_id.is_(None)).all()

    campaigns_json = []
    for c in campaigns:
        cam = {
            "id" : c.id,
            "name" : c.name,
            "description" : c.description,
            "start_date" : c.start_date,
            "end_date" : c.end_date,
            "budget" : c.budget,
            "visibility" : c.visibility,
            "flagged" : c.flagged
        }
        campaigns_json.append(cam)

    name = request.args.get("name", "")
    niche = request.args.get("niche", "")

    influencers = Influencer.query.filter(Influencer.user.has(User.flagged==False))
    if name:
        influencers = influencers.filter(Influencer.username.contains(name) | Influencer.name.contains(name))
    if niche:
        influencers = influencers.filter(Influencer.niche.contains(niche))
    influencers = influencers.order_by(Influencer.reach.desc()).all()

    influencers_json = []
    for i in influencers:
        avg_rating = []
        ratings = Rating.query.filter_by(influencer_id=i.id).all()
        if ratings:
            avg_rating = [round(sum([r.rating for r in ratings]) / len(ratings), 1), len(ratings)]
        
        profile_picture = User.query.filter_by(username=i.username).first().profile_picture
        inf = {
            "id" : i.id,
            "username" : i.username,
            "name" : i.name,
            "niche" : i.niche,
            "reach" : i.reach,
            "socials" : i.socials,
            "avg_rating" : avg_rating,
            "profile_picture" : profile_picture
        }
        influencers_json.append(inf)

    return jsonify({"status" : "success", "campaigns" : campaigns_json, "influencers" : influencers_json})


@sponsor.route("/send_request", methods=['POST'])
@jwt_required()
def send_request():
    username = get_jwt_identity()
    if not check_role(username, "sponsor"):
        return jsonify({"status" : "fail", "error" : "Invalid Token"})
    
    sponsor = Sponsor.query.filter_by(username=username).first()

    data = request.json
    messages = data.get("messages")
    requirements = data.get("requirements")
    influencer_id = data.get("influencer_id")
    campaign_id = data.get("campaign_id")
    req = Request.query.filter_by(campaign_id=campaign_id, influencer_id=influencer_id, sent_by="sponsor").first()
    if req:
        return jsonify({"status" : "fail", "message" : "Request has already been sent !"})
    
    campaign = Campaign.query.filter_by(id=campaign_id).first()
    req = Request(messages=messages, requirements=requirements, campaign_id=campaign_id, influencer_id=influencer_id, sent_by="sponsor", budget=campaign.budget)
    db.session.add(req)
    db.session.commit()
    return jsonify({"status" : "success", "message" : "Request has been sent !"})


@sponsor.route("/transactions")
@jwt_required()
def transactions():
    username = get_jwt_identity()
    if not check_role(username, "sponsor"):
        return jsonify({"status" : "fail", "error" : "Invalid Token"})
    
    sponsor = Sponsor.query.filter_by(username=username).first()

    campaign_ids = Campaign.query.filter(Campaign.sponsor_id==sponsor.id).with_entities(Campaign.id)
    transactions = Transaction.query.filter(Transaction.campaign_id.in_(campaign_ids)).all()

    transactions_json = []
    for t in transactions:
        inf = Influencer.query.filter_by(id=t.influencer_id).first()
        cam = Campaign.query.filter_by(id=t.campaign_id).first()
        tr = {
            "id" : t.id,
            "influencer" : {"id" : inf.id, "username" : inf.username, "name" : inf.name},
            "campaign" : {"id" : cam.id, "name" : cam.name},
            "amount" : t.amount,
            "date" : t.date.strftime("%d %b, %Y"),
            "time" : t.date.strftime("%H:%M:%S")
        }
        transactions_json.append(tr)

    return jsonify({"status" : "success", "transactions" : transactions_json[::-1]})


@sponsor.route("/profile_update", methods=['PUT'])
@jwt_required()
def profile_update():
    username = get_jwt_identity()
    if not check_role(username, "sponsor"):
        return jsonify({"status" : "fail", "error" : "Invalid Token"})
    
    sponsor = Sponsor.query.filter_by(username=username).first()

    data = request.json
    name, industry = data.get("name"), data.get("industry")

    sponsor.name = name
    sponsor.industry = industry
    db.session.commit()
    return jsonify({"status" : "success", "message" : "Profile Updated !", "name" : sponsor.name, "industry" : sponsor.industry})


@sponsor.route("/stats")
@jwt_required()
def stats():
    username = get_jwt_identity()
    if not check_role(username, "sponsor"):
        return jsonify({"status" : "fail", "error" : "Invalid Token"})
    
    sponsor = Sponsor.query.filter_by(username=username).first()

    campaigns = Campaign.query.filter_by(sponsor_id=sponsor.id)
    active_campaigns = campaigns.filter(Campaign.completed == False, Campaign.influencer_id.isnot(None)).all()
    pending_campaigns = campaigns.filter(Campaign.completed == False, Campaign.influencer_id.is_(None)).all()
    completed_campaigns = campaigns.filter_by(completed=True).all()
    campaign_labels = ["Active Campaigns", "Pending Campaigns", "Completed Campaigns"]
    campaign_values = [len(active_campaigns), len(pending_campaigns), len(completed_campaigns)]

    campaign_ids = [c.id for c in sponsor.campaigns.filter_by(paid=True).all()]
    transactions = Transaction.query.filter(Transaction.campaign_id.in_(campaign_ids)).all()
    transaction_labels = [t.campaign.name for t in transactions]
    transaction_values = [t.amount for t in transactions]

    return jsonify({"status" : "success", "campaign_labels" : campaign_labels, "campaign_values" : campaign_values, "transaction_labels" : transaction_labels, "transaction_values" : transaction_values})