from flask import render_template, request, flash, redirect, url_for
from app import app, db
from app.forms import RegisterForm
from app.models import User, Invites
import bcrypt
import bleach


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = request.form['username']
        password = request.form['password'].strip()
        invitecode = request.form['invitecode'].strip()
        invite = db.session.query(Invites).filter(Invites.invite_code == invitecode, Invites.active == True).first()
        if invite:
            newuser = User()
            newuser.username = username
            if bleach.clean(username) != username:
                flash("Bad user name")
                return render_template("register.html", form=form)
            newuser.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            newuser.role = 'User'
            try:
                # Add user
                db.session.add(newuser)
                db.session.commit()
                # Invalidate user code
                invite.active = False
                db.session.merge(invite)
                db.session.commit()
                flash('User {} created.'.format(username))
                return redirect(url_for('index'))
            except Exception as e:
                flash('Failed to create user {}'.format(username))
                db.session.rollback()
                return render_template("register.html", form=form)
        flash("Invalid invite code.")
        return render_template("register.html", form=form)
    return render_template("register.html", form=form)
