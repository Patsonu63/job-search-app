import json
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, jsonify
from src.models.user import db
from src.routes.user import user_bp
from src.routes.job import job_bp
from src.routes.application import application_bp
from src.routes.skill_gap import skill_gap_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Register all blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(job_bp, url_prefix='/api')
app.register_blueprint(application_bp, url_prefix='/api')
app.register_blueprint(skill_gap_bp, url_prefix='/api')

# Enable database
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USERNAME', 'root')}:{os.getenv('DB_PASSWORD', 'password')}@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '3306')}/{os.getenv('DB_NAME', 'mydb')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()
    
    # Add some sample data if the database is empty
    from src.models.user import User
    from src.models.user_profile import UserProfile
    from src.models.job import Job
    
    if User.query.count() == 0:
        # Create sample user
        user = User(username="demo_user", email="demo@example.com")
        db.session.add(user)
        db.session.commit()
        
        # Create sample profile
        profile = UserProfile(
            user_id=user.id,
            full_name="Demo User",
            headline="Software Developer seeking new opportunities",
            summary="Experienced software developer with 5 years of experience in web development.",
            experience_level="Mid-level",
            skills="Python,JavaScript,React,Flask,SQL,Git",
            preferred_job_types="Full-time,Remote",
            preferred_locations="San Francisco,New York,Remote",
            preferred_industries="Technology,Finance,Healthcare"
        )
        db.session.add(profile)
        
        # Create sample jobs
        jobs = [
            Job(
                title="Senior Software Engineer",
                company="Tech Innovations Inc.",
                location="San Francisco, CA",
                description="We are looking for a senior software engineer to join our team.",
                salary_range="$120,000 - $150,000",
                job_type="Full-time",
                required_skills="Python,JavaScript,React,AWS,Microservices,CI/CD",
                day_in_life_content="Start your day with a quick team standup. Work on challenging problems with a supportive team. Flexible hours and remote work options available."
            ),
            Job(
                title="Frontend Developer",
                company="WebDesign Pro",
                location="New York, NY",
                description="Join our creative team building beautiful web experiences.",
                salary_range="$90,000 - $110,000",
                job_type="Full-time",
                required_skills="HTML,CSS,JavaScript,React,UI/UX,Responsive Design",
                day_in_life_content="Collaborate with designers and backend developers to create seamless user experiences. Regular brainstorming sessions and design reviews."
            ),
            Job(
                title="Backend Developer",
                company="DataSystems Corp",
                location="Remote",
                description="Help us build robust backend systems for our enterprise clients.",
                salary_range="$100,000 - $130,000",
                job_type="Remote",
                required_skills="Python,Django,SQL,API Design,Docker,Kubernetes",
                day_in_life_content="Focus on building scalable systems with a globally distributed team. Regular code reviews and architecture discussions."
            ),
            Job(
                title="Full Stack Developer",
                company="StartupX",
                location="Austin, TX",
                description="Be part of a fast-growing startup revolutionizing the industry.",
                salary_range="$95,000 - $120,000",
                job_type="Full-time",
                required_skills="JavaScript,Node.js,React,MongoDB,Git,Agile",
                day_in_life_content="Work in a fast-paced environment where you'll wear multiple hats. Direct impact on product decisions and company growth."
            ),
            Job(
                title="DevOps Engineer",
                company="CloudSolutions Ltd",
                location="Remote",
                description="Help us maintain and improve our cloud infrastructure.",
                salary_range="$110,000 - $140,000",
                job_type="Remote",
                required_skills="AWS,Docker,Kubernetes,CI/CD,Terraform,Linux",
                day_in_life_content="Monitor systems, implement automation, and work on infrastructure improvements. On-call rotation with a supportive team."
            )
        ]
        
        for job in jobs:
            db.session.add(job)
            
        db.session.commit()

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "Job Search App API is running"})

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
