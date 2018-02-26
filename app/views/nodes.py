from flask import render_template, request, flash, abort, redirect, url_for
from flask_login import login_required, current_user
from app import app, db
from app.models import Nodes
from app.tables import Node, NodesTable
from sqlalchemy import desc, asc
from sqlalchemy import or_
from app.helpers import create_api_key, create_unqiue_id
import datetime


@app.route("/nodes", methods=["GET"])
@login_required
def nodes():
    sort = request.args.get('sort', 'id')
    # You would image that the library would support switching the sort automatically from asc to desc, but it 
    # doesn't appear it does that :(
    sort_dir = request.args.get('direction', 'asc')
    order = asc(sort) if sort_dir == "asc" else desc(sort)
    # Check if admin
    if current_user.check_role() >= 10:
        the_nodes = db.session.query(Nodes).order_by(order).all()
        # Populate the table
        table = NodesTable(the_nodes)
        return render_template("nodes.html", table=table)
    # Check if user
    elif current_user.check_role() >= 3:
        the_nodes = db.session.query(Nodes).filter(Nodes.owner == current_user.username).order_by(order).all()
        # Populate the table
        table = NodesTable(the_nodes)
        return render_template("nodes.html", table=table)
    else:
        # User unauthorized
        abort(401)


@app.route("/nodes/new", methods=["GET"])
@login_required
def new_node():
    if current_user.check_role() >= 3:
        # For now let's limit a user to 5 nodes.
        node_count = db.session.query(Nodes).filter(Nodes.owner == current_user.username).count()
        if node_count >= 5:
            flash('You have reached the limit of 5 nodes.')
            return redirect(url_for('nodes'))
        check_dup = True
        # Keep trying to create unique keys until they don't exist in the db.  This should really only run once.
        # Collisions should be very low.
        while check_dup:
            unique_id = create_unqiue_id()
            api_key = create_api_key()
            check_dup = db.session.query(Nodes).filter(
                or_(Nodes.unique_id == unique_id, Nodes.api_key == api_key)).first()
        new_node = Nodes()
        new_node.owner = current_user.username
        new_node.unique_id = unique_id
        new_node.api_key = api_key
        new_node.active = True
        try:
            db.session.add(new_node)
            db.session.commit()
            flash("Node {} added successfully.".format(unique_id))
            return redirect(url_for('nodes'))
        except:
            db.session.rollback()
            flash("Error adding node.  Please try again.")
            return redirect(url_for('nodes'))
    else:
        abort(401)


@app.route("/nodes/delete", methods=["POST"])
@login_required
def delete_node():
    id = request.args.get('id')
    if not id:
        flash('Node ID not provided.')
        return redirect(url_for('nodes'))
    if current_user.check_role() >= 10:
        del_node = db.session.query(Nodes).filter(Nodes.id == id).first()
        try:
            db.session.delete(del_node)
            db.session.commit()
            flash("Node {} deleted successfully.".format(del_node.unique_id))
            return redirect(url_for('nodes'))
        except:
            flash("Error deleting node. Please try again.")
            return redirect(url_for('nodes'))
    elif current_user.check_role() >= 3:
        del_node = db.session.query(Nodes).filter(Nodes.id == id).first()
        if del_node.owner != current_user.username:
            flash("Permission denied.")
            return redirect(url_for('nodes'))
        try:
            db.session.delete(del_node)
            db.session.commit()
            flash("Node {} deleted successfully.".format(del_node.unique_id))
            return redirect(url_for('nodes'))
        except:
            flash("Error deleting node. Please try again.")
            return redirect(url_for('nodes'))
    else:
        abort(401)


@app.route("/nodes/disable", methods=["POST"])
@login_required
def disable_node():
    id = request.args.get('id')
    if not id:
        flash('Node ID not provided.')
        return redirect(url_for('nodes'))
    if current_user.check_role() >= 10:
        disable_node = db.session.query(Nodes).filter(Nodes.id == id).first()
        try:
            disable_node.active = False
            db.session.merge(disable_node)
            db.session.commit()
            flash("Node {} disabled successfully.".format(disable_node.unique_id))
            return redirect(url_for('nodes'))
        except:
            flash("Error disabling node. Please try again.")
            return redirect(url_for('nodes'))
    elif current_user.check_role() >= 3:
        disable_node = db.session.query(Nodes).filter(Nodes.id == id).first()
        if disable_node.owner != current_user.username:
            flash("Permission denied.")
            return redirect(url_for('nodes'))
        try:
            disable_node.active = False
            db.session.merge(disable_node)
            db.session.commit()
            flash("Node {} disabled successfully.".format(disable_node.unique_id))
            return redirect(url_for('nodes'))
        except:
            flash("Error disabled node. Please try again.")
            return redirect(url_for('nodes'))
    else:
        abort(401)


@app.route("/nodes/regen_api", methods=["POST"])
@login_required
def regen_node_api():
    id = request.args.get('id')
    if not id:
        flash('Node ID not provided.')
        return redirect(url_for('nodes'))
    if current_user.check_role() >= 10:
        api_node = db.session.query(Nodes).filter(Nodes.id == id).first()
        check_dup = True
        # Keep trying to create a unique key until it doesn't exist in the db.  
        while check_dup:
            api_key = create_api_key()
            check_dup = db.session.query(Nodes).filter(Nodes.api_key == api_key).first()
        try:
            api_node.api_key = api_key
            db.session.merge(api_node)
            db.session.commit()
            flash("Node {} updated successfully.".format(api_node.unique_id))
            return redirect(url_for('nodes'))
        except:
            flash("Error deleting node. Please try again.")
            return redirect(url_for('nodes'))
    elif current_user.check_role() >= 3:
        api_node = db.session.query(Nodes).filter(Nodes.id == id).first()
        if api_node.owner != current_user.username:
            flash("Permission denied.")
            return redirect(url_for('nodes'))
        check_dup = True
        # Keep trying to create a unique key until it doesn't exist in the db.  
        while check_dup:
            api_key = create_api_key()
            check_dup = db.session.query(Nodes).filter(Nodes.api_key == api_key).first()
        try:
            api_node.api_key = api_key
            db.session.delete(api_node)
            db.session.commit()
            flash("Node {} updated successfully.".format(api_node.unique_id))
            return redirect(url_for('nodes'))
        except:
            flash("Error updating node. Please try again.")
            return redirect(url_for('nodes'))
    else:
        abort(401)
