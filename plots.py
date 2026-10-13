"""Plotting tool"""

import matplotlib.pyplot as plt



def plot_series(dates, values, title, ylabel, reference=None, outfile=None):
    """Plotting one series against its dates. 
    Shows the figure when outfile is None, otherwise saves it there 
    and closes it so the next plot starts clean.
    """
    plt.plot(dates, values)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xlabel("Date")
    plt.grid(True, alpha=0.3)
    plt.axhline(y=17.34, linestyle="--", label="mean")

    if outfile is None:
        plt.show()
    else:
        plt.savefig(outfile)
        plt.close()
