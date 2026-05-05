# Guía de Problemas - TDS SEM 7 - 11

## Problemas

1. Determine el ciclo o periodo de vida de los siguientes generadores congruenciales.
    - a) $X_{j+1} = (21x_{j} + 15) \pmod{31}$ con $x_{0} = 21$
    - b) $X_{j+1} = (13x_{j} + 9) \pmod{128}$ con $x_{0} = 7$
    - c) $X_{j+1} = (17x_{j}) \pmod{31}$ con $x_{0} = 23$
    - d) $X_{j+1} = (121 + x_{j}) \pmod{256}$ con $x_{0} = 17$
    - e) $X_{j+1} = (21x_{j} + 15x_{j-1}) \pmod{64}$ con $x_{0} = 21$ y $x_{1} = 43$

2. Determine el ciclo o periodo de vida de los siguientes generadores congruenciales.
    - a) $X_{j+1} = (137 \cdot X_{j} + 47) \pmod{17}$, $x_{0} = 17$
    - b) $X_{j+1} = (191 \cdot X_{j} + 17) \pmod{23}$, $x_{0} = 77$
    - c) $X_{j+1} = (237 \cdot X_{j} + 71) \pmod{37}$, $x_{0} = 27$
    - d) $X_{j+1} = (117 \cdot X_{j} + 31) \pmod{19}$, $x_{0} = 23$
    - e) $X_{j+1} = (157 \cdot X_{j} + 47) \pmod{37}$, $x_{0} = 29$
    - f) $X_{j+1} = (321 \cdot X_{j} + 11) \pmod{27}$, $x_{0} = 19$

3. Programe la serie congruencial $X_{j+1} = (553 + 121X_{j}) \pmod{177}$ con $X_{0} = 23$, y haga lo que se indica:
    - a) Determine el ciclo o periodo de vida.
    - b) Realice las pruebas de media, varianza y uniformidad.

4. Realice las pruebas de uniformidad, series y corridas a los primeros 100 aleatorios de los siguientes generadores:
    - a) $X_{j+1} = (1117 \cdot X_{i} + 3057) \pmod{1679567}$; semilla 1457
    - b) $X_{j+1} = (2177 \cdot X_{j} + 2367) \pmod{1351867}$; semilla 1117

5. Para cada uno de los generadores del problema anterior tome ahora los datos de 101 al 200 y realice las pruebas de media, varianza y póker.

6. Programe la generación automática de números pseudoaleatorios con el método de cuadrados medios. Genere una muestra de 50 números con la semilla 5735, y determine con un nivel de aceptación de 90% si son uniformes entre 0 y 1.

7. Realice las pruebas de media, varianza y uniformidad a los 50 números de la tabla siguiente, con un nivel de aceptación de 95%.


| 0.8797 | 0.3884 | 0.6289 | 0.8750 | 0.5999 | 0.8589 | 0.9996 | 0.2415 | 0.3808 | 0.9606 |
| :----- | :----- | :----- | :----- | :----- | :----- | :----- | :----- | :----- | :----- |
| 0.9848 | 0.3469 | 0.7977 | 0.5844 | 0.8147 | 0.6431 | 0.7387 | 0.5613 | 0.0318 | 0.7401 |
| 0.4557 | 0.1592 | 0.8536 | 0.8846 | 0.3410 | 0.1492 | 0.8681 | 0.5291 | 0.3188 | 0.5992 |
| 0.9170 | 0.2204 | 0.5991 | 0.5461 | 0.5739 | 0.3254 | 0.0856 | 0.2258 | 0.4603 | 0.5027 |
| 0.8376 | 0.6235 | 0.3681 | 0.2088 | 0.1525 | 0.2006 | 0.4720 | 0.4272 | 0.6360 | 0.0954 |

8. Genere la secuencia de aleatorios del generador congruencial $X_{j+1} = (71X_{j}) \pmod{357}$ con $X_{0} = 167$ y efectúe lo que se indica:
    - a) Realice la prueba de corridas arriba y abajo.
    - b) Realice la prueba de corridas arriba y abajo de la media.

9. Obtenga una secuencia de aleatorios de tamaño $n = 200$ con el generador congruencial MINSTD: $X_{j+1} = (16807X_{j}) \pmod{2147483647}$ con $x_{0} = 1$ y efectúe lo que se indica:
    - a) Realice la prueba de media, varianza y uniformidad.
    - b) Realice la prueba de corridas arriba y abajo.
    - c) Realice la prueba de corridas arriba y abajo de la media.
    - d) Realice la prueba de póker y series.
    - e) Realice la prueba de huecos.

10. Obtenga una secuencia de aleatorios con el generador congruencial Super-Duper: $X_{j+1} = (69069X_{j}) \pmod{4294967296}$ con $x_{0} = 1$ y efectúe lo que se indica:
    - a) Realice la prueba de media, varianza y uniformidad.
    - b) Realice la prueba de corridas arriba y abajo.
    - c) Realice la prueba de corridas arriba y abajo de la media.
    - d) Realice la prueba de póker y series.
    - e) Realice la prueba de huecos.

11. Determine si la siguiente lista de 100 números de 2 dígitos tiene una distribución uniforme con un nivel de aceptación de 90%.


| 0.78 | 0.98 | 0.24 | 0.73 | 0.43 | 0.16 | 0.78 | 0.47 | 0.18 | 0.55 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 0.04 | 0.29 | 0.68 | 0.77 | 0.16 | 0.03 | 0.79 | 0.22 | 0.37 | 0.80 |
| 0.96 | 0.26 | 0.91 | 0.55 | 0.75 | 0.55 | 0.64 | 0.39 | 0.53 | 0.45 |
| 0.61 | 0.14 | 0.38 | 0.12 | 0.40 | 0.74 | 0.78 | 0.98 | 0.27 | 0.60 |
| 0.43 | 0.67 | 0.62 | 0.32 | 0.53 | 0.54 | 0.24 | 0.29 | 0.18 | 0.08 |
| 0.82 | 0.94 | 0.19 | 0.98 | 0.41 | 1.00 | 0.74 | 0.92 | 0.14 | 0.43 |
| 0.83 | 0.88 | 0.18 | 0.21 | 0.50 | 0.13 | 0.43 | 0.69 | 0.08 | 0.12 |
| 0.22 | 0.50 | 0.16 | 0.11 | 0.18 | 0.89 | 0.80 | 0.42 | 0.29 | 0.87 |
| 0.83 | 0.79 | 0.65 | 0.28 | 0.78 | 0.49 | 0.36 | 0.86 | 0.87 | 0.64 |
| 0.51 | 0.07 | 0.18 | 0.94 | 0.50 | 0.22 | 0.66 | 0.91 | 0.48 | 0.24 |

12. Utilice la prueba de póker con nivel de aceptación de 95% para comprobar la hipótesis de que los números de la siguiente lista son aleatorios.

| | | | | | | | | | |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 0.5632 | 0.2395 | 0.5583 | 0.8050 | 0.4166 | 0.5454 | 0.5491 | 0.5593 | 0.7725 | 0.2326 |
| 0.1020 | 0.4708 | 0.5690 | 0.3802 | 0.8224 | 0.6866 | 0.7098 | 0.9352 | 0.1388 | 0.4535 |
| 0.0945 | 0.1357 | 0.9191 | 0.1503 | 0.1645 | 0.9770 | 0.1301 | 0.1100 | 0.2523 | 0.4439 |
| 0.9499 | 0.9415 | 0.7413 | 0.9335 | 0.0805 | 0.8295 | 0.4575 | 0.1863 | 0.5504 | 0.8926 |
| 0.9035 | 0.1133 | 0.1115 | 0.8761 | 0.0007 | 0.6222 | 0.4605 | 0.0688 | 0.9164 | 0.3482 |
| 0.9419 | 0.3802 | 0.8765 | 0.5340 | 0.6593 | 0.8266 | 0.5932 | 0.4277 | 0.9162 | 0.7300 |
| 0.0927 | 0.4691 | 0.5736 | 0.5615 | 0.1909 | 0.2143 | 0.2672 | 0.7864 | 0.3218 | 0.4765 |
| 0.5581 | 0.0888 | 0.3969 | 0.0151 | 0.8605 | 0.9615 | 0.7752 | 0.0461 | 0.1122 | 0.7559 |
| 0.4251 | 0.7327 | 0.8791 | 0.4445 | 0.8864 | 0.6384 | 0.6607 | 0.2892 | 0.8905 | 0.5126 |
| 0.7184 | 0.0512 | 0.5982 | 0.3277 | 0.0407 | 0.2668 | 0.5557 | 0.8139 | 0.3261 | 0.7949 |
| 0.2236 | 0.1455 | 0.5083 | 0.6106 | 0.7605 | 0.9788 | 0.0204 | 0.6006 | 0.1452 | 0.1234 |

13. Determine, mediante las pruebas de independencia (corridas arriba y abajo, corridas arriba y debajo de la media, de póker, de series o de huecos) si los 100 números de la tabla anterior (mismos que en el problema 11) son pseudoaleatorios con un nivel de aceptación de 90%.

14. Abra el directorio telefónico en la primera página de la letra D y seleccione los últimos 5 dígitos de los primeros 50 números telefónicos. Determine si esta selección es aleatoria con un nivel de aceptación de 95%; utilice para ello las pruebas de corridas arriba y abajo, arriba y abajo de la media, y póker.

*Datos proporcionados para el problema 14:*


| 48372 | 01945 | 77218 | 65039 | 28471 |
| ----- | ----- | ----- | ----- | ----- |
| 93056 | 11807 | 56422 | 70193 | 44580 |
| 26714 | 80933 | 39021 | 55678 | 10294 |
| 74831 | 66205 | 91472 | 07318 | 52869 |
| 34017 | 88562 | 21904 | 67158 | 49230 |
| 15083 | 76329 | 80451 | 29766 | 93814 |
| 42109 | 67532 | 18947 | 55028 | 72061 |
| 03485 | 99812 | 60273 | 14795 | 86320 |
| 57146 | 28039 | 73658 | 49127 | 61504 |
| 05273 | 84419 | 30968 | 77701 | 22653 |

15. Observe y anote los 4 dígitos de las placas de 100 automóviles que pasen por alguna calle (utilizar los del parqueo de la UES-FMO). Determine si esta selección es aleatoria con un nivel de aceptación de 95%; utilice para ello las pruebas de corridas arriba y abajo, arriba y abajo de la media, y la prueba de series.

16. Determine con la prueba de corridas arriba y abajo si los 50 números de la tabla son independientes con un nivel de aceptación de 90%.


| 0.6069 | 0.5316 | 0.5929 | 0.4131 | 0.2991 | 0.6848 | 0.8291 | 0.1233 | 0.2497 | 0.9481 |
| :----- | :----- | :----- | :----- | :----- | :----- | :----- | :----- | :----- | :----- |
| 0.4411 | 0.8195 | 0.3521 | 0.8068 | 0.1062 | 0.5384 | 0.9287 | 0.7954 | 0.7271 | 0.5739 |
| 0.4029 | 0.2549 | 0.1003 | 0.5523 | 0.1897 | 0.8725 | 0.4439 | 0.6056 | 0.8310 | 0.4709 |
| 0.1926 | 0.0266 | 0.5696 | 0.7504 | 0.8542 | 0.6045 | 0.2269 | 0.7970 | 0.3738 | 0.1284 |
| 0.6367 | 0.9543 | 0.5385 | 0.2574 | 0.2396 | 0.3468 | 0.4105 | 0.5143 | 0.2014 | 0.9900 |

17. Determine, con la prueba de corridas arriba y abajo de la media, si los 50 números de la tabla son independientes con un nivel de aceptación de 90%.


| 0.6351 | 0.0272 | 0.0227 | 0.3827 | 0.0659 | 0.3683 | 0.2270 | 0.7323 | 0.4088 | 0.2139 |
| :----- | :----- | :----- | :----- | :----- | :----- | :----- | :----- | :----- | :----- |
| 0.4271 | 0.4855 | 0.2028 | 0.1618 | 0.5336 | 0.7378 | 0.3670 | 0.6637 | 0.1864 | 0.6734 |
| 0.9498 | 0.9323 | 0.0265 | 0.4696 | 0.7730 | 0.9670 | 0.7500 | 0.5259 | 0.5269 | 0.5406 |
| 0.3641 | 0.0356 | 0.2181 | 0.0866 | 0.6085 | 0.4468 | 0.0539 | 0.9311 | 0.3128 | 0.1562 |
| 0.8559 | 0.7280 | 0.7789 | 0.1746 | 0.6637 | 0.0687 | 0.5494 | 0.1504 | 0.8397 | 0.2995 |

18. Utilice la prueba de series para determinar si los 50 números de la tabla son independientes con un nivel de aceptación de 90%.


| 0.5858 | 0.8863 | 0.8378 | 0.3203 | 0.4115 | 0.2710 | 0.9238 | 0.1959 | 0.9268 | 0.6702 |
| :----- | :----- | :----- | :----- | :----- | :----- | :----- | :----- | :----- | :----- |
| 0.6213 | 0.4360 | 0.6279 | 0.8415 | 0.5786 | 0.0543 | 0.3567 | 0.1655 | 0.3880 | 0.8080 |
| 0.1931 | 0.0843 | 0.9152 | 0.6093 | 0.7587 | 0.4515 | 0.3203 | 0.5139 | 0.7070 | 0.9123 |
| 0.1242 | 0.8826 | 0.9921 | 0.8523 | 0.6723 | 0.8540 | 0.4722 | 0.4781 | 0.2101 | 0.1680 |
| 0.8658 | 0.4028 | 0.6136 | 0.8720 | 0.1126 | 0.5857 | 0.9172 | 0.8943 | 0.8095 | 0.6408 |

19. Genere en una hoja de cálculo 200 números aleatorios en una misma columna, use la función predeterminada ALEATORIO (o RAND). Copie estos valores y ubíquelos en la siguiente columna, pero desfáselos una posición. Copie el último de los valores en el lugar que quedó vacío al principio, y haga una gráfica de relación XY. ¿Se observa que los datos están dispersos de manera uniforme?

20. Obtenga la media y la varianza de los datos del problema 18. ¿Son exactamente los mismos que para una distribución uniforme entre cero y uno? ¿A qué atribuye esta diferencia?
