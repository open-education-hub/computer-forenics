#!/bin/sh

# Use tshark to extract the query names
tshark -r dns.pcap -Y "dns.qry.name contains example.com" -T fields -e dns.qry.name > dns_queries.txt

# Use awk/sed to clean up the output and concatenate the encoded parts
cat dns_queries.txt | awk -F'.' '{print $1}' | tr -d '\n' > encoded_string.txt

# Base64-decode the string. You may need to add padding back.
cat encoded_string.txt | base64 -d ; echo

# Clean up.
rm -f dns_queries.txt encoded_string.txt
