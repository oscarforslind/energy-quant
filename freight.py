"""Freight costs between refined-product hubs, and arbitrage screening.

Freight is held as a symmetric matrix of $/bbl costs, indexed by position in
`hubs`. A route is economic when the price difference between two hubs exceeds
the cost of moving a cargo between them.
"""
hubs = ["Rotterdam", "New York", "Houston", "Singapore"]
freight = [
    [0.00, 2.10, 2.00, 3.40],
    [2.10, 0.00, 3.20, 4.50],
    [2.00, 3.20, 0.00, 4.20],
    [3.40, 4.50, 4.20, 0.00],
]

gasoline = {
    "Rotterdam": 81.90,
    "New York": 85.60,
    "Houston": 81.20,
    "Singapore": 84.00,
}


def reduce_freight(freight):
    """Return the lower half triangle, each hub pair's costs exactly once"""
    lower = []
    for i in range(1, len(freight)):
        row = []
        for j in range(i):
            row.append(freight[i][j])
        lower.append(row)
    return lower


def reduce_freight_comp(freight):
    """Lower half triangle of the freight matrix"""
    return [freight[i][:i] for i in range(1, len(freight))]


def screen_arbs(hubs, freight, prices):
    """Freight adjusted margin for every ordered hub pair.

    Returns a list of (margin, origin, destination) tuples, best first."""
    results = []
    for i in range(len(hubs)):
        for j in range(len(hubs)):
            if i == j:
                continue
            margin = prices[hubs[j]] - prices[hubs[i]] - freight[i][j]
            results.append((margin, hubs[i], hubs[j]))
    results.sort(reverse=True)
    return results


if __name__ == "__main__":
    assert reduce_freight(freight) == reduce_freight_comp(freight)

    for margin, origin, dest in screen_arbs(hubs, freight, gasoline):
        print(f"{origin:<12} -> {dest:<12} {margin:+6.2f}")