from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, NewApplication, ConnectForm
from flaskblog.models import User, Applications, friends
from flaskblog import app, bcrypt, db
from flask_login import login_user, current_user, logout_user, login_required
import secrets
import os
from PIL import Image
from sqlalchemy import select

