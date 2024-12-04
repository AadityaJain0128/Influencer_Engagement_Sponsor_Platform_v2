from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from .utils import check_role
from ..models import db, User, Influencer, Sponsor, Campaign, Request, Rating, Transaction
from datetime import datetime
from ..caching import cache


influencer = Blueprint("influencer", __name__)


@influencer.route("/getDetails", methods=['GET'])
@jwt_required()
def getDetails():
    username = get_jwt_identity()
    if not check_role(username, "influencer"):
        return jsonify({"status" : "fail", "error" : "Invalid Token"})

    influencer = Influencer.query.filter_by(username=username).first()
    
    return jsonify({"status" : "success", "id" : influencer.id, "name" : influencer.name, "category" : influencer.niche, "reach" : influencer.reach, "socials" : influencer.socials})


@influencer.route("/dashboard", methods=['GET'])
@jwt_required()
def dashboard():
    username = get_jwt_identity()
    if not check_role(username, "influencer"):
        return jsonify({"status" : "fail", "error" : "Invalid Token"})
    
    influencer = Influencer.query.filter_by(username=username).first()

    active_campaigns = Campaign.query.filter_by(influencer_id=influencer.id, completed=False).all()
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
        }
        active_campaigns_json.append(c)

    recieved_requests = Request.query.filter_by(influencer_id=influencer.id, sent_by="sponsor", status="pending").all()
    recieved_requests_json = []
    for req in recieved_requests:
        r = {
            "id" : req.id,
            "campaign" : {"id" : req.campaign_id, "name" : req.campaign.name, "description" : req.campaign.description, "budget" : req.campaign.budget, "start_date" : req.campaign.start_date.strftime("%d %B, %Y"), "end_date" : req.campaign.end_date.strftime("%d %B, %Y"), "visibility" : req.campaign.visibility, "flagged" : req.campaign.flagged},
            "messages" : req.messages,
            "requirements" : req.requirements,
            "budget" : req.budget,
            "status" : req.status,
            "sponsor" : {"id" : req.campaign.sponsor.id, "name" : req.campaign.sponsor.name}
        }
        recieved_requests_json.append(r)
    
    avg_rating = []
    ratings = Rating.query.filter_by(influencer_id=influencer.id).all()
    if ratings:
        avg_rating = [round(sum([r.rating for r in ratings]) / len(ratings), 1), len(ratings)]

    month = datetime.now().strftime("%Y-%m")
    month_earnings = sum([t.amount for t in influencer.transactions.filter(Transaction.date.contains(month)).all()])
    total_earnings = sum([t.amount for t in influencer.transactions.all()])


    return jsonify({"status" : "success", "active_campaigns" : active_campaigns_json[::-1], "recieved_requests" : recieved_requests_json[::-1], "avg_rating" : avg_rating, "month_earnings" : month_earnings, "total_earnings" : total_earnings})


@influencer.route("/handle_request", methods=['POST', 'PUT'])
@jwt_required()
def handle_request():
    username = get_jwt_identity()
    if not check_role(username, "influencer"):
        return jsonify({"status" : "fail", "error" : "Invalid Token"})
    
    influencer = Influencer.query.filter_by(username=username).first()

    id = request.json.get("id")
    req = Request.query.filter_by(id=id).first()
    campaign = req.campaign
    if not req or (req.influencer_id != influencer.id):
        return jsonify({"status" : "fail", "message" : "Invalid Request !"})
    
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


    action = request.json.get("action")

    if action == "accepted":
        if campaign.completed or campaign.influencer_id:
            return jsonify({"status" : "fail", "message" : "Invalid Request !"})
    
        for r in campaign.requests:
            r.status = "expired"
        req.status = "accepted"
        campaign.budget = req.budget
        campaign.influencer_id = req.influencer_id
        db.session.commit()
        return jsonify({"status" : "success", "message" : "Request accepted !"})
    
    req.status = "rejected"
    db.session.commit()
    return jsonify({"status" : "success", "message" : "Request rejected !"})


@influencer.route("/get_requests")
@jwt_required()
def get_requests():
    username = get_jwt_identity()
    if not check_role(username, "influencer"):
        return jsonify({"status" : "fail", "error" : "Invalid Token"})
    
    influencer = Influencer.query.filter_by(username=username).first()

    recieved_requests = Request.query.filter_by(influencer_id=influencer.id, sent_by="sponsor").all()
    recieved_requests_json = []
    for req in recieved_requests:
        r = {
            "id" : req.id,
            "campaign" : {"id" : req.campaign_id, "name" : req.campaign.name, "budget" : req.campaign.budget, "description" : req.campaign.description, "start_date" : req.campaign.start_date.strftime("%d %b, %Y"), "end_date" : req.campaign.end_date.strftime("%d %b, %Y"), "visibility" : req.campaign.visibility, "flagged" : req.campaign.flagged},
            "messages" : req.messages,
            "requirements" : req.requirements,
            "budget" : req.budget,
            "status" : req.status,
            "sponsor" : {"id" : req.campaign.sponsor.id, "name" : req.campaign.sponsor.name, "username" : req.campaign.sponsor.username},
        }
        recieved_requests_json.append(r)

    
    sent_requests = Request.query.filter_by(influencer_id=influencer.id, sent_by="influencer").all()
    sent_requests_json = []
    for req in sent_requests:
        r = {
            "id" : req.id,
            "campaign" : {"id" : req.campaign_id, "name" : req.campaign.name, "budget" : req.campaign.budget, "description" : req.campaign.description, "start_date" : req.campaign.start_date.strftime("%d %b, %Y"), "end_date" : req.campaign.end_date.strftime("%d %b, %Y"), "visibility" : req.campaign.visibility, "flagged" : req.campaign.flagged},
            "messages" : req.messages,
            "requirements" : req.requirements,
            "budget" : req.budget,
            "status" : req.status,
            "sponsor" : {"id" : req.campaign.sponsor.id, "name" : req.campaign.sponsor.name, "username" : req.campaign.sponsor.username}
        }
        sent_requests_json.append(r)

    return jsonify({"status" : "success", "recieved_requests" : recieved_requests_json[::-1], "sent_requests" : sent_requests_json[::-1]})


@influencer.route("/get_campaigns")
@cache.cached(key_prefix="campaigns")
@jwt_required()
def get_campaigns():
    cname = request.args.get("cname", "")
    sname = request.args.get("sname", "")

    campaigns = Campaign.query.filter(Campaign.flagged==False, Campaign.visibility=="public", Campaign.completed==False, Campaign.influencer_id.is_(None))

    if cname:
        campaigns = campaigns.filter(Campaign.name.contains(cname))
    if sname:
        sponsors = Sponsor.query.filter(Sponsor.name.contains(sname)).all()
        sponsor_ids = [sponsor.id for sponsor in sponsors]
        campaigns = campaigns.filter(Campaign.sponsor_id.in_(sponsor_ids))

    campaigns_json = []
    for campaign in campaigns:
        c = {
            "id" : campaign.id,
            "name" : campaign.name,
            "description" : campaign.description,
            "sponsor" : {"id" : campaign.sponsor.id, "username" : campaign.sponsor.username, "name" : campaign.sponsor.name, "industry" : campaign.sponsor.industry},
            "start_date" : campaign.start_date.strftime("%d %b, %Y"),
            "end_date" : campaign.end_date.strftime("%d %b, %Y"),
            "budget" : campaign.budget,
            "visibility" : campaign.visibility,
            "flagged" : campaign.flagged
        }
        campaigns_json.append(c)

    campaigns = campaigns.all()
    return jsonify({"status" : "success", "campaigns" : campaigns_json[::-1]})


@influencer.route("/send_request", methods=['POST'])
@jwt_required()
def send_request():
    username = get_jwt_identity()
    if not check_role(username, "influencer"):
        return jsonify({"status" : "fail", "error" : "Invalid Token"})
    
    influencer = Influencer.query.filter_by(username=username).first()

    data = request.json
    messages = data.get("messages")
    requirements = data.get("requirements")
    campaign_id = data.get("campaign_id")
    neg_budget = data.get("neg_budget")
    req = Request.query.filter_by(campaign_id=campaign_id, influencer_id=influencer.id, sent_by="influencer").first()
    if req:
        return jsonify({"status" : "fail", "message" : "Request has already been sent !"})
    
    req = Request(messages=messages, requirements=requirements, campaign_id=campaign_id, influencer_id=influencer.id, sent_by="influencer", budget=neg_budget)
    db.session.add(req)
    db.session.commit()
    return jsonify({"status" : "success", "message" : "Request has been sent !"})


@influencer.route("/completed_campaigns")
@jwt_required()
def completed_capaigns():
    username = get_jwt_identity()
    if not check_role(username, "influencer"):
        return jsonify({"status" : "fail", "error" : "Invalid Token"})
    
    influencer = Influencer.query.filter_by(username=username).first()

    completed_campaigns = Campaign.query.filter_by(influencer_id=influencer.id, completed=True).all()
    completed_campaigns_json = []
    for campaign in completed_campaigns:
        t = Transaction.query.filter_by(campaign_id=campaign.id).first()
        r = Rating.query.filter_by(campaign_id=campaign.id).first()
        if r:
            rating = {"id" : r.id, "rating" : r.rating}
        else:
            rating = {"id" : None, "rating" : None}

        c = {
            "id" : campaign.id,
            "name" : campaign.name,
            "description" : campaign.description,
            "sponsor" : {"id" : campaign.sponsor.id, "username" : campaign.sponsor.username, "name" : campaign.sponsor.name},
            "start_date" : campaign.start_date.strftime("%d %b, %Y"),
            "end_date" : campaign.end_date.strftime("%d %b, %Y"),
            "budget" : campaign.budget,
            "visibility" : campaign.visibility,
            "flagged" : campaign.flagged,
            "transaction" : {"id" : t.id, "amount" : t.amount, "date" : t.date},
            "rating" : rating
        }
        completed_campaigns_json.append(c)

    return jsonify({"status" : "success", "completed_campaigns" : completed_campaigns_json[::-1]})


@influencer.route("/profile_details")
@jwt_required()
def profile_details():
    username = get_jwt_identity()
    if not check_role(username, "influencer"):
        return jsonify({"status" : "fail", "error" : "Invalid Token"})
    
    influencer = Influencer.query.filter_by(username=username).first()

    avg_rating = []
    ratings = Rating.query.filter_by(influencer_id=influencer.id).all()
    if ratings:
        avg_rating = [round(sum([r.rating for r in ratings]) / len(ratings), 1), len(ratings)]

    month = datetime.now().strftime("%Y-%m")
    month_earnings = sum([t.amount for t in influencer.transactions.filter(Transaction.date.contains(month)).all()])
    total_earnings = sum([t.amount for t in influencer.transactions.all()])

    return jsonify({"status" : "success", "avg_rating" : avg_rating, "month_earnings" : month_earnings, "total_earnings" : total_earnings})


@influencer.route("/profile_update", methods=['PUT'])
@jwt_required()
def profile_update():
    username = get_jwt_identity()
    if not check_role(username, "influencer"):
        return jsonify({"status" : "fail", "error" : "Invalid Token"})
    
    influencer = Influencer.query.filter_by(username=username).first()

    data = request.json
    name, niche, socials = data.get("name"), data.get("niche"), data.get("socials")

    influencer.name = name
    influencer.niche = niche
    influencer.socials = socials
    influencer.calculate_reach()
    db.session.commit()
    return jsonify({"status" : "success", "message" : "Profile Updated !", "name" : influencer.name, "niche" : influencer.niche, "reach" : influencer.reach, "socials" : influencer.socials})


@influencer.route("/stats")
@jwt_required()
def stats():
    username = get_jwt_identity()
    if not check_role(username, "influencer"):
        return jsonify({"status" : "fail", "error" : "Invalid Token"})
    
    influencer = Influencer.query.filter_by(username=username).first()

    campaigns = Campaign.query.filter_by(influencer_id=influencer.id)
    active_campaigns = campaigns.filter(Campaign.completed == False).all()
    completed_campaigns = campaigns.filter_by(completed=True).all()
    campaign_labels = ["Active Campaigns", "Completed Campaigns"]
    campaign_values = [len(active_campaigns), len(completed_campaigns)]

    transactions = Transaction.query.filter_by(influencer_id=influencer.id).all()
    transaction_labels = [t.campaign.name for t in transactions]
    transaction_values = [t.amount for t in transactions]

    return jsonify({"status" : "success", "campaign_labels" : campaign_labels, "campaign_values" : campaign_values, "transaction_labels" : transaction_labels, "transaction_values" : transaction_values})