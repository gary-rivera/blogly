from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config["SECRET_KEY"] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

#### Users routes ###


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


@app.route('/users/<int:user_id>/edit')
def show_edit_user_form(user_id):
    """Direct to the user edit form page"""
    user_data = User.query.get_or_404(user_id)
    return render_template('userEdit.html', user=user_data)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user(user_id):
    """Modify user information"""
    user_data = User.query.get_or_404(user_id)
    user_data.first_name = request.form['first_name']
    user_data.last_name = request.form['last_name']
    user_data.image_url = request.form['image_url']

    db.session.add(user_data)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Delete user information"""
    user_data = User.query.get_or_404(user_id)
    db.session.delete(user_data)
    db.session.commit()

    return redirect("/users")


### Posts routes ###

@app.route('/users/<int:user_id>/posts/new')
def add_post_form(user_id):
    """render page for user to add a post"""
    user_data = User.query.get_or_404(user_id)

    return render_template('addPost.html', user=user_data)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_post(user_id):
    """ handle new post form redirect to user details """
    user_data = User.query.get_or_404(user_id)
    post = Post(
        title=request.form['title'],
        content=request.form['content'],
        user=user_data)

    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{user_id}")


@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """ generate a page with the corresponding users post """
    post = Post.query.get_or_404(post_id)

    return render_template('postDetails.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def edit_post_form(post_id):
    """show edit form page and redirect to the post view"""
    post = Post.query.get_or_404(post_id)
    return render_template('editPost.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def update_post(post_id):
    """Handle submission, update the form, and """

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()
    
    return redirect(f"/posts/{post_id}")


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete(post_id):
    """Handle deleting post"""
    post = Post.query.get_or_404(post_id)
    user_id = post.user_id
    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{user_id}")
