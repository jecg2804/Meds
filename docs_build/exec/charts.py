import json, base64, io, os
HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.environ.get('BUILD_DIR', os.path.join(HERE, '..', '..', 'build'))
os.makedirs(BUILD, exist_ok=True)
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

D = json.load(open(os.path.join(HERE, 'curves.json')))
BLUE, ORANGE, AQUA = '#2a78d6', '#eb6834', '#1baf7a'
INK, INK2, GRID = '#0b0b0b', '#52514e', '#e6e5e1'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10, 'axes.edgecolor': GRID, 'axes.labelcolor': INK2,
                     'xtick.color': INK2, 'ytick.color': INK2, 'text.color': INK})

def b64(fig):
    buf = io.BytesIO(); fig.savefig(buf, format='png', dpi=200, bbox_inches='tight', facecolor='white'); plt.close(fig)
    return 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode()

# ---- chart 1: cumulative capital by month, three scenarios
fig, ax = plt.subplots(figsize=(8.6, 3.5))
months = list(range(1, 61))
series = [('Pesimista', D['pes']['cum'], ORANGE), ('Base', D['base']['cum'], BLUE), ('Optimista', D['opt']['cum'], AQUA)]
for name, cum, col in series:
    y = [c / 1000 for c in cum]
    ax.plot(months, y, color=col, lw=2, solid_capstyle='round')
    ax.annotate(f'{name}  B/.{y[-1]:,.0f} mil', xy=(60, y[-1]), xytext=(6, 0), textcoords='offset points', va='center', fontsize=9.5, color=INK)
for m, lab in ((9, 'primera venta\n(caso base, mes 9)'), (27, 'pico de capital\n(mes 27)')):
    ax.axvline(m, color=GRID, lw=1, ls=(0, (3, 3)), zorder=0)
    ax.text(m + 0.6, 585, lab, fontsize=8.5, color=INK2, va='top')
ax.set_xlim(1, 60); ax.set_ylim(0, 620)
ax.set_xlabel('Mes desde la constitución de la S.A.')
ax.set_ylabel('Capital aportado acumulado (B/. mil)')
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f'{v:,.0f}'))
ax.grid(axis='y', color=GRID, lw=0.8); ax.set_axisbelow(True)
for s in ('top', 'right'): ax.spines[s].set_visible(False)
ax.set_xticks([1, 6, 12, 18, 24, 30, 36, 42, 48, 54, 60])
plt.subplots_adjust(right=0.78)
c1 = b64(fig)

# ---- chart 2: probability of losing more than phase 0, by structure
rows = [('Propuesta de Patel tal como está', 77), ('Registros propios + distribuidor establecido', 49),
        ('Por etapas, reestructurada', 38), ('Fábrica paga registros y da 180 días de crédito', 29),
        ('Lo anterior, con un socio operando sin sueldo', 18), ('Fábrica financia y Patel pone 70% del efectivo', 17)]
fig, ax = plt.subplots(figsize=(8.6, 3.0))
labels = [r[0] for r in rows][::-1]; vals = [r[1] for r in rows][::-1]
bars = ax.barh(labels, vals, color=BLUE, height=0.52)
for b, v in zip(bars, vals):
    ax.text(v + 1.2, b.get_y() + b.get_height() / 2, f'{v}%', va='center', fontsize=10, color=INK)
ax.set_xlim(0, 100); ax.set_xlabel('Probabilidad de perder más que la fase 0 (20,000 escenarios)')
ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f'{v:.0f}%'))
ax.grid(axis='x', color=GRID, lw=0.8); ax.set_axisbelow(True)
for s in ('top', 'right'): ax.spines[s].set_visible(False)
ax.tick_params(axis='y', length=0)
c2 = b64(fig)

json.dump({'c1': c1, 'c2': c2}, open(os.path.join(BUILD, 'charts.json'), 'w'))
print('charts ok', len(c1) // 1024, len(c2) // 1024, 'KB')
