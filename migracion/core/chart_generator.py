"""
Generador de Gráficos Analíticos con Matplotlib
================================================
Genera el gráfico analítico obligatorio:
"Tiempo de Espera vs Costo Total"
para cumplir al 100% el requisito de Python del profesor.
"""

import os
import io
import base64
import matplotlib
matplotlib.use('Agg')  # Backend no interactivo para entornos web y servidores
import matplotlib.pyplot as plt
import numpy as np

from .queue_theory import (
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


def generar_grafico_analitico_matplotlib(ruta_guardado: str = None) -> str:
    """
    Crea el gráfico de Tiempo de Espera vs Costo Total en estilo Dark Mode / Ejecutivo.
    Guarda la imagen en el path especificado y retorna el string base64 para HTML.
    """
    # 1. Obtención de datos calculados
    c_vals = list(range(13, 21))
    costos_totales = []
    costos_servicio = []
    costos_espera = []
    tiempos_espera_min = []
    
    for c in c_vals:
        from .queue_theory import calcular_metricas_mmc
        m = calcular_metricas_mmc(c)
        costos_totales.append(m['costo_total'])
        costos_servicio.append(m['costo_servicio'])
        costos_espera.append(m['costo_espera'])
        tiempos_espera_min.append(m['wq_minutos'])
        
    opt = encontrar_optimo_analitico()
    x_opt = opt['optimo']['c']
    ct_opt = opt['optimo']['costo_total']
    wq_opt = opt['optimo']['wq_minutos']

    # 2. Configuración de estilo Dark Theme moderno
    plt.style.use('dark_background')
    fig, ax1 = plt.subplots(figsize=(11, 6.5), dpi=150)
    fig.patch.set_facecolor('#0B1120')  # Fondo slate oscuro
    ax1.set_facecolor('#0F172A')

    # Eje 1 (Izquierdo): Costos
    color_costo_tot = '#38BDF8'  # Celeste Cyan neón
    color_costo_srv = '#64748B'  # Gris slate
    color_costo_esp = '#F43F5E'  # Rosa/Rojo advertencia
    
    line1 = ax1.plot(c_vals, costos_totales, color=color_costo_tot, linewidth=3.5,
                     marker='o', markersize=8, label='Costo Total ($ USD/h) [Eje Izq]', zorder=5)
    line2 = ax1.plot(c_vals, costos_servicio, color=color_costo_srv, linewidth=2,
                     linestyle='--', marker='s', markersize=5, label='Costo Operación Ventanillas ($50·x)', zorder=4)
    line3 = ax1.plot(c_vals, costos_espera, color=color_costo_esp, linewidth=2,
                     linestyle=':', marker='^', markersize=5, label='Costo Penalización Espera ($40·Lq)', zorder=4)

    ax1.set_xlabel('Número de Ventanillas Abiertas (x)', fontsize=12, fontweight='bold', color='#E2E8F0', labelpad=10)
    ax1.set_ylabel('Costo Horario ($ USD / hora)', fontsize=12, fontweight='bold', color=color_costo_tot, labelpad=10)
    ax1.set_xticks(c_vals)
    ax1.tick_params(axis='x', colors='#CBD5E1', labelsize=11)
    ax1.tick_params(axis='y', colors=color_costo_tot, labelsize=11)
    ax1.grid(True, linestyle='--', alpha=0.15, color='#94A3B8')

    # Eje 2 (Derecho): Tiempo de espera en cola
    ax2 = ax1.twinx()
    ax2.set_facecolor('none')
    color_tiempo = '#FBBF24'  # Ámbar / Dorado neón
    
    line4 = ax2.plot(c_vals, tiempos_espera_min, color=color_tiempo, linewidth=3,
                     marker='D', markersize=7, label='Tiempo Promedio Espera Wq (min) [Eje Der]', zorder=5)
    ax2.set_ylabel('Tiempo Promedio de Espera Wq (Minutos)', fontsize=12, fontweight='bold', color=color_tiempo, labelpad=10)
    ax2.tick_params(axis='y', colors=color_tiempo, labelsize=11)

    # Línea horizontal del límite de nivel de servicio (6 minutos = 0.1 horas)
    limite_line = ax2.axhline(y=6.0, color='#EF4444', linestyle='-.', linewidth=2,
                              alpha=0.85, label='Límite de Servicio (6 min = 0.1 h)')
    ax2.text(13.1, 6.2, 'LÍMITE MÁXIMO DE ESPERA (6.0 min)', color='#EF4444',
             fontweight='bold', fontsize=9)

    # 3. Resaltar el Punto Óptimo (x* = 15)
    ax1.scatter([x_opt], [ct_opt], color='#10B981', s=220, edgecolors='#FFFFFF', linewidth=2.5, zorder=10)
    ax1.annotate(f'ÓPTIMO x* = 15\nCosto: ${ct_opt:.2f}/h\nWq: {wq_opt:.2f} min',
                 xy=(x_opt, ct_opt),
                 xytext=(x_opt - 1.6, ct_opt + 90),
                 arrowprops=dict(facecolor='#10B981', edgecolor='#FFFFFF', shrink=0.08, width=2, headwidth=8),
                 bbox=dict(boxstyle='round,pad=0.6', facecolor='#064E3B', edgecolor='#10B981', alpha=0.95),
                 color='#ECFDF5', fontweight='bold', fontsize=10, zorder=11)

    # 4. Resaltar el Escenario Actual (x = 16)
    c_actual = ESCENARIO_ACTUAL_C
    costo_act_teorico = opt['actual_teorico']['costo_total']
    ax1.scatter([c_actual], [costo_act_teorico], color='#F59E0B', s=160, edgecolors='#FFFFFF', linewidth=2, zorder=9)
    ax1.annotate(f'ACTUAL x = 16\nCosto Teór: ${costo_act_teorico:.2f}/h\nReportado: ${COSTO_ACTUAL_REPORTADO:.0f}/h',
                 xy=(c_actual, costo_act_teorico),
                 xytext=(c_actual + 0.3, costo_act_teorico - 80),
                 arrowprops=dict(facecolor='#F59E0B', edgecolor='#FFFFFF', shrink=0.08, width=1.5, headwidth=6),
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='#451A03', edgecolor='#F59E0B', alpha=0.9),
                 color='#FEF3C7', fontsize=9, fontweight='bold', zorder=11)

    # Título principal del gráfico
    plt.title('OPTIMIZACIÓN DE COLAS: TIEMPO DE ESPERA vs COSTO TOTAL\n' + 
              r'Modelo M/M/c ($\lambda = 180$ pas/h, $\mu = 15$ pas/h/ventanilla)',
              fontsize=13, fontweight='bold', color='#F8FAFC', pad=18)

    # Combinar leyendas de ambos ejes
    lines = line1 + line2 + line3 + line4 + [limite_line]
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper right', framealpha=0.85, facecolor='#1E293B',
               edgecolor='#475569', fontsize=8.5)

    fig.tight_layout()

    # Guardar en archivo si se indicó
    if ruta_guardado:
        os.makedirs(os.path.dirname(ruta_guardado), exist_ok=True)
        fig.savefig(ruta_guardado, format='png', bbox_inches='tight', dpi=180)

    # Generar Base64 para incrustación directa en templates Django
    buffer = io.BytesIO()
    fig.savefig(buffer, format='png', bbox_inches='tight', dpi=180)
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close(fig)

    return image_base64

