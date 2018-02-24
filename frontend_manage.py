#!/usr/bin/env python
from os import environ
import os
import sys
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app
from app.models import *
import logging
from logging.handlers import TimedRotatingFileHandler

script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
manager = Manager(app)


class DB(object):
    def __init__(self, metadata):
        self.metadata = metadata


migrate = Migrate(app, DB(db.metadata))
manager.add_command('db', MigrateCommand)


@manager.command
def run():
    '''
    Run the server. 
    '''
    if not os.path.isdir(os.path.join(script_dir, 'logs')):
        os.makedirs(os.path.join(script_dir, 'logs'))
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler = TimedRotatingFileHandler(os.path.join(script_dir, 'logs', 'TorSpider.log'), when='midnight', interval=1)
    handler.setLevel(app.config['LOG_LEVEL'])
    handler.setFormatter(formatter)
    log = logging.getLogger('werkzeug')
    log.setLevel(app.config['LOG_LEVEL'])
    log.addHandler(handler)
    app.logger.addHandler(handler)
    app.logger.setLevel(app.config['APP_LOG_LEVEL'])
    port = int(environ.get('PORT', app.config['LISTEN_PORT']))
    addr = environ.get('LISTEN_ADDR', app.config['LISTEN_ADDR'])
    if app.config['USETLS']:
        context = (os.path.join(script_dir, 'certs', 'server.crt'), os.path.join(script_dir, 'certs', 'server.key'))
        app.run(host=addr, port=port, threaded=True, ssl_context=context)
    else:
        app.run(host=addr, port=port, threaded=True)


if __name__ == '__main__':
    if sys.version_info[0] < 3:
        raise Exception("Please use Python version 3 to run this script.")
    manager.run()
