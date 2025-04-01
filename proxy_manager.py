import random
import config

def load_proxies():
    """Load proxies from file."""
    try:
        with open(config.PROXY_FILE, "r") as file:
            return [line.strip() for line in file if line.strip()]
    except Exception as e:
        print(f"Error loading proxies: {e}")
        return []

PROXIES = load_proxies()

def get_random_proxy():
    """Returns a random proxy from the list."""
    if PROXIES:
        proxy = random.choice(PROXIES)
        return {"http": f"http://{proxy}", "https": f"http://{proxy}"}
    return None
