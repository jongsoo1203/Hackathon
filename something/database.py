from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lifenutrition.db'
db = SQLAlchemy(app)

# Define the Food model
class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    protein = db.Column(db.Float)
    fat = db.Column(db.Float)
    carbohydrates = db.Column(db.Float)
    portion_sizes = db.Column(db.String(255))

# Define the UserLog model
class UserLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'), nullable=False)
    meal_section = db.Column(db.String(50))
    portion_size = db.Column(db.Float)

# Create the database tables
db.create_all()
# Insert a new food item
food = Food(name='Apple', protein=0.3, fat=0.4, carbohydrates=19, portion_sizes='1 medium apple')
db.session.add(food)
db.session.commit()

# Retrieve food items
foods = Food.query.all()
for food in foods:
    print(food.name, food.protein, food.fat, food.carbohydrates, food.portion_sizes)
