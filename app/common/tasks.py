from app.db.database import db
from app.db.model import Email, Task
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
        db.session.flush()

        scheduler.add_job(
            func=self.send_email,
            args=[self.email_context.event_id],
            trigger='date',
            run_date=self.email_context.timestamp,
            id=scheduler_id,
            misfire_grace_time=5*60
        )

    def send_email(self, email_id):
        # need to be tested
        with scheduler.app.app_context():
            email_ctx = Email.query.filter_by(event_id=email_id).first()
            msg = Message(
                subject=email_ctx.email_subject,
                body=email_ctx.email_content,
                sender='test_email_bos@mailtrap.io',
                recipients=[email_ctx.recipient.email]
            )

            try:
                mail.send(msg)
                email_ctx.task.status = 'SENT'
            except Exception as e:
                print(e, flush=True)
                email_ctx.task.status = 'ERROR'

            db.session.commit()
