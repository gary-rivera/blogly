from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """user db info """
    __tablename__ = 'users'
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(
        db.String(50),
        nullable=False)
    last_name = db.Column(
        db.String(50),
        nullable=False)
    image_url = db.Column(
        db.Text,
        nullable=False,
        default='https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png')

    # __tablename__ = 'tablename3'

    def __repr__(self):
        """Show info about user."""

        u = self

        return f"<User {u.id} {u.first_name} {u.first_name}{u.last_name}>"

    # function to generate user name


def connect_db(app):
    """ connect to db """
    db.app = app
    db.init_app(app)
