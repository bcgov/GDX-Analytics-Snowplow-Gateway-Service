#!/bin/bash
openssl rand -base64 48 > server.passphrase
openssl genrsa -aes128 -passout file:server.passphrase -out server.key 2777
openssl req -new -passin file:server.passphrase -key server.key -out server.csr -subj "/C=CA/ST=British Columbia/L=Victoria/O=Government of the Province of British Columbia/OU=GDX/CN=analytics.gov.bc.ca"
cp server.key server.key.org
openssl rsa -in server.key.org -passin file:server.passphrase -out server.key
openssl x509 -req -days 36500 -in server.csr -signkey server.key -out server.crt
chmod 600 server.passphrase server.key  server.csr
