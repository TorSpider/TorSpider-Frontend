from flask import redirect, url_for, flash
from flask_login import logout_user, current_user
from app import app


@app.route("/logout", methods=["GET"])
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash("Logged out.")
    return redirect(url_for("login"))
