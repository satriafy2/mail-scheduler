from flask import Blueprint
from flask import request

from app.common.tasks import EmailTask
from app.common.validator import validate_email, validate_timestamp
from app.db.database import db
from app.db.model import Email, Recipient

bp = Blueprint('email', __name__)


@bp.route('/save_emails', methods=['POST'])
def save_email():
    if request.method == 'POST':
        data = request.json
        if not data:
            return 'Error', 400

        if (
            not validate_email(data['recipient'].get('email', ''))
            or not validate_timestamp(data.get('timestamp', ''))
        ):
            return 'Error', 400

        recipient = Recipient.query.filter_by(email=data['recipient']['email']).first()
        if not recipient:
            recipient = Recipient(
                name=data['recipient']['name'],
                email=data['recipient']['email']
            )
            db.session.add(recipient)

        email = Email(
            email_subject=data.get('email_subject', ''),
            email_content=data.get('email_content', ''),
            timestamp=data.get('timestamp', None),
            recipient=recipient
        )
        db.session.add(email)

        EmailTask(email_context=email).schedule_email()
        db.session.commit()

        return 'Success', 200
