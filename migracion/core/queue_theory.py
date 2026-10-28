"""
Módulo de Teoría de Colas (M/M/c - Erlang C)
==============================================
Contexto Operativo: Migración Aeropuerto Internacional
- Tasa de llegada: lambda = 180 pasajeros/hora
- Tasa de atención por ventanilla: mu = 15 pasajeros/hora
- Costo ventanilla abierta: $50 USD/hora
- Costo espera de pasajeros: $40 USD/hora por pasajero en cola
- Nivel de Servicio Restricción: Wq <= 0.1 horas (6 minutos)
- Escenario Actual: 16 ventanillas fijas, Costo reportado: $1,120 USD/hora
"""

import math
from typing import Dict, List, Any, Optional

# Parámetros estándar del ejercicio del profesor
DEFAULT_LAMBDA = 180.0   # pasajeros / hora
DEFAULT_MU = 15.0        # pasajeros / hora por ventanilla
COSTO_VENTANILLA = 50.0  # USD / hora por ventanilla
COSTO_ESPERA = 40.0      # USD / hora por pasajero en cola
MAX_ESPERA_HORAS = 0.1   # 6 minutos = 0.1 horas
ESCENARIO_ACTUAL_C = 16
COSTO_ACTUAL_REPORTADO = 1120.0  # USD / hora reportado por el aeropuerto


def calcular_metricas_mmc(c: int,
                          lam: float = DEFAULT_LAMBDA,
                          mu: float = DEFAULT_MU,
                          cs: float = COSTO_VENTANILLA,
                          cw: float = COSTO_ESPERA) -> Dict[str, Any]:
    """
    Calcula todas las métricas de desempeño y costos para un modelo M/M/c.
    
    Parámetros:
    -----------
    c : int -> Número entero de ventanillas abiertas
    lam : float -> Tasa de llegada de pasajeros (lambda)
    mu : float -> Tasa de atención por ventanilla (mu)
    cs : float -> Costo de operación por ventanilla abierta ($/hora)
    cw : float -> Costo de penalización por espera ($/hora por pasajero)
    
    Retorna:
    --------
    dict con métricas analíticas exactas.
    """
    a = lam / mu  # Carga de tráfico ofrecida (180 / 15 = 12)
    rho = a / c   # Factor de utilización del sistema
    
    # Si c <= a (c <= 12), el sistema es inestable
    if rho >= 1.0:
        return {
            'c': c,
            'estable': False,
            'rho': rho,
            'p0': 0.0,
            'pw': 1.0,
            'lq': float('inf'),
            'wq_horas': float('inf'),
            'wq_minutos': float('inf'),
            'l_total': float('inf'),
            'w_total_horas': float('inf'),
            'costo_servicio': cs * c,
            'costo_espera': float('inf'),
            'costo_total': float('inf'),
            'cumple_restriccion': False,
            'mensaje': f'Inestable: utilización rho = {rho:.2f} >= 1. La cola crece indefinidamente.'
        }
    
    # 1. Cálculo de P0 (Probabilidad de que el sistema esté vacío)
    sum_terms = sum((a ** n) / math.factorial(n) for n in range(c))
    last_term = (a ** c) / (math.factorial(c) * (1.0 - rho))
    p0 = 1.0 / (sum_terms + last_term)
    
    # 2. Probabilidad de espera (Fórmula Erlang C, Pw)
    pw = last_term * p0
    
    # 3. Número promedio de pasajeros en cola (Lq)
    lq = (pw * rho) / (1.0 - rho)
    
    # 4. Tiempo promedio de espera en cola (Wq, Ley de Little)
    wq_horas = lq / lam
    wq_minutos = wq_horas * 60.0
    
    # 5. Medidas del sistema completo
    l_total = lq + a
    w_total_horas = wq_horas + (1.0 / mu)
    
    # 6. Costos del sistema
    costo_servicio = cs * c
    costo_espera = cw * lq
    costo_total = costo_servicio + costo_espera
    
    # 7. Cumplimiento de restricción (Wq <= 0.1 horas = 6 minutos)
    cumple_restriccion = wq_horas <= MAX_ESPERA_HORAS
    
    return {
        'c': c,
        'estable': True,
        'rho': rho,
        'utilizacion_pct': rho * 100.0,
        'p0': p0,
        'pw': pw,
        'lq': lq,
        'wq_horas': wq_horas,
        'wq_minutos': wq_minutos,
        'l_total': l_total,
        'w_total_horas': w_total_horas,
        'w_total_minutos': w_total_horas * 60.0,
        'costo_servicio': costo_servicio,
        'costo_espera': costo_espera,
        'costo_total': costo_total,
        'cumple_restriccion': cumple_restriccion,
        'mensaje': 'Estable y convergente.'
    }


def generar_tabla_analitica(rango_c: Optional[range] = None,
                             lam: float = DEFAULT_LAMBDA,
                             mu: float = DEFAULT_MU,
                             cs: float = COSTO_VENTANILLA,
                             cw: float = COSTO_ESPERA) -> List[Dict[str, Any]]:
    """
    Genera la tabla analítica completa para diferentes valores de ventanillas.
    Por defecto explora de c=12 a c=20.
    """
    if rango_c is None:
        rango_c = range(12, 21)
    
    tabla = []
    for c in rango_c:
        m = calcular_metricas_mmc(c, lam, mu, cs, cw)
        tabla.append(m)
    return tabla


def encontrar_optimo_analitico(rango_c: Optional[range] = None,
                               lam: float = DEFAULT_LAMBDA,
                               mu: float = DEFAULT_MU,
                               cs: float = COSTO_VENTANILLA,
                               cw: float = COSTO_ESPERA,
                               max_wq_horas: float = MAX_ESPERA_HORAS) -> Dict[str, Any]:
    """
    Encuentra la solución óptima que minimiza el costo total cumpliendo la restricción de servicio.
    """
    tabla = generar_tabla_analitica(rango_c, lam, mu, cs, cw)
    
    # Filtrar solo candidatos que sean estables y cumplan Wq <= max_wq_horas
    factibles = [fila for fila in tabla if fila['estable'] and fila['wq_horas'] <= max_wq_horas]
    
    if not factibles:
        raise ValueError("No se encontraron soluciones factibles en el rango evaluado.")
    
    # Seleccionar el que minimiza el costo total
    optimo = min(factibles, key=lambda f: f['costo_total'])
    
    # Comparativa con el escenario actual (16 ventanillas fijas)
    actual_reportado = COSTO_ACTUAL_REPORTADO
    actual_teorico = calcular_metricas_mmc(ESCENARIO_ACTUAL_C, lam, mu, cs, cw)
    
    ahorro_hora_reportado = actual_reportado - optimo['costo_total']
    ahorro_hora_teorico = actual_teorico['costo_total'] - optimo['costo_total']
    
    # Horas operativas anuales (asumiendo 16 horas pico/día * 365 días)
    HORAS_PICO_DIA = 16
    DIAS_ANO = 365
    HORAS_ANO = HORAS_PICO_DIA * DIAS_ANO
    
    return {
        'optimo': optimo,
        'actual_teorico': actual_teorico,
        'costo_actual_reportado': actual_reportado,
        'ahorro_hora_vs_reportado': ahorro_hora_reportado,
        'ahorro_hora_vs_teorico': ahorro_hora_teorico,
        'pct_ahorro_vs_reportado': (ahorro_hora_reportado / actual_reportado) * 100.0,
        'pct_ahorro_vs_teorico': (ahorro_hora_teorico / actual_teorico['costo_total']) * 100.0,
        'ahorro_diario_16h': ahorro_hora_reportado * HORAS_PICO_DIA,
        'ahorro_mensual_30d': ahorro_hora_reportado * HORAS_PICO_DIA * 30,
        'ahorro_anual': ahorro_hora_reportado * HORAS_ANO,
        'tabla': tabla
    }

