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
