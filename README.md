# Face Attendance Backend

This is the backend service for the **Face Attendance Application** used in math tutoring centers.  
It provides REST APIs for managing students, classes, schedules, payments, and face recognition attendance.

## Features
- User authentication (student, teacher, admin)
- Student & class management
- Attendance via face recognition
- Homework & monthly score tracking
- Tuition payment record & proof upload
- RESTful API for Flutter mobile app

## Tech Stack
- **Backend**: Django REST Framework (Python)
- **Database**: PostgreSQL
- **Face Recognition**: ViT
- **Storage**: Firebase (for images/proofs)
- **Deployment**: Ubuntu / Docker-ready

## Installation
```bash
# Clone repo
git clone https://github.com/quoc14/FaceRCAPP.git
cd face-attendance-backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Migrate database
python manage.py migrate

# Create superuser
python manage.py createsuperuser
