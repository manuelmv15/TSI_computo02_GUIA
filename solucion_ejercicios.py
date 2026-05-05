import simulacion_estadistica as se

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

if __name__ == "__main__":
    ejercicio_1()
    #ejercicio_2()
    #ejercicio_3()
    #ejercicio_4()
    #ejercicio_5()
    #ejercicio_6()
    #ejercicio_7()
    #ejercicio_8()
