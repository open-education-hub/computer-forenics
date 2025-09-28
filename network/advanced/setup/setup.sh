#!/bin/sh

# Set the SSLKEYLOGFILE environment variable and start tshark.
export SSLKEYLOGFILE=./ssl_keys.log
sudo tshark -i lo -w /tmp/https.pcap -f "port 8443" &
TSHARK_PID=$!

# Start server.
python https_server.py &
SERVER_PID=$!

# Use curl to make an HTTPS request. We'll use a simple POST request.
# The "secret" is in the data payload.
sleep 2
curl -k -X POST -d "secret_code=AlphaBravoCharlie" https://localhost:8443

# Stop the capture.
sleep 2
sudo kill $TSHARK_PID

# Kill the server.
sudo kill $SERVER_PID
