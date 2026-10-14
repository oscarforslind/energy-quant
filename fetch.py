"""module fetching tomorrows energy prices"""


import requests

import json

def fetch_raw(url):
    """ Fetch one URL and return the parsed JSON body
    Raises RuntimeError if the server does not return 200.
    """

    try:
        response = requests.get(url, timeout=10)
    except requests.exceptions.RequestException as exc:
        raise RuntimeError(f"Could not reach {url}: {exc}") from exc
    if response.status_code != 200:
        raise RuntimeError(f"Got status {response.status_code} from {url}")
    return response.json()
    
def fetch_power_prices(area, limit=96):
    """ Return day ahead prices for one area
    area --- bidding zone e.g "DK1"
    limit --- how many quarter-hourly records to fetch, 96 = one day
    Returns a list of (TimeUTC, DayaheadpriceEUR) tuples, newest first.
    Raises RuntimeError if no records come back
    """
    url = ("https://api.energidataservice.dk/dataset/DayAheadPrices"
               f"?limit={limit}"
               f'&filter={{"PriceArea":["{area}"]}}'
               "&sort=TimeUTC%20DESC"
        )
    data = fetch_raw(url)
    records = data["records"]

    if not records:
        raise RuntimeError(f"No records for area {area}")
    if len(records) != limit:
        print(f"Warning: asked for {limit} records, only got {len(records)}")

    prices = []
    for record in records:
        prices.append((record["TimeUTC"], record["DayAheadPriceEUR"]))
    return prices

def cache_path(area, limit):
    """Return the filename a fetch is cached under."""
    return f"data/{area}_{limit}.json"

def save_cache(data, path):
    """Write the raw API response to disk as JSON"""
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def load_cache(path):
    """Read a previously saved response.
    Raises FileNotFoundError if the file is not there.
    """
    with open(path, "r") as f:
        return json.load(f)
    

def get_prices(area, limit=96, refresh=False):
    """Return prices, fetching from the API if not already cached."""
    path = cache_path(area, limit)
    
    if not refresh:
        try:
            return load_cache(path)
        except FileNotFoundError:
            pass

    prices = fetch_power_prices(area, limit)
    save_cache(prices, path)
    return prices

if __name__ == "__main__":
    prices = get_prices("DK1")
    print(len(prices))
    print(prices[0])
    path = cache_path("DK1", 96)
    

    