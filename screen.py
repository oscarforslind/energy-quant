"""Morning screen for refined products.
Entry point. Reconciles three price series across mismatched exchange
calendars, computes the 3:2:1 crack and its breakeven crude price, and
screens freight-adjusted gasoline arbs between four hubs

Run with: python screen.py
"""

from quotes import to_quote_dict, to_series, available_dates
from calendar_tools import coverage_report
from freight import hubs, freight, gasoline, screen_arbs
from solvers import crack_margin, breakeven_crude
from plots import plot_series

dates = ["2026-05-01", "2026-05-04", "2026-05-05",
         "2026-05-06", "2026-05-07", "2026-05-08"]

brent_dates = ["2026-05-01", "2026-05-05", "2026-05-06", "2026-05-07", "2026-05-08"]
brent_prices = [67.80, 68.55, 68.20, 68.90, 68.40]

rbob_dates = ["2026-05-01", "2026-05-04", "2026-05-05", "2026-05-07", "2026-05-08"]
rbob_prices = [1.92, 1.94, 1.93, 1.97, 1.95]

ulsd_dates = ["2026-05-01", "2026-05-04", "2026-05-05",
              "2026-05-06", "2026-05-07", "2026-05-08"]
ulsd_prices = [2.21, 2.23, 2.24, 2.22, 2.26, 2.25]

required = set(dates)

quotes = to_quote_dict(brent_dates, brent_prices, "brent")
quotes.update(to_quote_dict(rbob_dates, rbob_prices, "rbob"))
quotes.update(to_quote_dict(ulsd_dates, ulsd_prices, "ulsd"))


series = {
    "brent": available_dates(quotes, "brent"),
    "rbob": available_dates(quotes, "rbob"),
    "ulsd": available_dates(quotes, "ulsd"),
}

usable, missing = coverage_report(required, series)

LABEL = 30
print(f"==== REFINED PRODUCTS SCREEN - {dates[-1]:>8} ===") 
print()
print("DATA QUALITY")
print(f"{"Usable dates":{LABEL}}{len(usable)} of {len(required)}")
for name, dates_missing in missing.items():
    if dates_missing:
        label = name + " missing"
        print(f"{name + " missing":<{LABEL}}{",".join(sorted(dates_missing))}")

window = sorted(usable)

brent_series = to_series(quotes, "brent", window)
rbob_series = to_series(quotes, "rbob", window)
ulsd_series = to_series(quotes, "ulsd", window)

cracks = []
for b, r, u in zip(brent_series, rbob_series, ulsd_series):
    cracks.append(crack_margin(b, r, u))

latest = cracks[-1]
mean = sum(cracks) / len(cracks)
breakeven = breakeven_crude(rbob_series[-1], ulsd_series[-1])
headroom = breakeven - brent_series[-1]

print()
print("3:2:1 CRACK")
print(f"{"Latest":<30}${latest:>8.2f} /bbl")
print(f"{"Mean over the window":<30}${mean:>8.2f} /bbl")
print()
print("BREAKEVEN")
print(f"{"Margin reaches zero at Brent":<30}${breakeven:>8.2f}")
print(f"{"Brent today":<30}${brent_series[-1]:>8.2f}") 
print(f"{"Headroom":<30}${headroom:>8.2f}")

print()
print("GASOLINE ARB SCREEN")

shut = 0
for margin, origin, dest in screen_arbs(hubs, freight, gasoline):
    if margin > 0:
        print(f" {origin:<12} -> {dest:<12} {margin:>6.2f} OPEN")
    else:
        shut = shut + 1
print(f"({shut} routes shut)")

plot_series(window, cracks,"3:2:1 crack spread", "$/bbl", reference=mean)