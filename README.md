# TorSpider-Frontend
A web frontend for exploring the information collected by TorSpider.

## Installation
### First Steps

Run the installation script to install and configure the required software.
The installer will run you through a set of questions to configure your instance.

```
$ sudo bash install.sh
=== TorSpider Frontend Installer ===
This installed will walk you through the installation process.
<snip>
```

### SSL Certificates

#### Self-Signed Certificates
If you answered yes to installing self-signed certificates, your site is already set up.

**Warning:** We do not recommend running your site using self-signed certificates except for in testing or development.

#### Installing Your Own Certificates
In order to encrypt communication, you'll need SSL certificates. You can obtain these from a number of sources, or generate your own. Once you've got them, you'll need to save them in the `/etc/nginx/certs/torspider/` folder. You should have the following two files:

`/etc/nginx/certs/torspider/frontend.pem`
`/etc/nginx/certs/torspider/frontend-key.pem`

Once those certificates are in place, you should be able to run the frontend.

#### Using Let's Encrypt Certificates 
You can use a free certificate service from [Let's Encrypt](https://letsencrypt.org/).  

Install Let'sEncrypt
```
apt-get install -y software-properties-common python-software-properties
add-apt-repository -y ppa:certbot/certbot
apt-get update
apt-get install -y python-certbot-nginx
```

Update /etc/nginx/sites-available/frontend.  You will need to replace any instance of `server_name _;` with `server_name mydomain.com;`
```
EXAMPLE!!!!
<snip>
server {
        # SSL configuration

        listen 443 ssl default_server;
        listen [::]:443 ssl default_server;

        server_name myspider_frontend.com www.myspider_frontend.com;
<snip>
```

Reload Nginx
```
systemctl reload nginx
```

Configure Let's Encrypt. 
Let's Encrypt will update your nginx file with the appropriate certificates
```
# For each domain enter -d <domain> 
certbot --nginx --deploy-hook /path/to/TorSpider-Frontend/letsencrypt/deployhook.sh -d myspider_frontend.com -d www.myspider_frontend.com
```
Ensure you replace `/path/to` with the actual path of the TorSpider-Frontend.

Enable automatic certificate renewal.  Let's Encrypt certs are only good for a few months.
```
systemctl enable certbot.timer
systemctl start certbot.timer
```

Reload Nginx
```
systemctl reload nginx
```

### Initialize the TorSpider Frontend WebApp

Run the frontend_manage.py script once to generate the frontend.cfg file:
```
$ python frontend_manage.py
[+] Default configuration stored in frontend.cfg.
[+] Please edit frontend.cfg before running TorSpider frontend.
```

Update your frontend.cfg file with the PostgreSQL DB settings that were provided to you during the automated installation.

If for some reason you want to run the site without SSL, ensure you set the USETLS setting to False.

### Populate the Database 

Next, you'll need to initialize the frontend database and seed it with values:
```
# Create the database tables
python3 frontend_manage.py initdb
# Seed the initial required values
python3 frontend_manage.py seed
```

If you receive psycopg2 errors during this phase, either PostgreSQL is not running or your username/password is incorrect.

### Create an Admin User
Then you'll need to create a frontend admin user:
```
python frontend_manage.py create_admin_user [user] [pass]
```
Replace [user] and [pass] with the desired username and password.

### Tune PostgreSQL for your server
PostgreSQL should be tuned based on the number of CPUs and memory available on your system.

Head over to [PgTune](http://pgtune.leopard.in.ua/) to create a custom tuned configuration based on your parameters.
Remember to restart postgres after you add them.

## Running the Frontend
Let's get started:
`python3 frontend_manage.py run`

Run it as a service:
`systemctl start torspider-frontend`

You are now running your frontend website, exposed on https://yourip