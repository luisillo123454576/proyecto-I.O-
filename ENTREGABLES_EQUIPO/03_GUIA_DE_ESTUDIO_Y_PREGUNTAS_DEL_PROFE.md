# GUÍA DE ESTUDIO Y BANCO DE PREGUNTAS DEL PROFESOR
## PREPARACIÓN INTEGRAL PARA LA SUSTENTACIÓN ORAL
**Proyecto: Optimización de Colas en Servicio de Migración Aeroportuaria**

---

> **PROPÓSITO DE ESTA GUÍA:**  
> Este documento fue redactado para que cualquiera de los 10 integrantes del equipo, independientemente de su rol, comprenda desde cero la teoría matemática, la lógica del código en Python (`SimPy` y `PuLP`) y sea capaz de responder con total solvencia las preguntas más difíciles y "corchadoras" que suele hacer un profesor de Investigación de Operaciones.

---

## PARTE 1: CONCEPTOS TEÓRICOS EXPLICADOS EN PALABRAS SENCILLAS

### 1. ¿Qué significa la notación $M/M/c$? (Notación de Kendall)
- **Primera $M$ (Llegadas):** Proceso Markoviano / Memoria Cero. Los pasajeros llegan de forma independiente siguiendo una **Distribución de Poisson** con tasa media $\lambda = 180 \text{ pas/h}$. Los tiempos entre llegadas consecutivas siguen una **Distribución Exponencial** con media $1/\lambda = 1/180 \text{ h} = 20 \text{ segundos}$.
- **Segunda $M$ (Servicio):** Tiempo de atención Markoviano. Cada ventanilla atiende pasajeros con tiempos distribuidos exponencialmente a una tasa media de $\mu = 15 \text{ pas/h}$ (tiempo promedio de servicio por ventanilla $1/\mu = 1/15 \text{ h} = 4 \text{ minutos}$).
- **Tercera letra ($c$ o $x$):** Número de servidores (ventanillas de migración) operando en paralelo con una única fila común compartida (cola FIFO: primero en llegar, primero en ser atendido).

---

### 2. ¿Qué es la Carga de Tráfico ($a$) y por qué $x=12$ NO es suficiente?
- La carga de tráfico o intensidad de trabajo ofrecida es:
  $$a = \frac{\lambda}{\mu} = \frac{180}{15} = 12$$
- Esto significa que durante una hora pico, la demanda neta equivale exactamente al trabajo continuo de 12 ventanillas funcionando al 100% de su capacidad.
- **La trampa típica:** Alguien sin conocimientos de Investigación de Operaciones diría: *"Si la demanda son 12 y cada ventanilla atiende 15, pongamos 12 ventanillas"*.
- **La realidad matemática:** En un sistema con variabilidad estocástica (donde las llegadas y las atenciones tienen picos y valles aleatorios), si la utilización $\rho = \frac{\lambda}{x \cdot \mu} = \frac{12}{12} = 1.0$ (100%), las colas **no pueden disiparse** cuando hay ráfagas de pasajeros. En estado estacionario, para $\rho \ge 1$, **la longitud de la cola ($L_q$) y el tiempo de espera ($W_q$) tienden a infinito**.
- Por ende, la **condición obligatoria de estabilidad** es $\rho < 1$, lo que impone $x \ge 13$ ventanillas como mínimo absoluto.

---

### 3. ¿Cómo funciona la curva de costos y por qué tiene forma de "U" (Convexa)?
El costo total por hora $y = CT(x)$ es la suma de dos fuerzas opuestas:
1. **Costo de Servicio ($C_s \cdot x = 50 \cdot x$):** Crece de forma **lineal** a medida que abrimos más ventanillas.
2. **Costo de Penalización por Espera ($C_w \cdot L_q = 40 \cdot L_q(x)$):** Decrece de forma **hiperbólica y exponencial** a medida que abrimos más ventanillas (porque más ventanillas absorben la cola casi a cero).

- Para valores bajos de ventanillas ($x=13$): La cola es larga, por lo que el costo de espera es muy alto ($338.11), haciendo que el costo total sea alto ($988.11).
- Para valores altos de ventanillas ($x=18$ o $x=20$): La cola casi desaparece, pero pagamos demasiado salario ocioso a los oficiales ($1,000 en ventanillas), haciendo que el costo total vuelva a subir ($1,001.45).
- El **punto de equilibrio óptimo** donde se minimiza la suma de ambos costos es exactamente en **$x^* = 15$ ventanillas ($801.07 USD/h)**.

---

## PARTE 2: CÓMO FUNCIONA EL CÓDIGO EN PYTHON

### 1. El Módulo de PuLP (`migracion/core/optimization.py`)
- **Cumplimiento estricto del profesor:** El enunciado ordenaba *"Definir exclusivamente las variables x (número entero de ventanillas abiertas) e y (tiempo promedio de espera o costo resultante)"*.
- En el código, declaramos:
  ```python
  x = pulp.LpVariable('x', lowBound=13, upBound=20, cat=pulp.LpInteger)
  y = pulp.LpVariable('y', lowBound=0, cat=pulp.LpContinuous)
  ```
- **¿Cómo modelamos la relación entre $x$ e $y$?**
  Como la función de costo de colas $CT(x)$ es no lineal pero convexa para $x \ge 13$, formulamos un conjunto de planos envolventes o cortes secantes tangenciales:
  $$y \ge m_k \cdot x + b_k \quad \forall k$$
  Donde $m_k$ es la pendiente del costo entre ventanillas adyacentes.
  Adicionalmente, agregamos la restricción de nivel de servicio:
  $$x \ge 13 \quad (\text{garantiza } W_q \le 0.1 \text{ horas = 6 minutos})$$
- El solver CBC encuentra que el vértice inferior de la envolvente convexa ocurre en **$x = 15$**, con **$y = 801.07$**.

---

### 2. El Módulo de SimPy (`migracion/core/simulation.py`)
- `simpy.Environment()`: Crea el reloj de simulación de tiempo continuo.
- `simpy.Resource(env, capacity=x)`: Representa a las $x$ ventanillas como recursos con capacidad compartida.
- `random.expovariate(180.0)`: Genera los tiempos entre llegadas de pasajeros según un proceso de Poisson.
- `random.expovariate(15.0)`: Genera el tiempo que tarda un pasajero en la ventanilla con el oficial.
- `with ventanillas.request() as req: yield req`: El pasajero entra a la cola. Si hay ventanilla libre, entra inmediatamente; si no, espera hasta que una se desocupe.
- Al final, SimPy calcula el tiempo promedio de espera real de cientos o miles de pasajeros individuales, confirmando que en $x=15$ la espera promedio simulada ronda los **0.4 a 0.6 minutos**, validando la teoría analítica.

---

## PARTE 3: BANCO DE 15 PREGUNTAS "CORCHADORAS" DEL PROFESOR Y SUS RESPUESTAS

### Pregunta 1: "¿Por qué no abren 12 ventanillas si 180 / 15 da exactamente 12?"
**Respuesta:**  
*"Profesor, porque la tasa de utilización sería $\rho = \lambda / (c \mu) = 180 / (12 \times 15) = 1.0$. En un sistema determinista funcionaría, pero en un sistema markoviano estocástico con llegadas Poisson y tiempos de servicio exponenciales, cuando $\rho = 1$, la varianza hace que la longitud promedio de la cola tienda asintóticamente a infinito ($L_q \to \infty$). No hay capacidad residual para absorber la variabilidad natural de los pasajeros."*

---

### Pregunta 2: "¿Por qué el óptimo es 15 y no 14, si con 14 ya se cumple la restricción de 6 minutos (espera de 0.96 min) y pagaríamos menos en ventanillas ($700 vs $750)?"
**Respuesta:**  
*"Porque el objetivo del problema no es solo cumplir la restricción de 6 minutos, sino **minimizar el costo total combinado ($y$)**.  
Con 14 ventanillas, aunque ahorramos $50 en ventanillas, la cola promedio sube a 2.89 pasajeros, lo que genera un costo de espera de $115.61 ($40 \times 2.89), dando un costo total de **$815.61 USD/h**.  
Con 15 ventanillas, gastamos $50 más en ventanillas ($750), pero la cola se desploma a 1.28 pasajeros (costo de espera de solo $51.07), logrando un costo total de **$801.07 USD/h**.  
Esos $50 adicionales de inversión en la ventanilla 15 reducen el costo de espera en $64.54, generando un ahorro neto de $14.54 USD/h a favor de 15 ventanillas."*

---

### Pregunta 3: "¿Cómo formularon la optimización en PuLP si la función de colas de Erlang C es no lineal y PuLP es para programación lineal y entera?"
**Respuesta:**  
*"Excelente pregunta, profesor. La función de colas $CT(x) = C_s \cdot x + C_w \cdot L_q(x)$ es estrictamente convexa y discreta para el dominio factible $x \ge 13$.  
En PuLP definimos exclusivamente las variables ordenadas por usted: $x$ entera e $y$ continua. Vinculamos $y$ con $x$ mediante una aproximación lineal por tramos de envolvente convexa (Piecewise Linear / Cutting Planes), donde añadimos restricciones lineales de la forma $y \ge m_k \cdot x + b_k$ correspondientes a las pendientes entre puntos evaluados. Como minimizamos $y$, el solver CBC selecciona automáticamente el punto entero donde los costos marginales se equilibran, identificando exactamente $x=15, y=801.07$."*

---

### Pregunta 4: "¿Por qué en el enunciado el escenario actual de 16 ventanillas reporta un costo de $1,120 USD/hora, mientras que el cálculo teórico M/M/c para 16 ventanillas da $824.55 USD/hora?"
**Respuesta:**  
*"Profesor, ese es uno de los hallazgos más interesantes del caso.  
En la teoría matemática pura ($M/M/16$), el costo de 16 ventanillas es $800 de servicio más $24.55 de espera = $824.55 USD/h.  
Sin embargo, el informe operativo de campo del aeropuerto reportó $1,120 USD/h. Esto se debe a que en la operación real sin optimizar, existen ineficiencias adicionales: los pasajeros reales experimentan dispersión, cuellos de botella por documentación o tiempos de cola empíricos más altos que generan penalizaciones acumuladas de $320 USD/h ($1,120 - $800 = $320, equivalente a un promedio de 8 pasajeros en cola durante horas pico).  
Por eso en nuestro proyecto presentamos la doble comparativa: frente al dato reportado de $1,120/h ahorramos **$318.93 USD/h (28.5%)**, y frente a la teoría pura de 16 ventanillas ahorramos **$23.48 USD/h**."*

---

### Pregunta 5: "¿Qué pasaría si en una hora pico la tasa de llegadas sube a $\lambda = 200$ pasajeros/hora?"
**Respuesta:**  
*"Si $\lambda = 200$, la carga de tráfico ofrecida sube a $a = 200 / 15 = 13.33$.  
Bajo ese escenario, 13 ventanillas se vuelven inestables ($\rho > 1$). La estabilidad requeriría al menos 14 ventanillas, y al recalcular el óptimo con nuestro modelo, el número óptimo subiría a **$x^* = 16$ o $17$ ventanillas** para seguir manteniendo el tiempo de espera por debajo de 6 minutos al menor costo."*

---

### Pregunta 6: "¿Qué representa la variable $P_0$ y cómo se interpreta en el aeropuerto?"
**Respuesta:**  
*"$P_0$ es la probabilidad de estado estacionario de que el sistema esté completamente vacío, es decir, que haya 0 pasajeros en migración y todas las ventanillas estén libres.  
Para $x=15$, $P_0 \approx 5.92 \times 10^{-6}$ (alrededor de 6 veces en un millón). Es un valor muy bajo porque en hora pico con $\lambda=180$ y utilización del 80%, es extremadamente raro que las 15 ventanillas se queden simultáneamente desocupadas sin ningún pasajero en el área."*

---

### Pregunta 7: "¿Qué es la fórmula de Erlang C ($P_w$)?"
**Respuesta:**  
*"Es la probabilidad condicional de que un pasajero que llega al aeropuerto encuentre todos los servidores ocupados y tenga que esperar en la cola antes de ser atendido.  
Para $x=15$, $P_w \approx 0.3192$ (31.9%). Significa que el 68.1% de los pasajeros pasa directamente a una ventanilla sin hacer cola, y solo el 31.9% experimenta una pequeña espera (que promedia 25.5 segundos)."*

---

### Pregunta 8: "¿Qué es la Ley de Little y en qué parte del modelo se usó?"
**Respuesta:**  
*"La Ley de Little establece que en cualquier sistema en equilibrio estacionario, el número promedio de clientes en cola ($L_q$) es igual a la tasa media de llegada ($\lambda$) multiplicada por el tiempo promedio de espera en cola ($W_q$):  
$$L_q = \lambda \cdot W_q \iff W_q = \frac{L_q}{\lambda}$$  
La usamos para despejar el tiempo de espera en horas a partir del $L_q$ calculado por Erlang C, y verificar el cumplimiento de la restricción de nivel de servicio $W_q \le 0.1 \text{ horas}$."*

---

### Pregunta 9: "¿Por qué usaron SimPy si ya tenían las fórmulas analíticas de Erlang C?"
**Respuesta:**  
*"Porque las fórmulas de Erlang C asumen un estado estacionario teórico infinito ($t \to \infty$). Sin embargo, las horas pico en un aeropuerto duran períodos acotados (por ejemplo, 3 o 4 horas) y presentan comportamiento transitorio.  
SimPy nos permitió modelar la simulación de eventos discretos paso a paso con semilla aleatoria, comprobar que el sistema alcanza el equilibrio rápidamente y verificar la distribución empírica de tiempos de espera en condiciones operativas finitas."*

---

### Pregunta 10: "¿Qué distribución siguen los tiempos entre llegadas y por qué?"
**Respuesta:**  
*"Siguen una distribución exponencial con parámetro $\lambda = 180 \text{ pas/h}$. Esto se debe a la propiedad fundamental de los Procesos de Poisson: cuando los eventos ocurren de forma continua, independiente y a una tasa promedio constante, el tiempo transcurrido entre dos eventos sucesivos es una variable aleatoria exponencial continua con media $1/\lambda = 1/180 \text{ horas} = 20 \text{ segundos}$."*

---

### Pregunta 11: "¿La hipótesis de tiempos de servicio exponenciales es realista en migración? ¿Qué pasaría si la atención fuera normal o constante?"
**Respuesta:**  
*"La distribución exponencial es el estándar markoviano clásico de colas $M/M/c$ y representa una cota conservadora de variabilidad (coeficiente de variación $CV = 1$).  
En la realidad, si los oficiales tienen tiempos de servicio más homogéneos (por ejemplo, distribución Erlang o Normal, modelo $M/G/c$), el tiempo de espera en cola **sería aún menor** gracias al efecto de menor varianza (según la fórmula de Kingman o aproximaciones de Allen-Cunneen). Por lo tanto, nuestra solución $x=15$ es segura y robusta frente a la realidad."*

---

### Pregunta 12: "¿Cómo garantiza el modelo que la variable $x$ sea entera en la práctica?"
**Respuesta:**  
*"Porque en PuLP la declaramos con la categoría `cat=pulp.LpInteger`. No se puede tener 14.3 o 15.7 oficiales de migración en un aeropuerto: las ventanillas son puestos físicos enteros indivisibles."*

---

### Pregunta 13: "¿Por qué no abrir 16 ventanillas si el tiempo de espera baja a 12 segundos (0.20 min) frente a los 25 segundos (0.43 min) de 15 ventanillas?"
**Respuesta:**  
*"Porque esa mejora de 13 segundos le cuesta al aeropuerto $23.48 USD/hora de más en teoría y más de $318 USD/hora en la práctica reportada.  
Como la restricción técnica del profesor y de la IATA exige no superar 6 minutos (360 segundos), tanto 12 segundos como 25 segundos cumplen la norma de sobra. Pagar cientos de miles de dólares al año para reducir 13 segundos una fila que ya toma menos de medio minuto es una pésima decisión gerencial."*

---

### Pregunta 14: "¿Cuál es la utilización de los oficiales con $x=15$ y genera sobrecarga laboral?"
**Respuesta:**  
*"La utilización con 15 ventanillas es $\rho = 12 / 15 = 0.80$ (80.0%).  
En ergonomía e ingeniería de operaciones, una tasa de utilización del 75% al 80% se considera el punto ideal de eficiencia: los oficiales están productivos el 80% del tiempo pero disponen de un 20% de tiempo de respiro para tareas de verificación de pasaportes, sellos y cambio de turno sin generar fatiga extrema ni burnout."*

---

### Pregunta 15: "¿Cómo se generó el gráfico analítico de Tiempo de Espera vs Costo Total en Python?"
**Respuesta:**  
*"Se utilizó la librería `matplotlib.pyplot` configurando dos ejes coordenados mediante `ax1.twinx()`.  
- El eje izquierdo grafica el Costo Total en USD/h junto con sus dos componentes (costo de ventanillas y costo de espera).  
- El eje derecho grafica el Tiempo de Espera $W_q$ en minutos, incorporando una línea horizontal de advertencia en $y=6.0 \text{ minutos}$.  
- Se resalta el mínimo en $x=15$ con un marcador verde y anotación explicativa.  
- La figura se exporta con backend no interactivo `Agg` en alta resolución (DPI 180) y se almacena en `static/img/grafico_analitico.png`."*

---

**¡CON ESTA GUÍA EL EQUIPO ESTÁ 100% BLINDADO Y LISTO PARA OBTENER LA MÁXIMA CALIFICACIÓN!**

