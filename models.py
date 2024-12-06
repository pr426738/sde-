from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    _tablename_ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())


class Train(db.Model):
    _tablename_ = 'trains'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    source = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    total_seats = db.Column(db.Integer, nullable=False)


class TrainSchedule(db.Model):
    _tablename_ = 'train_schedules'
    id = db.Column(db.Integer, primary_key=True)
    train_id = db.Column(db.Integer, db.ForeignKey('trains.id'), nullable=False)
    available_seats = db.Column(db.Integer, nullable=False)
    journey_date = db.Column(db.Date, nullable=False)


class Booking(db.Model):
    _tablename_ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    train_schedule_id = db.Column(db.Integer, db.ForeignKey('train_schedules.id'), nullable=False)
    booking_date = db.Column(db.DateTime, default=db.func.current_timestamp())