#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from sqlalchemy import desc
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.json.compact = False

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Initialize the database
db.init_app(app)

# Define the root route
@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

# Define the route to get a list of all bakeries
@app.route('/bakeries')
def bakeries():
    # Create an empty list to store bakery dictionaries
    bakeries = []

    # Iterate through all bakeries in the database
    for bakery in Bakery.query.all():
        # Create a dictionary representing a bakery
        bakery_dict = {
            'id': bakery.id,              
            'name': bakery.name,         
            'created_at': bakery.created_at,  
        }

        # Add the bakery dictionary to the list
        bakeries.append(bakery_dict)

    # Create a JSON response with the list of bakery dictionaries
    response = make_response(jsonify(bakeries), 200)

    # Set the content type to indicate JSON format
    response.headers['Content-Type'] = 'application/json'

    return response

# Define the route to get a specific bakery by its ID
@app.route('/bakeries/<int:id>')
def bakery_by_id(id):

    # Query the database to find the bakery with the given ID
    bakery = Bakery.query.filter_by(id=id).first()

    # Convert the bakery object to a dictionary
    bakery_dict = bakery.to_dict()

    # Create a JSON response with the bakery dictionary
    response = make_response(jsonify(bakery_dict), 200)

    # Set the content type to indicate JSON format
    response.headers['Content-Type'] = 'application/json'

    return response

# Define the route to get a list of baked goods ordered by price
@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    # Query the database to get all baked goods ordered by price in descending order
    baked_goods = BakedGood.query.order_by(desc(BakedGood.price)).all()

    # Convert the list of baked goods to a list of dictionaries
    baked_goods_list = [good.to_dict() for good in baked_goods]

    # Create a JSON response with the list of baked goods dictionaries
    response = make_response(jsonify(baked_goods_list), 200)

    # Set the content type to indicate JSON format
    response.headers['Content-Type'] = 'application/json'

    return response

# Define the route to get the most expensive baked good
@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    
    # Query the database to get the most expensive baked good
    most_expensive_good = BakedGood.query.order_by(desc(BakedGood.price)).first()

    # Check if a most expensive baked good is found
    if most_expensive_good:
        most_expensive_dict = most_expensive_good.to_dict()
        response = make_response(jsonify(most_expensive_dict), 200)
    else:
        # If no baked goods are found, create a 404 error response
        response = make_response(jsonify({'error': 'No baked goods found'}), 404)

    # Set the content type to indicate JSON format
    response.headers['Content-Type'] = 'application/json'

    return response

# Run the Flask application
if __name__ == '__main__':
    app.run(port=5555, debug=True)
