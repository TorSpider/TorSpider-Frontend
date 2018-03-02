# TorSpider-Frontend
A web frontend for exploring the information collected by TorSpider.


## Installation

### First Steps

First, ensure you have installed the requirements:
`pip3 install -r requirements.txt`

Next, run the backend_manage.py script once to generate the backend.cfg file:
```
$ python frontend_manage.py
[+] Default configuration stored in frontend.cfg.
[+] Please edit frontend.cfg before running TorSpider frontend.
```

Update your app/config.py file with the PostgreSQL DB settings and ensure the database is created. You should not use the same database for the frontend as you do for the backend. **Note:** The frontend node name and key are generated using the backend_manage.py script in the backend. See the backend installation instructions for more details.

Next, you'll need to initialize the frontend database and seed it with values:
```
python3 frontend_manage.py initdb
python3 frontend_manage.py seed
```

Then you'll need to create a frontend admin user:
```
python frontend_manage.py create_admin_user [user] [pass]
```
Replace [user] and [pass] with the desired username and password.

### SSL Certificates

In order to encrypt communication with the backend API, you'll need SSL certificates. You can obtain these from a number of sources, or generate your own. Once you've got them, you'll need to save them in the `/etc/nginx/certs/torspider/` folder. You should have the following two files:

`/etc/nginx/certs/torspider/cert.crt`
`/etc/nginx/certs/torspider/cert.key`

Once those certificates are in place, you should be able to run the frontend.

**Note:** These certificates are the same certificates as the ones used in the backend installation.

### Installing the Frontend as a Service

If you'd like to install the backend as a service:
Please note, we assume torspider is installed as the torpsider user in /home/torspider.
1. Run `sudo cp init/torspider-frontend.service /etc/systemd/system/`
2. Run `sudo systemctl daemon-reload`
3. Run `sudo systemctl enable torspider-frontend`

## Running the Frontend
Let's get started:
`ptyhon3 frontend_manage.py run`

Run it as a service:
`systemctl start torspider-frontend`

You are now running your frontend, exposed on http://your_ip:1081

## Set up Nginx
Nginx is used to expose both the frontend (1081) and backend (1080) websites on one port (80) to regular users.
Ensure your have Nginx installed: `apt-get install nginx`

Copy one of the provided nginx config files to /etc/nginx/sites-available.

If you are installing the frontend on a separate system from the backend, copy the frontend configuration as follows:

`cp nginx_conf/frontend /etc/nginx/sites-available/default`

However, if you are running both the backend and frontend on the same system, copy the combined configuration as follows:

`cp nginx_conf/combined /etc/nginx/sites-available/default`

After copying the appropriate configuration file, restart Nginx:
`service nginx restart`

Once this is complete, you should be able to access the frontend from http://your_ip/.
