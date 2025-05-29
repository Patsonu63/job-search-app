from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    salary_range = db.Column(db.String(50))
    job_type = db.Column(db.String(50))  # Full-time, Part-time, Contract, etc.
    required_skills = db.Column(db.Text)  # Stored as comma-separated values
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # For "Day in the Life" feature
    day_in_life_content = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Job {self.title} at {self.company}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'company': self.company,
            'location': self.location,
            'description': self.description,
            'salary_range': self.salary_range,
            'job_type': self.job_type,
            'required_skills': self.required_skills,
            'day_in_life_content': self.day_in_life_content,
            'created_at': self.created_at.isoformat()
        }
