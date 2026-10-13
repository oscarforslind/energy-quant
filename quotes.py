"""Quote storage for refined products.

Prices arrive as parallel lists of dates and values, which is fragile: the link
between a date and its price is positional, so a single dropped element silently
misaligns everything after it. This module converts those into a dict keyed by
(product, date), where the two cannot drift apart, and provides the two readers
the rest of the project needs.
"""
def to_quote_dict(dates, prices, product):
    """Build a quote dictionary for a single product.

    dates   -- list of date strings
    prices  -- list of prices, same length as dates
    product -- product name, e.g. 'brent'

    Returns a dict mapping (product, date) tuples to prices.
    Raises ValueError if the two lists differ in length.
    """
    if len(dates) != len(prices):
        raise ValueError(f"got {len(dates)} dates but {len(prices)} prices")

    quotes = {}
    for i in range(len(dates)):
        quotes[(product, dates[i])] = prices[i]
    return quotes


def to_series(quote_dict, product, dates):
    """Returns the prices for one product, in the order given by dates"""
    prices = []
    for d in dates:
        prices.append(quote_dict[(product, d)])
    return prices


def available_dates(quote_dict, product):
    """Returns the set of dates for which the products has a quote"""
    existing = set()
    for p, d in quote_dict:
        if p == product:
            existing.add(d)
    return existing

if __name__ == "__main__":
    dates = ["2026-05-05", "2026-05-06", "2026-05-07"]
    brent = [68.40, 68.95, 69.10]
    rbob = [1.95, 1.97, 1.96]
    q = to_quote_dict(dates, brent, "brent")
    q.update(to_quote_dict(dates, rbob, "rbob"))


    print(len(q))
    print(available_dates(q, "brent"))
    print(to_series(q, "brent", dates))
    print(to_series(q, "brent", ["2026-05-07", "2026-05-05"]))
    print(available_dates(q, "wti"))
