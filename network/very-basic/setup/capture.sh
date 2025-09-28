#!/bin/sh

USER="galilei"
PASS="epursimove"

# Start capturing traffic with tshark.
sudo tcpdump -i lo tcp port 2021 -w ftp.pcap &
TSHARK_PID=$!

# Wait before login.
sleep 3

# Perform the FTP login in the background.
./ftp.exp

# Wait for login to complete.
sleep 5

# Stop the capture.
sudo kill $TSHARK_PID
