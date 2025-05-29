from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    headline = db.Column(db.String(200))
    summary = db.Column(db.Text)
    experience_level = db.Column(db.String(50))  # Junior, Mid-level, Senior, etc.
    skills = db.Column(db.Text)  # Stored as comma-separated values
    preferred_job_types = db.Column(db.String(100))  # Full-time, Part-time, Remote, etc.
    preferred_locations = db.Column(db.String(200))
    preferred_industries = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with User model
    user = db.relationship('User', backref=db.backref('profile', uselist=False))
    
    def __repr__(self):
        return f'<UserProfile {self.full_name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'full_name': self.full_name,
            'headline': self.headline,
            'summary': self.summary,
            'experience_level': self.experience_level,
            'skills': self.skills,
            'preferred_job_types': self.preferred_job_types,
            'preferred_locations': self.preferred_locations,
            'preferred_industries': self.preferred_industries,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
