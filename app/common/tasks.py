from app.db.database import db
from app.db.model import Task
from app.extension.mail import mail
from app.extension.scheduler import scheduler
from flask_mail import Message 
import uuid


class EmailTask:
    def __init__(self, email_context):
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
            func=self.send_email,
            trigger='date',
            run_date=self.email_context.timestamp,
            id=scheduler_id,
            misfire_grace_time=5*60
        )

    def send_email(self):
        # need to be tested
        with scheduler.app.app_context():
            msg = Message(
                subject=self.email_context.email_subject,
                body=self.email_context.email_content,
                sender='test_email_bos@mailtrap.io',
                recipients=[self.email_context.recipient.email]
            )

            try:
                mail.send(msg)
                self.email_context.task.status = 'SENT'
            except Exception as e:
                print(e, flush=True)
                self.email_context.task.status = 'ERROR'

            db.session.commit()
