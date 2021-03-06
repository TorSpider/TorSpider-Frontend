#! /usr/bin/env python3
from os import environ
import os
import sys
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app
from app.models import *
import logging
from logging.handlers import TimedRotatingFileHandler
import bcrypt
import uuid

script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
manager = Manager(app)


class DB(object):
    def __init__(self, metadata):
        self.metadata = metadata


migrate = Migrate(app, DB(db.metadata))
manager.add_command('db', MigrateCommand)


@manager.command
def create_admin_user(username, password):
    """
    Create an admin user.
    """
    newuser = User()
    newuser.username = username
    newuser.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    newuser.role = 'Admin'
    try:
        db.session.add(newuser)
        db.session.commit()
        print('User {} created.'.format(username))
        return True
    except Exception as e:
        print('Failed to create user {}'.format(username))
        db.session.rollback()
        return False

@manager.command
def reset_password(username, password):
    """
    Create an admin user.
    """
    theuser = db.session.query(User).filter(User.username == username).first()
    theuser.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    try:
        db.session.merge(theuser)
        db.session.commit()
        print('User {} Update.'.format(username))
        return True
    except Exception as e:
        print('Failed to update user {}'.format(username))
        db.session.rollback()
        return False

@manager.command
def create_invite_code():
    """
    Create an invite code
    """
    invite = Invites()
    invite.invite_code = str(uuid.uuid4())
    invite.active = True
    try:
        db.session.add(invite)
        db.session.commit()
        print('Invite code created: {}'.format(invite.invite_code))
    except Exception as e:
        db.session.rollback()
        print("Failed to create invite code.")


@manager.command
def initdb():
    """
    Initialize the database and create all tables.
    """
    print("[+] Initializing database...")
    print("[+] Creating tables...")
    db.create_all(bind=None)
    print('[+] Done!')


@manager.command
def seed():
    """
    Seed the database with the initial data required.
    """
    # Populate the database with basic user roles.
    print('[+] Splinkle sprinkle!!!')

    roles = [
        Role(id=10, title="Admin"),
        Role(id=3, title="User"),
        Role(id=0, title="None")
    ]

    for role in roles:
        db.session.merge(role)
    db.session.commit()

    print('[+] Done.')


@manager.command
def run():
    """
    Run the server.
    """

    # Set up the logger.
    if not os.path.isdir(os.path.join(script_dir, 'logs')):
        os.makedirs(os.path.join(script_dir, 'logs'))
    # Format the logs.
    formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    # Enable the logs to split files at midnight.
    handler = TimedRotatingFileHandler(
            os.path.join(script_dir, 'logs', 'TorSpider.log'),
            when='midnight', backupCount=7, interval=1)
    handler.setLevel(app.config['LOG_LEVEL'])
    handler.setFormatter(formatter)
    log = logging.getLogger('werkzeug')
    log.setLevel(app.config['LOG_LEVEL'])
    log.addHandler(handler)
    app.logger.addHandler(handler)
    app.logger.setLevel(app.config['APP_LOG_LEVEL'])

    # Set up the app server, port, and configuration.
    port = int(environ.get('PORT', app.config['LISTEN_PORT']))
    addr = environ.get('LISTEN_ADDR', app.config['LISTEN_ADDR'])
    if app.config['USETLS']:
        context = (app.config['CERT_FILE'], app.config['CERT_KEY_FILE'])
        app.run(host=addr, port=port, threaded=True, ssl_context=context)
    else:
        app.run(host=addr, port=port, threaded=True)


if __name__ == '__main__':
    if sys.version_info[0] < 3:
        raise Exception("Please use Python version 3 to run this script.")
    manager.run()
