from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class User(db.model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(
        db.String(50),
        nullable=False,
        unique=True 
    )
    last_name = db.Column(
        db.String(50),
        nullable=False,
        unique=True )
    image_url = db.Column(
        db.Text,
        nullable=False,
        default='https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png'
    )

    __tablename__ = 'tablename2'
    __tablename__ = 'tablename3'

    def __repr__(self):
        """Show info about user."""

        u = self
        return f"<USer {u.id} {u.name} {u.species} {u.hunger}>"
