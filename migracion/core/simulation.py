"""
Módulo de Simulación de Eventos Discretos con SimPy
===================================================
Simulación estocástica de colas de migración aeroportuaria:
- Llegadas de pasajeros según Proceso de Poisson (tiempos interarribo Exp(lambda))
- Tiempos de servicio por ventanilla distribuidos exponencialmente (Exp(mu))
- Recurso multicanal compartido: simpy.Resource con capacidad x (ventanillas)
- Registro cronológico de eventos para alimentar visualización en el dashboard
"""

import random
import simpy
from typing import Dict, Any, List
from .queue_theory import (
    DEFAULT_LAMBDA,
    DEFAULT_MU,
    COSTO_VENTANILLA,
    COSTO_ESPERA,
    MAX_ESPERA_HORAS
)


class SimulacionMigracionAeropuerto:
    def __init__(self,
                 num_ventanillas: int = 15,
                 tasa_llegada_lam: float = DEFAULT_LAMBDA,
                 tasa_servicio_mu: float = DEFAULT_MU,
                 costo_ventanilla: float = COSTO_VENTANILLA,
                 costo_espera: float = COSTO_ESPERA,
                 duracion_horas: float = 4.0,
                 seed: int = 42):
        """
        Inicializa el entorno de simulación SimPy.
        """
        self.num_ventanillas = num_ventanillas
        self.lam = tasa_llegada_lam
        self.mu = tasa_servicio_mu
        self.cs = costo_ventanilla
        self.cw = costo_espera
        self.duracion_horas = duracion_horas
        self.seed = seed
        
        # Registros estadísticos
        self.tiempos_espera_cola = []      # Wq para cada pasajero
        self.tiempos_servicio = []         # Ws para cada pasajero
        self.tiempos_sistema = []          # W total
        self.longitud_cola_tiempo = []     # (tiempo, longitud_cola)
        self.utilizacion_tiempo = []       # (tiempo, servidores_ocupados)
        self.log_eventos = []              # Para inspección y animación
        
        self.total_llegadas = 0
        self.total_atendidos = 0

    def proceso_pasajero(self, env: simpy.Environment, pasajero_id: int, ventanillas: simpy.Resource):
        """Ciclo de vida de un pasajero en la zona de migración."""
        tiempo_llegada = env.now
        self.total_llegadas += 1
        
        # Registrar estado de cola al momento de llegada
        longitud_actual = len(ventanillas.queue)
        self.longitud_cola_tiempo.append((tiempo_llegada, longitud_actual))
        self.utilizacion_tiempo.append((tiempo_llegada, ventanillas.count))
        
        if len(self.log_eventos) < 100:
            self.log_eventos.append({
                'evento': 'llegada',
                'id': pasajero_id,
                'tiempo_min': round(tiempo_llegada * 60, 2),
                'cola_espera': longitud_actual,
                'ventanillas_ocupadas': ventanillas.count
            })
            
        # Solicitar una ventanilla disponible
        with ventanillas.request() as req:
            yield req
            
            tiempo_inicio_servicio = env.now
            espera_cola = tiempo_inicio_servicio - tiempo_llegada
            self.tiempos_espera_cola.append(espera_cola)
            
            # Tiempo de servicio exponencial (media = 1/mu horas = 4 minutos)
            tiempo_atencion = random.expovariate(self.mu)
            self.tiempos_servicio.append(tiempo_atencion)
            
            if len(self.log_eventos) < 100:
                self.log_eventos.append({
                    'evento': 'inicio_atencion',
                    'id': pasajero_id,
                    'tiempo_min': round(tiempo_inicio_servicio * 60, 2),
                    'espera_min': round(espera_cola * 60, 2)
                })
                
            yield env.timeout(tiempo_atencion)
            
            tiempo_salida = env.now
            tiempo_total = tiempo_salida - tiempo_llegada
            self.tiempos_sistema.append(tiempo_total)
            self.total_atendidos += 1
            
            if len(self.log_eventos) < 100:
                self.log_eventos.append({
                    'evento': 'salida',
                    'id': pasajero_id,
                    'tiempo_min': round(tiempo_salida * 60, 2),
                    'tiempo_total_min': round(tiempo_total * 60, 2)
                })

    def generador_llegadas(self, env: simpy.Environment, ventanillas: simpy.Resource):
        """Generador continuo de llegadas Poisson."""
        pasajero_id = 1
        while True:
            # Intervalo exponencial entre llegadas (media = 1/lambda horas = 20 segundos)
            tiempo_interarribo = random.expovariate(self.lam)
            yield env.timeout(tiempo_interarribo)
            
            env.process(self.proceso_pasajero(env, pasajero_id, ventanillas))
            pasajero_id += 1

    def ejecutar(self) -> Dict[str, Any]:
        """Ejecuta la simulación completa y calcula métricas empíricas."""
        random.seed(self.seed)
        env = simpy.Environment()
        ventanillas = simpy.Resource(env, capacity=self.num_ventanillas)
        
        env.process(self.generador_llegadas(env, ventanillas))
        env.run(until=self.duracion_horas)
        
        # Métricas empíricas
        num_atendidos = len(self.tiempos_espera_cola)
        if num_atendidos > 0:
            wq_promedio_horas = sum(self.tiempos_espera_cola) / num_atendidos
            ws_promedio_horas = sum(self.tiempos_servicio) / num_atendidos
            w_total_promedio_horas = sum(self.tiempos_sistema) / len(self.tiempos_sistema) if self.tiempos_sistema else 0
            
            # Estimación de Lq mediante Ley de Little: Lq = lambda * Wq
            lq_estimado = self.lam * wq_promedio_horas
            
            # Utilización promedio de servidores
            utilizacion_promedio = (self.lam * ws_promedio_horas) / self.num_ventanillas
            
            # Costos simulados
            costo_servicio = self.cs * self.num_ventanillas
            costo_espera = self.cw * lq_estimado
            costo_total = costo_servicio + costo_espera
            
            cumple_restriccion = wq_promedio_horas <= MAX_ESPERA_HORAS
            
            # Porcentaje de pasajeros con espera menor a 6 minutos
            pasajeros_en_norma = sum(1 for w in self.tiempos_espera_cola if w <= MAX_ESPERA_HORAS)
            pct_en_norma = (pasajeros_en_norma / num_atendidos) * 100.0
        else:
            wq_promedio_horas = 0.0
            ws_promedio_horas = 0.0
            w_total_promedio_horas = 0.0
            lq_estimado = 0.0
            utilizacion_promedio = 0.0
            costo_servicio = self.cs * self.num_ventanillas
            costo_espera = 0.0
            costo_total = costo_servicio
            cumple_restriccion = False
            pct_en_norma = 0.0

        return {
            'num_ventanillas': self.num_ventanillas,
            'duracion_horas': self.duracion_horas,
            'total_llegadas': self.total_llegadas,
            'total_atendidos': num_atendidos,
            'wq_promedio_horas': wq_promedio_horas,
            'wq_promedio_minutos': wq_promedio_horas * 60.0,
            'ws_promedio_minutos': ws_promedio_horas * 60.0,
            'w_total_minutos': w_total_promedio_horas * 60.0,
            'lq_estimado': lq_estimado,
            'utilizacion_promedio_pct': utilizacion_promedio * 100.0,
            'costo_servicio': costo_servicio,
            'costo_espera': costo_espera,
            'costo_total': costo_total,
            'cumple_restriccion': cumple_restriccion,
            'pct_pasajeros_en_norma_6min': pct_en_norma,
            'log_eventos_muestra': self.log_eventos[:20],
            'codigo_simpy_fuente': self.obtener_codigo_fuente()
        }

    def obtener_codigo_fuente(self) -> str:
        return """import simpy
import random

def pasajero(env, id_p, ventanillas, tiempos_espera):
    llegada = env.now
    with ventanillas.request() as req:
        yield req
        espera = env.now - llegada
        tiempos_espera.append(espera)
        # Servicio exponencial con media 1/15 h = 4 min
        yield env.timeout(random.expovariate(15.0))

def generador_flujo(env, ventanillas, tiempos_espera):
    id_p = 1
    while True:
        # Llegadas Poisson con tasa lambda = 180 pas/h
        yield env.timeout(random.expovariate(180.0))
        env.process(pasajero(env, id_p, ventanillas, tiempos_espera))
        id_p += 1

# Entorno y recurso SimPy con x ventanillas abiertas
env = simpy.Environment()
x_ventanillas = 15  # Solución óptima
ventanillas = simpy.Resource(env, capacity=x_ventanillas)
tiempos_espera = []

env.process(generador_flujo(env, ventanillas, tiempos_espera))
env.run(until=4.0)  # Simular 4 horas pico

print(f"Espera promedio simulada: {sum(tiempos_espera)/len(tiempos_espera)*60:.2f} min")
"""


def ejecutar_simulacion_simpy(num_ventanillas: int = 15,
                              duracion_horas: float = 4.0,
                              seed: int = 42) -> Dict[str, Any]:
    """Helper directo para ejecutar la simulación."""
    sim = SimulacionMigracionAeropuerto(
        num_ventanillas=num_ventanillas,
        duracion_horas=duracion_horas,
        seed=seed
    )
    return sim.ejecutar()

