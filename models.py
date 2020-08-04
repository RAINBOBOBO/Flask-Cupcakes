"""Models for Cupcake app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_URL = 'https://tinyurl.com/demo-cupcake'

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class Cupcake(db.Model):
    """Cupcake."""

    __tablename__ = 'cupcakes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flavor = db.Column(db.String(30), nullable=False)
    size = db.Column(db.String(30), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(250), default=DEFAULT_URL)

    def __repr__(self):
        """Show info about Cupcake."""

        return f"<Cupcake {self.id} {self.flavor} {self.size} {self.rating} {self.image}>"


    def serialize(self):
        """Serialize Cupcake response to dictionary."""

        return {
            "id": self.id,
            "flavor": self.flavor,
            "size": self.size,
            "rating": self.rating,
            "image": self.image
        }