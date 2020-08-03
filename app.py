"""Flask app for Cupcakes"""

from flask import Flask, jsonify, request #redirect, render_template, flash
from models import db, connect_db, Cupcake

app = Flask(__name__)
 
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
# Comment the line below and uncomment the line above if not on windows.
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://rainb:qwerty@localhost/cupcakes'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
# db.create_all()

@app.route('/api/cupcakes')
def get_cupcakes():
    """Get data about all cupcakes.
    Return JSON: {cupcakes: [{id, flavor, size, rating, image}, ...]}."""

    cupcakes = Cupcake.query.all()
    serialized = [c.serialize() for c in cupcakes]

    return jsonify(cupcakes=serialized)


@app.route('/api/cupcakes/<int:cupcake_id>')
def get_single_cupcake(cupcake_id):
    """Get data about a single cupcake.
    Return JSON: {cupcake: {id, flavor, size, rating, image}}."""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = cupcake.serialize()

    return jsonify(cupcake=serialized)


@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    """Create a cupcake with flavor, size, rating and image data from the body of the request.
    Return JSON: {cupcake: {id, flavor, size, rating, image}}."""

    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json["image"]

    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)
    db.session.add(new_cupcake)
    db.session.commit()

    serialized = new_cupcake.serialize()

    return (jsonify(cupcake=serialized), 201)
