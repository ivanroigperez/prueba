"""Práctica 3 - Ensayo de fatiga. Cálculo de σth (Navier), Kf, Marin, A, B y N teórico.
Se ejecuta con: python3 calculos_p3.py  (cambiar solo el bloque DATOS para repetir)."""
import math
import numpy as np

# ---------------- DATOS ----------------
cargas = [60, 80, 100, 120]                      # N
ciclos = {0.4: [9858, 7533, 5593, 5292],         # pizarra de la sesión (r = 0,4 mm)
          0.8: [12612, 6956, 9257, 4328]}        # (r = 0,8 mm)
L, d, D = 100.5, 8.0, 12.0                       # mm
Sut, Sy = 611.0, 560.0                           # MPa (tabla del guion, AISI 1010)
n_motor = 2800                                   # rpm
Kt = {0.4: 2.15, 0.8: 1.75}                      # gráfica Kt (D/d = 1,5)
q = {0.4: 0.64, 0.8: 0.72}                       # gráfica de sensibilidad a la entalla
f = 0.861                                        # gráfica f(Sut)
# ---------------------------------------

I = math.pi * d**4 / 64                          # mm^4
ymax = d / 2
def sigma_th(F):                                 # MPa = N/mm^2
    return F * L * ymax / I

Se_p = 0.5 * Sut
ka = 4.51 * Sut**-0.265
kb = 1.24 * d**-0.107
kc = kd = 1.0
Se = Se_p * ka * kb * kc * kd
A = (f * Sut)**2 / Se
B = -(1/3) * math.log10(f * Sut / Se)
Kf = {r: 1 + q[r] * (Kt[r] - 1) for r in Kt}

print(f"I = {I:.4f} mm^4   ymax = {ymax} mm")
print(f"D/d = {D/d:.3f}   r/d: 0,4 -> {0.4/d:.3f}  0,8 -> {0.8/d:.3f}")
print(f"Se' = {Se_p:.2f} MPa  ka = {ka:.5f}  kb = {kb:.5f}  Se = {Se:.3f} MPa")
print(f"f·Sut = {f*Sut:.3f} MPa  A = {A:.4f} MPa  B = {B:.6f}  1/B = {1/B:.4f}")
print("Kf:", {r: round(k, 4) for r, k in Kf.items()})
print("Comprobación curva: A·1e3^B =", round(A*1e3**B, 3), " A·1e6^B =", round(A*1e6**B, 3))

filas = []
for r in (0.4, 0.8):
    for F, Nexp in zip(cargas, ciclos[r]):
        s = sigma_th(F)
        sKt = Kt[r] * s
        sKf = Kf[r] * s
        Nteo = (sKf / A)**(1/B)
        t = Nexp / (n_motor / 60)
        filas.append((r, F, Nexp, t, s, sKt, sKf, Nteo, sKf < Se, Nteo / Nexp))
print()
print(f"{'r':>4} {'F':>4} {'Nexp':>6} {'t(s)':>7} {'σth':>8} {'Kt·σ':>8} {'Kf·σ':>8} {'Nteo':>11} {'<Se':>4} {'Nteo/Nexp':>9}")
for r, F, Nexp, t, s, sKt, sKf, Nteo, inf, rat in filas:
    print(f"{r:>4} {F:>4} {Nexp:>6} {t:7.1f} {s:8.3f} {sKt:8.2f} {sKf:8.2f} {Nteo:11.4g} {str(inf):>4} {rat:9.3g}")

# Tensión que daría la curva teórica para la vida medida (para la discusión)
print()
for x in filas:
    r, F, Nexp = x[0], x[1], x[2]
    print(f"r={r} F={F}: A·Nexp^B = {A*Nexp**B:.1f} MPa  frente a Kf·σth = {x[6]:.1f} MPa")

# Sensibilidad: N ∝ (Kf·σ)^(1/B)
for e in (0.02, 0.05, 0.10):
    print(f"error {e:.0%} en la tensión -> N x{(1+e)**(1/B):.3f} / x{(1-e)**(1/B):.3f}")
# Kt ±0,05 y q ±0,02 en N
for r in (0.4, 0.8):
    for dKt in (-0.05, 0.05):
        Kf2 = 1 + q[r]*(Kt[r]+dKt-1)
        print(f"r={r} Kt{dKt:+.2f}: N x{(Kf2/Kf[r])**(1/B):.3f}")
    for dq in (-0.02, 0.02):
        Kf2 = 1 + (q[r]+dq)*(Kt[r]-1)
        print(f"r={r} q{dq:+.2f}: N x{(Kf2/Kf[r])**(1/B):.3f}")
# diámetro ±0,05 mm
for dd in (-0.05, 0.05):
    print(f"d {dd:+.2f} mm -> σ x{(d/(d+dd))**3:.4f} -> N x{((d/(d+dd))**3)**(1/B):.3f}")
# Comprobación f con la expresión de Shigley (Se = Se' = 0,5 Sut, Ne = 1e6)
Sut_k = Sut / 6.894757
sF = Sut_k + 50
b = -math.log10(sF / (0.5 * Sut_k)) / math.log10(2e6)
print(f"Sut = {Sut_k:.2f} kpsi  f(Shigley) = {(sF/Sut_k)*(2e3)**b:.4f}")
# q con Neuber (Shigley) y Kt con la expresión de Peterson, para comparar con la lectura
sa = 0.246 - 3.08e-3*Sut_k + 1.51e-5*Sut_k**2 - 2.67e-8*Sut_k**3   # sqrt(in)
sa_mm = sa * math.sqrt(25.4)
for r in (0.4, 0.8):
    print(f"q Neuber r={r}: {1/(1+sa_mm/math.sqrt(r)):.3f}")
t = (D - d) / 2
for r in (0.4, 0.8):
    tr = t / r
    C1 = 1.232 + 0.832*math.sqrt(tr) - 0.008*tr
    C2 = -3.813 + 0.968*math.sqrt(tr) - 0.260*tr
    C3 = 7.423 - 4.868*math.sqrt(tr) + 0.869*tr
    C4 = -3.839 + 3.070*math.sqrt(tr) - 0.600*tr
    x = 2*t/D
    print(f"Kt Peterson r={r}: {C1 + C2*x + C3*x**2 + C4*x**3:.3f}")
