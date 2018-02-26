from flask import render_template, request, flash, abort, redirect, url_for
from flask_login import login_required, current_user
from app import app, db
from app.models import Invites
from app.tables import Invite, InviteTable
from sqlalchemy import desc, asc
from app.helpers import create_invite_code


@app.route("/invites", methods=["GET"])
@login_required
def invites():
    sort = request.args.get('sort', 'id')
    # You would image that the library would support switching the sort automatically from asc to desc, but it 
    # doesn't appear it does that :(
    sort_dir = request.args.get('direction', 'asc')
    order = asc(sort) if sort_dir == "asc" else desc(sort)
    # Check if admin
    if current_user.check_role() >= 10:
        the_invites = db.session.query(Invites).order_by(order).all()
        # Populate the table
        table = InviteTable(the_invites)
        return render_template("invites.html", table=table)
    else:
        # User unauthorized
        abort(401)


@app.route("/invites/new", methods=["GET"])
@login_required
def new_invite():
    if current_user.check_role() >= 10:
        check_dup = True
        # Keep trying to create unique keys until they don't exist in the db.  This should really only run once.
        # Collisions should be very low.
        while check_dup:
            invite_code = create_invite_code()
            check_dup = db.session.query(Invites).filter(Invites.invite_code == invite_code).first()
        new_code = Invites()
        new_code.created_by = current_user.username
        new_code.invite_code = invite_code
        new_code.active = True
        try:
            db.session.add(new_code)
            db.session.commit()
            flash("Invite code {} added successfully.".format(invite_code))
            return redirect(url_for('invites'))
        except:
            db.session.rollback()
            flash("Error adding invite code.  Please try again.")
            return redirect(url_for('invites'))
    else:
        abort(401)


@app.route("/invites/delete", methods=["POST"])
@login_required
def delete_invite():
    id = request.args.get('id')
    if not id:
        flash('Invite code ID not provided.')
        return redirect(url_for('invites'))
    if current_user.check_role() >= 10:
        del_invite_code = db.session.query(Invites).filter(Invites.id == id).first()
        try:
            db.session.delete(del_invite_code)
            db.session.commit()
            flash("Invite code {} deleted successfully.".format(del_invite_code.invite_code))
            return redirect(url_for('invites'))
        except:
            flash("Error deleting invite code. Please try again.")
            return redirect(url_for('invites'))
    else:
        abort(401)


@app.route("/invites/disable", methods=["POST"])
@login_required
def disable_invite():
    # I'm doing provide a disable function for now, perhaps update it to fill edit later.
    id = request.args.get('id')
    if not id:
        flash('Invite code ID not provided.')
        return redirect(url_for('invites'))
    if current_user.check_role() >= 10:
        the_invite = db.session.query(Invites).filter(Invites.id == id).first()
        the_invite.active = False
        try:
            db.session.merge(the_invite)
            db.session.commit()
            flash("Invite code {} updated successfully.".format(the_invite.invite_code))
            return redirect(url_for('invites'))
        except:
            flash("Error disabling invite code. Please try again.")
            return redirect(url_for('invites'))
    else:
        abort(401)
