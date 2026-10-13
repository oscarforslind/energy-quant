# oil-crack-spreads

A refined-products morning screen in pure Python — refinery margins, data
quality, and freight-adjusted arbitrage between trading hubs.

## Preview

```
$ python screen.py

==== REFINED PRODUCTS SCREEN - 2026-05-08 ====

DATA QUALITY
  Usable dates                  4 of 6
  brent missing                 2026-05-04
  rbob missing                  2026-05-06

3:2:1 CRACK
  Latest                        $   17.70 /bbl
  Mean over the window          $   17.34 /bbl

BREAKEVEN
  Margin reaches zero at Brent  $   86.10
  Brent today                   $   68.40
  Headroom                      $   17.70

GASOLINE ARB SCREEN
  Rotterdam    -> New York      +1.60   OPEN
  Houston      -> New York      +1.20   OPEN
  (10 routes shut)
```

## What it answers

Four questions a refined-products desk asks before the market opens:

1. **Can I trust today's data?** Brent settles on ICE, RBOB and ULSD on NYMEX,
   and the two exchanges run different holiday calendars. Pairing the series by
   position silently misaligns everything after the first gap. The screen
   reconciles the calendars first and reports which days were dropped and why.
2. **What is the refining margin?** A 3:2:1 crack — three barrels of crude into
   two of gasoline and one of distillate — with explicit $/gal to $/bbl
   conversion.
3. **At what crude price does the margin disappear?** Solved numerically with a
   hand-written bisection solver.
4. **Where should the barrels go?** Every ordered hub pair screened for a price
   gap wider than the freight between them.

## Modules

| File | Purpose |
|---|---|
| `quotes.py` | Prices keyed by `(product, date)`, so a date cannot drift from its price |
| `calendar_tools.py` | Reconciles series with different date coverage |
| `freight.py` | Freight matrix and the arbitrage screen |
| `solvers.py` | Bisection root finder; breakeven crude price and project IRR |
| `screen.py` | Entry point — runs the above and prints the report |

Standard library only, no dependencies.

## Design notes

**The freight matrix is symmetric; the arbitrage matrix is not.** Rotterdam→New
York and New York→Rotterdam cost the same to ship and earn opposite margins, so
the screen iterates over every ordered pair rather than half of them.

**Missing data stops the calculation.** `to_series` raises on a date with no
quote rather than defaulting to zero — a missing price should halt a P&L, not
quietly understate it. Brent and RBOB settle on different exchange calendars,
so this is the normal case, not the edge case.

**The solver is checked against a known root first.** `bisect` is validated on
`3x² − 5`, whose roots are exact, before being pointed at a breakeven that has
no closed form. It refuses to run when no sign change is bracketed, rather than
returning a plausible wrong number.

## Limitations

Prices are hardcoded for a sample week. The next step is a live price API,
which replaces the literals in `screen.py` without touching the modules.