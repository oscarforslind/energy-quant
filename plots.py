"""Plotting tool"""

import matplotlib.pyplot as plt



def plot_series(dates, values, title, ylabel, label="series", reference=None, outfile=None):
    """Plotting one series against its dates. 
    Shows the figure when outfile is None, otherwise saves it there 
    and closes it so the next plot starts clean.
    """
    plt.plot(dates, values, label=label)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xlabel("Date")
    plt.grid(True, alpha=0.3)
    
    

    if reference is not None:
        plt.axhline(y=reference, linestyle="--", label="mean")
    
    plt.legend()
    if outfile is None:
        plt.show()
    else:
        plt.savefig(outfile)
        plt.close()
