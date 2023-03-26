from typing import Sequence
from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime, time
from typing import List
from typing import Optional
import uuid

db = SQLAlchemy()


class Restaurant(db.Model):
    __tablename__ = "p3restaurants"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    position = db.Column(db.Integer, nullable=True)
    name = db.Column(db.String(1024), nullable=False)
    score = db.Column(db.String(1024), nullable=True)
    ratings = db.Column(db.String(1024), nullable=True)
    category = db.Column(db.String(1024), nullable=False)
    price_range = db.Column(db.String(1024), nullable=True)
    full_address = db.Column(db.String(1024), nullable=True)
    zip_code = db.Column(db.Integer, nullable=True)
    lat = db.Column(db.Float, nullable=True)
    lng = db.Column(db.Float, nullable=True)
    state = db.Column(db.String(1024), nullable=False)
    # defining the reverse side of the relationship
    p3menu = db.relationship("MenuItems", back_populates="p3restaurants")

    def rep(self):
        return {
            "id": self.id,
            "position": self.position,
            "name": self.name,
            "score": self.score,
            "ratings": self.ratings,
            "category": self.category,
            "price_range": self.price_range,
            "full_address": self.full_address,
            "zip_code": self.zip_code,
            "lat": self.lat,
            "lng": self.lng,
            "state": self.state
        }

    def serialize(self):

        menuitems = []

        for food in self.p3menu:
            menuitems.append(food.rep())

        return {
            "id": self.id,
            "position": self.position,
            "name": self.name,
            "score": self.score,
            "ratings": self.ratings,
            "category": self.category,
            "price_range": self.price_range,
            "full_address": self.full_address,
            "zip_code": self.zip_code,
            "lat": self.lat,
            "lng": self.lng,
            "menuitems": menuitems,
            "state": self.state
        }


class MenuItems(db.Model):
    __tablename__ = "p3menu"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey(
        "p3restaurants.id"), nullable=False)
    category = db.Column(db.String(1024), nullable=True)
    name = db.Column(db.String(1024), nullable=False)
    description = db.Column(db.String(1024), nullable=True)
    price = db.Column(db.String(1024), nullable=True)
    p3restaurants = db.relationship("Restaurant", back_populates="p3menu")

    def rep(self):
        return {
            "restaurant_id": self.restaurant_id,
            "category": self.category,
            "name": self.name,
            "description": self.description,
            "price": self.price

        }

    def serialize(self):
        return {
            "restaurant_id": self.restaurant_id,
            "category": self.category,
            "name": self.name,
            "description": self.description,
            "price": self.price

        }
