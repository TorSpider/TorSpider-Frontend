#!/bin/sh
echo "Letsencrypt renewal hook running..."
echo "RENEWED_DOMAINS=$RENEWED_DOMAINS"
echo "RENEWED_LINEAGE=$RENEWED_LINEAGE"

cat $RENEWED_LINEAGE/privkey.pem > /etc/nginx/certs/torspider/frontend-key.pem
chown REPLACE_THE_USER: /etc/nginx/certs/torspider/frontend-key.pem
cat $RENEWED_LINEAGE/fullchain.pem > /etc/nginx/certs/torspider/frontend.pem
chown REPLACE_THE_USER: /etc/nginx/certs/torspider/frontend.pem
systemctl restart torspider-frontend
echo "TorSpider frontend key and cert chain updated and restarted"