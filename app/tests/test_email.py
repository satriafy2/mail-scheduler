from datetime import datetime, timedelta
from flask import Flask
from flask_testing import TestCase
from app.apps import email
from app.db.database import db


class TestEmail(TestCase):
    # this test is still work in progress

    def create_app(self):
        app = Flask(__name__)
        app.config.from_object('app.config.BaseConfig')

        db.init_app(app)
        app.config['TESTING'] = True

        app.register_blueprint(email.bp)
        return app
    
    def setUp(self):
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_email_success(self):
        client = self.create_app().test_client()
        timestamp_date = datetime.now() + timedelta(days=1)
        mock_data = {
            'email_subject': 'subject',
            'email_content': 'content',
            'timestamp': timestamp_date.strftime('%Y-%m-%d %H:%M:%S'),
            'recipient': {
                'name': 'Bambang',
                'email': 'bambang@google.com'
            }
        }

        response = client.post('/save_emails', json=mock_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, 'Success')
