from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog.applications.forms import NewApplication
from flaskblog.models import Applications
from flaskblog import bcrypt, db
from flask_login import current_user, login_required

from flask import Blueprint

applications = Blueprint('applications',__name__)

@applications.route("/application/new", methods=['GET','POST'])
@login_required
def new_application():
    form = NewApplication()
    if form.validate_on_submit():
        application = Applications(companyname=form.companyname.data, jobrole=form.jobrole.data,joblocation=form.joblocation.data,jobwebsite=form.jobwebsite.data,jobdescription=form.jobdescription.data, author=current_user)
        db.session.add(application)
        db.session.commit()
        flash(' Your application has been created','success')
        return redirect(url_for('main.home'))
    return render_template('create_application.html', title='NewApplication', legendvalue = 'New Application',form=form)

@applications.route("/application/<int:application_id>")
def application(application_id):
    application = Applications.query.get_or_404(application_id)
    return render_template('application.html', title='application.companyname', application=application)

@applications.route("/application/<int:application_id>/update", methods=['GET','POST'])
@login_required
def update_application(application_id):
    application = Applications.query.get_or_404(application_id)
    if application.author != current_user:
        abort(403)
    form = NewApplication()
    if form.validate_on_submit():
        application.companyname = form.companyname.data
        application.jobrole = form.jobrole.data 
        application.joblocation =  form.joblocation.data
        application.jobwebsite = form.jobwebsite.data
        application.jobdescription = form.jobdescription.data
        db.session.commit()
        flash("Your application has been updated",'success')
        return redirect(url_for('applications.application', application_id=application.id))
    elif request.method == 'GET':
        form.companyname.data = application.companyname
        form.jobrole.data = application.jobrole
        form.joblocation.data = application.joblocation
        form.jobwebsite.data = application.jobwebsite
        form.jobdescription.data = application.jobdescription
    return render_template('create_application.html', title='UpdateApplication',legendvalue = 'Update Post', form=form)


@applications.route("/application/<int:application_id>/delete", methods=['POST'])
@login_required
def delete_application(application_id):
    application = Applications.query.get_or_404(application_id)
    if application.author != current_user:
        abort(403)
    db.session.delete(application)
    db.session.commit()
    flash('Your application has been deleted!','success')
    return redirect(url_for('main.home'))
