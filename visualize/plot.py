import matplotlib.pyplot as plt
from utils.logger import logger
import numpy as np
import matplotlib

def plot(t, data, labels, log_scale=False, filename=None):
    fig = plt.figure(facecolor='w')
    ax = fig.add_subplot(111)
    # ax.plot(t, S, 'b', alpha=0.5, lw=2, label='Susceptible')
    for dd, (color, label) in zip(data, labels):
        ax.plot(t, dd, color, alpha=0.5, lw=2, label=label)
    
    ax.set_xlabel('Time /days')
    ax.set_ylabel('Number')
    # ax.xaxis.set_ticks(range(max(t)), minor=True)
    ax.xaxis.set_ticks(range(0, max(t), 7), minor=False)
    ax.xaxis.set_tick_params(length=0)
    if log_scale:
      ax.set_yscale("log")
      locmin = matplotlib.ticker.LogLocator(base=10.0,subs=(0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9),numticks=10)
      ax.yaxis.set_minor_locator(locmin)
      ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    ax.grid(True, which="both")
    legend = ax.legend()
    legend.get_frame().set_alpha(0.5)
    for spine in ('top', 'right', 'bottom', 'left'):
        ax.spines[spine].set_visible(False)
    fig.show()
    if filename:
        plt.savefig(filename)
        logger.info(f"Plot saved to {filename}")
    return fig, ax
