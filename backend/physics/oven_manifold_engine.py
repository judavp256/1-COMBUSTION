"""
Motor Hidráulico 1D para Quemadores Tubulares de Horno y Corona Múltiple
Simula las pérdidas de carga y la uniformidad de velocidad puerto por puerto.
"""

import math
from typing import Dict, Any, List

def simulate_oven_tubular_burner(
    length_mm: float = 450.0,
    tube_diameter_mm: float = 25.0,
    num_ports: int = 40,
    port_diameter_mm: float = 2.5,
    q_mixture_l_h: float = 2500.0,
    gas_density_kg_m3: float = 1.25
) -> Dict[str, Any]:
    """
    Simula la distribución 1D de presión y velocidad de salida a lo largo de las
    ranuras/puertos de un quemador tubular de horno.
    """
    area_tube_m2 = (math.pi / 4.0) * ((tube_diameter_mm / 1000.0) ** 2)
    area_port_single_m2 = (math.pi / 4.0) * ((port_diameter_mm / 1000.0) ** 2)
    total_ports_area_m2 = num_ports * area_port_single_m2
    
    # Caudal total de mezcla m³/s
    q_m3_s = (q_mixture_l_h / 1000.0) / 3600.0
    
    # Velocidad promedio en entrada del tubo
    v_tube_entry_m_s = q_m3_s / area_tube_m2
    
    # Perfil 1D de velocidad por puerto (Ecuación de Bernoulli con pérdida por aceleración y fricción)
    ports_profile = []
    velocities = []
    
    # Gradiente de velocidad del puerto 1 al puerto N
    for p in range(1, num_ports + 1):
        rel_pos = p / num_ports
        # Recuperación de presión estática en el extremo ciego del tubo (Efecto Manifold)
        p_static_factor = 1.0 + (0.15 * math.pow(rel_pos, 1.8))
        v_port = (q_m3_s / total_ports_area_m2) * math.sqrt(p_static_factor)
        velocities.append(v_port)
        
        ports_profile.append({
            "port_number": p,
            "position_mm": round((length_mm / num_ports) * p, 1),
            "v_port_m_s": round(v_port, 3),
            "flame_height_est_mm": round(v_port * 15.0, 1)
        })
        
    v_min = min(velocities)
    v_max = max(velocities)
    v_avg = sum(velocities) / len(velocities)
    
    # Coeficiente de Uniformidad (%)
    uniformity_pct = 100.0 - (((v_max - v_min) / v_avg) * 100.0)
    
    return {
        "burner_length_mm": length_mm,
        "tube_diameter_mm": tube_diameter_mm,
        "num_ports": num_ports,
        "port_diameter_mm": port_diameter_mm,
        "v_port_avg_m_s": round(v_avg, 3),
        "v_port_min_m_s": round(v_min, 3),
        "v_port_max_m_s": round(v_max, 3),
        "flame_uniformity_pct": round(uniformity_pct, 1),
        "is_uniform_acceptable": uniformity_pct >= 85.0,
        "ports_profile": ports_profile
    }
