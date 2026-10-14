"""module fetching tomorrows energy prices"""


import requests

def fetch_raw(url):
    """ Fetch one URL and return the parsed JSON body
    Raises RuntimeError if the server does not return 200.
    """

    try:
        response = requests.get(url, timeout=10)
    except requests.exceptions.RequestException as exc:
        raise RuntimeError(f" Could not reach {url}: {exc}") from exc
    if response.status_code != 200:
        raise RuntimeError(f"Got status {response.status_code} from {url}")
    return response.json()
    
def fetch_power_prices(area, limit=96):
    """ Return day ahead prices for one area
    are --- bidding zone e.g "DK1"
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


if __name__ == "__main__":
    prices = fetch_power_prices("DK1")
    print(len(prices))
    print(prices[3])

   # fetch_power_prices("DK9")

    