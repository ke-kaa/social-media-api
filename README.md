Social Media API Project

Overview

The Social Media API project is a backend application built with Django that provides functionality for a social media platform. The API enables features such as user authentication, post creation, liking, commenting, and user profile management, offering a scalable and secure foundation for a social media application.

Features

User Management

JWT Authentication: Secure login and registration using JSON Web Tokens.

User Profiles: Users can view and update their profiles.

Posts

Create, Read, Update, Delete (CRUD): Users can create, edit, delete, and view posts.

Media Support: Upload and manage images or other media files for posts.

Interactions

Likes: Users can like or unlike posts.

Comments: Add, edit, and delete comments on posts.

Follower System

Follow/unfollow other users.

View a list of followers and following.

Notifications

Real-time notifications for interactions like likes, comments, and follows.

Search and Filtering

Search for users or posts using keywords.

Filter posts by hashtags or categories.

Technologies Used

Backend

Django: Web framework for building robust APIs.

Django REST Framework (DRF): Simplified API creation and management.

Django REST Framework SimpleJWT: Handles JWT-based authentication.

Database

PostgreSQL: Scalable and reliable database for storing user data, posts, and interactions.

Other Tools

Pillow: Image processing library for handling media files.

Celery: Task queue for handling asynchronous tasks like sending notifications.

Redis: In-memory data store used with Celery for task management.

Testing

Pytest: Comprehensive testing framework for the API.

Installation and Setup

Prerequisites

Python 3.10 or higher

PostgreSQL

Virtual environment (optional but recommended)

Steps

Clone the Repository

git clone https://github.com/your-username/social-media-api.git cd social-media-api

Set Up a Virtual Environment

python -m venv venv source venv/bin/activate # On Windows: venv\Scripts\activate

Install Dependencies

pip install -r requirements.txt

Configure Environment Variables Create a .env file in the root directory with the following variables:

DEBUG=True SECRET_KEY=your_secret_key DATABASE_NAME=your_database_name DATABASE_USER=your_database_user DATABASE_PASSWORD=your_database_password DATABASE_HOST=localhost DATABASE_PORT=5432

Apply Migrations

python manage.py makemigrations python manage.py migrate

Run the Server

python manage.py runserver

API Endpoints

Authentication

POST /api/auth/register/ - Register a new user.

POST /api/auth/login/ - Login and retrieve a JWT token.

POST /api/auth/refresh/ - Refresh the JWT token.

User Profiles

GET /api/profiles/{username}/ - Retrieve a user profile.

PUT /api/profiles/{username}/ - Update a user profile.

Posts

GET /api/posts/ - Retrieve all posts.

POST /api/posts/ - Create a new post.

GET /api/posts/{id}/ - Retrieve a specific post.

PUT /api/posts/{id}/ - Update a specific post.

DELETE /api/posts/{id}/ - Delete a specific post.

Interactions

POST /api/posts/{id}/like/ - Like or unlike a post.

POST /api/posts/{id}/comments/ - Add a comment to a post.

Follower System

POST /api/users/{username}/follow/ - Follow a user.

POST /api/users/{username}/unfollow/ - Unfollow a user.

GET /api/users/{username}/followers/ - Retrieve followers of a user.

GET /api/users/{username}/following/ - Retrieve the users a user is following.
