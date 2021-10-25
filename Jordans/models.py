from enum import unique
from os import name
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import uuid
from sqlalchemy.orm import backref
from flask_wtf.recaptcha import fields
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from flask_login import LoginManager, UserMixin, login_manager

from flask_marshmallow import Marshmallow

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)



class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = False)
    token = db.Column(db.String, unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    drone = db.relationship('Jordan', backref= 'owner', lazy = True)

    def __init__(self,email, password,token= '', id='') -> None:
        self.id = self.set_id()
        self.email = email
        self.password = self.set_password(password)
        self.token = self.set_token(24)
        
    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self,password):
        self.pw_hash =generate_password_hash(password)
        return self.pw_hash

    def set_token(self,length):
        return secrets.token_hex(length)



class Jordan(db.Model):
    id = db.Column(db.String, primary_key= True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(200), nullable = True)
    camera_quality = db.Column(db.Numeric(precision=10, scale= 2))
    flight_time = db.Column(db.String(100),nullable = True)
    max_speed = db.Column(db.String(100))
    dimensions = db.Column(db.String(100))
    weight = db.Column(db.String(50))
    cost_of_prod = db.Column(db.Numeric(precision=10,scale= 2))
    series = db.Column(db.String(150))
    user_token =db.Column(db.String, db.ForeignKey('user.token'), nullable = False)


    def __init__(self, name, description, camera_quality, flight_time, max_speed, dimensions, weight, cost_of_prod, series, user_token, id = ''):
        self.id = self.set_id()
        self.name = name
        self.description = description
        self.camera_quality = camera_quality
        self.flight_time = flight_time
        self.max_speed = max_speed
        self.dimensions = dimensions
        self.weight = weight
        self.cost_of_prod = cost_of_prod
        self.series = series
        self.user_token = user_token
    
    def set_id(self):
        return(secrets.token_urlsafe())

    # creating our marshaller to pull/create k,v pairs out of Drone attributes
class JordanSchema(ma.Schema):
        class Meta:
            # detailing fields(attributes) to be pulled out of our Drone class
            # instance(s) and sent to API call and vice-versa
            fields = ['id', 'name','description', 'camera_quality', 'flight_time', 'max_speed', 'dimensions', 'weight', 'cost_of_prod', 'series']

jordan_schema =JordanSchema()
jordans_schema = JordanSchema(many = True)

