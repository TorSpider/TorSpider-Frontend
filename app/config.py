import sys
import os
import logging
import configparser
import uuid
import requests

script_dir = os.path.dirname(os.path.realpath(sys.argv[0]))


def read_config():
    if os.path.isfile(os.path.join(script_dir, 'frontend.cfg')):
        # Load the configuration file.
        try:
            my_config = {}
            config = configparser.ConfigParser()
            config.read(os.path.join(script_dir, 'frontend.cfg'))
            my_config['Database'] = {
                'user': config['Database'].get('user'),
                'password': config['Database'].get('password'),
                'host': config['Database'].get('host'),
                'database': config['Database'].get('database')
            }
            my_config['Flask'] = {
                'SECRET_KEY': config['Flask'].get('SECRET_KEY'),
                'USETLS': config['Flask'].getboolean('USETLS'),
                'CERT_FILE': config['Flask'].get('CERT_FILE'),
                'CERT_KEY_FILE': config['Flask'].get('CERT_KEY_FILE'),
                'DEBUG': config['Flask'].getboolean('DEBUG'),
                'LISTEN_PORT': config['Flask'].getint('LISTEN_PORT'),
                'LISTEN_ADDR': config['Flask'].get('LISTEN_ADDR')
            }
            my_config['SQLAlchemy'] = {
                'SQLALCHEMY_ECHO': config['SQLAlchemy'].getboolean('SQLALCHEMY_ECHO'),
                'SQLALCHEMY_TRACK_MODIFICATIONS': config['SQLAlchemy'].getboolean('SQLALCHEMY_TRACK_MODIFICATIONS')
            }
            my_config['WTForms'] = {
                'WTF_CSRF_ENABLED': config['WTForms'].getboolean('WTF_CSRF_ENABLED'),
                'WTF_CSRF_SECRET_KEY': config['WTForms'].get('WTF_CSRF_SECRET_KEY')
            }
            my_config['LOGGING'] = {
                'loglevel': logging.getLevelName(config['LOGGING'].get('loglevel')),
                'apploglevel': logging.getLevelName(config['LOGGING'].get('apploglevel'))
            }
            my_config['Backend'] = {
                'API_URL': config['Backend'].get('API_URL'),
                'API_KEY': config['Backend'].get('API_KEY'),
                'API_NODE': config['Backend'].get('API_NODE'),
                'VERIFY_SSL': config['Backend'].getboolean('VERIFY_SSL')
            }
            return my_config
        except Exception as e:
            print('Could not parse frontend.cfg. Please verify its syntax.')
            print('Error: {}'.format(e))
            sys.exit(0)


def make_config():
    """
    Create the initial config file.
    """
    if not os.path.exists(os.path.join(script_dir, 'frontend.cfg')):
        # If we don't yet have a configuration file, make one and tell the
        # user to set it up before continuing.
        default_config = configparser.RawConfigParser()
        default_config.optionxform = lambda option: option
        default_config['Database'] = {
            'user': 'torspider',
            'password': 'password',
            'host': '127.0.0.1',
            'database': 'TorSpider-Frontend'
        }
        default_config['Flask'] = {
            'SECRET_KEY': uuid.uuid4(),
            'USETLS': True,
            'DEBUG': False,
            'LISTEN_PORT': 1081,
            'LISTENING_ADDR': '127.0.0.1',
            'CERT_FILE': '/etc/nginx/certs/torspider/frontend.pem',
            'CERT_KEY_FILE': '/etc/nginx/certs/torspider/frontend-key.pem'
        }
        default_config['SQLAlchemy'] = {
            'SQLALCHEMY_ECHO': False,
            'SQLALCHEMY_TRACK_MODIFICATIONS': False
        }
        default_config['WTForms'] = {
            'WTF_CSRF_ENABLED': True,
            'WTF_CSRF_SECRET_KEY': uuid.uuid4()
        }
        default_config['LOGGING'] = {
            'loglevel': 'INFO',
            'apploglevel': 'CRITICAL'
        }
        default_config['Backend'] = {
            'API_URL': 'https://127.0.0.1/api/',
            'API_KEY': 'Specify_API_Key',
            'API_NODE': 'Specify_API_Node',
            'VERIFY_SSL': True
        }
        with open(os.path.join(script_dir, 'frontend.cfg'), 'w') as config_file:
            default_config.write(config_file)
        print('[+] Default configuration stored in frontend.cfg.')
        print('[+] Please edit frontend.cfg before running TorSpider frontend.')
    else:
        print('[!] The frontend.cfg file already exists.  Please delete it to create a fresh one.')


server_config = read_config()


class ProductionConf(object):
    if not server_config:
        make_config()
        server_config = read_config()

    LOG_LEVEL = server_config['LOGGING'].get('loglevel')
    APP_LOG_LEVEL = server_config['LOGGING'].get('apploglevel')
    SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@{}:5432/{}".format(server_config['Database'].get('user'),
                                                                     server_config['Database'].get('password'),
                                                                     server_config['Database'].get('host'),
                                                                     server_config['Database'].get('database'))
    SECRET_KEY = server_config['Flask'].get('SECRET_KEY')
    DEBUG = server_config['Flask'].get('DEBUG')
    LISTEN_PORT = server_config['Flask'].get('LISTEN_PORT')
    LISTEN_ADDR = server_config['Flask'].get('LISTEN_ADDR')
    USETLS = server_config['Flask'].get('USETLS')
    CERT_FILE = server_config['Flask'].get('CERT_FILE')
    CERT_KEY_FILE = server_config['Flask'].get('CERT_KEY_FILE')
    API_URL = server_config['Backend'].get('API_URL')
    API_KEY = server_config['Backend'].get('API_KEY')
    API_NODE = server_config['Backend'].get('API_NODE')
    WTF_CSRF_ENABLED = server_config['WTForms'].get('SQLALCHEMY_ECHO')
    WTF_CSRF_SECRET_KEY = server_config['WTForms'].get('WTF_CSRF_SECRET_KEY')
    SQLALCHEMY_ECHO = server_config['SQLAlchemy'].get('SQLALCHEMY_ECHO')
    SQLALCHEMY_TRACK_MODIFICATIONS = server_config['SQLAlchemy'].get('SQLALCHEMY_TRACK_MODIFICATIONS')
    VERIFY_SSL = server_config['Backend'].get('VERIFY_SSL')
    if not VERIFY_SSL:
        # if we disable ssl verification, we'll also disable warning messages.
        from requests.packages.urllib3.exceptions import InsecureRequestWarning
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

