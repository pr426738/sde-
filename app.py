from flask import Flask, request, jsonify
from models import db, User, Train, TrainSchedule, Booking
from database import init_db
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime

app = Flask(_name_)
app.config['SECRET_KEY'] = 'your_secret_key'

# Initialize DB
db_session = scoped_session(sessionmaker(bind=init_db()))
db.init_app(app)


# User Registration
@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    if not username or not password or not role:
        return jsonify({'message': 'Missing fields'}), 400

    hashed_password = generate_password_hash(password, method='sha256')
    user = User(username=username, password_hash=hashed_password, role=role)

    try:
        db_session.add(user)
        db_session.commit()
        return jsonify({'message': 'User registered successfully'}), 201
    except SQLAlchemyError:
        return jsonify({'message': 'Error registering user'}), 500


# User Login
@app.route('/login', methods=['POST'])
def login_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = db_session.query(User).filter_by(username=username).first()

    if user and check_password_hash(user.password_hash, password):
        token = jwt.encode(
            {'user_id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
            app.config['SECRET_KEY']
        )
        return jsonify({'token': token}), 200
    return jsonify({'message': 'Invalid credentials'}), 401


# Add Train (Admin Only)
@app.route('/trains', methods=['POST'])
def add_train():
    data = request.json
    name = data.get('name')
    source = data.get('source')
    destination = data.get('destination')
    total_seats = data.get('total_seats')

    train = Train(name=name, source=source, destination=destination, total_seats=total_seats)
    try:
        db_session.add(train)
        db_session.commit()
        return jsonify({'message': 'Train added successfully'}), 201
    except SQLAlchemyError:
        return jsonify({'message': 'Error adding train'}), 500


# Get Seat Availability
@app.route('/trains/availability', methods=['GET'])
def get_availability():
    source = request.args.get('source')
    destination = request.args.get('destination')
    journey_date = request.args.get('journey_date')

    trains = db_session.query(Train).filter_by(source=source, destination=destination).all()
    result = []

    for train in trains:
        schedule = db_session.query(TrainSchedule).filter_by(train_id=train.id, journey_date=journey_date).first()
        if schedule:
            result.append({
                'train_id': train.id,
                'train_name': train.name,
                'available_seats': schedule.available_seats
            })

    return jsonify(result), 200


# Book a Seat
@app.route('/bookings', methods=['POST'])
def book_seat():
    data = request.json
    user_id = data.get('user_id')
    train_id = data.get('train_id')
    journey_date = data.get('journey_date')

    try:
        db_session.begin()
        schedule = db_session.query(TrainSchedule).filter_by(train_id=train_id, journey_date=journey_date).with_for_update().first()

        if schedule and schedule.available_seats > 0:
            schedule.available_seats -= 1
            booking = Booking(user_id=user_id, train_schedule_id=schedule.id)
            db_session.add(booking)
            db_session.commit()
            return jsonify({'message': 'Booking successful'}), 200
        else:
            db_session.rollback()
            return jsonify({'message': 'No seats available'}), 400
    except SQLAlchemyError:
        db_session.rollback()
        return jsonify({'message': 'Error occurred during booking'}), 500


# Get Booking Details
@app.route('/bookings/<int:booking_id>', methods=['GET'])
def get_booking(booking_id):
    booking = db_session.query(Booking).get(booking_id)
    if booking:
        return jsonify({
            'booking_id': booking.id,
            'user_id': booking.user_id,
            'train_schedule_id': booking.train_schedule_id,
            'booking_date': booking.booking_date
        }), 200
    return jsonify({'message': 'Booking not found'}), 404


if _name_ == '_main_':
    app.run(debug=True)