import os
from datetime import datetime
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, DateTime, ARRAY, Float
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash

database_username = os.environ.get('DB_USERNAME', 'postgres')
database_password = os.environ.get('DB_PASSWORD', 'password')
database_name = 'roomee'
database_path = 'postgresql://{}:{}@{}/{}'.format(database_username, database_password, 'localhost:5432', database_name)

db = SQLAlchemy()


"""
DATABASE INITIATION
"""
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.secret_key = os.environ.get('SECRET_KEY', 'secret') #TODO :remove secret
    db.app = app
    db.init_app(app)
    db.create_all()
    migrate = Migrate(app, db)


class CRUDMixin(object):
    __table_args__ = {'extend_existing': True}

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()



"""
User Model
"""
class User(CRUDMixin, db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone_num = Column(String, nullable = False)
    address = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    hotel_id = Column(Integer, ForeignKey('hotels.id'), nullable=True)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=True)
    approved = Column(Boolean, default=False)
    approve_time = Column(DateTime)
    create_time = Column(DateTime)
    checkins = db.relationship('CheckIn', backref='staff', lazy='dynamic')

    def __init__(self, first_name, last_name, phone_num, address, email, password, hotel_id, role_id):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_num = phone_num
        self.address = address
        self.email = email
        self.password = password
        self.hotel_id = hotel_id
        self.role_id = role_id
        self.create_time = datetime.now()

    def hash_password(self, password):
        """  Hash user password. """
        self.password = generate_password_hash(password, method="pbkdf2:sha256", salt_length=16)

    def check_password(self, password):
        """verify password"""
        return check_password_hash(self.password, password)

    def insert(self):
        self.password = generate_password_hash(self.password)
        db.session.add(self)
        db.session.commit()
    
    def __repr__(self):
        return f'<User "{self.id}...">'

    def format(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone_num': self.phone_num,
            'address': self.address
            }



"""
Client Model
"""
class Client(CRUDMixin, db.Model):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone_num = Column(String, nullable = False)
    address = Column(String, nullable=False)
    email = Column(String)
    identity_type = Column(String)
    identity_num = Column(String)
    identity_pic = Column(String)
    create_time = Column(DateTime)
    checkin = db.relationship('CheckIn', backref='client', uselist=False)

    def __init__(self, first_name, last_name, phone_num, address, email, identity_type='', identity_num = '', identity_pic=''):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_num = phone_num
        self.address = address
        self.email = email
        self.identity_type = identity_type
        self.identity_num = identity_num
        self.identity_pic = identity_pic
        self.create_time = datetime.now()

    def __repr__(self):
        return f'<Client "{self.first_name + self.last_name}">'

    def format(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone_num': self.phone_num,
            'address': self.address, 
            'id_type': self.identity_type,
            'id_num': self.identity_num,
            'id_pic': self.identity_pic
            }



"""
Hotel Model
"""
class Hotel(CRUDMixin, db.Model):
    __tablename__ = 'hotels'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    phone_num = Column(String, nullable = False)
    address = Column(String, nullable=False)
    email = Column(String)
    website = Column(String)
    room_prefixes = Column(String) #TODO : change to array
    users = db.relationship('User', backref='hotel', lazy='dynamic')
    rooms = db.relationship('Room', backref='hotel', lazy='dynamic' )
    checkins = db.relationship('CheckIn', backref='checkin_hotel', lazy='dynamic')
    create_time = Column(DateTime)

    def __init__(self, name, phone_num, address, email, website='', room_prefix=[]):
        self.name = name
        self.phone_num = phone_num
        self.address = address
        self.email = email
        self.website = website
        self.room_prefix = room_prefix
        self.create_time = datetime.now()

    def __repr__(self):
        return f'<Hotel "{self.name}...">'

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone_num': self.phone_num,
            'address': self.address, 
            'website': self.website,
            'room_prefix': self.room_prefix
            }



"""
Room Model
"""
class Room(CRUDMixin, db.Model):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable = False)
    amenities = Column(String) #TODO :change to array
    pictures = Column(String) #TODO :change to array
    hotel_id = Column(Integer, ForeignKey('hotels.id'))
    checkins = db.relationship('CheckIn', backref='checkin_room', lazy='dynamic')
    price = Column(Float)
    occupied = Column(Boolean, default=False)
    last_update = Column(DateTime, onupdate=datetime.now())
    create_time = Column(DateTime)


    def __init__(self, name, price, location='', amenities=[], pictures=[]):
        self.name = name
        self.location = location
        self.amenities = amenities
        self.pictures = pictures
        self.price = price
        self.create_time = datetime.now()


    def __repr__(self):
        return f'<Room "{self.name}...">'

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'pictures': self.pictures,
            'price': self.price
            }



"""
Checkin Model
"""
class CheckIn(CRUDMixin, db.Model):
    __tablename__ = 'checkins'
    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey('rooms.id'))
    checked_in_by_id = Column(Integer, ForeignKey('users.id'))
    client_id = Column(Integer, ForeignKey('clients.id'))
    hotel_id = Column(Integer, ForeignKey('hotels.id'))
    checkout = db.relationship('CheckOut', backref='checkin', uselist=False)
    create_time = Column(DateTime)

    def __init__(self, room_id, checked_in_by_id, client_id):
        self.room_id = room_id
        self.checked_in_by_id = checked_in_by_id
        self.client_id = client_id
        self.create_time = datetime.now()

    def __repr__(self):
        return f'<Check "{self.id}...">'

    def format(self):
        return {
            'id': self.id,
            'room': db.query(Room).filter_by(id=self.room_id).first(),
            'checked_in_by': db.query(User).filter_by(id=self.checked_in_by_id).first(),
            'occupant': db.query(Room).filter_by(id=self.room_id).first(),
            }



"""
Checkout Model
"""
class CheckOut(CRUDMixin, db.Model):
    __tablename__ = 'checkouts'
    id = Column(Integer, primary_key=True)
    checked_out_by_id = Column(Integer, ForeignKey('users.id'))
    checkin_id = Column(Integer, ForeignKey('checkins.id'))
    create_time = Column(DateTime)

    def __init__(self, checked_out_by_id, checkin_id):
        self.checked_out_by_id = checked_out_by_id
        self.checkin_id = checkin_id
        self.create_time = datetime.now()

    def __repr__(self):
        return f'<Check "{self.id}...">'

    def format(self):
        checked_out_by = db.query(User).filter_by(id=self.checked_in_by_id).first()
        return {
            'id': self.id,
            'checked_out_by': checked_out_by.first_name + checked_out_by.last_name,
            'checkin_id': self.id,
            }



"""
Role Model
"""
class Role(CRUDMixin, db.Model):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Role "{self.id}...">'

    def format(self):
        return {
            'id': self.id,
            'name': self.name
            }
