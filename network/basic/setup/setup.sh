#!/bin/sh

# 1. Create a secret file
wget -O secret.jpg https://smarterforensics.com/wp-content/uploads/2016/08/spok.jpg

# 2. Start a simple web server in the current directory
python3 -m http.server 8000 &
SERVER_PID=$!

# 3. Start capturing traffic
sudo tcpdump -i lo tcp port 8000 -w image.pcap &
TSHARK_PID=$!

# 4. Download the file
sleep 2
wget http://localhost:8000/secret.jpg -o /dev/null

# 5. Stop the capture and server
sleep 2
sudo kill $TSHARK_PID
kill $SERVER_PID

rm secret.jpg
