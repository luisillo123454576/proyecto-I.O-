import os
import json
from pathlib import Path
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings

from .core.queue_theory import (
    calcular_metricas_mmc,
    generar_tabla_analitica,
    encontrar_optimo_analitico,
    DEFAULT_LAMBDA,
    DEFAULT_MU,
    COSTO_VENTANILLA,
    COSTO_ESPERA,
    MAX_ESPERA_HORAS,
    ESCENARIO_ACTUAL_C,
    COSTO_ACTUAL_REPORTADO
)
from .core.optimization import resolver_optimizacion_pulp
from .core.simulation import SimulacionMigracionAeropuerto, ejecutar_simulacion_simpy
from .core.chart_generator import generar_grafico_analitico_matplotlib


def dashboard(request):
    """
    Vista principal del Dashboard SaaS Shark Tank.
    """
    # 1. Obtener optimización analítica y PuLP
    analisis = encontrar_optimo_analitico()
    res_pulp = resolver_optimizacion_pulp()
    
    # 2. Asegurar que el gráfico estático de Matplotlib esté generado
    ruta_grafico = os.path.join(settings.BASE_DIR, 'static', 'img', 'grafico_analitico.png')
    grafico_b64 = ""
    try:
        if not os.path.exists(ruta_grafico):
            grafico_b64 = generar_grafico_analitico_matplotlib(ruta_grafico)
        else:
            with open(ruta_grafico, 'rb') as f:
                import base64
                grafico_b64 = base64.b64encode(f.read()).decode('utf-8')
    except Exception as e:
        grafico_b64 = ""

    # 3. Preparar estados de las 16 ventanillas físicas
    # Para el óptimo x* = 15: ventanillas 1 a 15 abiertas, ventanilla 16 cerrada.
    x_opt = res_pulp['x_optimo']
    ventanillas_info = []
    for num in range(1, 17):
        abierta = num <= x_opt
        ventanillas_info.append({
            'numero': num,
            'abierta': abierta,
            'estado': 'ABIERTA' if abierta else 'CERRADA (Ahorro)',
            'color': 'emerald' if abierta else 'rose',
            'clase_bg': 'bg-emerald-500/10 border-emerald-500/40 text-emerald-400' if abierta else 'bg-rose-500/10 border-rose-500/30 text-rose-400 opacity-60',
        })

    # 4. Datos para gráficos en Chart.js (JSON-serializables)
    tabla = analisis['tabla']
    labels_chart = [f"c={fila['c']}" for fila in tabla if fila['c'] >= 13]
    datos_costo_total = [round(fila['costo_total'], 2) for fila in tabla if fila['c'] >= 13]
    datos_costo_servicio = [round(fila['costo_servicio'], 2) for fila in tabla if fila['c'] >= 13]
    datos_costo_espera = [round(fila['costo_espera'], 2) for fila in tabla if fila['c'] >= 13]
    datos_tiempo_espera = [round(fila['wq_minutos'], 3) for fila in tabla if fila['c'] >= 13]

    contexto = {
        'analisis': analisis,
        'optimo': analisis['optimo'],
        'actual_teorico': analisis['actual_teorico'],
        'costo_reportado': COSTO_ACTUAL_REPORTADO,
        'res_pulp': res_pulp,
        'tabla': tabla,
        'ventanillas_info': ventanillas_info,
        'grafico_b64': grafico_b64,
        # JSON stringificados para Chart.js
        'chart_labels_json': json.dumps(labels_chart),
        'chart_costo_total_json': json.dumps(datos_costo_total),
        'chart_costo_servicio_json': json.dumps(datos_costo_servicio),
        'chart_costo_espera_json': json.dumps(datos_costo_espera),
        'chart_tiempo_espera_json': json.dumps(datos_tiempo_espera),
        # Parámetros operativos
        'lambda_param': DEFAULT_LAMBDA,
        'mu_param': DEFAULT_MU,
        'cs_param': COSTO_VENTANILLA,
        'cw_param': COSTO_ESPERA,
        'max_wq_param': MAX_ESPERA_HORAS * 60,  # en minutos
    }
    return render(request, 'dashboard.html', contexto)


def api_optimizar(request):
    """
    API AJAX para ejecutar la optimización PuLP con variables x e y.
    """
    lam = float(request.GET.get('lambda', DEFAULT_LAMBDA))
    mu = float(request.GET.get('mu', DEFAULT_MU))
    cs = float(request.GET.get('cs', COSTO_VENTANILLA))
    cw = float(request.GET.get('cw', COSTO_ESPERA))
    max_wq_min = float(request.GET.get('max_wq_min', 6.0))
    max_wq_h = max_wq_min / 60.0

    res = resolver_optimizacion_pulp(
        lam=lam, mu=mu, cs=cs, cw=cw, max_wq_horas=max_wq_h
    )
    return JsonResponse({
        'status': 'success',
        'x_optimo': res['x_optimo'],
        'y_optimo': round(res['y_optimo'], 2),
        'estado': res['estado_solucion'],
        'wq_minutos': round(res['metricas_optimo']['wq_minutos'], 3),
        'costo_total': round(res['metricas_optimo']['costo_total'], 2),
        'costo_servicio': round(res['metricas_optimo']['costo_servicio'], 2),
        'costo_espera': round(res['metricas_optimo']['costo_espera'], 2),
        'ahorro_hora_reportado': round(res['ahorro_hora_reportado'], 2),
        'pct_ahorro_reportado': round(res['pct_ahorro_reportado'], 2),
        'ahorro_anual': round(res['ahorro_anual'], 2),
        'codigo_fuente': res['codigo_pulp_fuente']
    })


def api_simular(request):
    """
    API AJAX para ejecutar la simulación estocástica en SimPy.
    """
    num_ventanillas = int(request.GET.get('ventanillas', 15))
    duracion = float(request.GET.get('duracion', 4.0))
    seed = int(request.GET.get('seed', 42))

    res = ejecutar_simulacion_simpy(
        num_ventanillas=num_ventanillas,
        duracion_horas=duracion,
        seed=seed
    )
    return JsonResponse({
        'status': 'success',
        'ventanillas': res['num_ventanillas'],
        'total_atendidos': res['total_atendidos'],
        'total_llegadas': res['total_llegadas'],
        'wq_minutos': round(res['wq_promedio_minutos'], 3),
        'ws_minutos': round(res['ws_promedio_minutos'], 3),
        'w_total_minutos': round(res['w_total_minutos'], 3),
        'utilizacion_pct': round(res['utilizacion_promedio_pct'], 1),
        'costo_total': round(res['costo_total'], 2),
        'costo_servicio': round(res['costo_servicio'], 2),
        'costo_espera': round(res['costo_espera'], 2),
        'pct_en_norma_6min': round(res['pct_pasajeros_en_norma_6min'], 1),
        'cumple_restriccion': res['cumple_restriccion'],
        'eventos': res['log_eventos_muestra']
    })


def api_recalcular(request):
    """
    API AJAX instantánea para recalcular métricas teóricas al mover sliders interactivos.
    """
    c = int(request.GET.get('c', 15))
    lam = float(request.GET.get('lambda', DEFAULT_LAMBDA))
    mu = float(request.GET.get('mu', DEFAULT_MU))
    cs = float(request.GET.get('cs', COSTO_VENTANILLA))
    cw = float(request.GET.get('cw', COSTO_ESPERA))

    m = calcular_metricas_mmc(c, lam, mu, cs, cw)
    
    ahorro_reportado = COSTO_ACTUAL_REPORTADO - m['costo_total'] if m['estable'] else 0
    return JsonResponse({
        'c': c,
        'estable': m['estable'],
        'rho_pct': round(m.get('utilizacion_pct', 0), 1),
        'wq_minutos': round(m['wq_minutos'], 3) if m['estable'] else 'Infinito',
        'lq': round(m['lq'], 2) if m['estable'] else 'Infinito',
        'costo_total': round(m['costo_total'], 2) if m['estable'] else 'Infinito',
        'costo_servicio': round(m['costo_servicio'], 2),
        'costo_espera': round(m['costo_espera'], 2) if m['estable'] else 'Infinito',
        'cumple_restriccion': m['cumple_restriccion'],
        'ahorro_hora_reportado': round(ahorro_reportado, 2)
    })


def vista_codigo(request):
    """
    Vista dedicada para exhibir el código de SimPy y PuLP con las variables x e y
    al profesor, junto con las explicaciones matemáticas y la gráfica de Python.
    """
    res_pulp = resolver_optimizacion_pulp()
    sim_ejemplo = ejecutar_simulacion_simpy(15, duracion_horas=1.0)
    
    ruta_grafico = os.path.join(settings.BASE_DIR, 'static', 'img', 'grafico_analitico.png')
    grafico_b64 = ""
    try:
        with open(ruta_grafico, 'rb') as f:
            import base64
            grafico_b64 = base64.b64encode(f.read()).decode('utf-8')
    except Exception:
        grafico_b64 = ""

    contexto = {
        'codigo_pulp': res_pulp['codigo_pulp_fuente'],
        'codigo_simpy': sim_ejemplo['codigo_simpy_fuente'],
        'grafico_b64': grafico_b64,
        'res_pulp': res_pulp
    }
    return render(request, 'codigo.html', contexto)


def vista_documentacion(request, doc_id='01'):
    """
    Visor interactivo de los entregables markdown creados para el equipo de 10 personas.
    """
    mapa_docs = {
        '01': {
            'archivo': '01_TRABAJO_ESCRITO_A_MANO.md',
            'titulo': '01. Trabajo Escrito a Mano (Entregable Profesor)',
            'subtitulo': 'Desarrollo matemático paso a paso listo para transcribir en hojas'
        },
        '02': {
            'archivo': '02_GUION_SHARK_TANK_10_PERSONAS.md',
            'titulo': '02. Guion Shark Tank para 10 Integrantes',
            'subtitulo': 'Estructura por roles, pitch comercial, métricas y props para el stand'
        },
        '03': {
            'archivo': '03_GUIA_DE_ESTUDIO_Y_PREGUNTAS_DEL_PROFE.md',
            'titulo': '03. Guía de Estudio y Preguntas Corchadoras',
            'subtitulo': 'Explicación conceptual desde cero y 15 preguntas difíciles con respuestas'
        }
    }

    doc_info = mapa_docs.get(doc_id, mapa_docs['01'])
    ruta_archivo = os.path.join(settings.BASE_DIR, 'ENTREGABLES_EQUIPO', doc_info['archivo'])
    
    contenido_markdown = ""
    if os.path.exists(ruta_archivo):
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            contenido_markdown = f.read()
    else:
        contenido_markdown = f"# Archivo {doc_info['archivo']} en preparación..."

    contexto = {
        'doc_id_actual': doc_id,
        'doc_info': doc_info,
        'mapa_docs': mapa_docs,
        'contenido_markdown': contenido_markdown
    }
    return render(request, 'documentacion.html', contexto)
