#!/bin/bash

# Prompt user for server details
read -p "Enter the server IP address or hostname (use 127.0.0.1 for local): " SERVER_IP
read -p "Enter the server username: " SERVER_USER
read -s -p "Enter the server password (leave blank if running locally): " SERVER_PASS
echo

# The ssl configuration file for generating certificates.
SSLCONFIG="[ req ]
default_bits       = 2048
distinguished_name = req_distinguished_name
req_extensions     = req_ext
prompt             = no

[ req_distinguished_name ]
CN = $SERVER_IP

[ req_ext ]
subjectAltName = @alt_names

[ alt_names ]
DNS.1 = localhost
IP.1 = 127.0.0.1
IP.2 = $SERVER_IP"

# Variables
PROJECT_NAME="pyosirix_script"
SERVER_PATH="~/certs/$PROJECT_NAME/server"
CLIENT_PATH="$HOME/certs/$PROJECT_NAME/client/$SERVER_IP"

# Flag to track if a new CA is generated
NEW_CA_GENERATED="false"

# Check for Existing CA Certificate and Generate if Needed
echo "Checking for existing CA certificate on the server..."
CA_CHECK_RESULT=$(sshpass -p "$SERVER_PASS" ssh $SERVER_USER@$SERVER_IP "mkdir -p $SERVER_PATH && cd $SERVER_PATH && \
if [ ! -f 'ca.key' ] || [ ! -f 'ca.crt' ]; then \
  echo 'CA not found. Generating new CA...' && \
  openssl genpkey -algorithm RSA -out ca.key && \
  openssl req -new -x509 -key ca.key -out ca.crt -days 365 -subj '/CN=ServerCA' && \
  echo 'NEW_CA'; \
else \
  echo 'CA already exists.'; \
fi")

# Check the result and set the flag
if [[ "$CA_CHECK_RESULT" == *"NEW_CA"* ]]; then
  NEW_CA_GENERATED="true"
fi

# Check for Server Key and Certificate and Generate if Needed
echo "Checking for existing server key and certificate on the server..."
sshpass -p "$SERVER_PASS" ssh $SERVER_USER@$SERVER_IP <<EOF
  cd $SERVER_PATH
  if [ ! -f "server.key" ] || [ ! -f "server.crt" ] || [ "$NEW_CA_GENERATED" == "true" ]; then
    echo "Server key or certificate not found or new CA was generated. Regenerating server key and certificate..."
    echo "$SSLCONFIG" > openssl.cnf
    openssl genpkey -algorithm RSA -out server.key
    openssl req -new -key server.key -out server.csr -config openssl.cnf
    openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 365 -extfile openssl.cnf -extensions req_ext
    rm server.csr
  else
    echo "Server key and certificate already exist and are valid."
  fi
EOF

# Check for Client Key and Certificate and Generate if Needed
if [ ! -f "$CLIENT_PATH/client.key" ] || [ ! -f "$CLIENT_PATH/client.crt" ] || [ "$NEW_CA_GENERATED" == "true" ]; then
  # Create local key and CSR
  echo "Client key or certificate not found or new CA was generated. Generating new client private key and CSR locally..."
  mkdir -p $CLIENT_PATH
  openssl genpkey -algorithm RSA -out $CLIENT_PATH/client.key
  openssl req -new -key $CLIENT_PATH/client.key -out $CLIENT_PATH/client.csr -subj "/CN=client.local"

  # Transfer Client CSR to Server
  echo "Transferring client CSR to the server..."
  sshpass -p "$SERVER_PASS" scp $CLIENT_PATH/client.csr $SERVER_USER@$SERVER_IP:$SERVER_PATH/

  # Sign Client CSR with CA Certificate on the server
  echo "Signing client CSR with CA certificate on the server..."
  sshpass -p "$SERVER_PASS" ssh $SERVER_USER@$SERVER_IP "
    cd $SERVER_PATH && \
    if [ -f 'client.csr' ]; then
      openssl x509 -req -in client.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out client.crt -days 365 && \
      rm client.csr
    else
      echo 'client.csr not found, skipping certificate generation.'
    fi
  "

  # Retrieve the Signed Client Certificate
  echo "Retrieving signed client certificate from the server..."
  sshpass -p "$SERVER_PASS" scp $SERVER_USER@$SERVER_IP:$SERVER_PATH/client.crt $CLIENT_PATH/

  # Retrieve the CA Certificate from the server
  echo "Retrieving CA certificate from the server..."
  sshpass -p "$SERVER_PASS" scp $SERVER_USER@$SERVER_IP:$SERVER_PATH/ca.crt $CLIENT_PATH/

else
  echo "Client key and certificate already exist and are valid."
fi

echo "Certificate setup completed successfully!"
