from flask import Flask, request, jsonify
from datetime import datetime, date
from sqlalchemy import create_engine, Column, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import re
import os

app = Flask(__name__)
db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')
engine = create_engine(f'postgresql://{db_user}:{db_pass}@{db_host}:5432/{db_name}')

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    username = Column(String, primary_key=True)
    date_of_birth = Column(Date)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

@app.route('/hello/<username>', methods=['PUT'])
def update_birthday(username):
    if not re.match(r'^[A-Za-z]+$', username):
        return 'Invalid username', 400

    data = request.get_json()
    dob_str = data.get('dateOfBirth')
    try:
        dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
        if dob >= date.today():
            return 'Date must be before today', 400
    except ValueError:
        return 'Invalid date format', 400

    session = Session()
    user = session.query(User).get(username)
    if user:
        user.date_of_birth = dob
    else:
        user = User(username=username, date_of_birth=dob)
    session.add(user)
    session.commit()
    session.close()
    return '', 204

@app.route('/hello/<username>', methods=['GET'])
def get_birthday(username):
    session = Session()
    user = session.query(User).get(username)
    session.close()
    if not user:
        return 'User not found', 404

    today = date.today()
    next_birthday = user.date_of_birth.replace(year=today.year)
    if next_birthday < today:
        next_birthday = next_birthday.replace(year=today.year + 1)
    days_left = (next_birthday - today).days

    if days_left == 0:
        message = f'Hello, {username}! Happy birthday!'
    else:
        message = f'Hello, {username}! Your birthday is in {days_left} day(s)'
    return jsonify({'message': message}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
