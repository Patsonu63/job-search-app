from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class SkillGap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    missing_skills = db.Column(db.Text)  # Stored as comma-separated values
    learning_resources = db.Column(db.Text)  # JSON string of resource links
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('skill_gaps', lazy=True))
    job = db.relationship('Job', backref=db.backref('skill_gaps', lazy=True))
    
    def __repr__(self):
        return f'<SkillGap {self.id} - User {self.user_id} - Job {self.job_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'job_id': self.job_id,
            'missing_skills': self.missing_skills,
            'learning_resources': self.learning_resources,
            'created_at': self.created_at.isoformat()
        }
