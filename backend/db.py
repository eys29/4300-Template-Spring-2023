from typing import Sequence
from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime, time
from typing import List
from typing import Optional
import uuid

db = SQLAlchemy()


class Restaurant(db.Model):
    __tablename__ = "restaurant_table"
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
    item_table = db.relationship("MenuItems", back_populates="restaurant_table")

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

        for food in self.item_table:
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
    __tablename__ = "item_table"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey(
        "restaurant_table.id"), nullable=False)
    category = db.Column(db.String(1024), nullable=True)
    name = db.Column(db.String(1024), nullable=False)
    description = db.Column(db.String(1024), nullable=True)
    price = db.Column(db.String(1024), nullable=True)
    restaurant_table = db.relationship("Restaurant", back_populates="item_table")

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
