from typing import Sequence
from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime, time
from typing import List
from typing import Optional
import uuid

db = SQLAlchemy()


class Restaurant(db.Model):
    __tablename__ = "restaurant"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    position = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(1024), nullable=False)
    score = db.Column(db.String(1024), nullable=False)
    ratings = db.Column(db.String(1024), nullable=False)
    category = db.Column(db.String(1024), nullable=False)
    price_range = db.Column(db.String(1024), nullable=False)
    full_address = db.Column(db.String(1024), nullable=False)
    zip_code = db.Column(db.Integer, nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)
    state = db.Column(db.String(1024), nullable=False)
    # defining the reverse side of the relationship
    items = db.relationship(
        "MenuItems", back_populates="restaurant")

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

        for food in self.items:
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
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey(
        "restaurant.id"), nullable=False)
    category = db.Column(db.String(1024), nullable=False)
    name = db.Column(db.String(1024), nullable=False)
    description = db.Column(db.String(1024), nullable=False)
    price = db.Column(db.String(1024), nullable=False)
    restaurant = db.relationship(
        "Restaurant", back_populates="items")

    def str_rep(self):
        elements = [self.category, self.name, self.description]
        str_item = " ".join(elem for elem in elements if elem is not None)
        return str_item

    def rep(self):
        return {
            "restaurant_id": self.restaurant_id,
            "category": self.category,
            "name": self.name,
            "description": self.description,
            "price": self.price

        }

    def serialize(self):
        restaurant = Restaurant.query.filter_by(id=self.restaurant_id).first()
        return {
            "restaurant_id": self.restaurant_id,
            "restaurant": restaurant.rep(),
            "category": self.category,
            "name": self.name,
            "description": self.description,
            "price": self.price

        }
