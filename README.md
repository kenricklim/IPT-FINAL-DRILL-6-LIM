# My Flask Application README

## 2. Overview

This Flask application provides a simple RESTful API to manage country data stored in a MySQL database. The application includes endpoints for public access, user authentication, and various operations on country data. JWT tokens are used for securing specific routes.

## 3. Features

Public Routes: Accessible without authentication.
Protected Routes: Require a valid JWT token.
CRUD Operations: Create, read, update, and delete country data.
JWT Authentication: Secure routes with token-based authentication.

## 4. Requirements

Python 3.x
Flask
Flask-MySQLdb
PyJWT
unittest (for testing)


## 5. Installation

Clone the repository
Create a virtual environment and activate it
Install the dependencies
Configure MySQL Database
Set up a MySQL database and update the app.config in the application with your database credentials.

## 6. API Endpoints
Public Endpoints

###### GET /: Welcome message.
###### GET /public: Public access endpoint.
###### GET /login: Render login page.
###### POST /login: Authenticate user and return JWT token.
###### GET /countries: Get a list of all countries.

## 7. Protected Endpoints (Require JWT Token)
###### GET /countries/<int:id>: Get country details by ID.
###### GET /Continents: Get continents with more than five countries.
###### POST /countries: Add a new country.
###### PUT /countries/<int:id>: Update country details by ID.
###### DELETE /countries/<int:id>: Delete country by ID.

## 8. Authentication
Use the /login endpoint to obtain a JWT token. Include this token in the x-access-token header for requests to protected endpoints.

## Login Page
The application includes a simple HTML login page located at /templates/login.html

## Testing
Unit tests are included in the application to verify functionality. Tests are located in tests/test_app.py


