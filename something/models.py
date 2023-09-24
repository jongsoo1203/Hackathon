from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    protein = db.Column(db.Float, nullable=False)
    fat = db.Column(db.Float, nullable=False)
    carbohydrates = db.Column(db.Float, nullable=False)
    portion_sizes = db.Column(db.String(50), nullable=False)

class UserLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'), nullable=False)
    food = db.relationship('Food', backref='user_logs')

