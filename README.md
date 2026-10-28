# OptiQueue AI: Optimización Inteligente de Colas en Migración Aeroportuaria
### Proyecto Final de Investigación de Operaciones e Inteligencia Artificial
**Sistema SaaS B2B en Django + PuLP + SimPy + Matplotlib + Chart.js (Estilo Shark Tank)**

---

## ✈️ Descripción del Proyecto
OptiQueue AI es una plataforma web y motor algorítmico diseñado para resolver el problema de dimensionamiento óptimo de ventanillas en la zona de migración de un aeropuerto internacional durante horas pico.

El sistema resuelve formalmente el **Ejercicio 4** de la guía docente combinando:
1. **Teoría de Colas Multicanal ($M/M/c$ con fórmulas de Erlang C y Ley de Little).**
2. **Simulación de Eventos Discretos en `SimPy`** (proceso estocástico de Poisson y servicio exponencial).
3. **Optimización Entera Mixta en `PuLP`** cumpliendo estrictamente la instrucción de **definir exclusivamente las variables $x$ (número entero de ventanillas abiertas) e $y$ (tiempo de espera o costo resultante)**.
4. **Gráfico Analítico Obligatorio:** *Tiempo de Espera vs Costo Total* generado en `matplotlib` (Python nativo) y en `Chart.js` (interactivo en web).
5. **Dashboard SaaS Dark Mode** con visualización interactiva de las 16 ventanillas de migración y control dinámico.

---

## 📊 Respuestas a las Preguntas Analíticas del Profesor

### Pregunta 1:
> **¿Cuál es el número entero óptimo de ventanillas que minimiza el costo total combinado cumpliendo la restricción de 6 minutos de espera?**

- **Solución Óptima:** **$x^* = 15$ Ventanillas Abiertas**.
- **Costo Total Resultante ($y^*$):** **$801.07 USD / hora** ($750 de operación de ventanillas + $51.07 de penalización por espera).
- **Tiempo Promedio de Espera en Cola ($W_q$):** **0.426 minutos (≈ 25.5 segundos)**, cumpliendo sobradamente la restricción de $W_q \le 0.1 \text{ horas}$ ($6 \text{ minutos}$).

### Pregunta 2:
> **¿Qué impacto cuantitativo en tiempo de espera y costo por hora genera la solución optimizada frente a las 16 ventanillas fijas?**

- **Frente al Costo Reportado por el Aeropuerto ($1,120 USD/h):**
  - **Ahorro por hora:** **$318.93 USD/h** (Reducción del **28.48%** en el gasto operativo).
  - **Ahorro por turno diario (16 horas pico):** **$5,102.88 USD/día**.
  - **Ahorro mensual (30 días):** **$153,086.40 USD/mes**.
  - **Ahorro anual (5,840 horas operativas pico):** **$1,862,551 USD/año** (¡Casi $1.86 Millones de Dólares al año!).
- **Frente al Costo Teórico de 16 Ventanillas ($824.55 USD/h):**
  - **Ahorro neto:** **$23.48 USD/h** (Cerrar 1 ventanilla ahorra $50 en salario de oficiales y el incremento en espera apenas suma $26.52).
- **Impacto en Tiempo de Espera:**
  - Pasa de $0.20 \text{ min}$ ($12 \text{ s}$) a $0.43 \text{ min}$ ($25.5 \text{ s}$), un aumento marginal imperceptible de **+13.2 segundos**, manteniéndose 93% por debajo del límite de 6 minutos.

---

## 📁 Estructura del Repositorio

```text
AIVIDEO/
├── config/                         # Configuración central de Django
│   ├── settings.py                 # Apps, templates y archivos estáticos
│   ├── urls.py                     # Enrutador principal
│   └── wsgi.py
├── migracion/                      # Aplicación principal de Django
│   ├── core/                       # Motores matemáticos y algorítmicos
│   │   ├── queue_theory.py         # Teoría M/M/c, Erlang C, Little y costos
│   │   ├── optimization.py         # Optimización PuLP con variables x e y
│   │   ├── simulation.py           # Simulación de eventos discretos con SimPy
│   │   └── chart_generator.py      # Generador de gráficos con Matplotlib
│   ├── views.py                    # Vistas del dashboard y APIs AJAX
│   └── urls.py                     # Rutas de la aplicación
├── templates/                      # Interfaz visual de usuario
│   ├── base.html                   # Layout base con Tailwind CSS y Chart.js
│   ├── dashboard.html              # Dashboard Shark Tank interactivo
│   ├── codigo.html                 # Módulo de verificación para el profesor
│   └── documentacion.html          # Visor interactivo de entregables
├── static/                         # Archivos estáticos y recursos generados
│   └── img/
│       └── grafico_analitico.png   # Gráfico generado nativamente por Python
├── ENTREGABLES_EQUIPO/             # Documentación para los 10 integrantes
│   ├── 01_TRABAJO_ESCRITO_A_MANO.md          # Desarrollo listo para copiar a mano
│   ├── 02_GUION_SHARK_TANK_10_PERSONAS.md    # Guion comercial por roles y stand
│   └── 03_GUIA_DE_ESTUDIO_Y_PREGUNTAS_DEL_PROFE.md # Glosario y 15 preguntas difíciles
├── requirements.txt                # Dependencias de Python
├── manage.py                       # Administrador de Django
└── README.md                       # Documentación principal
```

---

## 🚀 Instalación y Puesta en Marcha

### 1. Clonar o ingresar a la carpeta del proyecto:
```bash
cd c:\Users\ASUS\OneDrive\Desktop\AIVIDEO
```

### 2. Instalar las dependencias requeridas:
```bash
pip install -r requirements.txt
```

### 3. Aplicar migraciones iniciales de Django:
```bash
python manage.py migrate
```

### 4. Ejecutar el servidor de desarrollo:
```bash
python manage.py runserver
```

### 5. Abrir en el navegador web:
- **Dashboard Principal:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Código y Verificación para el Profesor:** [http://127.0.0.1:8000/codigo/](http://127.0.0.1:8000/codigo/)
- **Entregables y Guion Shark Tank:** [http://127.0.0.1:8000/documentacion/](http://127.0.0.1:8000/documentacion/)

---

## 👥 Equipo Shark Tank (10 Integrantes)
Ver archivo detallado en [`ENTREGABLES_EQUIPO/02_GUION_SHARK_TANK_10_PERSONAS.md`](ENTREGABLES_EQUIPO/02_GUION_SHARK_TANK_10_PERSONAS.md) para el reparto exacto de líneas, roles y elementos recomendados para el stand.

