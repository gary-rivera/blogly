from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config["SECRET_KEY"] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def root():
    """ redirect to users page"""

    return redirect('/users')


@app.route('/users')
def list_users():
    """ list current users in db"""

    users = User.query.order_by(User.last_name).all()
    return render_template('index.html', users=users)


@app.route('/users/new')
def show_new_user_form():
    """ render the form to create new user and post """

    return render_template('newUser.html')


@app.route('/users/new', methods=['POST'])
def create_user():
    """ forward form input to generate a new user """

    # add logic if url empty
    user_data = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None)

    db.session.add(user_data)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>')
def user_details(user_id):
    """rendering user details"""

    user_data = User.query.get_or_404(user_id)
    return render_template('userDetails.html', user=user_data)


# # cross relationship between tables
