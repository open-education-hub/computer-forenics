# Network Forensics Challenges

This document provides a series of practical exercises focused on network traffic analysis for a computer forensics and hacking class. The challenges involve analyzing captured network traffic (`.pcap` files) to extract hidden information.

## Very Basic: Plaintext Credentials (FTP)

**Objective:** Identify user credentials from an unencrypted FTP login session.

### Instructions

You are given a network capture file, `ftp.pcap`. This file contains traffic from a user logging into a service. Your task is to find the username and password they used.

**Hints:**
- The capture contains traffic from an FTP session.
- FTP is an old protocol and does not encrypt all communications by default.
- Use Wireshark's "Follow TCP Stream" feature to easily read the conversation.

### Solution

You can solve this using Wireshark or the command-line tool `tshark`.

**Wireshark Method:**
1. Open `ftp.pcap` in Wireshark.
2. In the display filter bar, type `ftp` and press Enter.
3. Right-click on one of the packets in the list and select `Follow > TCP Stream`.
4. In the window that appears, you will see the entire conversation. Look for the `USER` and `PASS` commands to find the credentials.

**Tshark Method:**

```bash
# Filter for FTP traffic and display the relevant fields
tshark -r exercise1.pcap -Y "ftp.request.command == USER || ftp.request.command == PASS" -T fields -e ftp.request.command -e ftp.request.arg
```
This command will output the username and password directly.

---

## Basic: File Extraction from HTTP

**Objective:** Reconstruct a file that was downloaded over an unencrypted HTTP connection.

### Instructions

A user downloaded an important image, but then accidentally deleted it. Luckily, the network traffic was captured. You are given the `image.pcap` file. Your task is to recover the original image file from the capture.

**Hints:**
- The file was downloaded over HTTP.
- Wireshark has a feature to export objects transferred over HTTP.

### Solution

Wireshark makes this task very simple.

1. Open `image.pcap` in Wireshark.
2. Go to the menu `File > Export Objects > HTTP`.
3. A list of all HTTP objects found in the capture will be displayed. You should see the `secret.jpg` file.
4. Select it and click `Save`. You have now recovered the file.

---

## Intermediate: Data Exfiltration via DNS

**Objective:** Discover and decode a secret message being exfiltrated through DNS queries.

### Instructions

You are given `dns.pcap`. The capture contains a large number of DNS queries to subdomains of `example.com`. The subdomains themselves look like random garbage, but they contain a hidden message. Your task is to extract and decode this message.

**Hints:**
- Look at the content of the DNS queries, specifically the domain names being requested.
- The garbage-looking text might be encoded. Base64 is a common encoding for representing binary data as text.

### 3. Solution

The solution involves extracting the subdomains from the DNS queries, concatenating them, and then Base64-decoding the result.

```bash
# 1. Use tshark to extract the query names
tshark -r dns.pcap -Y "dns.qry.name contains example.com" -T fields -e dns.qry.name > dns_queries.txt

# 2. Use awk/sed to clean up the output and concatenate the encoded parts
cat dns_queries.txt | awk -F'.' '{print $1}' | tr -d '\n' > encoded_string.txt

# 3. Base64-decode the string. You may need to add padding back.
cat encoded_string.txt | bas64 -d
```

---

## Advanced: Decrypting HTTPS Traffic

**Objective:** Decrypt an HTTPS session using a provided key log file and find a secret submitted in a web form.

### Student Instructions

A user submitted a secret code through a secure web form. You are given the network capture, `https.pcap`, and a file named `ssl_keys.log` that was leaked from the user's computer. Your task is to decrypt the traffic and find the secret code.

**Hints:**
- The traffic is encrypted with TLS (HTTPS).
- Wireshark can decrypt TLS traffic if it's provided with the session keys.
- Look in Wireshark's preferences under `Protocols > TLS`.

### 3. Solution

This solution requires configuring Wireshark to use the provided key log file.

1. Open `https.pcap` in Wireshark.
2. You will see that the protocol is `TLS` and the data is encrypted.
3. Go to the menu `Edit > Preferences`.
4. In the Preferences window, expand `Protocols` and scroll down to `TLS`.
5. In the `(Pre)-Master-Secret log filename` field, click `Browse` and select the `ssl_keys.log` file.
6. Click `OK`.
7. Wireshark will immediately re-dissect the packets. The `TLS` traffic will now be replaced by the decrypted protocol, likely `HTTP` or `HTTP/2`.
8. Filter for `http.request.method == "POST"`.
9. Select the packet, and in the packet details pane, expand the `HTML Form URL Encoded` section. You will find the `secret_code` inside.
10. Alternatively, right-click the packet and `Follow > TCP Stream` to see the decrypted HTTP request and the POST data.
