"""Shared figure style (same palette and chrome as the other repositories in this portfolio)."""
import os

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # repository root
FIG = os.path.join(ROOT, 'figures')

# categorical slots (fixed order), ink, chrome, status
BLUE, ORANGE, AQUA, YELLOW = '#2a78d6', '#eb6834', '#1baf7a', '#eda100'
INK, INK2, MUTED = '#0b0b0b', '#52514e', '#898781'
GRID, AXIS, SURFACE = '#e1e0d9', '#c3c2b7', '#fcfcfb'
GOOD, WARNING, CRITICAL = '#0ca30c', '#fab219', '#d03b3b'
# one-hue blue ramp for ordered magnitudes (fan duty)
BLUE_RAMP = ['#86b6ef', '#5598e7', '#2a78d6', '#1c5cab', '#104281', '#0d366b']

plt.rcParams.update({
    'font.family': 'DejaVu Sans', 'font.size': 9.5, 'axes.titlesize': 10.5, 'axes.titleweight': 'bold',
    'axes.edgecolor': AXIS, 'axes.labelcolor': INK2, 'axes.linewidth': 0.8, 'xtick.color': INK2,
    'ytick.color': INK2, 'xtick.major.size': 0, 'ytick.major.size': 0, 'axes.grid': True,
    'grid.color': GRID, 'grid.linewidth': 0.6, 'axes.spines.top': False, 'axes.spines.right': False,
    'figure.facecolor': SURFACE, 'axes.facecolor': SURFACE, 'savefig.facecolor': SURFACE,
    'legend.frameon': False, 'text.color': INK, 'axes.titlecolor': INK, 'lines.linewidth': 1.8,
})


def save(fig, name):
    os.makedirs(FIG, exist_ok=True)
    fig.savefig(os.path.join(FIG, name), dpi=170, bbox_inches='tight')
    plt.close(fig)
    print('wrote figures/' + name)


def subtitle(ax, text, y=1.01):
    ax.text(0, y, text, transform=ax.transAxes, color=INK2, fontsize=8.6, va='bottom')
