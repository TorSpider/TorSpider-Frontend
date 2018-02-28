from flask import render_template, request, flash, abort, redirect, url_for
from flask_login import login_required, current_user

from app import app
from app.helpers import create_api_key, create_unique_id, api_get, api_create, api_update, api_delete
from app.tables import NodesTable


@app.route("/nodes", methods=["GET"])
@login_required
def nodes():
    sort = request.args.get('sort', 'id')
    # You would image that the library would support switching the sort automatically from asc to desc, but it 
    # doesn't appear it does that :(
    sort_dir = request.args.get('direction', 'asc')
    # Check if admin
    if current_user.check_role() >= 10:
        query = {"filters": [], "order_by": [{"field": sort, "direction": sort_dir}]}
        the_nodes = api_get('nodes', query)
        if not the_nodes:
            the_nodes = []
        # Populate the table
        table = NodesTable(the_nodes)
        return render_template("nodes.html", table=table)
    # Check if user
    elif current_user.check_role() >= 3:
        query = {"filters": [{"op": "eq", "name": "owner", "val": current_user.username}],
                 "order_by": [{"field": sort, "direction": sort_dir}]}
        the_nodes = api_get('nodes', query)
        if not the_nodes:
            the_nodes = []
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
        # For now let's limit a user to 5 nodes.  Admins can have unlimited nodes.
        if current_user.check_role() >= 10:
            # We will just trick it into always being lower than 5
            node_count = 0
        else:
            query = {"filters": [{
                "op": "eq",
                "name": "owner",
                "val": current_user.username
            }]}
            node_count = api_get('nodes', query)
        if len(node_count) >= 5:
            flash('You have reached the limit of 5 nodes.')
            return redirect(url_for('nodes'))
        check_dup = True
        # Keep trying to create unique keys until they don't exist in the db.  This should really only run once.
        # Collisions should be very low.
        while check_dup:
            unique_id = create_unique_id()
            api_key = create_api_key()
            query = {"filters": [{"or": [{
                "op": "eq",
                "name": "unique_id",
                "val": unique_id
            }, {
                "op": "eq",
                "name": "api_key",
                "val": api_key
            }]}],
                "single": True}
            check_dup = api_get('nodes', query)
        data = {
            "owner": current_user.username,
            "unique_id": unique_id,
            "api_key": api_key,
            "active": True
        }
        add_node = api_create('nodes', data)
        if add_node:
            flash("Node {} added successfully.".format(unique_id))
            return redirect(url_for('nodes'))
        else:
            flash("Error adding node.  Please try again.")
            return redirect(url_for('nodes'))
    else:
        abort(401)


@app.route("/nodes/delete", methods=["POST"])
@login_required
def delete_node():
    id_ = request.args.get('id')
    if not id_:
        flash('Node ID not provided.')
        return redirect(url_for('nodes'))
    if current_user.check_role() >= 10:
        del_node = api_delete('nodes', id_)
        if del_node:
            flash("Node deleted successfully.")
            return redirect(url_for('nodes'))
        else:
            flash("Error deleting node. Please try again.")
            return redirect(url_for('nodes'))
    elif current_user.check_role() >= 3:
        query = {"filters": [{"op": "eq", "name": "id", "val": id_}]}
        test_node = api_get('nodes', query)
        if test_node:
            if test_node[0].get('owner') != current_user.username:
                flash("Permission denied.")
                return redirect(url_for('nodes'))
        del_node = api_delete('nodes', id_)
        if del_node:
            flash("Node deleted successfully.")
            return redirect(url_for('nodes'))
        else:
            flash("Error deleting node. Please try again.")
            return redirect(url_for('nodes'))
    else:
        abort(401)


@app.route("/nodes/disable", methods=["POST"])
@login_required
def disable_node():
    id_ = request.args.get('id')
    if not id_:
        flash('Node ID not provided.')
        return redirect(url_for('nodes'))
    if current_user.check_role() >= 10:
        query = {"filters": [
            {
                "op": "eq",
                "name": "id",
                "val": id_
            }]}
        data = {"active": False, 'q': query}
        disable_node = api_update('nodes', data)
        if disable_node:
            flash("Node disabled successfully.")
            return redirect(url_for('nodes'))
        else:
            flash("Error disabling node. Please try again.")
            return redirect(url_for('nodes'))
    elif current_user.check_role() >= 3:
        query = {"filters": [{"op": "eq", "name": "id", "val": id_}]}
        test_node = api_get('nodes', query)
        if test_node.get('owner') != current_user.username:
            flash("Permission denied.")
            return redirect(url_for('nodes'))
        query = {"filters": [
            {
                "op": "eq",
                "name": "id",
                "val": id_
            }]}
        data = {"active": False, 'q': query}
        disable_node = api_update('nodes', data)
        if disable_node:
            flash("Node disabled successfully.")
            return redirect(url_for('nodes'))
        else:
            flash("Error disabling node. Please try again.")
            return redirect(url_for('nodes'))
    else:
        abort(401)


@app.route("/nodes/regen_api", methods=["POST"])
@login_required
def regen_node_api():
    id_ = request.args.get('id')
    if not id_:
        flash('Node ID not provided.')
        return redirect(url_for('nodes'))
    if current_user.check_role() >= 10:
        check_dup = True
        # Keep trying to create unique keys until they don't exist in the db.  This should really only run once.
        # Collisions should be very low.
        while check_dup:
            api_key = create_api_key()
            query = {"filters": [{
                "op": "eq",
                "name": "api_key",
                "val": api_key
            }],
                "single": True}
            check_dup = api_get('nodes', query)
        query = {"filters": [
            {
                "op": "eq",
                "name": "id",
                "val": id_
            }]}
        data = {"api_key": api_key, 'q': query}

        api_node = api_create('nodes', data)
        if api_node:
            flash("Node updated successfully.")
            return redirect(url_for('nodes'))
        else:
            flash("Error updating node. Please try again.")
            return redirect(url_for('nodes'))
    elif current_user.check_role() >= 3:
        query = {"filters": [{"op": "eq", "name": "id", "val": id_}]}
        test_node = api_get('nodes', query)
        if test_node.get('owner') != current_user.username:
            flash("Permission denied.")
            return redirect(url_for('nodes'))
        check_dup = True
        # Keep trying to create unique keys until they don't exist in the db.  This should really only run once.
        # Collisions should be very low.
        while check_dup:
            api_key = create_api_key()
            query = {"filters": [{
                "op": "eq",
                "name": "api_key",
                "val": api_key
            }],
                "single": True}
            check_dup = api_get('nodes', query)
        query = {"filters": [
            {
                "op": "eq",
                "name": "id",
                "val": id_
            }]}
        data = {"api_key": api_key, 'q': query}

        api_node = api_create('nodes', data)
        if api_node:
            flash("Node updated successfully.")
            return redirect(url_for('nodes'))
        else:
            flash("Error updating node. Please try again.")
            return redirect(url_for('nodes'))
    else:
        abort(401)
