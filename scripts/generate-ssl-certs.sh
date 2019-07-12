#!/bin/bash
openssl rand -base64 48 > tls.passphrase
openssl genrsa -aes128 -passout file:tls.passphrase -out tls.key 2777
openssl req -new -passin file:tls.passphrase -key tls.key -out tls.csr -subj "/C=CA/ST=British Columbia/L=Victoria/O=Government of the Province of British Columbia/OU=GDX/CN=analytics.gov.bc.ca"
cp tls.key tls.key.org
openssl rsa -in tls.key.org -passin file:tls.passphrase -out tls.key
openssl x509 -req -days 36500 -in tls.csr -signkey tls.key -out tls.crt
chmod 600 tls.passphrase tls.key  tls.csr
