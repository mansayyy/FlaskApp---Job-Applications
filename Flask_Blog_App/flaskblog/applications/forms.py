from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired

class NewApplication(FlaskForm):
    companyname = StringField('Company Name', validators=[DataRequired()])
    jobrole = StringField('Role/Position', validators=[DataRequired()])
    joblocation = StringField('Location')
    jobwebsite = StringField('Role Website')
    jobdescription = TextAreaField('Role Description')
    submit = SubmitField('Add')

class ConnectForm(FlaskForm):
    user_id = IntegerField('Your User ID', validators=[DataRequired()])
    friend_id = IntegerField("Friend's User ID", validators=[DataRequired()])
    submit = SubmitField('Connect')   