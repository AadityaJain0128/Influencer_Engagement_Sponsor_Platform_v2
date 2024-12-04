from flask import current_app as app
from celery import Celery
from celery.schedules import crontab
from backend.tasks import daily_reminder, monthly_activity_report


celery = Celery("IESCP")
celery.autodiscover_tasks(['backend'])

class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=12, minute=0),
        daily_reminder.s()
    )
    sender.add_periodic_task(
        crontab(hour=8, minute=0, day_of_month=1),
        monthly_activity_report.s()
    )
