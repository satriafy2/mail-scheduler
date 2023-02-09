from app.db.database import db
from sqlalchemy.sql import func
from sqlalchemy.orm import backref, relationship

import sqlalchemy as sa


class Email(db.Model):
    event_id = sa.Column(sa.Integer, primary_key=True)
    email_subject = sa.Column(sa.String(128), nullable=False)
    email_content = sa.Column(sa.String(500))
    timestamp = sa.Column(sa.TIMESTAMP(timezone=True), default=func.now(), nullable=False)
    created_at = sa.Column(sa.TIMESTAMP(timezone=True), default=func.now(), nullable=False)
    updated_at = sa.Column(sa.TIMESTAMP(timezone=True), default=None)

    task_id = sa.Column(sa.Integer, sa.ForeignKey('task.id'))
    task = relationship('Task', backref=backref('email', uselist=False))

    recipient_id = sa.Column(sa.Integer, sa.ForeignKey('recipient.id'))
    recipient = relationship('Recipient', back_populates='email_context')

    __tablename__ = 'email'

    def __repr__(self):
        return f'<Email {self.event_id} - {self.email_subject}>'


class Recipient(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(50))
    email = sa.Column(sa.String(50), unique=True, nullable=False)
    email_context = relationship('Email', back_populates='recipient')

    __tablename__ = 'recipient'

    def __repr__(self):
        return f'<Recipient {self.email}>'


class Task(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    scheduled_at = sa.Column(sa.DateTime, default=func.now())
    status = sa.Column(sa.String(50))
    scheduler_id = sa.Column(sa.String(32))

    __tablename__ = 'task'

    def __repr__(self) -> str:
        return f'<Task {self.task_id} - {self.status}>'
