IRCTC Reservation API

A Python-based RESTful API for managing IRCTC (Indian Railway Catering and Tourism Corporation) reservations. This API interacts with a MySQL database to handle train schedules, bookings, and user information.

Features

User Registration and Authentication:
Register new users.
Login and manage sessions securely.
Train Management:
Add, update, and delete train schedules.
View available trains and their schedules.
Reservation System:
Book tickets for available trains.
Cancel existing bookings.
View reservation history.
Admin Features:
Manage users and train schedules.

Tech Stack

Backend: Python (Flask/FastAPI/Django Rest Framework)
Database: MySQL
Authentication: JWT (JSON Web Tokens) or Session-based authentication
Tools: Postman (for API testing)

Installation

Prerequisites
Install Python 3.8+.
Install MySQL Server.
Install pip (Python package manager).
Steps
Clone the repository:

bash
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Set up the MySQL database:

Create a database in MySQL:
sql
Copy code
CREATE DATABASE irctc_reservation;
Update database credentials in config.py (or .env file):
python
Copy code
DB_HOST = "localhost"
DB_USER = "your-username"
DB_PASSWORD = "your-password"
DB_NAME = "irctc_reservation"
Run database migrations:

bash
Copy code
python manage.py migrate
Start the development server:

bash
Copy code
python manage.py runserver

API Endpoints

Authentication
POST /register: Register a new user.
POST /login: Login a user.
Train Management
GET /trains: Get a list of all trains.
POST /trains: Add a new train (Admin only).
PUT /trains/{id}: Update train details (Admin only).
DELETE /trains/{id}: Delete a train (Admin only).
Reservations
POST /reservations: Book a ticket.
GET /reservations: View user reservations.
DELETE /reservations/{id}: Cancel a reservation.

Project Structure

bash
Copy code
irctc-reservation-api/
│
├── app/
│   ├── models/          # Database models
│   ├── routes/          # API route definitions
│   ├── services/        # Business logic
│   ├── utils/           # Helper functions
│   ├── __init__.py      # App initialization
│
├── migrations/          # Database migration files
├── tests/               # Unit and integration tests
├── config.py            # Configuration settings
├── requirements.txt     # Python dependencies
├── README.md            # Project documentation
Contributing
Fork the repository.
Create a new branch for your feature or bugfix:
bash
Copy code
git checkout -b feature-name
Commit and push your changes.
Open a pull request.
