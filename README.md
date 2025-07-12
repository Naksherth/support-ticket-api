# 🛠️ Support Ticket API

A secure and scalable RESTful API built with **Flask** for managing support tickets within an organization. Features include user registration, JWT‑based login, role‑based access, ticket CRUD operations, and administrative user controls.

---

## 📚 Table of Contents
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Environment Configuration](#environment-configuration)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Authentication](#authentication)
- [Testing](#testing)
- [CI/CD](#cicd)
- [Deployment](#deployment)
- [License](#license)

---

## 🚀 Features
- User registration and JWT‑based login  
- Role‑based access control (user vs admin)  
- Create, view, update, and delete support tickets  
- Administrators can manage any user and any ticket  
- Ticket audit logging and comment capability  
- Marshmallow schema validation for all inputs  
- Secure environment‑based configuration  
- Automated testing and GitHub Actions integration  

---

## 🧰 Technology Stack
- **Flask** – lightweight web framework  
- **Flask‑JWT‑Extended** – authentication  
- **Flask‑SQLAlchemy** – ORM for database interactions  
- **Flask‑Migrate** – database migrations  
- **Flask‑Marshmallow** – schema validation  
- **Pytest + pytest‑flask** – automated testing  
- **Gunicorn** – WSGI server for production  
- **Render.com** – cloud deployment platform  
- **GitHub Actions** – CI/CD pipeline  

---

## ⚙️ Installation

1. **Clone the repository**
   git clone https://github.com/Naksherth/support-ticket-api.git
   cd support-ticket-api

2.**Create a virtual environment and activate it**
python -m venv venv
# Linux / macOS
source venv/bin/activate
# Windows
venv\Scripts\activate
3.**Install dependencies**
pip install -r requirements.txt

4.**Running the Application**

#  start via run.py
python run.py

In production (e.g., on Render.com):
gunicorn run:app

**API Endpoints**

# Auth Routes
Method	Endpoint	Description
POST	/auth/register	Register a new user
POST	/auth/login	Authenticate user, get JWT
GET	/auth/me	Get current user profile

# Ticket Routes
Method	Endpoint	Description
POST	/tickets	Create a support ticket (logged‑in user)
GET	/tickets	List own tickets / all tickets (admin)
PUT	/tickets/<id>	Update a ticket
DELETE	/tickets/<id>	Delete a ticket (admin only)

# Admin Routes
Method	Endpoint	Description
GET	/admin/users	List all users (admin only)
PUT	/admin/users/<id>	Update user details (admin)
DELETE	/admin/users/<id>	Delete a user (admin)

 **Authentication**
Add the JWT access token (from /auth/login) to requests that hit protected routes:

Authorization: Bearer <access_token>

**Testing**
Run the automated test suite:
pytest

# The suite covers:

Registration and login flows

JWT‑protected routes

Ticket CRUD operations

Admin‑only endpoints

**⚙️ CI/CD**
GitHub Actions workflow (.github/workflows/ci.yml) automatically:

Checks out the code

Installs dependencies

Runs the pytest suite

Executes flake8 linting

A green build ensures code quality before merging or deployment.

**🚀 Deployment**
The project is configured for Render.com:

Start command: gunicorn run:app

Procfile provided for portability

Environment variables managed via Render dashboard

Automatic HTTPS and continuous deployment on push

# CI/CD
GitHub Actions workflow (.github/workflows/ci.yml) automatically:

Checks out the code

Installs dependencies

Runs the pytest suite

Executes flake8 linting

A green build ensures code quality before merging or deployment.

**🚀 Deployment**
The project is configured for Render.com:

Start command: gunicorn run:app

Procfile provided for portability

Environment variables managed via Render dashboard

Automatic HTTPS and continuous deployment on push



Developer — Naksherth 
Mentor — Thinula Damsith, CEO • Infinity AI