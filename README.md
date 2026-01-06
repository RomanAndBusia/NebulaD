# NebulaD

NebulaD is a small Python project made for **educational purposes**.  
It demonstrates how HTTP requests, threading, proxies, and payload files work together in a simple script.

Created as a learning experiment.

---

## About

NebulaD sends repeated HTTP requests using multiple threads.  
It supports:

- GET and POST requests
- Optional proxy usage
- External payload loading for POST
- Basic console output for learning/debugging

The goal is to keep the code simple and readable.

---

## Files

nebulaD.py main script
proxies.txt proxy list (optional)
p.txt POST request payload

---

## Proxies (`proxies.txt`)

Proxies are loaded from `proxies.txt` if the file exists.

**Format (one per line):**
ip:port:username:password

Example:
1.2.3.4:8000:user:pass

On each request, one proxy is randomly selected.  
This shows how authenticated HTTP proxies work in Python.

Proxies used for testing are typically obtained from providers like **webshare.com**.

If `proxies.txt` is empty or missing, the script runs without proxies.

---

## POST Payload (`p.txt`)

Used only when the POST method is selected.

The file content is sent as the request body.

Examples:

Form data:
username=test&password=123

JSON:
{"example":"value"}

This demonstrates how POST request bodies are handled.

---

## Notes

- Thread count controls how many parallel workers run
- Delay controls time between requests per thread
- Output is synchronized to keep logs readable

---

## Author

Made by **RomanAndBusia**
