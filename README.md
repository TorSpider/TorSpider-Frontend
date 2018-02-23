# TorSpider-Frontend
A web frontend for exploring the information collected by TorSpider.


## Installation
Update your app/config.py file with the PostgreSQL DB settings and ensure the database is created.

Ensure you have installed the requirements:
`pip3 install -r requirements.txt` 

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

## Running with Nginx
If you already set up the backend with Nginx, you can access the url with http://your_ip
