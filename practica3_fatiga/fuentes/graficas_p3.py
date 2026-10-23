"""Gráficas de la práctica 3 con el estilo de hoja de cálculo (sección 6 de la skill)."""
import math
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter, LogLocator, NullFormatter

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Carlito", "Liberation Sans", "DejaVu Sans"],
    "font.size": 9, "axes.labelsize": 10,
    "text.color": "#595959", "axes.labelcolor": "#595959",
    "xtick.color": "#595959", "ytick.color": "#595959",
    "axes.edgecolor": "#D9D9D9", "axes.linewidth": 0.75,
    "axes.spines.top": False, "axes.spines.right": False, "axes.spines.left": False,
    "axes.grid": True, "grid.color": "#D9D9D9", "grid.linewidth": 0.75, "axes.axisbelow": True,
    "xtick.major.size": 0, "ytick.major.size": 0, "xtick.minor.size": 0, "ytick.minor.size": 0,
    "legend.frameon": False,
    "mathtext.fontset": "custom", "mathtext.rm": "Carlito", "mathtext.it": "Carlito:italic",
})
COLORES = ["#4472C4", "#ED7D31", "#A5A5A5", "#FFC000"]
coma = FuncFormatter(lambda v, p: format(v, "g").replace(".", ","))

# Datos (pizarra de la sesión) y resultados del cálculo
cargas = np.array([60, 80, 100, 120])
ciclos = {0.4: np.array([9858, 7533, 5593, 5292]), 0.8: np.array([12612, 6956, 9257, 4328])}
L, d, Sut = 100.5, 8.0, 611.0
I = math.pi * d**4 / 64
sig = cargas * L * (d / 2) / I
Kt = {0.4: 2.15, 0.8: 1.75}; q = {0.4: 0.64, 0.8: 0.72}
Kf = {r: 1 + q[r] * (Kt[r] - 1) for r in Kt}
f = 0.861
Se = 0.5 * Sut * 4.51 * Sut**-0.265 * 1.24 * d**-0.107
A = (f * Sut)**2 / Se
B = -(1/3) * math.log10(f * Sut / Se)

# Figura 1: ciclos hasta la rotura frente a la carga
fig, ax = plt.subplots(figsize=(5, 3))
for i, r in enumerate((0.4, 0.8)):
    ax.plot(cargas, ciclos[r], "o", ms=5, color=COLORES[i], label=f"r = {str(r).replace('.', ',')} mm")
ax.set_xlim(50, 130); ax.set_ylim(0, 14000)
ax.set_xlabel("Carga F (N)"); ax.set_ylabel("Ciclos hasta la rotura N")
ax.xaxis.set_major_formatter(coma); ax.yaxis.set_major_formatter(coma)
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.22), ncol=2)
fig.tight_layout(); fig.savefig("fig_ciclos_carga.png", dpi=300, bbox_inches="tight"); plt.close(fig)

# Figura 2: diagrama S-N con la curva teórica y los puntos del ensayo
def curva(Kfr):
    N = np.logspace(3, 7, 400)
    S = np.where(N <= 1e6, A * N**B, Se) / Kfr
    return N, S

fig, ax = plt.subplots(figsize=(5, 3.2))
for i, r in enumerate((0.4, 0.8)):
    rr = str(r).replace('.', ',')
    N, S = curva(Kf[r])
    ax.plot(N, S, ":", color=COLORES[i], lw=1.5, label=f"Teórica r = {rr} mm")
for i, r in enumerate((0.4, 0.8)):
    rr = str(r).replace('.', ',')
    ax.plot(ciclos[r], sig, "o", ms=5, color=COLORES[i], label=f"Ensayo r = {rr} mm")
ax.set_xscale("log"); ax.set_xlim(1e3, 1e7); ax.set_ylim(0, 400)
ax.xaxis.set_major_locator(LogLocator(base=10, numticks=10))
ax.xaxis.set_minor_formatter(NullFormatter())
ax.xaxis.set_major_formatter(FuncFormatter(lambda v, p: f"$10^{{{int(round(math.log10(v)))}}}$"))
ax.yaxis.set_major_formatter(coma)
ax.set_xlabel("Número de ciclos N"); ax.set_ylabel(r"Tensión $\mathregular{σ_{th}}$ (MPa)")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=2)
fig.tight_layout(); fig.savefig("fig_wohler.png", dpi=300, bbox_inches="tight"); plt.close(fig)
print("Se =", round(Se, 2), "A =", round(A, 2), "B =", round(B, 5), "Kf =", Kf)
print("Curva r=0,4: 1e3 ->", round(A*1e3**B/Kf[0.4], 1), " 1e6 ->", round(Se/Kf[0.4], 1))
print("Curva r=0,8: 1e3 ->", round(A*1e3**B/Kf[0.8], 1), " 1e6 ->", round(Se/Kf[0.8], 1))
