
from flask import render_template, url_for, flash, redirect, request
from flaskblog.users.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flaskblog.applications.forms import ConnectForm
from flaskblog.models import User, Applications, friends
from flaskblog import bcrypt, db
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import select
from flask import Blueprint
from flaskblog.users.utils import save_picture

users = Blueprint('users',__name__)


@users.route("/register", methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created! You are now able to login.", "success")
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form)

@users.route("/", methods=['GET','POST'])
@users.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('main.home'))
        else:
            flash("Login Unsuccessful.Please check email and password", "danger")
    return render_template('login.html', title='Login',form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))



@users.route("/account", methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    page = request.args.get('page',1,type=int)
    applications = applications = Applications.query.filter_by(author=current_user)\
        .order_by(Applications.date_applied.desc())\
        .paginate(page=page,per_page = 5)
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!','success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename = 'profile_pics/'+ current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form, applications=applications)


@users.route("/user/<string:username>", methods=['GET','POST'])
def user_applications(username):
    form = ConnectForm()
    page = request.args.get('page',1,type=int)
    user = User.query.filter_by(username = username).first_or_404()
    applications = Applications.query.filter_by(author=user)\
        .order_by(Applications.date_applied.desc())\
        .paginate(page=page,per_page = 5)
    
    already_connected = False  # Assume users are not connected initially
    if current_user.is_authenticated:
        user_id = current_user.id
        friend_id = user.id
        existing_connection = db.session.query(friends).filter(
            (friends.c.user_id == user_id) & (friends.c.friend_id == friend_id)
            | (friends.c.user_id == friend_id) & (friends.c.friend_id == user_id)
        ).first()
        if existing_connection:
            already_connected = True  # Update already_connected if the connection exists
    
    if form.validate_on_submit():
        if current_user.is_authenticated:
            if not already_connected:  # If the connection does not exist, add it
                new_connection = friends.insert().values(user_id=user_id, friend_id=friend_id)
                db.session.execute(new_connection)
                db.session.commit()
                flash('You are now connected with {}'.format(user.username), 'success')
            else:
                flash('You are already connected with {}'.format(user.username), 'info')
        else:
            flash('You need to be logged in to connect with other users', 'danger')
        return redirect(url_for('users.user_applications', username=username))  # Redirect to the same page after processing
    form.user_id.data = current_user.id
    form.friend_id.data = user.id
    return render_template('user_applications.html',applications=applications, user=user, form=form, already_connected=already_connected)


@users.route("/allusers")
def allusers():
    page = request.args.get('page', 1, type=int)
    username_query = request.args.get('username_query', None)
    
    if username_query:
        users = User.query.filter(User.username.ilike(f'%{username_query}%')).paginate(page=page, per_page=5)
    else:
        users = User.query.paginate(page=page, per_page=5)
    
    return render_template('allusers.html', users=users)
    