from flask import render_template, request, flash, abort, redirect, url_for
from flask_login import login_required, current_user
from app import app, db
from app.models import User
from app.tables import Users, UsersTable
from sqlalchemy import desc, asc
from app.helpers import generate_password
import bcrypt


@app.route("/users", methods=["GET"])
@login_required
def users():
    if current_user.check_role() >= 10:
        sort = request.args.get('sort', 'id')
        # You would image that the library would support switching the sort automatically from asc to desc, but it 
        # doesn't appear it does that :(
        sort_dir = request.args.get('direction', 'asc')
        order = asc(sort) if sort_dir == "asc" else desc(sort)
        # Check if admin
        the_users = db.session.query(User).order_by(order).all()
        # Populate the table
        table = UsersTable(the_users)
        return render_template("users.html", table=table)
    else:
        # User unauthorized
        abort(401)


@app.route("/users/delete", methods=["POST"])
@login_required
def delete_user():
    id = request.args.get('id')
    if not id:
        flash('User ID not provided.')
        return redirect(url_for('users'))
    if current_user.check_role() >= 10:
        del_user = db.session.query(User).filter(User.id == id).first()
        try:
            db.session.delete(del_user)
            db.session.commit()
            flash("User {} deleted successfully.".format(del_user.username))
            return redirect(url_for('users'))
        except:
            flash("Error deleting user. Please try again.")
            return redirect(url_for('users'))
    else:
        abort(401)


@app.route("/users/disable", methods=["POST"])
@login_required
def disable_user():
    id = request.args.get('id')
    if not id:
        flash('User ID not provided.')
        return redirect(url_for('users'))
    if current_user.check_role() >= 10:
        disable_user = db.session.query(User).filter(User.id == id).first()
        try:
            disable_user.active = False
            db.session.merge(disable_user)
            db.session.commit()
            flash("User {} disabled successfully.".format(disable_user.username))
            return redirect(url_for('users'))
        except:
            flash("Error disabling user. Please try again.")
            return redirect(url_for('users'))
    else:
        abort(401)


@app.route("/users/regen_password", methods=["POST"])
@login_required
def regen_password():
    id = request.args.get('id')
    if not id:
        flash('Node ID not provided.')
        return redirect(url_for('users'))
    if current_user.check_role() >= 10:
        the_user = db.session.query(User).filter(User.id == id).first()
        try:
            thepassword = generate_password()
            the_user.password = bcrypt.hashpw(thepassword.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            db.session.merge(the_user)
            db.session.commit()
            flash("User {} updated successfully.".format(the_user.username))
            return render_template("users_newpass.html", the_pass=thepassword, the_user=the_user.username)
        except Exception as e:
            print(e)
            flash("Error updating user. Please try again.")
            return redirect(url_for('users'))
    else:
        abort(401)
