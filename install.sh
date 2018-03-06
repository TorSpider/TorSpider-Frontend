#! /bin/bash
# A script to install the frontend
if ! type strings > /dev/null; then
  echo "[-] You need to install strings.  Run sudo apt-get install -y binutils"
  exit 1
fi

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
frontend_user=$(who am i | awk '{print $1}')
postgres_user=$frontend_user
postgres_user_pass=$(strings /dev/urandom | grep -o '[[:alnum:]]' | head -n 15 | tr -d '\n'; echo)
# 1 = false 0=true
self_signed=1

check_root() {
    if [[ $EUID -ne 0 ]]; then
       echo "[-] This script must be run as root!"
       echo "[+] Run: sudo bash install.sh" 
       exit 1
    fi
}

check_same_server() {
    read -p "[?] Are you installing the frontend on the same server as the backend? (Y/n)? " answer
    case ${answer:0:1} in
        n|N )
            echo "[-] Ok. We don't need to do anything special."
        ;;
        * )
            echo "[+] Ok. Reconfiguring..."
            postgres_user="$postgres_user"frontend
        ;;
    esac
}

check_user() {
    echo "[+] Directory of TorSpider-Frontend: $DIR"
    echo "[+] Installation Username: $frontend_user"
    echo "[+] Postgres Username: $postgres_user"
    read -p "[?] Are the directory and installation details correct? (Y/n)? " answer
    case ${answer:0:1} in
        n|N )
            echo "[-] Ok. Exiting."
            exit 1
        ;;
        * )
            echo "[+] Continuing..."
            
        ;;
    esac
}


update_and_install_apt_packages() {
    read -p "[?] Would you like to install required apt packages? (Y/n)? " answer
        case ${answer:0:1} in
            n|N )
                echo "[+] Ok. Skipping apt package installation."
                ;;
            * )
                echo "[+] Performing apt-get update"
                apt-get update
                echo "[+] Installing required apt packages."
                apt-get install -y git postgresql postgresql-server-dev-9.5 nginx python3 python3-pip python3-dev
            ;;
        esac
   
}

setup_postgres() {
    read -p "[?] Would you like to configure the PostgreSQL database for Torspider Frontend? (Y/n)? " answer
        case ${answer:0:1} in
            n|N )
                echo "[+] Ok. Skipping PostgreSQL configuration."
            ;;
            * )
                echo "[+] Creating database TorSpider-Frontend."
                sudo -u postgres createdb TorSpider-Frontend
                echo "[+] Creating postgres user $postgres_user"
                sudo -u postgres createuser $postgres_user
                echo "[+] Changing postgres user password to: $postgres_user_pass"
                sudo -u postgres psql -c "alter user $postgres_user with encrypted password '$postgres_user_pass';"
                echo "[+] Granting all privileges on db TorSpider-Frontend to postgres user $postgres_user"
                sudo -u postgres psql -c "grant all privileges on database \"TorSpider-Frontend\" to $postgres_user;"
            ;;
        esac

}

get_frontend() { 
    echo "[+] Installing pip requirements"
    pip3 install --upgrade -r $DIR/requirements.txt
}

create_selfsigned() {
    read -p "[?] Would you like to configure a self signed certificate?  If no, you can configure letencrypt later. (Y/n)? " answer
        case ${answer:0:1} in
            n|N )
                echo "[+] Ok. Skipping self signed certificate creation."
            ;;
            * )
                echo "[+] Setting up Nginx with a self-signed certificate."
                mkdir -p /etc/nginx/certs/torspider
                echo "[+] Creating self-signed certificate.  Accept defaults or fill-in as you wish."
                openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 -keyout /etc/nginx/certs/torspider/frontend-key.pem -out /etc/nginx/certs/torspider/frontend.pem
                # Accept Defaults
                echo "[+] Setting permissions on /etc/nginx/certs/torspider/frontend*"
                chmod 440 /etc/nginx/certs/torspider/frontend*
                chown root:$frontend_user /etc/nginx/certs/torspider/frontend*
                read -p "[?] Delete /etc/nginx/sites-available/default? You won't need this unless you have an existing site on this server. (Y/n)? " answer
                    case ${answer:0:1} in
                        n|N )
                            echo "[+] Ok. We will leave it in place.  We will skip the rest of the Nginx configuration."
                            echo "[+] Anything else we do will likely impact an existing site."
                        ;;
                        * )
                            echo "[+] Stopping nginx..."
                            systemctl stop nginx
                            echo "[+] Deleting /etc/nginx/sites-available/default"
                            if [  -f /etc/nginx/sites-available/default ]; then
                                rm /etc/nginx/sites-available/default
                            fi
                            echo "[+] Copying frontend Nginx config files."
                            cp $DIR/nginx_conf/frontend /etc/nginx/sites-available/frontend
                            ln -s /etc/nginx/sites-available/frontend /etc/nginx/sites-enabled/frontend
                            systemctl restart nginx
                        ;;
                    esac
                self_signed=0            
            ;;
        esac
}

install_service() {
    read -p "[?] Register TorSpider-Frontend as a systemd service? (Y/n)? " answer
        case ${answer:0:1} in
            n|N )
                echo "[+] Ok. Skipping self signed certificate creation."
            ;;
            * )
                echo "[+] Registering service."
                sed -i "s#REPLACE_THE_PATH#$DIR#g" $DIR/init/torspider-frontend.service
                sed -i "s#REPLACE_THE_USER#$frontend_user#g" $DIR/init/torspider-frontend.service
                cp $DIR/init/torspider-frontend.service /etc/systemd/system/
                systemctl daemon-reload
                echo "[+] Enabling service."
                systemctl enable torspider-frontend
            ;;
        esac
}

update_hook() {
sed -i "s/REPLACE_THE_USER/$frontend_user/g" $DIR/letsencrypt/deployhook.sh
}




# Main body

echo '=== TorSpider Frontend Installer ==='
echo 'This installed will walk you through the installation process.'
# check if root
check_root
# Check if we are installing on the same server
check_same_server
# Verify the user info
check_user
# Install apt-packages
update_and_install_apt_packages 
# Set up PostgreSQL
setup_postgres
# Clone frontend
get_frontend
# Update letsencrypt hook
update_hook
# Self signed cert
create_selfsigned
# Install service
install_service

echo ""
echo "======== Install completed ========"
if [[ $EUID -ne 0 ]]; then
    echo "[+] You chose to not use a self-signed certificate.  Please read the readme file on how to configure a letsencrypt certificate. "
fi
echo "[+] Postgresql Username: $postgres_user"
echo "[+] Postgresql Password: $postgres_user_pass"
echo "[+] Please follow the steps in the README to finalize the configuration."