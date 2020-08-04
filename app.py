"""Flask app for Cupcakes"""

from flask import Flask, jsonify, request, render_template #redirect, , flash
from models import db, connect_db, Cupcake, DEFAULT_URL

app = Flask(__name__)
 
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
# Comment the line below and uncomment the line above if not on windows.
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://rainb:qwerty@localhost/cupcakes'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

@app.route('/')
def root():
    return render_template('cupcakes.html')


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
    """Create a cupcake with flavor, size, rating and image data from the body 
    of the request.
    Return JSON: {cupcake: {id, flavor, size, rating, image}}."""

    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = DEFAULT_URL if request.json["image"] == "" else request.json["image"] 

    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)
    db.session.add(new_cupcake)
    db.session.commit()

    serialized = new_cupcake.serialize()

    return (jsonify(cupcake=serialized), 201)


@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def get_cupcake(cupcake_id):
    """ Update cupcake information.
    Return JSON: {cupcake: {id, flavor, size, rating, image}}."""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    # print('cupcake', cupcake)
    
    if "flavor" in request.json:
        cupcake.flavor = request.json["flavor"]
    if "size" in request.json:
        cupcake.size = request.json["size"] 
    if "rating" in request.json:
        cupcake.rating = request.json["rating"]
    if "image" in request.json:
        # if leave blank, set it None, in model it will set to default pict 
        cupcake.image = DEFAULT_URL if request.json["image"] == "" else request.json["image"] 
    
    db.session.commit()

    serialized = cupcake.serialize()

    return jsonify(cupcake=serialized)


@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def delete_cupcake(cupcake_id):
    """ Delete Cupcake. 
    Return JSON: {message: "Deleted"}."""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    delete_msg = {"message": "Deleted"}
    
    return delete_msg