from flask import render_template, flash
from flask_login import login_user

from . import admin_blueprint
from .forms import LoginForm
from ..models import User


@admin_blueprint.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            flash('Successfully logged in')
        flash('Invalid username or password')
    return render_template('login.html', form=form)
