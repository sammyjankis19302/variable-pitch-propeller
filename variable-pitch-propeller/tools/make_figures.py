"""Draw the figures in figures/ (python3 tools/make_figures.py).

Data: cfd/cfd_runs.csv (the CFD numbers as typed into cfd/Final_graph_code.py) and
bench/measured_thrust.csv (the bench measurements in the report). The bench and mechanism
figures are drawings of what is in the photos, the CAD and the Arduino code; the timeline is
dated from the files themselves (CAD metadata, solver logs, photo stamps, the report).
"""
import csv
import os

import numpy as np
from matplotlib.patches import FancyBboxPatch
from mpl_toolkits.mplot3d.art3d import Line3DCollection
from PIL import Image

from plotstyle import (AQUA, AXIS, BLUE, BLUE_RAMP, GRID, INK, INK2, MUTED, ORANGE, ROOT, SURFACE, YELLOW,
                       plt, save, subtitle)


def read_csv(path):
    with open(os.path.join(ROOT, path)) as f:
        return list(csv.DictReader(line for line in f if not line.startswith('#')))


# ----------------------------------------------------------------------------------------------
def fig_cfd_vs_measured():
    cfd = [r for r in read_csv('cfd/cfd_runs.csv') if r['pitch_deg'] != '21']
    bench = read_csv('bench/measured_thrust.csv')
    a = np.array([float(r['pitch_deg']) for r in cfd])
    t = np.array([float(r['thrust_estimate_N']) for r in cfd])
    ab = np.array([float(r['pitch_deg']) for r in bench])
    tb = np.array([float(r['thrust_N']) for r in bench])

    fig, ax = plt.subplots(figsize=(8.2, 4.4))
    ax.set_axisbelow(True)
    ax.axhline(0, color=AXIS, lw=1.0, zorder=1)
    ax.axhspan(-2.2, 0, color=MUTED, alpha=0.07, lw=0, zorder=0)
    ax.text(30.6, -2.05, 'below zero: six of the sixteen CFD estimates', ha='right', va='bottom', fontsize=7.8,
            color=INK2)
    ax.plot(a, t, color=ORANGE, lw=1.0, alpha=0.55, zorder=2)
    ax.plot(a, t, 'o', color=ORANGE, ms=7, mec=SURFACE, mew=1.6, zorder=3, label='CFD estimate (16 June 2025)')
    ax.plot(ab, tb, color=BLUE, lw=2.0, zorder=4)
    ax.plot(ab, tb, 's', color=BLUE, ms=7.5, mec=SURFACE, mew=1.6, zorder=5, label='measured on the bench')
    for x, y, g in zip(ab, tb, [102, 130, 172, 202]):
        ax.text(x, y + 0.2, f'{g} g', ha='center', va='bottom', fontsize=7.8, color=INK2)
    ax.set_xlim(-1, 31)
    ax.set_ylim(-2.2, 4.0)
    ax.set_xticks(range(0, 31, 2))
    ax.set_xlabel('blade pitch setting [°]')
    ax.set_ylabel('thrust [N]')
    ax.legend(loc='upper left', fontsize=8.4, handlelength=1.4)
    ax.set_title('What the CFD said, and what the bench measured', loc='left', pad=36)
    subtitle(ax, 'Both at 3000 RPM. CFD: thrust worked out from velocities on two surfaces beside the blades '
                 '(the force goal was invalid).\nBench: the load cell in the motor stand (report, Section 2.8). '
                 'The script\'s entry at "21°" (a mistyped re-run of the 20° model) is left out.', y=1.02)
    save(fig, 'cfd-vs-measured.png')


# ----------------------------------------------------------------------------------------------
def fig_bench():
    fig, ax = plt.subplots(figsize=(11.2, 6.6))
    ax.set_xlim(0, 112)
    ax.set_ylim(0, 66)
    ax.axis('off')

    def box(x, y, w, h, title, sub='', col=INK2, fill=SURFACE, lw=1.4, ls='-', fs=9.0):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0,rounding_size=1.1', facecolor=fill,
                                    edgecolor=col, lw=lw, ls=ls))
        n = sub.count('\n') + 1 if sub else 0
        ty = y + h / 2 + 0.95 * n
        ax.text(x + w / 2, ty, title, ha='center', va='center', fontsize=fs, fontweight='bold', color=INK)
        if sub:
            ax.text(x + w / 2, ty - 1.7, sub, ha='center', va='top', fontsize=7.3, color=INK2, linespacing=1.3)

    def wire(pts, col=INK, lw=1.0, arrow=True, ls='-'):
        pts = np.array(pts, float)
        ax.plot(pts[:, 0], pts[:, 1], color=col, lw=lw, ls=ls, solid_capstyle='round')
        if arrow:
            ax.annotate('', xy=pts[-1], xytext=pts[-1] - 0.01 * (pts[-1] - pts[-2]),
                        arrowprops=dict(arrowstyle='-|>', color=col, lw=lw, mutation_scale=9, shrinkA=0, shrinkB=0))

    def label(x, y, text, ha='center', va='bottom', fs=7.2, col=INK2):
        ax.text(x, y, text, ha=ha, va=va, fontsize=fs, color=col, linespacing=1.25)

    # the four Arduinos, one job each
    rows = {'throttle': 47, 'pitch': 33, 'rpm': 19, 'thrust': 5}
    for key, y in rows.items():
        name = {'throttle': 'throttle', 'pitch': 'pitch', 'rpm': 'RPM', 'thrust': 'thrust'}[key]
        box(21, y, 15, 8, 'Arduino Uno', name, col=BLUE)
    box(1, 20, 13, 20, 'Laptop', 'Arduino IDE,\nserial monitors\n(RPM, grams)', col=BLUE)
    for y in rows.values():
        wire([(14, 30), (17.5, 30), (17.5, y + 4), (21, y + 4)], col=BLUE, lw=1.6, arrow=False)
    label(16.2, 41.2, 'USB', fs=7.4)

    # throttle: potentiometer -> Arduino -> ESC -> motor, battery -> ESC
    box(21, 56.2, 15, 3.6, 'potentiometer', fs=7.6, col=MUTED, lw=1.0)
    wire([(28.5, 56.2), (28.5, 55)], col=INK)
    box(43, 47, 13, 8, 'ESC', 'speed controller', col=ORANGE)
    box(43, 56.2, 13, 3.6, '4 × 18650 Li-ion', fs=7.6, col=ORANGE, lw=1.0)
    wire([(49.5, 56.2), (49.5, 55)], col=ORANGE, lw=1.6)
    wire([(36, 51), (43, 51)])
    label(39.5, 51.5, 'pin 9')
    box(63, 47, 15, 8, 'BLDC motor', 'outrunner', col=ORANGE)
    wire([(56, 51), (63, 51)], col=ORANGE, lw=1.6)
    label(59.5, 51.5, '3 phases')

    # pitch: Arduino -> servo -> pinion/rack -> linkage
    box(43, 33, 13, 8, 'MG995 servo', 'set to one angle', col=AQUA)
    wire([(36, 37), (43, 37)])
    label(39.5, 37.5, 'pin 9')
    box(63, 33, 15, 8, 'pinion + rack', 'turning into sliding', col=AQUA)
    wire([(56, 37), (63, 37)], col=AQUA, lw=1.6)

    # rpm: laser across the blades -> receiver -> Arduino
    box(43, 19, 13, 8, 'receiver', 'sees the laser', col=YELLOW)
    box(63, 19, 15, 8, 'laser', 'aimed across\nthe blade path', col=YELLOW)
    wire([(63, 23), (56, 23)], col=YELLOW, lw=1.4, ls=(0, (3, 2)))
    label(59.5, 23.5, 'beam')
    wire([(43, 23), (36, 23)])
    label(39.5, 23.5, 'pin 2')

    # thrust: load cell -> HX711 -> Arduino -> LCD
    box(43, 5, 13, 8, 'HX711', '24-bit ADC', col=INK2)
    box(63, 5, 15, 8, 'load cell', '5 kg, in the\nmotor stand', col=INK2)
    wire([(63, 9), (56, 9)])
    wire([(43, 9), (36, 9)])
    label(39.5, 9.5, 'pins 4, 5')
    box(21, 0.3, 15, 3.4, '16 × 2 LCD (I2C)', fs=7.4, col=MUTED, lw=1.0)
    wire([(28.5, 5), (28.5, 3.7)], col=INK)

    # the propeller on its stand
    ax.add_patch(FancyBboxPatch((85, 5), 25, 50, boxstyle='round,pad=0,rounding_size=1.4', facecolor='#f6f1e7',
                                edgecolor=MUTED, lw=1.0, ls=(0, (4, 3))))
    ax.text(97.5, 51.6, 'on the stand', ha='center', fontsize=8.6, color=INK2, fontweight='bold')
    ax.text(97.5, 49.4, 'a wooden post on a board', ha='center', fontsize=7.2, color=INK2)
    box(88, 31, 19, 14, 'hub + 2 blades', 'printed hub, links,\npivoting blade roots', col=INK, fs=9.2)
    wire([(78, 51), (82, 51), (82, 42), (88, 42)], col=ORANGE, lw=1.6)
    label(83.2, 46.5, 'spins', ha='left')
    wire([(78, 37), (88, 37)], col=AQUA, lw=1.6)
    label(83, 37.5, 'turns\nblades', fs=6.9)
    wire([(97.5, 31), (97.5, 25), (78, 25)], col=YELLOW, lw=1.4, ls=(0, (3, 2)), arrow=False)
    label(98.4, 27.6, 'each blade\ncuts the beam', ha='left', fs=6.9)
    wire([(97.5, 13), (97.5, 9), (78, 9)], col=INK2, lw=1.4)
    label(98.4, 13.6, 'thrust pushes\non the stand', ha='left', fs=6.9)
    ax.plot([97.5, 97.5], [31, 13], color=MUTED, lw=3.0, solid_capstyle='butt', alpha=0.5)

    ax.text(0.5, 65.6, 'The thrust bench: four Arduinos, one job each', fontsize=10.5, fontweight='bold',
            color=INK, va='top')
    ax.text(0.5, 63.2, 'Drawn from our photos and the sketches in bench/firmware.', fontsize=8.4, color=INK2,
            va='top')
    save(fig, 'thrust-bench.png')


# ----------------------------------------------------------------------------------------------
def fig_mechanism():
    """The pitch-change linkage of the two-blade hub, from the CAD previews in cad/previews."""
    parts = [('v2-cont.png', 'controller', 'slides along the axis,\nmoved by the rack'),
             ('v2-string.png', 'link', 'one per blade,\npinned at both ends'),
             ('v2-bolt1.png', 'bolt', 'the pins at the\nends of the links'),
             ('v2-coupler.png', 'coupler', 'holds a blade root;\nthe link pulls its arm'),
             ('v2-hub.png', 'hub', 'the couplers turn\nin its two sockets')]
    fig = plt.figure(figsize=(11.0, 3.9))
    n = len(parts)
    for i, (fn, name, note) in enumerate(parts):
        im = np.asarray(Image.open(os.path.join(ROOT, 'cad/previews', fn)).convert('RGB'))
        mask = (im < 245).any(axis=2)
        ys, xs = np.where(mask)
        im = im[max(ys.min() - 8, 0):ys.max() + 8, max(xs.min() - 8, 0):xs.max() + 8].copy()
        im[(im > 245).all(axis=2)] = [252, 252, 251]          # the preview's white background -> SURFACE
        w = 0.8 / n
        ax = fig.add_axes([0.02 + i * (0.96 / n) + 0.006, 0.26, w, 0.52])
        ax.imshow(im)
        ax.axis('off')
        fig.text(0.02 + i * (0.96 / n) + 0.006 + w / 2, 0.2, name, ha='center', va='top', fontsize=9.6,
                 fontweight='bold', color=INK)
        fig.text(0.02 + i * (0.96 / n) + 0.006 + w / 2, 0.135, note, ha='center', va='top', fontsize=7.8,
                 color=INK2, linespacing=1.3)
        if i < n - 1:
            x = 0.02 + (i + 1) * (0.96 / n) - 0.012
            fig.text(x, 0.52, '→', ha='center', va='center', fontsize=17, color=MUTED)
    fig.text(0.02, 0.97, 'How the blades change pitch', fontsize=10.5, fontweight='bold', color=INK, va='top')
    fig.text(0.02, 0.9, 'The two-blade hub (June 2025), as drawn in SolidWorks. The servo moves the rack, the rack '
                        'slides the controller, the links pull the couplers round, and the blades turn with them.',
             fontsize=8.4, color=INK2, va='top')
    save(fig, 'pitch-mechanism.png')


# ----------------------------------------------------------------------------------------------
def fig_printed_parts():
    """The mechanism parts as the printer laid them down, from print/final1.gcode."""
    import re
    x = y = z = e = 0.0
    segs, cur = [], None
    for line in open(os.path.join(ROOT, 'print/final1.gcode'), errors='ignore'):
        if line.startswith(';TYPE:'):
            cur = line[6:].strip()
            continue
        s = line.split(';', 1)[0].strip()
        if not s:
            continue
        if s.startswith('G92'):
            m = re.search(r'E([-\d.]+)', s)
            if m:
                e = float(m.group(1))
            continue
        if s.startswith(('G0', 'G1')):
            d = dict((k, float(v)) for k, v in re.findall(r'([XYZE])([-\d.]+)', s))
            nx, ny, nz = d.get('X', x), d.get('Y', y), d.get('Z', z)
            ne = d.get('E')
            if ne is not None and ne > e + 1e-6 and (nx != x or ny != y) and cur in ('WALL-OUTER', 'WALL-INNER'):
                segs.append(((x, y, z), (nx, ny, nz)))
            if ne is not None:
                e = ne
            x, y, z = nx, ny, nz
    segs = np.array(segs)
    zz = segs[:, 0, 2]
    fig = plt.figure(figsize=(8.6, 4.3))
    ax = fig.add_axes([0.0, -0.1, 1.0, 1.0], projection="3d", computed_zorder=False)
    ax.set_facecolor(SURFACE)
    keep = segs
    cols = np.array([plt.matplotlib.colors.to_rgb(c) for c in BLUE_RAMP[1:]])
    idx = np.clip((keep[:, 0, 2] - zz.min()) / np.ptp(zz) * (len(cols) - 1), 0, len(cols) - 1)
    lo = np.floor(idx).astype(int)
    hi = np.minimum(lo + 1, len(cols) - 1)
    f = (idx - lo)[:, None]
    rgb = cols[lo] * (1 - f) + cols[hi] * f
    ax.add_collection3d(Line3DCollection(keep, colors=rgb, linewidths=0.45, alpha=1.0))
    for i, lab in enumerate('xyz'):
        getattr(ax, f'set_{lab}lim')(segs[:, :, i].min(), segs[:, :, i].max())
    ax.set_box_aspect((np.ptp(segs[:, :, 0]), np.ptp(segs[:, :, 1]), np.ptp(segs[:, :, 2])), zoom=1.1)
    ax.view_init(elev=32, azim=-62)
    ax.set_axis_off()
    fig.text(0.04, 0.95, 'The pitch mechanism, as the printer laid it down', fontsize=10.5, fontweight='bold',
             color=INK, va='top')
    fig.text(0.04, 0.885, 'The walls of every layer in print/final1.gcode (Creality Ender-3 Pro, 175 layers of '
                          '0.2 mm, 100 % infill, about 2.5 hours):\nthe hub pieces, the controller, two couplers and four pins. '
                          'Darker is higher.', fontsize=8.4, color=INK2, va='top', linespacing=1.4)
    save(fig, 'printed-parts.png')


# ----------------------------------------------------------------------------------------------
def fig_timeline():
    events = [  # (date label, day, category, text)
        ('May 2025', '24', 'cad', 'First hub mechanism drawn: three blades, a sliding plate and links'),
        ('', '25', 'cad', 'Three-blade assembly; the pitch mate turned through its range'),
        ('', '31', 'cad', '"Phase 2": a two-blade hub, controller, couplers and bolts (to 11 June)'),
        ('June 2025', '15', 'cfd', 'Propeller models and the first blade-angle model, saved at 23:34'),
        ('', '16', 'cfd', 'CFD from 07:09: eight pitch settings, the force goal "Invalid" every time'),
        ('', '16', 'cfd', 'Re-runs with inlet and outlet velocities; the thrust script at 22:08'),
        ('July 2025', '01', 'build', 'Rack and pinions from SP Road, for a servo-driven pitch change'),
        ('', '03', 'course', 'Report dated'),
    ]
    colour = {'cad': BLUE, 'cfd': ORANGE, 'build': AQUA, 'course': MUTED}
    fig, ax = plt.subplots(figsize=(8.6, 4.4))
    ax.axis('off')
    n = len(events)
    ax.set_xlim(0, 10)
    ax.set_ylim(-0.6, n + 0.9)
    ax.plot([2.05, 2.05], [-0.3, n - 0.6], color=AXIS, lw=1.6, zorder=1)
    for i, (month, day, cat, text) in enumerate(events):
        yy = n - 1 - i
        if month:
            ax.text(0.0, yy, month, va='center', fontsize=9.2, fontweight='bold', color=INK)
        ax.text(1.75, yy, day, va='center', ha='right', fontsize=9.0, color=INK2)
        ax.scatter([2.05], [yy], s=46, color=colour[cat], zorder=3, edgecolors=SURFACE, linewidths=1.2)
        ax.text(2.35, yy, text, va='center', fontsize=9.0, color=INK)
    ax.text(0, n + 0.55, 'Six weeks, one propeller', fontsize=10.5, fontweight='bold', color=INK, va='bottom')
    for x, cat, lab in ((0.1, 'cad', 'CAD'), (1.1, 'cfd', 'CFD'), (2.1, 'build', 'parts'), (3.2, 'course', 'course')):
        ax.scatter([x], [n - 0.05], s=36, color=colour[cat], edgecolors=SURFACE, linewidths=1.0)
        ax.text(x + 0.17, n - 0.05, lab, va='center', fontsize=8.4, color=INK2)
    ax.text(4.2, n - 0.05, 'Dated from the files themselves. The printing, the bench and the tests fill the gaps.',
            va='center', fontsize=8.0, color=INK2)
    save(fig, 'timeline.png')


if __name__ == '__main__':
    fig_cfd_vs_measured()
    fig_bench()
    fig_mechanism()
    fig_printed_parts()
    fig_timeline()
