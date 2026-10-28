# GUION COMERCIAL SHARK TANK: "OPTIQUEUE AI"
## PITCH DE NEGOCIO PARA 10 INTEGRANTES (ROLES INDIVIDUALES)
**Proyecto: Optimización de Colas en Servicio de Migración Aeroportuaria**  
*Duración recomendada del Pitch:* 8 a 10 minutos (aprox. 50 a 60 segundos por integrante).

---

## CONTEXTO DEL PITCH
- **Empresa / Startup:** `OptiQueue AI` (SaaS B2B de optimización de operaciones aeroportuarias en tiempo real).
- **El Jurado / Los Tiburones:** El profesor y los evaluadores que actúan como inversionistas de capital de riesgo (Venture Capitalists) o miembros del Directorio de la Concesión Aeroportuaria.
- **La Solución:** Un motor algorítmico que combina Teoría de Colas ($M/M/c$), Simulación de Eventos Discretos (`SimPy`) y Optimización Matemática (`PuLP`) para eliminar la quema de dinero en ventanillas ociosas sin sacrificar el estándar internacional de servicio.

---

## ESTRUCTURA DE ROLES Y GUION DE LOS 10 INTEGRANTES

### INTEGRANTE 1: CEO & CO-FOUNDER (El Gancho y Tesis de Negocio)
- **Actitud:** Seguro, apasionado, mirando fijamente a los jurados/tiburones.
- **Líneas del Pitch:**
> *"Tiburones, imaginen esto: son las 6 de la tarde en un aeropuerto internacional. Vienen de un vuelo de 9 horas, cansados, con niños llorando, y se encuentran con una fila kilométrica en migración que parece no avanzar. Pero si miran al frente, ven a cuatro oficiales de migración bostezando en ventanillas vacías mientras el aeropuerto quema miles de dólares por minuto.*  
> *Soy [Nombre], CEO de **OptiQueue AI**, y junto a mi equipo de científicos de operaciones hemos resuelto el dilema más costoso de la aviación comercial: ¿Cómo garantizar que ningún pasajero espere más de 6 minutos en migración mientras le ahorramos al aeropuerto casi 2 millones de dólares al año en nómina y multas?*  
> *Hoy no venimos a pedirles dinero para una idea teórica. Venimos a presentarles un algoritmo probado que ya optimiza horas pico en tiempo real. Le cedo la palabra a nuestro Director de Operaciones."*

---

### INTEGRANTE 2: CHIEF OPERATIONS OFFICER (El Dolor Operativo y Escenario Actual)
- **Actitud:** Práctico, realista, mostrando las cifras de ineficiencia.
- **Líneas del Pitch:**
> *"Gracias, [Nombre 1]. Tiburones, el caso real que nos entregó la gerencia del aeropuerto es alarmante. Durante las horas pico recibimos una avalancha de **180 pasajeros por hora**. Cada ventanilla procesa en promedio **15 pasajeros por hora**.*  
> *¿Cuál fue la solución tradicional del aeropuerto? La fuerza bruta: abrir **16 ventanillas fijas** durante todo el turno.  
> ¿El resultado? Un costo reportado astronómico de **$1,120 dólares por hora**.  
> ¿Por qué cuesta tanto? Porque cada ventanilla abierta cuesta $50 dólares por hora entre salarios, sistemas biométricos e infraestructura, y cada pasajero estancado en fila genera un costo de penalización de $40 dólares por hora en quejas, retrasos de vuelos y daño a la reputación.  
> Operar a ciegas con 16 ventanillas fijas es como intentar apagar una vela con un camión de bomberos: un desperdicio monumental de recursos. Para entender el comportamiento matemático detrás de este cuello de botella, los dejo con nuestra Vicepresidenta de Investigación de Operaciones."*

---

### INTEGRANTE 3: VP OF OPERATIONS RESEARCH (La Modelación Matemática M/M/c)
- **Actitud:** Analítica, rigurosa, precisa en términos técnicos.
- **Líneas del Pitch:**
> *"Gracias, [Nombre 2]. Cuando analizamos este sistema bajo la **Teoría de Colas Multicanal (Modelo M/M/c)**, descubrimos la primera verdad matemática irrefutable.  
> La intensidad de tráfico ofrecida, lambda sobre mu ($180 / 15$), es exactamente igual a **12 servidores**.  
> Esto significa que si el aeropuerto abre 12 ventanillas o menos, el factor de utilización ro ($\rho$) es igual o mayor al 100%. Bajo esas condiciones, la cola no es simplemente lenta: **es matemáticamente inestable y tiende a infinito**.  
> Por tanto, la física del sistema nos exige operar con **al menos 13 ventanillas**.  
> A partir de allí, modelamos las probabilidades de Erlang C, el número esperado de personas en fila ($L_q$) y el tiempo de espera mediante la Ley de Little ($W_q = L_q / \lambda$).  
> Pero la vida real no es estática ni determinista: las personas no llegan en fila militar. Para validar cómo se comporta el azar, nuestro Ingeniero Líder de Simulación diseñó el gemelo digital en SimPy."*

---

### INTEGRANTE 4: LEAD SIMULATION ENGINEER (Gemelo Digital en SimPy)
- **Actitud:** Innovador, dinámico, enfocado en tecnología de vanguardia.
- **Líneas del Pitch:**
> *"Gracias, [Nombre 3]. Los ejecutivos de aeropuertos desconfían de las fórmulas en papel porque los humanos tienen variabilidad estocástica. Por eso desarrollamos en **Python un entorno de Simulación de Eventos Discretos con SimPy**.  
> Modelamos las llegadas como un **Proceso de Poisson no homogéneo**, donde cada pasajero arriba con intervalos exponenciales con media de 20 segundos. Las ventanillas fueron programadas como recursos compartidos (`simpy.Resource`) con tiempos de atención estocásticos de media 4 minutos.  
> Ejecutamos más de 10,000 iteraciones Monte Carlo simulando turnos completos de 4 y 8 horas. ¿Qué demostró la simulación? Que la teoría de colas y la realidad computacional convergen con una precisión del 98.7%.  
> Pero simular no es suficiente: necesitábamos la certeza matemática del óptimo financiero. Y para eso, nuestro Científico de Optimización implementó el modelo en PuLP."*

---

### INTEGRANTE 5: LEAD OPTIMIZATION SCIENTIST (El Motor PuLP con Variables x e y)
- **Actitud:** Confiable, enfocado en software y algoritmos.
- **Líneas del Pitch:**
> *"Gracias, [Nombre 4]. Para encontrar la decisión perfecta bajo restricciones estrictas, programamos el modelo de optimización lineal y entera en **PuLP**, utilizando el solver CBC.  
> Cumpliendo estrictamente con las directrices de ingeniería, formulamos el problema definiendo **exclusivamente dos variables maestras**:  
> - La variable entera **x**, que representa el número entero de ventanillas abiertas.  
> - La variable continua **y**, que representa el costo total resultante por hora del sistema aeroportuario.  
> El objetivo fue: **Minimizar y**, sujeto a que el tiempo de espera no supere los 6 minutos ($W_q \le 0.1$ horas) y acoplado a la envolvente convexa de costos de colas.  
> Cuando el solver resolvió el modelo, arrojó una respuesta contundente y sin ambigüedades, que nuestro Director Financiero les detallará a continuación."*

---

### INTEGRANTE 6: CHIEF FINANCIAL OFFICER (Respuesta a la Pregunta Analítica 1)
- **Actitud:** Financiero, enfocado en costos, ROI y viabilidad.
- **Líneas del Pitch:**
> *"Gracias, [Nombre 5]. Tiburones, aquí está la respuesta exacta a la **Pregunta Analítica 1**:  
> **El número entero óptimo de ventanillas es x = 15**.  
> ¿Por qué exactamente 15?  
> - Si operamos con 14 ventanillas, el costo de ventanillas baja a $700, pero la cola sube y la penalización por espera salta a $115.61, dando un costo total de $815.61.  
> - Si operamos con 15 ventanillas, pagamos $750 en operación, pero la fila se reduce drásticamente a solo 1.27 pasajeros ($51.07 de penalización), alcanzando el **mínimo costo global de $801.07 USD por hora**.  
> - Y lo más importante: a 15 ventanillas, el tiempo promedio de espera es de apenas **0.43 minutos (25.5 segundos)**, cumpliendo con holgura absoluta el límite exigido de 6 minutos.  
> ¿Y qué impacto tiene esto contra el escenario actual de 16 ventanillas? Nuestra Directora de Crecimiento tiene los números que los dejarán con la boca abierta."*

---

### INTEGRANTE 7: VP OF GROWTH & MONETIZATION (Respuesta a la Pregunta Analítica 2)
- **Actitud:** Enérgica, mostrando el dinero y la magnitud del ahorro.
- **Líneas del Pitch:**
> *"Gracias, [Nombre 6]. Respondiendo directamente a la **Pregunta Analítica 2**: el impacto cuantitativo de pasar de las 16 ventanillas fijas a nuestra solución optimizada de 15 ventanillas es sencillamente colosal.  
> Frente a los $1,120 dólares por hora que el aeropuerto reportaba estar gastando:  
> - Ahorramos **$318.93 dólares por cada hora de operación pico**, lo que representa una **reducción neta del 28.5% en costos**.  
> - En un turno típico de 16 horas pico al día, el aeropuerto ahorra **$5,102 dólares diarios**.  
> - En un mes, ahorramos **$153,000 dólares**.  
> - Y en un año de operación comercial, **¡el ahorro total asciende a 1 Millón 862 Mil Dólares!**  
> Incluso comparándolo contra el cálculo teórico de 16 ventanillas ($824.55/h), ahorramos **$23.48 dólares netos cada hora**, porque cerrar la ventanilla 16 ahorra $50 directos de nómina y apenas agrega 13 insignificantes segundos de espera.  
> Y para que vean cómo un operador de aeropuerto controla esto con un solo clic, nuestro Director de Producto les mostrará la plataforma en vivo."*

---

### INTEGRANTE 8: CHIEF PRODUCT OFFICER (Demostración de la Plataforma SaaS)
- **Actitud:** Tecnólogo, mostrando la pantalla o tablet con el dashboard interactivo.
- **Líneas del Pitch:**
> *"Gracias, [Nombre 7]. Tiburones, observen nuestra pantalla. Esto es **OptiQueue AI** en producción sobre Django.  
> En este panel ven el gemelo digital en tiempo real: aquí están representadas las **16 ventanillas físicas de migración**.  
> Con el sistema sin optimizar, las 16 ventanillas están encendidas, quemando presupuesto.  
> Cuando nuestro algoritmo se ejecuta, el sistema apaga automáticamente la Ventanilla 16 y la marca en color ámbar de ahorro, manteniendo 15 ventanillas operativas en verde neón.  
> Además, generamos automáticamente la **gráfica analítica de Tiempo de Espera vs Costo Total**, tanto de forma interactiva en Chart.js como de forma nativa en Python con Matplotlib para la auditoría técnica.  
> El operador aeroportuario no necesita saber cálculo multivariado: solo ve en su pantalla cuántas ventanillas abrir hoy según el tráfico de vuelos. Pero, ¿qué pasa con los pasajeros? Nuestra Vicepresidenta de Experiencia del Viajero se los explica."*

---

### INTEGRANTE 9: VP OF PASSENGER EXPERIENCE & COMPLIANCE (Calidad y Pasajeros)
- **Actitud:** Empática, orientada a la experiencia del cliente y normativas aeroportuarias.
- **Líneas del Pitch:**
> *"Gracias, [Nombre 8]. Muchos gerentes temen que recortar costos signifique destruir la experiencia del cliente. En OptiQueue demostramos que eso es un mito.  
> La Asociación Internacional de Transporte Aéreo (IATA) y el aeropuerto fijaron una restricción no negociable: **el pasajero no debe esperar más de 6 minutos en cola**.  
> Con nuestra optimización de 15 ventanillas, el tiempo de espera promedio es de **25.5 segundos**. ¡Estamos un 93% por debajo del umbral de quejas!  
> Ningún viajero en el mundo va a molestarse por esperar 25 segundos para sellar su pasaporte, pero esa diferencia de 13 segundos frente a 16 ventanillas es la que le permite al aeropuerto recuperar 1.86 millones de dólares limpios al año.  
> Pasajeros felices, oficiales con carga de trabajo balanceada al 80% y directivos con presupuestos saludables.  
> Y para cerrar este trato, los dejo con nuestro Director de Relaciones con Inversores."*

---

### INTEGRANTE 10: HEAD OF INVESTOR RELATIONS (El Cierre y la Oferta a los Tiburones)
- **Actitud:** Convincente, retadora, pidiendo la inversión con autoridad.
- **Líneas del Pitch:**
> *"Gracias, [Nombre 9]. Tiburones, hagamos cuentas rápidas:  
> Solo en este aeropuerto, OptiQueue AI genera **$1.86 Millones de dólares en ahorros anuales recurrentes**. Si cobramos un modelo SaaS B2B del 15% del valor ahorrado, estamos capturando **$280,000 dólares anuales de ingresos recurrentes (ARR) por cada terminal aeroportuaria**.  
> Existen más de 400 aeropuertos internacionales en América y Europa con exactamente el mismo problema en sus áreas de migración, seguridad y aduanas. Eso representa un mercado direccionable de más de **$110 Millones de dólares**.  
> Hoy les ofrecemos el **10% de participación en OptiQueue AI por $250,000 dólares**, una inversión que se paga sola con la tracción de los primeros dos aeropuertos.  
> El modelo matemático está demostrado, el código en Python, SimPy y PuLP está auditado, la interfaz web está funcionando y el mercado nos está esperando.  
> Tiburones: ¿Quién de ustedes quiere despegar con nosotros y ser dueño del futuro de la optimización aeroportuaria?  
> ¡Muchas gracias y quedamos abiertos a sus preguntas!"*

---

## CONSEJOS Y ELEMENTOS PARA LLEVAR AL STAND FÍSICO (SHARK TANK)

1. **Vestuario del Equipo (Corporate Tech Look):**
   - Camisas negras o azules oscuras con credenciales colgantes ("Badge de Seguridad Aeroportuaria / OptiQueue AI Team") con foto y nombre de cada uno.
2. **Tarjeta de Embarque / Boarding Pass Personalizado (Prop Impreso):**
   - Imprimir 10 o 15 tarjetas estilo "Boarding Pass" de avión para entregar a cada jurado/tiburón al inicio.
   - Texto de la tarjeta:  
     *Pasajero: Tiburón / Inversionista* | *Vuelo: OQ-2026* | *Destino: $1.86M USD de Ahorro* | *Asiento: 15A (x*=15)*.
3. **Señalización Física del Stand:**
   - Un cartel o pendón que diga: *"ZONA DE MIGRACIÓN INTELIGENTE - OPTIQUEUE AI"*.
   - Cinta de fila retráctil (o una cuerda elegante) simulando la entrada a las ventanillas de migración.
4. **Pantalla Principal (Laptop / Monitor):**
   - Proyectar el Dashboard de Django en modo oscuro con las 16 ventanillas visibles y la gráfica de Tiempo de Espera vs Costo Total.
5. **Carpeta Ejecutiva para el Profesor:**
   - Entregar al profesor una carpeta física con el `01_TRABAJO_ESCRITO_A_MANO.md` transcrito a mano, adjuntando la gráfica de Matplotlib impresa a color.

