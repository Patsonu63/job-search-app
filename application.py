from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    status = db.Column(db.String(50), default='Submitted')  # Submitted, Under Review, Interview, Offer, Rejected
    application_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    notes = db.Column(db.Text)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('applications', lazy=True))
    job = db.relationship('Job', backref=db.backref('applications', lazy=True))
    
    def __repr__(self):
        return f'<Application {self.id} - {self.status}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'job_id': self.job_id,
            'status': self.status,
            'application_date': self.application_date.isoformat(),
            'last_updated': self.last_updated.isoformat(),
            'notes': self.notes,
            'job_title': self.job.title if self.job else None,
            'company': self.job.company if self.job else None
        }
