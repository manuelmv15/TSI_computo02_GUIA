import simulacion_estadistica as se
import random


def imprimir_titulo(texto):
    print(f"\n{'='*80}\n {texto}\n{'='*80}")

def ejercicio_1():
    imprimir_titulo("Ejercicio 1 - Período de generadores congruenciales")
    
    params = [
        ("1.a", 21, 15, 31, 21),
        ("1.b", 13, 9, 128, 7),
        ("1.c", 17, 0, 31, 23),
        ("1.d", 1, 121, 256, 17)
    ]
    for nombre, a, c, m, x0 in params:
        p = se.calcular_periodo(se.congruencial_lineal, a=a, c=c, m=m, x0=x0)
        print(f"Ejercicio {nombre}: a={a}, c={c}, m={m}, x0={x0} -> Período: {p}")

    # ── Inciso e: generador de segundo orden ──────────────────────────
    print("\nEjercicio 1.e - Generador de Segundo Orden")
    a, b, m, x0, x1 = 21, 15, 64, 21, 43

    vistos = {}
    hist = [x0, x1]

    while True:
        estado = (hist[-2], hist[-1])

        if estado in vistos:
            periodo_e = len(hist) - 2 - vistos[estado]
            break

        vistos[estado] = len(hist) - 2

        siguiente = (a * hist[-1] + b * hist[-2]) % m
        hist.append(siguiente)
        
        if len(hist) > 10_000:
            periodo_e = -1
            break

    print(f"Ejercicio 1.e: a={a}, b={b}, m={m}, x0={x0}, x1={x1} -> Período: {periodo_e}")

    res_1e = se.segundo_orden(a=a, b=b, m=m, x0=x0, x1=x1, n=100)
    print("Secuencia generada (primeros 100):")
    se.imprimir_ri(res_1e["ri"])

def ejercicio_2():
    imprimir_titulo("Ejercicio 2 - Período de más generadores congruenciales")
    params = [
        ("2.a", 137, 47, 17, 17),
        ("2.b", 191, 17, 23, 77),
        ("2.c", 237, 71, 37, 27),
        ("2.d", 117, 31, 19, 23),
        ("2.e", 157, 47, 37, 29),
        ("2.f", 321, 11, 27, 19)
    ]
    for nombre, a, c, m, x0 in params:
        p = se.calcular_periodo(se.congruencial_lineal, a=a, c=c, m=m, x0=x0)
        print(f"Ejercicio {nombre}: a={a}, c={c}, m={m}, x0={x0} -> Período: {p}")

def ejercicio_3():
    imprimir_titulo("Ejercicio 3 - Xj+1 = (553 + 121·Xj) mod 177, X0 = 23")
    a, c, m, x0 = 121, 553, 177, 23
    p = se.calcular_periodo(se.congruencial_lineal, a=a, c=c, m=m, x0=x0)
    print(f"3.a - Período: {p}")
    
    print("\n3.b - Generar 87 números y aplicar Pruebas de Media, Varianza y Uniformidad (k=10, α=0.05)")
    res = se.congruencial_lineal(a=a, c=c, m=m, x0=x0, n=87)
    ri = res["ri"]
    se.imprimir_resultado(se.prueba_media(ri, alpha=0.05), "PRUEBA DE MEDIA")
    se.imprimir_resultado(se.prueba_varianza(ri, alpha=0.05), "PRUEBA DE VARIANZA")
    se.imprimir_resultado(se.prueba_uniformidad_chi2(ri, k=10, alpha=0.05), "PRUEBA DE UNIFORMIDAD")

def ejercicio_4():
    imprimir_titulo("Ejercicio 4 - Uniformidad, Series y Corridas A/B (primeros 100 números)")
    params = [
        ("4.a", 1117, 3057, 1679567, 1457),
        ("4.b", 2177, 2367, 1351867, 1117)
    ]
    for nombre, a, c, m, x0 in params:
        print(f"\n--- Ejercicio {nombre} ---")
        res = se.congruencial_lineal(a=a, c=c, m=m, x0=x0, n=100)
        ri = res["ri"]
        print(f"X100 generado = {res['generados'][-1]}")
        se.imprimir_resultado(se.prueba_uniformidad_chi2(ri, k=10, alpha=0.05), "PRUEBA DE UNIFORMIDAD")
        se.imprimir_resultado(se.prueba_series(ri, k=10, alpha=0.05), "PRUEBA DE SERIES")
        se.imprimir_resultado(se.prueba_corridas_arriba_abajo(ri, alpha=0.05), "PRUEBA DE CORRIDAS (Arriba/Abajo)")

def ejercicio_5():
    imprimir_titulo("Ejercicio 5 - Números 101–200: Media, Varianza y Póker")
    params = [
        ("5.a", 1117, 3057, 1679567, 1617073),
        ("5.b", 2177, 2367, 1351867, 341666)
    ]
    for nombre, a, c, m, x0 in params:
        print(f"\n--- Ejercicio {nombre} ---")
        res = se.congruencial_lineal(a=a, c=c, m=m, x0=x0, n=100)
        ri = res["ri"]
        se.imprimir_resultado(se.prueba_media(ri, alpha=0.05), "PRUEBA DE MEDIA")
        se.imprimir_resultado(se.prueba_varianza(ri, alpha=0.05), "PRUEBA DE VARIANZA")
        se.imprimir_resultado(se.prueba_poker(ri, alpha=0.05), "PRUEBA DE PÓKER")

def ejercicio_6():
    imprimir_titulo("Ejercicio 6 - Cuadrados Medios: semilla 5735, n=50, nivel 90%")
    res = se.cuadrados_medios(x0=5735, n=50, digitos=4)
    ri = res["ri"]
    se.imprimir_resultado(se.prueba_uniformidad_chi2(ri, k=10, alpha=0.10), "PRUEBA DE UNIFORMIDAD")

def ejercicio_7():
    imprimir_titulo("Ejercicio 7 - Pruebas a 50 números manuales (nivel 95%)")
    ri = [0.8797, 0.3884, 0.6289, 0.8750, 0.5999, 0.8589, 0.9996, 0.2415, 0.3808, 0.9606, 0.9848, 0.3469, 0.7977, 0.5844, 0.8147, 0.6431, 0.7387, 0.5613, 0.0318, 0.7401, 0.4557, 0.1592, 0.8536, 0.8846, 0.3410, 0.1492, 0.8681, 0.5291, 0.3188, 0.5992, 0.9170, 0.2204, 0.5991, 0.5461, 0.5739, 0.3254, 0.0856, 0.2258, 0.4603, 0.5027, 0.8376, 0.6235, 0.3681, 0.2088, 0.1525, 0.2006, 0.4720, 0.4272, 0.6360, 0.0954]
    se.imprimir_resultado(se.prueba_media(ri, alpha=0.05), "PRUEBA DE MEDIA")
    se.imprimir_resultado(se.prueba_varianza(ri, alpha=0.05), "PRUEBA DE VARIANZA")
    se.imprimir_resultado(se.prueba_uniformidad_chi2(ri, k=10, alpha=0.05), "PRUEBA DE UNIFORMIDAD")

def ejercicio_8():
    imprimir_titulo("Ejercicio 8 - Xj+1 = (71·Xj) mod 357, X0 = 167")
    a, c, m, x0 = 71, 0, 357, 167
    p = se.calcular_periodo(se.congruencial_lineal, a=a, c=c, m=m, x0=x0)
    print(f"8.a - Período: {p}")
    
    print("\n8.b - Corridas arriba/abajo y corridas de la media (n=100)")
    res = se.congruencial_lineal(a=a, c=c, m=m, x0=x0, n=100)
    ri = res["ri"]
    se.imprimir_resultado(se.prueba_corridas_arriba_abajo(ri, alpha=0.05), "PRUEBA DE CORRIDAS (Arriba/Abajo)")
    se.imprimir_resultado(se.prueba_corridas_media(ri, alpha=0.05), "PRUEBA DE CORRIDAS (Media)")

def ejercicio_9():
    imprimir_titulo("Ejercicio 9 - MINSTD: Xj+1 = (16807·Xj) mod 2147483647, X0 = 1, n=200")
    a, c, m, x0 = 16807, 0, 2147483647, 1
    res = se.congruencial_lineal(a=a, c=c, m=m, x0=x0, n=200)
    ri = res["ri"]
    
    print("\n9.a - Prueba de Media, Varianza y Uniformidad (alpha=0.05)")
    se.imprimir_resultado(se.prueba_media(ri, alpha=0.05), "PRUEBA DE MEDIA")
    se.imprimir_resultado(se.prueba_varianza(ri, alpha=0.05), "PRUEBA DE VARIANZA")
    se.imprimir_resultado(se.prueba_uniformidad_chi2(ri, k=10, alpha=0.05), "PRUEBA DE UNIFORMIDAD")
    
    print("\n9.b - Prueba de Corridas Arriba y Abajo")
    se.imprimir_resultado(se.prueba_corridas_arriba_abajo(ri, alpha=0.05), "PRUEBA DE CORRIDAS (A/B)")
    
    print("\n9.c - Prueba de Corridas Arriba y Abajo de la Media")
    se.imprimir_resultado(se.prueba_corridas_media(ri, alpha=0.05), "PRUEBA DE CORRIDAS (Media)")
    
    print("\n9.d - Prueba de Póker y Series")
    # Para Póker pasamos formato a 5 decimales.
    se.imprimir_resultado(se.prueba_poker(ri, alpha=0.05, decimales=5), "PRUEBA DE PÓKER")
    se.imprimir_resultado(se.prueba_series(ri, k=10, alpha=0.05), "PRUEBA DE SERIES")
    
    print("\n9.e - Prueba de Huecos (intervalo [0.0, 0.5))")
    se.imprimir_resultado(se.prueba_huecos(ri, alpha_val=0.0, beta_val=0.5, alpha=0.05), "PRUEBA DE HUECOS")

def ejercicio_10():
    imprimir_titulo("Ejercicio 10 - Super-Duper: Xj+1 = (69069·Xj) mod 4294967296, X0 = 1, n=200")
    a, c, m, x0 = 69069, 0, 4294967296, 1
    res = se.congruencial_lineal(a=a, c=c, m=m, x0=x0, n=200)
    ri = res["ri"]
    
    print("\n10.a - Prueba de Media, Varianza y Uniformidad (alpha=0.05)")
    se.imprimir_resultado(se.prueba_media(ri, alpha=0.05), "PRUEBA DE MEDIA")
    se.imprimir_resultado(se.prueba_varianza(ri, alpha=0.05), "PRUEBA DE VARIANZA")
    se.imprimir_resultado(se.prueba_uniformidad_chi2(ri, k=10, alpha=0.05), "PRUEBA DE UNIFORMIDAD")
    
    print("\n10.b - Prueba de Corridas Arriba y Abajo")
    se.imprimir_resultado(se.prueba_corridas_arriba_abajo(ri, alpha=0.05), "PRUEBA DE CORRIDAS (A/B)")
    
    print("\n10.c - Prueba de Corridas Arriba y Abajo de la Media")
    se.imprimir_resultado(se.prueba_corridas_media(ri, alpha=0.05), "PRUEBA DE CORRIDAS (Media)")
    
    print("\n10.d - Prueba de Póker y Series")
    se.imprimir_resultado(se.prueba_poker(ri, alpha=0.05, decimales=5), "PRUEBA DE PÓKER")
    se.imprimir_resultado(se.prueba_series(ri, k=10, alpha=0.05), "PRUEBA DE SERIES")
    
    print("\n10.e - Prueba de Huecos (intervalo [0.0, 0.5))")
    se.imprimir_resultado(se.prueba_huecos(ri, alpha_val=0.0, beta_val=0.5, alpha=0.05), "PRUEBA DE HUECOS")

def ejercicio_11():
    imprimir_titulo("Ejercicio 11 - Uniformidad de 100 números (2 dígitos) al 90%")
    ri = [
        0.78, 0.98, 0.24, 0.73, 0.43, 0.16, 0.78, 0.47, 0.18, 0.55,
        0.04, 0.29, 0.68, 0.77, 0.16, 0.03, 0.79, 0.22, 0.37, 0.80,
        0.96, 0.26, 0.91, 0.55, 0.75, 0.55, 0.64, 0.39, 0.53, 0.45,
        0.61, 0.14, 0.38, 0.12, 0.40, 0.74, 0.78, 0.98, 0.27, 0.60,
        0.43, 0.67, 0.62, 0.32, 0.53, 0.54, 0.24, 0.29, 0.18, 0.08,
        0.82, 0.94, 0.19, 0.98, 0.41, 1.00, 0.74, 0.92, 0.14, 0.43,
        0.83, 0.88, 0.18, 0.21, 0.50, 0.13, 0.43, 0.69, 0.08, 0.12,
        0.22, 0.50, 0.16, 0.11, 0.18, 0.89, 0.80, 0.42, 0.29, 0.87,
        0.83, 0.79, 0.65, 0.28, 0.78, 0.49, 0.36, 0.86, 0.87, 0.64,
        0.51, 0.07, 0.18, 0.94, 0.50, 0.22, 0.66, 0.91, 0.48, 0.24
    ]
    # Reemplazar 1.00 por 0.99 para evitar error fuera de rango
    ri = [0.99 if x == 1.0 else x for x in ri]
    se.imprimir_resultado(se.prueba_uniformidad_chi2(ri, k=10, alpha=0.10), "PRUEBA DE UNIFORMIDAD")

def ejercicio_12():
    imprimir_titulo("Ejercicio 12 - Prueba de Póker (95%) a 100 números")
    ri = [
        0.5632, 0.2395, 0.5583, 0.8050, 0.4166, 0.5454, 0.5491, 0.5593, 0.7725, 0.2326,
        0.1020, 0.4708, 0.5690, 0.3802, 0.8224, 0.6866, 0.7098, 0.9352, 0.1388, 0.4535,
        0.0945, 0.1357, 0.9191, 0.1503, 0.1645, 0.9770, 0.1301, 0.1100, 0.2523, 0.4439,
        0.9499, 0.9415, 0.7413, 0.9335, 0.0805, 0.8295, 0.4575, 0.1863, 0.5504, 0.8926,
        0.9035, 0.1133, 0.1115, 0.8761, 0.0007, 0.6222, 0.4605, 0.0688, 0.9164, 0.3482,
        0.9419, 0.3802, 0.8765, 0.5340, 0.6593, 0.8266, 0.5932, 0.4277, 0.9162, 0.7300,
        0.0927, 0.4691, 0.5736, 0.5615, 0.1909, 0.2143, 0.2672, 0.7864, 0.3218, 0.4765,
        0.5581, 0.0888, 0.3969, 0.0151, 0.8605, 0.9615, 0.7752, 0.0461, 0.1122, 0.7559,
        0.4251, 0.7327, 0.8791, 0.4445, 0.8864, 0.6384, 0.6607, 0.2892, 0.8905, 0.5126,
        0.7184, 0.0512, 0.5982, 0.3277, 0.0407, 0.2668, 0.5557, 0.8139, 0.3261, 0.7949,
        0.2236, 0.1455, 0.5083, 0.6106, 0.7605, 0.9788, 0.0204, 0.6006, 0.1452, 0.1234
    ]
    # Formateamos con 5 dígitos para ser compatible con la distribución de la prueba
    se.imprimir_resultado(se.prueba_poker(ri, alpha=0.05, decimales=5), "PRUEBA DE PÓKER (5 DÍGITOS)")

def ejercicio_13():
    imprimir_titulo("Ejercicio 13 - Pruebas de Independencia (90%) con datos del Ej 11")
    ri = [
        0.78, 0.98, 0.24, 0.73, 0.43, 0.16, 0.78, 0.47, 0.18, 0.55,
        0.04, 0.29, 0.68, 0.77, 0.16, 0.03, 0.79, 0.22, 0.37, 0.80,
        0.96, 0.26, 0.91, 0.55, 0.75, 0.55, 0.64, 0.39, 0.53, 0.45,
        0.61, 0.14, 0.38, 0.12, 0.40, 0.74, 0.78, 0.98, 0.27, 0.60,
        0.43, 0.67, 0.62, 0.32, 0.53, 0.54, 0.24, 0.29, 0.18, 0.08,
        0.82, 0.94, 0.19, 0.98, 0.41, 1.00, 0.74, 0.92, 0.14, 0.43,
        0.83, 0.88, 0.18, 0.21, 0.50, 0.13, 0.43, 0.69, 0.08, 0.12,
        0.22, 0.50, 0.16, 0.11, 0.18, 0.89, 0.80, 0.42, 0.29, 0.87,
        0.83, 0.79, 0.65, 0.28, 0.78, 0.49, 0.36, 0.86, 0.87, 0.64,
        0.51, 0.07, 0.18, 0.94, 0.50, 0.22, 0.66, 0.91, 0.48, 0.24
    ]
    ri = [0.99 if x == 1.0 else x for x in ri]
    se.imprimir_resultado(se.prueba_corridas_arriba_abajo(ri, alpha=0.10), "CORRIDAS A/B")
    se.imprimir_resultado(se.prueba_corridas_media(ri, alpha=0.10), "CORRIDAS MEDIA")
    se.imprimir_resultado(se.prueba_series(ri, k=5, alpha=0.10), "PRUEBA SERIES")
    se.imprimir_resultado(se.prueba_huecos(ri, alpha_val=0.0, beta_val=0.5, alpha=0.10), "PRUEBA HUECOS")
    print("Nota: La prueba de Póker no se ejecutó ya que los datos constan de sólo 2 dígitos y la prueba asume 5 dígitos para sus probabilidades.")

def ejercicio_14():
    imprimir_titulo("Ejercicio 14 - Directorio Telefónico (95%)")
    numeros = [
        48372, 1945, 77218, 65039, 28471,
        93056, 11807, 56422, 70193, 44580,
        26714, 80933, 39021, 55678, 10294,
        74831, 66205, 91472, 7318, 52869,
        34017, 88562, 21904, 67158, 49230,
        15083, 76329, 80451, 29766, 93814,
        42109, 67532, 18947, 55028, 72061,
        3485, 99812, 60273, 14795, 86320,
        57146, 28039, 73658, 49127, 61504,
        5273, 84419, 30968, 77701, 22653
    ]
    # Normalizamos los 5 dígitos dividiendo entre 100,000 para que ri en [0,1)
    ri = [x / 100000 for x in numeros]
    
    se.imprimir_resultado(se.prueba_corridas_arriba_abajo(ri, alpha=0.05), "CORRIDAS A/B")
    se.imprimir_resultado(se.prueba_corridas_media(ri, alpha=0.05), "CORRIDAS MEDIA")
    se.imprimir_resultado(se.prueba_poker(ri, alpha=0.05, decimales=5), "PRUEBA DE PÓKER")

def ejercicio_15():
    imprimir_titulo("Ejercicio 15 - Placas de 100 automóviles (95%)")
    print("Nota: Se han generado 100 valores aleatorios ya que el ejercicio exige ir a tomar datos reales al parqueo.")
    numeros = [random.randint(0, 9999) for _ in range(100)]
    ri = [x / 10000 for x in numeros]
    
    se.imprimir_resultado(se.prueba_corridas_arriba_abajo(ri, alpha=0.05), "CORRIDAS A/B")
    se.imprimir_resultado(se.prueba_corridas_media(ri, alpha=0.05), "CORRIDAS MEDIA")
    se.imprimir_resultado(se.prueba_series(ri, k=10, alpha=0.05), "PRUEBA SERIES")

def ejercicio_16():
    imprimir_titulo("Ejercicio 16 - Corridas Arriba y Abajo (90%) - 50 números")
    ri = [
        0.6069, 0.5316, 0.5929, 0.4131, 0.2991, 0.6848, 0.8291, 0.1233, 0.2497, 0.9481,
        0.4411, 0.8195, 0.3521, 0.8068, 0.1062, 0.5384, 0.9287, 0.7954, 0.7271, 0.5739,
        0.4029, 0.2549, 0.1003, 0.5523, 0.1897, 0.8725, 0.4439, 0.6056, 0.8310, 0.4709,
        0.1926, 0.0266, 0.5696, 0.7504, 0.8542, 0.6045, 0.2269, 0.7970, 0.3738, 0.1284,
        0.6367, 0.9543, 0.5385, 0.2574, 0.2396, 0.3468, 0.4105, 0.5143, 0.2014, 0.9900
    ]
    se.imprimir_resultado(se.prueba_corridas_arriba_abajo(ri, alpha=0.10), "CORRIDAS A/B")

def ejercicio_17():
    imprimir_titulo("Ejercicio 17 - Corridas Media (90%) - 50 números")
    ri = [
        0.6351, 0.0272, 0.0227, 0.3827, 0.0659, 0.3683, 0.2270, 0.7323, 0.4088, 0.2139,
        0.4271, 0.4855, 0.2028, 0.1618, 0.5336, 0.7378, 0.3670, 0.6637, 0.1864, 0.6734,
        0.9498, 0.9323, 0.0265, 0.4696, 0.7730, 0.9670, 0.7500, 0.5259, 0.5269, 0.5406,
        0.3641, 0.0356, 0.2181, 0.0866, 0.6085, 0.4468, 0.0539, 0.9311, 0.3128, 0.1562,
        0.8559, 0.7280, 0.7789, 0.1746, 0.6637, 0.0687, 0.5494, 0.1504, 0.8397, 0.2995
    ]
    se.imprimir_resultado(se.prueba_corridas_media(ri, alpha=0.10), "CORRIDAS MEDIA")

def ejercicio_18():
    imprimir_titulo("Ejercicio 18 - Prueba de Series (90%) - 50 números")
    ri = [
        0.5858, 0.8863, 0.8378, 0.3203, 0.4115, 0.2710, 0.9238, 0.1959, 0.9268, 0.6702,
        0.6213, 0.4360, 0.6279, 0.8415, 0.5786, 0.0543, 0.3567, 0.1655, 0.3880, 0.8080,
        0.1931, 0.0843, 0.9152, 0.6093, 0.7587, 0.4515, 0.3203, 0.5139, 0.7070, 0.9123,
        0.1242, 0.8826, 0.9921, 0.8523, 0.6723, 0.8540, 0.4722, 0.4781, 0.2101, 0.1680,
        0.8658, 0.4028, 0.6136, 0.8720, 0.1126, 0.5857, 0.9172, 0.8943, 0.8095, 0.6408
    ]
    se.imprimir_resultado(se.prueba_series(ri, k=5, alpha=0.10), "PRUEBA SERIES")

def ejercicio_19():
    imprimir_titulo("Ejercicio 19 - Generar 200 aleatorios en hoja de cálculo y relación XY")
    print("Nota: Este ejercicio se debe resolver en Excel creando un scatter plot de pares (Ri, Ri+1).")
    print("Sin embargo, aquí podemos simular los 200 datos y comprobar teóricamente que son uniformes.")
    ri = [random.random() for _ in range(200)]
    se.imprimir_resultado(se.prueba_uniformidad_chi2(ri, k=10, alpha=0.05), "PRUEBA DE UNIFORMIDAD (Simulación)")

def ejercicio_20():
    imprimir_titulo("Ejercicio 20 - Media y Varianza de datos del Ej 18")
    ri = [
        0.5858, 0.8863, 0.8378, 0.3203, 0.4115, 0.2710, 0.9238, 0.1959, 0.9268, 0.6702,
        0.6213, 0.4360, 0.6279, 0.8415, 0.5786, 0.0543, 0.3567, 0.1655, 0.3880, 0.8080,
        0.1931, 0.0843, 0.9152, 0.6093, 0.7587, 0.4515, 0.3203, 0.5139, 0.7070, 0.9123,
        0.1242, 0.8826, 0.9921, 0.8523, 0.6723, 0.8540, 0.4722, 0.4781, 0.2101, 0.1680,
        0.8658, 0.4028, 0.6136, 0.8720, 0.1126, 0.5857, 0.9172, 0.8943, 0.8095, 0.6408
    ]
    se.imprimir_resultado(se.prueba_media(ri, alpha=0.05), "PRUEBA DE MEDIA")
    se.imprimir_resultado(se.prueba_varianza(ri, alpha=0.05), "PRUEBA DE VARIANZA")
    print("Respuesta teórica: No son exactamente los mismos que para una distribución uniforme (0.5 y 1/12).")
    print("La diferencia se atribuye a que es una muestra empírica (n=50) y presenta variaciones de muestreo naturales.")


if __name__ == "__main__":
    ejercicio_1()
    ejercicio_2()
    ejercicio_3()
    ejercicio_4()
    ejercicio_5()
    ejercicio_6()
    ejercicio_7()
    ejercicio_8()
    ejercicio_9()
    ejercicio_10()
    ejercicio_11()
    ejercicio_12()
    ejercicio_13()
    ejercicio_14()
    ejercicio_15()
    ejercicio_16()
    ejercicio_17()
    ejercicio_18()
    ejercicio_19()
    ejercicio_20()
