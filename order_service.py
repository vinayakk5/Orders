import requests
import logging
import concurrent.futures
import config
from proxy_manager import get_random_proxy

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

session = requests.Session()
HEADERS = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "authorization": f"Bearer {config.ACCESS_TOKEN}",
    "content-type": "application/x-www-form-urlencoded",
    "referer": "https://a.xincheng.baby/h5/",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
}

def send_order_request(pay_order_id):
    """Sends a request to process an order."""
    url = f"{config.API_BASE_URL}/payoutuser/order"
    params = {"access_token": config.ACCESS_TOKEN, "pay_order_id": pay_order_id}
    proxy = get_random_proxy()

    try:
        response = session.get(url, headers=HEADERS, params=params, proxies=proxy, verify=False, timeout=5)
        logging.info(f"Order {pay_order_id} response: {response.text}")
    except requests.RequestException as e:
        logging.error(f"Failed to send order {pay_order_id} using proxy {proxy}: {e}")

def get_order_list():
    """Fetches orders and processes them concurrently."""
    url = f"{config.API_BASE_URL}/payoutuser/getOrderList"
    params = {"access_token": config.ACCESS_TOKEN, "page": 1, "limit": 10, "status": 0}
    proxy = get_random_proxy()

    try:
        response = session.get(url, headers=HEADERS, params=params, proxies=proxy, verify=False, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if "data" in data and data["data"]:
                orders = [order["pay_order_id"] for order in data["data"] if float(order.get("total_price", 0)) < config.PRICE_LIMIT]

                with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                    executor.map(send_order_request, orders)
        else:
            logging.error("Failed to get order list: %s", response.text)
    except requests.RequestException as e:
        logging.error(f"Failed to fetch orders using proxy {proxy}: {e}")
