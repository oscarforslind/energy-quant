"""module fetching tomorrows energy prices"""


import requests

def fetch_raw(url):
    """ Fetch one URL and return the parsed JSON body
    Raises RuntimeError if the server does not return 200.
    """
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        raise RuntimeError(f"Got status {response.status_code} from {url}")
    return response.json()



if __name__ == "__main__":
    
    url = ("https://api.energidataservice.dk/dataset/DayAheadPrices"
               "?limit=96"
               '&filter={"PriceArea":["DK1"]}'
               "&sort=TimeUTC%20DESC"
        )
    data = fetch_raw(url) 
    print(len(data["records"]))
    print(data["records"][0])
    