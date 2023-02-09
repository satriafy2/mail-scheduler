from flask import Blueprint, Response, request
from app.common.tasks import schedule_email
from app.db.database import db
from app.db.model import Email, Recipient

bp = Blueprint('email', __name__)


@bp.route('/save_emails', methods=('POST', 'GET'))
def save_email():
    if request.method == 'POST':
        data = request.json
        if not data:
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

        schedule_email(email_context=email)
        db.session.commit()

        return 'Success', 200

    data = {
        'message': 'success dek',
        'kacatu': 'kacauu'
    }
    return Response(data, status=200, mimetype='application/json')
