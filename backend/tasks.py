from .mail_service import send_email
from celery import shared_task
from .models import User, Influencer, Sponsor, Request, Campaign, Transaction
from datetime import datetime
from dateutil.relativedelta import relativedelta


@shared_task(ignore_result=True)
def daily_reminder():
    subject = "Daily Reminder from IESCP !"
    users = User.query.all()
    for user in users:
        if user.role == "influencer":
            inf = Influencer.query.filter_by(username=user.username).first()
            message = f'''<h1>Hey there, {inf.name.capitalize()}</h1><br>
                        <p>This email is sent to you by IESCP because you may have been offline for a while.<br>You may have some important task to checkout on our app !<br><br>
                        Regards,<br>Team IESCP
                        </p>'''
            reqs = Request.query.filter_by(influencer_id=inf.id, status="pending", sent_by="sponsor").all()
            if reqs != []:
                message = f'''<h1>Hey there, {inf.name.capitalize()}</h1><br>
                            <p>This email is sent to you by IESCP because you have some pending requests from sponsors.<br>Please checkout them before someone else does.<br><br>
                            Regards,<br>Team IESCP
                            </p>'''
            send_email(to=user.email, subject=subject, content=message)


        if user.role == "sponsor":
            sp = Sponsor.query.filter_by(username=user.username).first()
            message = f'''<h1>Hey there, {sp.name.capitalize()}</h1><br>
                        <p>This email is sent to you by IESCP because you may have been offline for a while.<br>You may have some important task to checkout on our app !<br><br>
                        Regards,<br>Team IESCP
                        </p>'''
            campaign_ids = Campaign.query.filter(Campaign.sponsor_id==sp.id).with_entities(Campaign.id)
            reqs = Request.query.filter(Request.campaign_id in campaign_ids, Request.status=="pending", Request.sent_by=="influencer").all()
            if reqs != []:
                message = f'''<h1>Hey there, {sp.name.capitalize()}</h1><br>
                            <p>This email is sent to you by IESCP because you have some pending requests from influencers.<br>Please checkout them before someone else does.<br><br>
                            Regards,<br>Team IESCP
                            </p>'''
        
            send_email(to=user.email, subject=subject, content=message)


@shared_task(ignore_result=True)
def monthly_activity_report():
    users = User.query.all()
    today = datetime.today()
    prev_month = (today - relativedelta(months=1)).strftime("%Y-%m")

    for user in users:
        if user.role == "influencer":
            inf = Influencer.query.filter_by(username=user.username).first()

            completed_campaigns = Campaign.query.filter(Campaign.completed==True, Campaign.end_date.contains(prev_month)).all()
            month_earnings = sum([t.amount for t in inf.transactions.filter(Transaction.date.contains(prev_month)).all()])
            total_earnings = sum([t.amount for t in inf.transactions.all()])
            
            message = f'''
                <h1>Hey there, {inf.name}</h1><br><h4>This is your monthly activity report from IESCP Team !</h4><br><p>You have completed <b>{len(completed_campaigns)}</b> campaigns last month.<br>You earned INR {month_earnings} last month from {len(completed_campaigns)} campaigns which makes your total earning INR {total_earnings}.</p><br><br>Regards,<br>Team IESCP
            '''
            send_email(to=user.email, subject="Monthly Activity Report", content=message)

        elif user.role == "sponsor":
            sp = Sponsor.query.filter_by(username=user.username).first()
            campaign_ids = Campaign.query.filter(Campaign.sponsor_id==sp.id).with_entities(Campaign.id)
            completed_campaigns = Campaign.query.filter(Campaign.sponsor_id==sp.id, Campaign.completed==True, Campaign.end_date.contains(prev_month)).all()
            transactions = [t.amount for t in Transaction.query.filter(Transaction.campaign_id.in_(campaign_ids), Transaction.date.contains(prev_month)).all()]
            
            message = f'''
                <h1>Hey there, {sp.name}</h1><br><h4>This is your monthly activity report from IESCP Team !</h4><br><p>You have completed <b>{len(completed_campaigns)}</b> campaigns last month.<br>You have done transactions of INR {sum(transactions)} last month on our platform.</p><br><br>Regards,<br>Team IESCP
            '''
            send_email(to=user.email, subject="Monthly Activity Report", content=message)
