from app.config import BaseConfig as config
from app.db.database import db
from app.db.model import Task
from apscheduler.schedulers.background import BackgroundScheduler
from flask import current_app
from flask_mail import Message

import uuid

scheduler = BackgroundScheduler(
    jobstores=config.SCHEDULER_JOBSTORE,
    timezone=config.SCHEDULER_TZ
)


class EmailTask:
    def __init__(self, email_context) -> None:
        self.email_context = email_context

    def schedule_email(self):
        scheduler_id = uuid.uuid4().hex
        task = Task(
            scheduled_at=self.email_context.timestamp,
            status='PENDING',
            scheduler_id=scheduler_id
        )
        db.session.add(task)
        self.email_context.task = task

        scheduler.add_job(
            self.send_email,
            id=scheduler_id,
            trigger='date',
            run_date=self.email_context.timestamp,
            misfire_grace_time=5*60
        )

    def send_email(self):
        # need to be tested
        msg = Message(
            subject=self.email_context.email_subject,
            body=self.email_context.email_content,
            sender='test_email_bos@mailtrap.io',
            recipients=[self.email_context.recipient.email]
        )

        from app import mail        
        with current_app.app_context():
            mail.send(msg)

        self.email_context.task.status = 'SENT'
        db.session.commit()
