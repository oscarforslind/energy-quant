from math import sqrt 


GALLONS_PER_BARREL = 42


def square_minus_five(x):
    return 3 * x ** 2 - 5 


def bisect(f, a, b, tol=1e-8, max_iter=200):
    """Find a root of f in [a, b] by bisection. 

    f -- a function of one variable
    a,b -- interval endpoints, f(a) and f(b) must have opposite signs.
    tol  -- stop when the interval is narrower than this
    max_iter -- safety limit on the number of halvings

    Returns (root, n_inter)
    Raises ValueError if no sign change is bracketed.
    """ 
    
    if f(a) * f(b) >= 0:
        raise ValueError(f" no sign change, f({a}) = {f(a)}, f({b}) = {f(b)}")
    n = 0
    while b - a > tol and n < max_iter:
        mid = (a + b) / 2 
        if f(a) * f(mid) < 0:
            b = mid
        else:
            a = mid
        n = n + 1
    return (a + b) / 2, n 


def crack_margin(brent, rbob, ulsd, opex=0.0):
    """3:2:1 margin, $/bbl of crude."""
    revenue = (2 * rbob + 1 * ulsd) * GALLONS_PER_BARREL
    return (revenue - 3 * brent) / 3 - opex


def npv(rate, capex, annual_margin, years): 
    """Net present value of a flat annual margin against an upfront capex
    """
    total = -capex
    for t in range(1, years + 1):
        total = total + annual_margin / (1 + rate) ** t
    return total


def breakeven_crude(rbob, ulsd, opex=0.0):
    """Crude price at which the 3:2:1 margin reaches zero."""
    def margin_at(brent):
        return crack_margin(brent, rbob, ulsd, opex)

    root, n = bisect(margin_at, 40.0, 120.0)
    return root 


def irr(capex, annual_margin, years, lo=0.0, hi=0.30):
    """Discount rate at which NPV reaches zero"""
    def npv_at(rate):
        return npv(rate, capex, annual_margin, years)
    root, n = bisect(npv_at, lo, hi)
    return root 
    
   
if __name__ == "__main__": 

    root, n = bisect(square_minus_five, -1.5, -0.4)
    print(root, n)
    print(-sqrt(5 / 3))
    assert abs(root + sqrt(5 / 3)) < 1e-7
    print(breakeven_crude(1.95, 2.25))
    print(breakeven_crude(1.95, 2.25, 4.00))
    
    
    
    print(irr(600, 95, 10))
    print(95e6 / (100_000 * 350)) 
