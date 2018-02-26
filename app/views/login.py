from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user
from app.forms import LoginForm
from app.models import User
from app import app, db
import bcrypt


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = request.form['username']
        password = request.form['password']
        user = db.session.query(User).filter(User.username == username.lower()).first()
        if user:
            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                login_user(user)
                flash("Logged in as {}.".format(user.username))
                return redirect(url_for('index'))
        flash("Login failed.  Bad username or password.")
        return render_template("login.html", form=form)
    return render_template("login.html", form=form)

