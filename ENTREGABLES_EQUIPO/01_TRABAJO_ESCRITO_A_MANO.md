# UNIVERSIDAD NACIONAL / FACULTAD DE INGENIERÍA
## ASIGNATURA: INVESTIGACIÓN DE OPERACIONES E INTELIGENCIA ARTIFICIAL
### PROYECTO FINAL - EJERCICIO 4: OPTIMIZACIÓN DE COLAS EN SERVICIO DE MIGRACIÓN AEROPORTUARIA
**Guía de Transcripción a Mano para Entregable Escrito**

---

> **NOTA PARA LOS INTEGRANTES DEL GRUPO:**  
> Este documento contiene el desarrollo analítico, formal y matemático completo del ejercicio. Está formateado de manera clara y secuencial para que puedan transcribirlo a mano directamente en hojas de examen o cuadernillo. Sigan cada paso, copien las fórmulas, los cálculos y la tabla.

---

## 1. TEXTO LITERAL DEL EJERCICIO PROPUESTO

**Contexto Operativo:**  
En la zona de migración de un aeropuerto internacional se registra una tasa de llegada de pasajeros $\lambda = 180 \text{ pasajeros/hora}$ durante horas pico. Cada ventanilla abierta procesa en promedio $\mu = 15 \text{ pasajeros/hora}$. Se debe determinar el número óptimo de ventanillas para cumplir los estándares de servicio al menor costo.

- **Estructura de Costos:**  
  - Costo de operación por ventanilla abierta: $C_s = \$50 \text{ USD/hora}$.  
  - Costo de penalización por espera de pasajeros: $C_w = \$40 \text{ USD/hora por pasajero en cola}$.
- **Restricción de Nivel de Servicio:**  
  El tiempo promedio de espera en cola de un pasajero no debe superar los 6 minutos ($W_q \le 0.1 \text{ horas}$).
- **Escenario Actual (Sin Optimizar):**  
  Apertura fija tradicional de 16 ventanillas fijas durante todo el turno.  
  Costo total del sistema reportado: $\$1,120 \text{ USD/hora}$.

**Preguntas Analíticas a Resolver:**
1. ¿Cuál es el número entero óptimo de ventanillas que minimiza el costo total combinado cumpliendo la restricción de 6 minutos de espera?
2. ¿Qué impacto cuantitativo en tiempo de espera y costo por hora genera la solución optimizada frente a las 16 ventanillas fijas?

---

## 2. DEFINICIÓN DE VARIABLES Y PARÁMETROS

### A. Parámetros de Entrada (Constantes del Sistema)
- $\lambda = 180 \text{ pasajeros/hora}$: Tasa media de llegadas (Proceso de Poisson).
- $\mu = 15 \text{ pasajeros/hora}$: Tasa media de atención de una ventanilla individual (distribución exponencial).
- $C_s = 50 \text{ USD/hora}$: Costo horario de mantener una ventanilla abierta y con oficial activo.
- $C_w = 40 \text{ USD/hora/pasajero}$: Costo horario atribuido a la insatisfacción/penalización por pasajero en cola.
- $W_{q,\text{máx}} = 0.1 \text{ horas} = 6 \text{ minutos}$: Límite superior tolerable de espera en cola.
- $c_{\text{actual}} = 16 \text{ ventanillas}$: Dotación actual fija sin optimización.
- $CT_{\text{actual, rep}} = \$1,120 \text{ USD/hora}$: Costo reportado en campo por el aeropuerto.

### B. Variables del Modelo
- $x \in \mathbb{Z}^+$: Número entero de ventanillas abiertas simultáneamente (variable de decisión).
- $y \in \mathbb{R}^+$: Costo total resultante del sistema por hora ($CT(x)$ en USD/hora).
- $\rho = \frac{\lambda}{x \cdot \mu}$: Factor de utilización de las ventanillas.
- $L_q$: Número medio de pasajeros esperando en cola.
- $W_q$: Tiempo medio de espera en cola de un pasajero (en horas o minutos).
- $P_0$: Probabilidad de que el sistema de migración esté totalmente vacío.
- $P_w$: Probabilidad de que un pasajero que llega deba esperar en fila (Fórmula de Erlang C).

---

## 3. ANÁLISIS DE ESTABILIDAD OPERATIVA (CONDICIÓN ERGÓDICA)

La carga de tráfico ofrecida al sistema ($a$) representa el número mínimo teórico de servidores requeridos para procesar el flujo continuo de pasajeros:

$$a = \frac{\lambda}{\mu} = \frac{180 \text{ pasajeros/hora}}{15 \text{ pasajeros/hora}} = 12 \text{ canales de servicio}$$

Para que un sistema multicanal $M/M/x$ alcance un estado estacionario estable (régimen permanente), la tasa global de servicio ($x \cdot \mu$) debe ser estrictamente mayor que la tasa de llegada ($\lambda$):

$$\rho = \frac{\lambda}{x \cdot \mu} = \frac{12}{x} < 1 \implies x > 12$$

**Conclusión Fundamental de Estabilidad:**
- Si $x \le 12$, la cola crece indefinidamente ($\lim_{t \to \infty} L_q = \infty$, $W_q = \infty$). El aeropuerto colapsa.
- Por tanto, el espacio de soluciones enteras factibles inicia obligatoriamente en:
$$x \ge 13 \quad (x \in \{13, 14, 15, 16, 17, 18, \dots\})$$

---

## 4. FORMULACIÓN ANALÍTICA DE TEORÍA DE COLAS ($M/M/x$)

### 4.1. Probabilidad de Sistema Vacío ($P_0$)
$$P_0 = \left[ \sum_{n=0}^{x-1} \frac{a^n}{n!} + \frac{a^x}{x! \left(1 - \frac{a}{x}\right)} \right]^{-1}$$
Donde $a = 12$.

### 4.2. Probabilidad de Espera en Fila (Fórmula C de Erlang, $P_w$)
$$P_w = \frac{\frac{a^x}{x! \left(1 - \frac{a}{x}\right)}}{\sum_{n=0}^{x-1} \frac{a^n}{n!} + \frac{a^x}{x! \left(1 - \frac{a}{x}\right)}} = \frac{a^x}{x! \left(1 - \frac{a}{x}\right)} \cdot P_0$$

### 4.3. Número Promedio de Pasajeros en Cola ($L_q$)
$$L_q = \frac{P_w \cdot \rho}{1 - \rho} = \frac{P_0 \cdot a^x \cdot \rho}{x! (1 - \rho)^2}$$

### 4.4. Tiempo Promedio de Espera en Cola ($W_q$, Ley de Little)
$$W_q = \frac{L_q}{\lambda} \text{ (horas)} \implies W_q \text{ (minutos)} = W_q \times 60$$

### 4.5. Función de Costo Total Combinado ($y$)
El costo total por hora $y$ es la suma del costo de capacidad instalada más el costo de insatisfacción:
$$y = CT(x) = C_s \cdot x + C_w \cdot L_q(x) = 50 \cdot x + 40 \cdot L_q(x)$$

---

## 5. CÁLCULO PASO A PASO PARA LOS CANDIDATOS CRÍTICOS

### Caso A: $x = 13$ ventanillas
- Utilización: $\rho = \frac{12}{13} \approx 0.9231$ (92.31%)
- Suma de términos finitos: $\sum_{n=0}^{12} \frac{12^n}{n!} \approx 92,725.96$
- Término del denominador para $x=13$: $\frac{12^{13}}{13! \cdot (1 - 12/13)} \approx 221,684.82$
- $P_0 = \frac{1}{92,725.96 + 221,684.82} = \frac{1}{314,410.78} \approx 3.1805 \times 10^{-6}$
- Probabilidad de hacer fila ($P_w$): $P_w = 221,684.82 \times 3.1805 \times 10^{-6} \approx 0.7044$ (70.44%)
- Pasajeros en cola ($L_q$):
  $$L_q = 0.7044 \cdot \frac{0.9231}{1 - 0.9231} = 0.7044 \cdot 12.0039 \approx 8.4527 \text{ pasajeros}$$
- Tiempo de espera ($W_q$):
  $$W_q = \frac{8.4527}{180} = 0.04696 \text{ horas} \times 60 = 2.818 \text{ minutos}$$
- Verificación de restricción: $2.818 \text{ min} \le 6.0 \text{ min}$ $\rightarrow$ **CUMPLE**.
- Costo Total ($y$):
  $$y = (50 \times 13) + (40 \times 8.4527) = 650 + 338.11 = \$988.11 \text{ USD/hora}$$

---

### Caso B: $x = 14$ ventanillas
- Utilización: $\rho = \frac{12}{14} \approx 0.8571$ (85.71%)
- $P_0 \approx 5.3789 \times 10^{-6}$
- $P_w \approx 0.4817$ (48.17%)
- Pasajeros en cola ($L_q$):
  $$L_q = 0.4817 \cdot \frac{0.8571}{1 - 0.8571} \approx 2.8902 \text{ pasajeros}$$
- Tiempo de espera ($W_q$):
  $$W_q = \frac{2.8902}{180} = 0.01606 \text{ horas} \times 60 = 0.963 \text{ minutos (57.8 segundos)}$$
- Verificación: $0.963 \text{ min} \le 6.0 \text{ min}$ $\rightarrow$ **CUMPLE**.
- Costo Total ($y$):
  $$y = (50 \times 14) + (40 \times 2.8902) = 700 + 115.61 = \$815.61 \text{ USD/hora}$$

---

### Caso C: $x = 15$ ventanillas (¡SOLUCIÓN ÓPTIMA!)
- Utilización: $\rho = \frac{12}{15} = 0.8000$ (80.00%)
- $P_0 \approx 5.9221 \times 10^{-6}$
- $P_w \approx 0.3192$ (31.92%)
- Pasajeros en cola ($L_q$):
  $$L_q = 0.3192 \cdot \frac{0.8000}{1 - 0.8000} = 0.3192 \cdot 4 = 1.2768 \text{ pasajeros}$$
- Tiempo de espera ($W_q$):
  $$W_q = \frac{1.2768}{180} = 0.007093 \text{ horas} \times 60 = 0.4256 \text{ minutos (25.5 segundos)}$$
- Verificación: $0.426 \text{ min} \ll 6.0 \text{ min}$ $\rightarrow$ **CUMPLE AMPLIAMENTE**.
- Costo Total ($y$):
  $$y = (50 \times 15) + (40 \times 1.2768) = 750 + 51.07 = \$801.07 \text{ USD/hora}$$

---

### Caso D: $x = 16$ ventanillas (Escenario Actual)
- Utilización: $\rho = \frac{12}{16} = 0.7500$ (75.00%)
- $P_0 \approx 6.0792 \times 10^{-6}$
- $P_w \approx 0.2046$ (20.46%)
- Pasajeros en cola ($L_q$):
  $$L_q = 0.2046 \cdot \frac{0.7500}{1 - 0.7500} = 0.2046 \cdot 3 = 0.6137 \text{ pasajeros}$$
- Tiempo de espera ($W_q$):
  $$W_q = \frac{0.6137}{180} = 0.003409 \text{ horas} \times 60 = 0.2046 \text{ minutos (12.3 segundos)}$$
- Costo Total Teórico ($y_{\text{teórico}}$):
  $$y = (50 \times 16) + (40 \times 0.6137) = 800 + 24.55 = \$824.55 \text{ USD/hora}$$
- Costo Total Reportado por el Aeropuerto:
  $$CT_{\text{reportado}} = \$1,120.00 \text{ USD/hora}$$

---

## 6. TABLA ANALÍTICA COMPARATIVA DE RESULTADOS

| Ventanillas ($x$) | $\rho$ (%) | $P_w$ | $L_q$ (pas) | $W_q$ (min) | Costo Serv. ($C_s \cdot x$) | Costo Espera ($C_w \cdot L_q$) | Costo Total ($y$, USD/h) | ¿$W_q \le 6$ min? | Veredicto |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **12** | 100.0% | 1.0000 | $\infty$ | $\infty$ | $600.00 | $\infty$ | $\infty$ | NO | **Inadmisible** |
| **13** | 92.3% | 0.7044 | 8.453 | 2.818 | $650.00 | $338.11 | $988.11 | SÍ | Factible |
| **14** | 85.7% | 0.4817 | 2.890 | 0.963 | $700.00 | $115.61 | $815.61 | SÍ | Factible |
| **15** | **80.0%** | **0.3192** | **1.277** | **0.426** | **$750.00** | **$51.07** | **$801.07** | **SÍ** | **★ MÍNIMO GLOBAL (ÓPTIMO)** |
| **16** | 75.0% | 0.2046 | 0.614 | 0.205 | $800.00 | $24.55 | $824.55 | SÍ | Escenario Actual Fijo |
| **17** | 70.6% | 0.1266 | 0.304 | 0.101 | $850.00 | $12.16 | $862.16 | SÍ | Sobredimensionado |
| **18** | 66.7% | 0.0756 | 0.151 | 0.050 | $900.00 | $6.05 | $906.05 | SÍ | Sobredimensionado |
| **19** | 63.2% | 0.0435 | 0.075 | 0.025 | $950.00 | $2.98 | $952.98 | SÍ | Sobredimensionado |
| **20** | 60.0% | 0.0242 | 0.036 | 0.012 | $1,000.00 | $1.45 | $1,001.45 | SÍ | Sobredimensionado |

---

## 7. FORMULACIÓN EN PuLP CON VARIABLES EXCLUSIVAS $x$ e $y$

Cumpliendo con la indicación del profesor de definir **exclusivamente las variables $x$ e $y$**:

### 7.1. Definición de Variables:
$$\begin{aligned}
x &\in \mathbb{Z}^+, \quad 13 \le x \le 20 \quad \text{(Número entero de ventanillas abiertas)} \\
y &\in \mathbb{R}^+, \quad y \ge 0 \quad \text{(Costo total horario resultante del sistema)}
\end{aligned}$$

### 7.2. Función Objetivo:
$$\text{Minimizar } Z = y$$

### 7.3. Restricciones:
1. **Restricción de Nivel de Servicio:**
   Como $W_q(x) \le 0.1 \text{ horas}$ (6 minutos), y la tabla demuestra que para todo $x \ge 13$ el tiempo de espera es menor a 2.82 minutos:
   $$x \ge 13$$
2. **Restricciones de Convexidad Envolvente (Cortes Secantes sobre la Curva de Costo $CT(x)$):**
   Dado que $CT(x)$ es una función convexa y discreta, se generan planos de soporte $y \ge m_k \cdot x + b_k$:
   - Entre $x=13$ y $x=14$: $m = \frac{815.61 - 988.11}{1} = -172.50 \implies y \ge -172.50 \cdot x + 3,230.61$
   - Entre $x=14$ y $x=15$: $m = \frac{801.07 - 815.61}{1} = -14.54 \implies y \ge -14.54 \cdot x + 1,019.17$
   - Entre $x=15$ y $x=16$: $m = \frac{824.55 - 801.07}{1} = +23.48 \implies y \ge 23.48 \cdot x + 448.87$
   - Entre $x=16$ y $x=17$: $m = \frac{862.16 - 824.55}{1} = +37.61 \implies y \ge 37.61 \cdot x + 222.79$

### 7.4. Resultado del Solver CBC de PuLP:
$$\mathbf{x^* = 15 \text{ ventanillas}}, \quad \mathbf{y^* = \$801.07 \text{ USD/hora}}$$

---

## 8. RESPUESTAS EXACTAS A LAS PREGUNTAS ANALÍTICAS

### RESPUESTA A LA PREGUNTA 1:
> **¿Cuál es el número entero óptimo de ventanillas que minimiza el costo total combinado cumpliendo la restricción de 6 minutos de espera?**

**Respuesta Oficial:**  
El número entero óptimo de ventanillas es **$x^* = 15$ ventanillas abiertas**.  
- **Costo total mínimo resultante:** $y^* = \$801.07 \text{ USD/hora}$  
  - Costo de servicio: $\$750.00 \text{ USD/hora}$ ($15 \times \$50$)  
  - Costo de espera: $\$51.07 \text{ USD/hora}$ ($1.2768 \text{ pas} \times \$40$)  
- **Tiempo promedio de espera en cola:** $W_q = 0.426 \text{ minutos (25.5 segundos)}$, el cual cumple con holgura absoluta el estándar máximo de 6 minutos exigido por el aeropuerto ($0.426 \text{ min} \ll 6.0 \text{ min}$).

---

### RESPUESTA A LA PREGUNTA 2:
> **¿Qué impacto cuantitativo en tiempo de espera y costo por hora genera la solución optimizada frente a las 16 ventanillas fijas?**

**Respuesta Oficial y Análisis Cuantitativo:**

1. **Impacto Financiero Directo (Ahorro de Costos):**
   - **Frente al Costo Reportado por el Aeropuerto (\$1,120.00 USD/hora):**
     - **Ahorro por hora:** $\$1,120.00 - \$801.07 = \mathbf{\$318.93 \text{ USD/hora}}$ (Reducción del **28.48%**).
     - **Ahorro por turno diario (16 horas pico):** $\$318.93 \times 16 = \mathbf{\$5,102.88 \text{ USD/día}}$.
     - **Ahorro mensual (30 días):** $\$5,102.88 \times 30 = \mathbf{\$153,086.40 \text{ USD/mes}}$.
     - **Ahorro anual (365 días $\times$ 16h = 5,840 horas):** $\$318.93 \times 5,840 = \mathbf{\$1,862,551 \text{ USD/año}}$ (Casi **$1.86 Millones de Dólares al año**).
   - **Frente al Costo Teórico de 16 Ventanillas (\$824.55 USD/hora):**
     - **Ahorro por hora:** $\$824.55 - \$801.07 = \mathbf{\$23.48 \text{ USD/hora}}$ de ahorro neto.
     - Este ahorro se produce porque cerrar 1 ventanilla ociosa ahorra inmediatamente $\$50 \text{ USD/hora}$ en salarios de oficiales, y el leve incremento de pasajeros en fila apenas agrega $\$26.52 \text{ USD/hora}$ en penalización, generando un beneficio neto de $\$23.48 \text{ USD/hora}$.

2. **Impacto en el Nivel de Servicio y Tiempo de Espera:**
   - En el escenario de 16 ventanillas, el tiempo de espera era de $0.205 \text{ minutos (12.3 segundos)}$.
   - En la solución óptima de 15 ventanillas, el tiempo de espera es de $0.426 \text{ minutos (25.5 segundos)}$.
   - **Diferencia cuantitativa:** Un incremento marginal de apenas **$+13.2 \text{ segundos}$** por pasajero.
   - Para un viajero internacional en migración, pasar de esperar 12 segundos a 25 segundos es psicológicamente imperceptible, pero para la gerencia financiera del aeropuerto representa una reducción drástica de costos operativos cumpliendo con creces la norma de 6 minutos.

---

## 9. GUÍA DE COORDENADAS PARA DIBUJAR EL GRÁFICO A MANO

Para dibujar la gráfica requerida por el profesor en papel milimetrado o cuadriculado:

### Instrucciones de Dibujo:
1. **Eje Horizontal ($X$):** Representa $x$ (Ventanillas Abiertas).  
   - Escala: Marcar desde $x = 12$ hasta $x = 20$.
2. **Eje Vertical Izquierdo ($Y_1$):** Representa el Costo Horario en USD/h.  
   - Escala: De $\$0$ a $\$1,200 \text{ USD/h}$ (marcas cada $\$100$ o $\$200$).
3. **Eje Vertical Derecho ($Y_2$):** Representa el Tiempo de Espera $W_q$ en minutos.  
   - Escala: De $0$ a $7 \text{ minutos}$ (marcas cada $1 \text{ minuto}$).

### Puntos Exactos a Graficar:

#### A. Curva de Costo Total ($y$ en Eje Izquierdo):
- $x = 12 \implies y \to \infty$ (Dibujar asíntota vertical discontinua hacia arriba en $x=12$).
- $x = 13 \implies (13, \$988)$
- $x = 14 \implies (14, \$816)$
- $x = 15 \implies (15, \$801)$ $\leftarrow$ **Punto más bajo de la curva (MÍNIMO GLOBAL)**
- $x = 16 \implies (16, \$825)$
- $x = 17 \implies (17, \$862)$
- $x = 18 \implies (18, \$906)$
- $x = 19 \implies (19, \$953)$
- $x = 20 \implies (20, \$1,001)$

#### B. Curva de Tiempo de Espera ($W_q$ en Eje Derecho):
- $x = 12 \implies W_q \to \infty$
- $x = 13 \implies (13, 2.82 \text{ min})$
- $x = 14 \implies (14, 0.96 \text{ min})$
- $x = 15 \implies (15, 0.43 \text{ min})$
- $x = 16 \implies (16, 0.20 \text{ min})$
- $x = 17 \implies (17, 0.10 \text{ min})$
- $x = 18 \implies (18, 0.05 \text{ min})$

#### C. Líneas Especiales a Resaltar:
1. **Línea Roja Discontinua Horizontal en $Y_2 = 6.0 \text{ min}$:** Rotular como *"Límite Máximo de Servicio (Wq = 6 min)"*. Observar que todos los puntos desde $x=13$ están por debajo.
2. **Círculo Verde en $(x=15, \$801)$:** Marcar con flecha: *"Solución Óptima: x* = 15, y* = $801.07"*.
3. **Punto Naranja en $(x=16, \$825)$:** Marcar con flecha: *"Escenario Actual Fijo: x = 16"*.

---

**FIN DEL TRABAJO ESCRITO A MANO**

