from typing import Sequence
from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime, time
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
import uuid

db = SQLAlchemy()


class Restaurant(db.Model):
    __tablename__ = "restaurant"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    position = db.Column(db.Integer, nullable=True)
    name = db.Column(db.String, nullable=False)
    score = db.Column(db.Float, nullable=True)
    ratings = db.Column(db.Float, nullable=True)
    category = db.Column(db.String, nullable=False)
    price_range = db.Column(db.String, nullable=True)
    full_address = db.Column(db.String, nullable=True)
    zip_code = db.Column(db.Integer, nullable=True)
    lat = db.Column(db.Float, nullable=True)
    lng = db.Column(db.Float, nullable=True)
    # defining the reverse side of the relationship
    items = db.relationship("MenuItems", back_populates="restaurant")

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
            "lng": self.lng
        }

    def serialize(self):

        menuitems = []

        for food in self.items:
            menuitems.append(food.menu_items.rep())

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
            "menuitems": menuitems
        }


class MenuItems(db.Model):
    __tablename__ = "menu_items"
    restaurant_id = db.Column(db.Integer, db.ForeignKey(
        "restaurant.id"), nullable=False)
    category = db.Column(db.String, nullable=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    price = db.Column(db.String, nullable=True)
    restaurant = db.relationship(Restaurant, back_populates="restaurant")

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
