import threading
import time
import urllib.request
import os

def start_self_ping():
    public_url = os.environ.get('PUBLIC_URL')
    if not public_url:
        print("Self-ping warmer: PUBLIC_URL env variable is not set. Self-ping is disabled.")
        return

    def ping_loop():
        # Wait 30 seconds after server start before sending first ping
        time.sleep(30)
        url = public_url.rstrip('/') + '/api/ping/'
        print(f"Self-ping warmer: Initialized targeting {url}")
        
        while True:
            try:
                req = urllib.request.Request(
                    url,
                    headers={'User-Agent': 'SelfPingWarmer/1.0'}
                )
                with urllib.request.urlopen(req, timeout=15) as response:
                    status = response.getcode()
                    print(f"Self-ping warmer: Pinged public URL. Response status: {status}")
            except Exception as e:
                print(f"Self-ping warmer warning: Failed to ping public URL: {e}")
            
            # Sleep 10 minutes (600 seconds)
            time.sleep(600)

    # Start as a background daemon thread
    thread = threading.Thread(target=ping_loop, daemon=True)
    thread.start()
