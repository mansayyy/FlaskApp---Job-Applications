from flask import render_template, request
from flaskblog.models import Applications, friends
from flaskblog import db
from flask_login import current_user, login_required
from flask import Blueprint

main = Blueprint('main',__name__)


@main.route("/home")
@login_required
def home():
    page = request.args.get('page', 1, type=int)
    if current_user.is_authenticated:
        #  Construct subquery to check if the user_id is in friends' user_id or friend_id
        subquery = db.session.query(friends.c.friend_id).filter(
            ((friends.c.user_id == current_user.id) & (friends.c.friend_id == Applications.user_id)) |
            ((friends.c.friend_id == current_user.id) & (friends.c.user_id == Applications.user_id))
        ).exists()
        applications = Applications.query.filter(subquery).order_by(Applications.date_applied.desc()).paginate(page=page, per_page=5)
    else:
        applications = Applications.query.order_by(Applications.date_applied.desc()).paginate(page=page, per_page=5)
    
    return render_template('home.html', applications=applications)


@main.route("/about/")
def about():
    return render_template('about.html',title="About")
