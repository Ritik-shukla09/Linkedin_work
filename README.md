# LinkedIn Clone – Django Based Professional Networking Platform

## Overview

This project is a **LinkedIn-style professional networking web application** built using the Django framework. It allows users to create professional profiles, connect with other users, and share posts in a social networking feed. The project demonstrates the use of Django’s **MVT architecture, ORM, authentication system, and database management**.

The goal of this project is to replicate the core features of LinkedIn while applying best practices in **backend development and full-stack web development**.

## Features

* User registration and login authentication
* Create and update professional profiles
* Send and accept connection requests
* Create and share posts with connections
* View a feed of posts from connected users
* Secure session-based authentication
* Database management using Django ORM
* Admin panel for managing users and content

## Tech Stack

* **Backend:** Django (Python)
* **Frontend:** HTML, CSS, JavaScript
* **Database:** SQLite
* **Authentication:** Django Authentication System
* **Architecture:** Django MVT (Model–View–Template)

## Project Workflow

1. User registers and creates an account.
2. User logs in using authentication credentials.
3. User creates or updates their professional profile.
4. Users can send and accept connection requests.
5. Connected users can share posts.
6. Posts appear in the networking feed of connections.

## Installation and Setup

### 1. Create virtual environment

```
python3 -m venv venv
```

### 2. Activate virtual environment

```
   source venv/bin/activate
```

### 3. Run the development server

```
python manage.py runserver
```
## Project Folder Structure

```
linkedin-work/
│
├── manage.py
│
├── linkedin_work/              # Main project configuration
│   ├── __init__.py
│   ├── settings.py              # Project settings
│   ├── urls.py                  # Main URL routing
│   ├── asgi.py
│   └── wsgi.py
│
├── accounts/                    # Authentication and user profiles
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   └── admin.py
│
├── connections/                 # Connection request system
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── posts/                       # User posts and activity feed
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── jobs/                        # Job posting and job applications
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── messages/                    # Messaging system between users
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── templates/                   # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── signup.html
│   ├── profile.html
│   ├── feed.html
│   ├── jobs.html
│   └── messages.html
│
├── static/                      # CSS, JavaScript, images
│   ├── css/
│   ├── js/
│   └── images/
│
├── db.sqlite3                   # Database
├── requirements.txt
├── README.md
└── .gitignore
```
