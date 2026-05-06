"""
=============================================================================
HERRAMIENTAS DE SIMULACIÓN DE SISTEMAS
Generadores de Números Pseudoaleatorios y Pruebas Estadísticas
=============================================================================
Dependencias: solo librería estándar de Python (math, itertools, collections).
              Implementa distribuciones Z y Chi² de forma pura en Python.
=============================================================================
Incluye:
  Generadores:
    - Congruencial Lineal (Mixto y Multiplicativo)
    - Generador de Segundo Orden
    - Método de Cuadrados Medios
    - Cálculo de Período

  Pruebas Estadísticas:
    - Prueba de Media (distribución Z)
    - Prueba de Varianza (distribución Chi²)
    - Prueba de Uniformidad (Chi²)
    - Prueba de Series
    - Prueba de Corridas (Arriba/Abajo y Media)
    - Prueba de Póker
=============================================================================
"""

import math
from collections import Counter


# ─────────────────────────────────────────────────────────────
#  SECCIÓN 0: IMPLEMENTACIONES PURAS DE DISTRIBUCIONES
#  (sin scipy, usando aproximaciones numéricas estándar)
# ─────────────────────────────────────────────────────────────

def _norm_ppf(p: float) -> float:
    """
    Aproximación de la función cuantil (inversa CDF) de la Normal estándar.
    Algoritmo de Beasley-Springer-Moro (precisión ~5 decimales).
    """
    if p <= 0 or p >= 1:
        raise ValueError("p debe estar en (0,1)")
    a = [2.50662823884, -18.61500062529, 41.39119773534, -25.44106049637]
    b = [-8.47351093090, 23.08336743743, -21.06224101826, 3.13082909833]
    c = [0.3374754822726147, 0.9761690190917186, 0.1607979714918209,
         0.0276438810333863, 0.0038405729373609, 0.0003951896511349,
         0.0000321767881768, 0.0000002888167364, 0.0000003960315187]
    y = p - 0.5
    if abs(y) < 0.42:
        r = y * y
        x = y * (((a[3] * r + a[2]) * r + a[1]) * r + a[0]) / \
            ((((b[3] * r + b[2]) * r + b[1]) * r + b[0]) * r + 1)
    else:
        r = p if y < 0 else 1 - p
        r = math.log(-math.log(r))
        x = c[0] + r * (c[1] + r * (c[2] + r * (c[3] + r * (c[4] + r * (c[5] +
            r * (c[6] + r * (c[7] + r * c[8])))))))
        if y < 0:
            x = -x
    return x


def _chi2_ppf(p: float, df: int) -> float:
    """
    Aproximación del cuantil p de la distribución Chi² con 'df' grados de libertad.
    Usa la aproximación de Wilson-Hilferty (excelente para df >= 1).
    """
    if df <= 0:
        raise ValueError("df debe ser > 0")
    z = _norm_ppf(p)
    h = 2.0 / (9.0 * df)
    x = df * (1 - h + z * math.sqrt(h)) ** 3
    return max(x, 0.0)


# ─────────────────────────────────────────────────────────────
#  SECCIÓN 1: GENERADORES DE NÚMEROS PSEUDOALEATORIOS
# ─────────────────────────────────────────────────────────────

def congruencial_lineal(a: int, c: int, m: int, x0: int, n: int) -> dict:
    """
    Generador Congruencial Lineal.
    Fórmula: X_{n+1} = (a * X_n + c) mod m

      c != 0  →  Método Mixto
      c == 0  →  Método Multiplicativo

    Args:
        a  : multiplicador
        c  : incremento (0 = multiplicativo)
        m  : módulo
        x0 : semilla inicial
        n  : cantidad de números a generar

    Returns dict con:
        tipo      – 'Mixto' o 'Multiplicativo'
        semillas  – lista de todos los Xi (incluye x0)
        generados – Xi generados (sin x0)
        ri        – valores normalizados Xi/m ∈ [0,1)
    """
    tipo = "Mixto" if c != 0 else "Multiplicativo"
    semillas = [x0]
    for _ in range(n):
        semillas.append((a * semillas[-1] + c) % m)
    generados = semillas[1:]
    ri = [x / m for x in generados]
    return {"tipo": tipo, "semillas": semillas, "generados": generados, "ri": ri}


def segundo_orden(a: int, b: int, m: int, x0: int, x1: int, n: int) -> dict:
    """
    Generador de Segundo Orden.
    Fórmula: X_{j+1} = (a*X_j + b*X_{j-1}) mod m

    Args:
        a, b : coeficientes
        m    : módulo
        x0   : semilla X_{j-1} (valor previo inicial)
        x1   : semilla X_j     (valor de arranque)
        n    : cantidad de números a generar

    Returns dict con historial, generados y ri.
    """
    hist = [x0, x1]
    for _ in range(n):
        hist.append((a * hist[-1] + b * hist[-2]) % m)
    generados = hist[2:]
    ri = [x / m for x in generados]
    return {"historial": hist, "generados": generados, "ri": ri}


def cuadrados_medios(x0: int, n: int, digitos: int = 4) -> dict:
    """
    Método de Cuadrados Medios.
    Eleva al cuadrado la semilla, extrae los dígitos centrales.

    Args:
        x0     : semilla inicial
        n      : cantidad de números a generar
        digitos: número de dígitos de la semilla (default 4)

    Returns dict con semillas, cuadrados y ri.
    """
    semillas = [x0]
    cuadrados = []
    for _ in range(n):
        cuad = semillas[-1] ** 2
        cuadrados.append(cuad)
        cuad_str = str(cuad).zfill(2 * digitos)
        inicio = (len(cuad_str) - digitos) // 2
        semillas.append(int(cuad_str[inicio: inicio + digitos]))
    generados = semillas[1:]
    ri = [x / (10 ** digitos) for x in generados]
    return {"semillas": semillas, "cuadrados": cuadrados, "generados": generados, "ri": ri}


def calcular_periodo(generador_fn, **kwargs) -> int:
    """
    Calcula el período de cualquier generador iterando hasta
    que la semilla actual ya apareció en la secuencia.

    Args:
        generador_fn : función del generador
        **kwargs     : argumentos del generador (sin 'n')
                       Debe incluir x0 (semilla inicial).

    Returns: tamaño del ciclo (período). -1 si superó 10 000 iteraciones.

    Ejemplo:
        calcular_periodo(congruencial_lineal, a=5, c=3, m=16, x0=7)
    """
    x0 = kwargs.get("x0", 0)
    kw = {k: v for k, v in kwargs.items()}
    kw["n"] = 1
    secuencia = []
    x_actual = x0
    for i in range(10_000):
        if i > 0:
            kw["x0"] = x_actual
            x_actual = generador_fn(**kw)["generados"][0]
        if x_actual in secuencia:
            return len(secuencia) - secuencia.index(x_actual)
        secuencia.append(x_actual)
    return -1


# ─────────────────────────────────────────────────────────────
#  SECCIÓN 2: PRUEBAS ESTADÍSTICAS
# ─────────────────────────────────────────────────────────────

def prueba_media(ri: list, alpha: float = 0.05) -> dict:
    """
    Prueba de Media — H0: μ = 0.5

    Estadístico:  Z = (R̄ - 0.5) / sqrt(1 / (12n))
    Rechazo:      |Z| > Z_{α/2}

    Args:
        ri    : lista de Ri ∈ [0,1)
        alpha : nivel de significancia
    """
    n = len(ri)
    media = sum(ri) / n
    z_calc = (media - 0.5) / math.sqrt(1 / (12 * n))
    z_crit = _norm_ppf(1 - alpha / 2)
    acepta = abs(z_calc) <= z_crit
    return {
        "n": n,
        "media_muestral": round(media, 6),
        "Z_calculado": round(z_calc, 6),
        "Z_critico (±)": round(z_crit, 6),
        "alpha": alpha,
        "acepta_H0": acepta,
        "decision": "✅ Se acepta H0 (μ ≈ 0.5)" if acepta else "❌ Se rechaza H0 (μ ≠ 0.5)",
    }


def prueba_varianza(ri: list, alpha: float = 0.05) -> dict:
    """
    Prueba de Varianza — H0: σ² = 1/12

    Estadístico:  χ² = (n-1) * S² / (1/12)
    GL = n - 1
    Rechazo:      χ² < χ²_{α/2} ó χ² > χ²_{1-α/2}

    Args:
        ri    : lista de Ri ∈ [0,1)
        alpha : nivel de significancia
    """
    n = len(ri)
    media = sum(ri) / n
    s2 = sum((x - media) ** 2 for x in ri) / (n - 1)
    chi_calc = (n - 1) * s2 / (1 / 12)
    chi_inf = _chi2_ppf(alpha / 2, df=n - 1)
    chi_sup = _chi2_ppf(1 - alpha / 2, df=n - 1)
    acepta = chi_inf <= chi_calc <= chi_sup
    return {
        "n": n,
        "varianza_muestral": round(s2, 8),
        "varianza_teorica (1/12)": round(1 / 12, 8),
        "chi2_calculado": round(chi_calc, 6),
        "chi2_inferior (L)": round(chi_inf, 6),
        "chi2_superior (U)": round(chi_sup, 6),
        "GL": n - 1,
        "alpha": alpha,
        "acepta_H0": acepta,
        "decision": "✅ Se acepta H0 (σ² ≈ 1/12)" if acepta else "❌ Se rechaza H0 (σ² ≠ 1/12)",
    }


def prueba_uniformidad_chi2(ri: list, k: int = 10, alpha: float = 0.05) -> dict:
    """
    Prueba de Uniformidad — Chi² de Bondad de Ajuste.
    Divide [0,1) en k intervalos iguales.

    Estadístico:  χ² = Σ (Oi - Ei)² / Ei     Ei = n/k
    GL = k - 1
    Rechazo:      χ² > χ²_{α, k-1}

    Args:
        ri    : lista de Ri ∈ [0,1)
        k     : número de intervalos
        alpha : nivel de significancia
    """
    n = len(ri)
    ei = n / k
    obs = [0] * k
    for r in ri:
        obs[min(int(r * k), k - 1)] += 1
    chi_calc = sum((o - ei) ** 2 / ei for o in obs)
    chi_crit = _chi2_ppf(1 - alpha, df=k - 1)
    acepta = chi_calc <= chi_crit
    tabla = [
        {
            "intervalo": f"[{i/k:.2f}, {(i+1)/k:.2f})",
            "Oi": obs[i],
            "Ei": round(ei, 4),
            "(Oi-Ei)²/Ei": round((obs[i] - ei) ** 2 / ei, 6),
        }
        for i in range(k)
    ]
    return {
        "n": n, "k": k,
        "tabla": tabla,
        "chi2_calculado": round(chi_calc, 6),
        "chi2_critico": round(chi_crit, 6),
        "GL": k - 1, "alpha": alpha,
        "acepta_H0": acepta,
        "decision": "✅ Se acepta H0 (distribución uniforme)" if acepta else "❌ Se rechaza H0 (no uniforme)",
    }


def prueba_series(ri: list, k: int = 10, alpha: float = 0.05) -> dict:
    """
    Prueba de Series — Independencia en pares consecutivos.
    Forma pares (Ri, Ri+1) y los clasifica en cuadrícula k×k.

    Estadístico:  χ² = (k² / (n-1)) * Σ n_ij² - (n-1)
    GL = k² - 1
    Rechazo:      χ² > χ²_{α, k²-1}

    Args:
        ri    : lista de Ri ∈ [0,1)
        k     : divisiones por dimensión
        alpha : nivel de significancia
    """
    n = len(ri)
    frec = Counter()
    for i in range(n - 1):
        col = min(int(ri[i] * k), k - 1)
        fila = min(int(ri[i + 1] * k), k - 1)
        frec[(fila, col)] += 1
    m = n - 1
    suma_cuad = sum(v ** 2 for v in frec.values())
    chi_calc = (k ** 2 / m) * suma_cuad - m
    gl = k ** 2 - 1
    chi_crit = _chi2_ppf(1 - alpha, df=gl)
    acepta = chi_calc <= chi_crit
    return {
        "n": n, "k": k, "pares_totales": m,
        "chi2_calculado": round(chi_calc, 6),
        "chi2_critico": round(chi_crit, 6),
        "GL": gl, "alpha": alpha,
        "acepta_H0": acepta,
        "decision": "✅ Se acepta H0 (pares independientes)" if acepta else "❌ Se rechaza H0 (dependencia en series)",
    }


def prueba_corridas_arriba_abajo(ri: list, alpha: float = 0.05) -> dict:
    """
    Prueba de Corridas Arriba y Abajo.
    Asigna '+' si Ri+1 > Ri, '-' si no. Cuenta corridas de signos iguales.

    Para n grande (aprox. normal):
        μ_R  = (2n - 1) / 3
        σ²_R = (16n - 29) / 90
        Z    = (R - μ_R) / sqrt(σ²_R)
    Rechazo: |Z| > Z_{α/2}

    Args:
        ri    : lista de Ri ∈ [0,1)
        alpha : nivel de significancia
    """
    n = len(ri)
    signos = ['+' if ri[i + 1] > ri[i] else '-' for i in range(n - 1)]
    corridas = 1 + sum(1 for i in range(1, len(signos)) if signos[i] != signos[i - 1])
    mu = (2 * n - 1) / 3
    sigma2 = (16 * n - 29) / 90
    z_calc = (corridas - mu) / math.sqrt(sigma2)
    z_crit = _norm_ppf(1 - alpha / 2)
    acepta = abs(z_calc) <= z_crit
    return {
        "n": n,
        "corridas_observadas": corridas,
        "mu_R": round(mu, 4),
        "sigma2_R": round(sigma2, 4),
        "Z_calculado": round(z_calc, 6),
        "Z_critico (±)": round(z_crit, 6),
        "alpha": alpha,
        "acepta_H0": acepta,
        "decision": "✅ Se acepta H0 (corridas aleatorias A/B)" if acepta else "❌ Se rechaza H0 (patrón ascend./descend.)",
    }


def prueba_corridas_media(ri: list, alpha: float = 0.05) -> dict:
    """
    Prueba de Corridas Respecto a la Media.
    Clasifica cada Ri como E (≥ media) o D (< media).
    Cuenta corridas de símbolos iguales.

    n1 = # sobre media, n2 = # bajo media:
        μ_R  = 2*n1*n2 / (n1+n2) + 1
        σ²_R = 2*n1*n2*(2*n1*n2 - n1 - n2) / ((n1+n2)²*(n1+n2-1))
        Z    = (R - μ_R) / sqrt(σ²_R)
    Rechazo: |Z| > Z_{α/2}

    Args:
        ri    : lista de Ri ∈ [0,1)
        alpha : nivel de significancia
    """
    n = len(ri)
    media = sum(ri) / n
    clases = ['E' if x >= media else 'D' for x in ri]
    n1 = clases.count('E')
    n2 = n - n1
    corridas = 1 + sum(1 for i in range(1, n) if clases[i] != clases[i - 1])
    mu = (2 * n1 * n2) / (n1 + n2) + 1
    sigma2 = (2 * n1 * n2 * (2 * n1 * n2 - n1 - n2)) / ((n1 + n2) ** 2 * (n1 + n2 - 1))
    z_calc = (corridas - mu) / math.sqrt(sigma2)
    z_crit = _norm_ppf(1 - alpha / 2)
    acepta = abs(z_calc) <= z_crit
    return {
        "n": n,
        "media_muestral": round(media, 6),
        "n1_sobre_media": n1,
        "n2_bajo_media": n2,
        "corridas_observadas": corridas,
        "mu_R": round(mu, 4),
        "sigma2_R": round(sigma2, 6),
        "Z_calculado": round(z_calc, 6),
        "Z_critico (±)": round(z_crit, 6),
        "alpha": alpha,
        "acepta_H0": acepta,
        "decision": "✅ Se acepta H0 (corridas aleatorias Media)" if acepta else "❌ Se rechaza H0 (tendencia respecto a media)",
    }


def prueba_poker(ri: list, alpha: float = 0.05, decimales: int = 5) -> dict:
    """
    Prueba de Póker (5 dígitos decimales).
    Clasifica los primeros 5 dígitos de cada Ri en categorías de mano:

        TC  : Todos distintos     P = 0.30240
        1P  : Un par              P = 0.50400
        2P  : Dos pares           P = 0.10800
        FH  : Full House          P = 0.07200
        4K  : Cuatro iguales      P = 0.04500
        Q   : Quintilla (5=)      P = 0.00090

    Estadístico: χ² = Σ (Oi - Ei)² / Ei    GL = 5
    Rechazo: χ² > χ²_{α, 5}

    Args:
        ri        : lista de Ri ∈ [0,1)
        alpha     : nivel de significancia
        decimales : dígitos a usar (se recomienda 5)
    """
    # Probabilidades teóricas (normalizadas para que sumen 1)
    probs_raw = {"TC": 0.30240, "1P": 0.50400, "2P": 0.10800,
                 "FH": 0.07200, "4K": 0.04500, "Q": 0.00090}
    total_p = sum(probs_raw.values())
    probs = {k: v / total_p for k, v in probs_raw.items()}

    def _mano(dig: str) -> str:
        c = sorted(Counter(dig).values(), reverse=True)
        if c[0] == 5:             return "Q"
        if c[0] == 4:             return "4K"
        if c[0] == 3 and c[1] == 2: return "FH"
        if c[0] == 2 and c[1] == 2: return "2P"
        if c[0] == 2:             return "1P"
        return "TC"

    n = len(ri)
    obs_cnt = Counter()
    detalles = []
    for r in ri:
        d = f"{r:.{decimales}f}"[2:2 + decimales]
        mano = _mano(d)
        obs_cnt[mano] += 1
        detalles.append({"Ri": round(r, decimales), "dígitos": d, "mano": mano})

    cats = list(probs.keys())
    tabla = []
    chi_calc = 0.0
    for cat in cats:
        oi = obs_cnt.get(cat, 0)
        ei = probs[cat] * n
        chi_calc += (oi - ei) ** 2 / ei if ei > 0 else 0
        tabla.append({
            "Categoría": cat,
            "Oi": oi,
            "Ei": round(ei, 4),
            "P_teórica": round(probs[cat], 6),
            "(Oi-Ei)²/Ei": round((oi - ei) ** 2 / ei if ei > 0 else 0, 6),
        })

    gl = len(cats) - 1
    chi_crit = _chi2_ppf(1 - alpha, df=gl)
    acepta = chi_calc <= chi_crit
    return {
        "n": n, "decimales_usados": decimales,
        "tabla": tabla,
        "chi2_calculado": round(chi_calc, 6),
        "chi2_critico": round(chi_crit, 6),
        "GL": gl, "alpha": alpha,
        "acepta_H0": acepta,
        "decision": "✅ Se acepta H0 (distribución de póker)" if acepta else "❌ Se rechaza H0 (no pasa prueba de póker)",
        "detalle_clasificacion": detalles,
    }


def prueba_huecos(ri: list, alpha_val: float = 0.0, beta_val: float = 0.5, alpha: float = 0.05) -> dict:
    """
    Prueba de Huecos (Gap Test) — H0: Las secuencias de huecos son independientes.
    Busca ocurrencias en el intervalo [alpha_val, beta_val).
    
    Estadístico: Chi² = Σ (Oi - Ei)² / Ei
    
    Args:
        ri        : lista de Ri ∈ [0,1)
        alpha_val : Límite inferior del intervalo a observar
        beta_val  : Límite superior del intervalo a observar
        alpha     : Nivel de significancia
    """
    huecos = []
    hueco_actual = 0
    encontrado = False
    
    for r in ri:
        if alpha_val <= r < beta_val:
            if encontrado:
                huecos.append(hueco_actual)
            encontrado = True
            hueco_actual = 0
        else:
            if encontrado:
                hueco_actual += 1
                
    P = beta_val - alpha_val
    N = len(huecos)
    if N == 0:
        return {"error": "No hay suficientes huecos para la prueba."}
        
    max_h = max(huecos) if huecos else 0
    Oi = [0] * (max_h + 1)
    for h in huecos:
        Oi[h] += 1
        
    Ei = [N * P * ((1 - P) ** i) for i in range(max_h + 1)]
    Ei[-1] += N * ((1 - P) ** (max_h + 1))
    
    min_ei = 3.0
    while len(Ei) > 2 and Ei[-1] < min_ei:
        Ei[-2] += Ei[-1]
        Oi[-2] += Oi[-1]
        Ei.pop()
        Oi.pop()
        
    chi_calc = sum((o - e)**2 / e for o, e in zip(Oi, Ei))
    gl = len(Ei) - 1
    
    if gl <= 0:
        chi_calc = 0.0
        gl = 1
        chi_crit = _chi2_ppf(1 - alpha, df=gl)
        acepta = True
    else:
        chi_crit = _chi2_ppf(1 - alpha, df=gl)
        acepta = chi_calc <= chi_crit

    return {
        "N_huecos": N,
        "intervalo": f"[{alpha_val}, {beta_val})",
        "chi2_calculado": round(chi_calc, 6),
        "chi2_critico": round(chi_crit, 6),
        "GL": gl, "alpha": alpha,
        "acepta_H0": acepta,
        "decision": "✅ Se acepta H0 (huecos aleatorios)" if acepta else "❌ Se rechaza H0 (patrón de huecos)"
    }



# ─────────────────────────────────────────────────────────────
#  SECCIÓN 3: PRESENTACIÓN DE RESULTADOS
# ─────────────────────────────────────────────────────────────

def _sep(titulo: str = "", ancho: int = 65) -> None:
    if titulo:
        print(f"\n{'─' * ancho}")
        print(f"  {titulo}")
        print(f"{'─' * ancho}")
    else:
        print("─" * ancho)


def imprimir_ri(ri: list, titulo: str = "Números generados Ri") -> None:
    """Muestra tabla de Ri generados."""
    _sep(titulo)
    cols = 5
    for i, r in enumerate(ri, 1):
        end = "\n" if i % cols == 0 or i == len(ri) else "   "
        print(f"  R{i:>3} = {r:.8f}", end=end)
    print()


def imprimir_resultado(res: dict, titulo: str = "") -> None:
    """Imprime el resultado de una prueba estadística."""
    if titulo:
        _sep(titulo)
    claves_excluir = {"tabla", "detalle_clasificacion"}
    for k, v in res.items():
        if k in claves_excluir:
            continue
        print(f"  {k:<28} : {v}")
    if "tabla" in res:
        tabla = res["tabla"]
        if not tabla:
            return
        cab = list(tabla[0].keys())
        anchos = {h: max(len(h), max(len(str(f[h])) for f in tabla)) for h in cab}
        print()
        print("  " + "  ".join(h.ljust(anchos[h]) for h in cab))
        print("  " + "  ".join("─" * anchos[h] for h in cab))
        for fila in tabla:
            print("  " + "  ".join(str(fila[h]).ljust(anchos[h]) for h in cab))


# ─────────────────────────────────────────────────────────────
#  SECCIÓN 4: MENÚ INTERACTIVO
# ─────────────────────────────────────────────────────────────

def _pedir_int(prompt: str, default: int = None) -> int:
    """Pide un entero al usuario, con valor por defecto opcional."""
    while True:
        raw = input(prompt).strip()
        if raw == "" and default is not None:
            return default
        try:
            return int(raw)
        except ValueError:
            print("  ⚠  Ingresa un número entero válido.")


def _pedir_float(prompt: str, default: float = None) -> float:
    """Pide un flotante al usuario, con valor por defecto opcional."""
    while True:
        raw = input(prompt).strip()
        if raw == "" and default is not None:
            return default
        try:
            return float(raw)
        except ValueError:
            print("  ⚠  Ingresa un número decimal válido (usa punto: 0.05).")


def _ejecutar_pruebas(ri: list):
    """Sub-menú de pruebas estadísticas sobre una lista de Ri."""
    if len(ri) < 5:
        print("  ⚠  Se necesitan al menos 5 valores para las pruebas.\n")
        return

    alpha = _pedir_float("\n  Nivel de significancia α [0.05]: ", default=0.05)

    print("\n  Pruebas disponibles:")
    print("  [1] Media        [2] Varianza      [3] Uniformidad")
    print("  [4] Series       [5] Corridas A/B  [6] Corridas Media")
    print("  [7] Póker        [8] Huecos        [9] TODAS")
    sel = set(s.strip() for s in input("  Selección (ej: 1,3,7  o  9): ").split(","))

    if "9" in sel or "1" in sel:
        imprimir_resultado(prueba_media(ri, alpha), "PRUEBA DE MEDIA")
    if "9" in sel or "2" in sel:
        imprimir_resultado(prueba_varianza(ri, alpha), "PRUEBA DE VARIANZA")
    if "9" in sel or "3" in sel:
        k = _pedir_int("  k intervalos para uniformidad [10]: ", default=10)
        imprimir_resultado(prueba_uniformidad_chi2(ri, k, alpha), "PRUEBA DE UNIFORMIDAD")
    if "9" in sel or "4" in sel:
        k = _pedir_int("  k divisiones para series [10]: ", default=10)
        imprimir_resultado(prueba_series(ri, k, alpha), "PRUEBA DE SERIES")
    if "9" in sel or "5" in sel:
        imprimir_resultado(prueba_corridas_arriba_abajo(ri, alpha), "PRUEBA DE CORRIDAS (Arriba/Abajo)")
    if "9" in sel or "6" in sel:
        imprimir_resultado(prueba_corridas_media(ri, alpha), "PRUEBA DE CORRIDAS (Media)")
    if "9" in sel or "7" in sel:
        imprimir_resultado(prueba_poker(ri, alpha), "PRUEBA DE PÓKER")
    if "9" in sel or "8" in sel:
        alpha_val = _pedir_float("  Límite inferior de huecos [0.0]: ", default=0.0)
        beta_val = _pedir_float("  Límite superior de huecos [0.5]: ", default=0.5)
        imprimir_resultado(prueba_huecos(ri, alpha_val, beta_val, alpha), "PRUEBA DE HUECOS")


def menu_interactivo():
    """Menú principal de la aplicación."""
    while True:
        print("\n" + "=" * 65)
        print("  SIMULACIÓN DE SISTEMAS — GENERADORES Y PRUEBAS ESTADÍSTICAS")
        print("=" * 65)
        print("  [1] Ingresar lista de Ri manualmente")
        print("  [2] Generar con Congruencial Lineal (Mixto o Multiplicativo)")
        print("  [3] Generar con Cuadrados Medios")
        print("  [4] Generar con Generador de Segundo Orden")
        print("  [5] Calcular período de un generador")
        print("  [0] Salir")
        print("─" * 65)
        op = input("  Opción: ").strip()

        if op == "0":
            print("  ¡Hasta luego!\n")
            break

        elif op == "1":
            print("  Ingrese los Ri separados por comas.")
            print("  Ejemplo: 0.14, 0.87, 0.53, 0.29, ...")
            raw = input("  Ri: ")
            try:
                ri = [float(x.strip()) for x in raw.split(",") if x.strip()]
                if not ri:
                    print("  ⚠  No se ingresaron valores.")
                    continue
                print(f"\n  {len(ri)} valores cargados.")
                imprimir_ri(ri)
                _ejecutar_pruebas(ri)
            except ValueError as e:
                print(f"  ⚠  Error al leer los datos: {e}")

        elif op == "2":
            print("\n  CONGRUENCIAL LINEAL")
            print("  (c=0 → Multiplicativo | c≠0 → Mixto)")
            try:
                a  = _pedir_int("  a (multiplicador)         : ")
                c  = _pedir_int("  c (incremento, 0=multic.) : ")
                m  = _pedir_int("  m (módulo)                : ")
                x0 = _pedir_int("  x0 (semilla inicial)      : ")
                n  = _pedir_int("  n (cantidad a generar)    : ")
                res = congruencial_lineal(a, c, m, x0, n)
                print(f"\n  Tipo     : {res['tipo']}")
                print(f"  Semillas : {res['semillas']}")
                imprimir_ri(res["ri"])
                _ejecutar_pruebas(res["ri"])
            except Exception as e:
                print(f"  ⚠  Error: {e}")

        elif op == "3":
            print("\n  CUADRADOS MEDIOS")
            try:
                x0  = _pedir_int("  x0 (semilla)          : ")
                dig = _pedir_int("  Dígitos de la semilla [4]: ", default=4)
                n   = _pedir_int("  n (cantidad)          : ")
                res = cuadrados_medios(x0, n, dig)
                print(f"\n  Semillas  : {res['semillas']}")
                print(f"  Cuadrados : {res['cuadrados']}")
                imprimir_ri(res["ri"])
                _ejecutar_pruebas(res["ri"])
            except Exception as e:
                print(f"  ⚠  Error: {e}")

        elif op == "4":
            print("\n  GENERADOR DE SEGUNDO ORDEN")
            print("  Fórmula: X(j+1) = (a·Xj + b·X(j-1)) mod m")
            try:
                a  = _pedir_int("  a : ")
                b  = _pedir_int("  b : ")
                m  = _pedir_int("  m : ")
                x0 = _pedir_int("  x0 — semilla X(j-1) : ")
                x1 = _pedir_int("  x1 — semilla X(j)   : ")
                n  = _pedir_int("  n (cantidad)        : ")
                res = segundo_orden(a, b, m, x0, x1, n)
                print(f"\n  Historial : {res['historial']}")
                imprimir_ri(res["ri"])
                _ejecutar_pruebas(res["ri"])
            except Exception as e:
                print(f"  ⚠  Error: {e}")

        elif op == "5":
            print("\n  CÁLCULO DE PERÍODO")
            print("  Generadores: [1] Congruencial  [2] Cuadrados Medios")
            g = input("  Generador: ").strip()
            try:
                if g == "1":
                    a  = _pedir_int("  a : ")
                    c  = _pedir_int("  c : ")
                    m  = _pedir_int("  m : ")
                    x0 = _pedir_int("  x0: ")
                    p  = calcular_periodo(congruencial_lineal, a=a, c=c, m=m, x0=x0)
                elif g == "2":
                    x0  = _pedir_int("  x0    : ")
                    dig = _pedir_int("  dígitos [4]: ", default=4)
                    p   = calcular_periodo(cuadrados_medios, x0=x0, digitos=dig)
                else:
                    print("  ⚠  Opción no válida.")
                    continue
                print(f"\n  ➜ Período encontrado: {p}")
            except Exception as e:
                print(f"  ⚠  Error: {e}")

        else:
            print("  Opción no reconocida. Elige un número del menú.")


# ─────────────────────────────────────────────────────────────
#  PUNTO DE ENTRADA
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    menu_interactivo()
