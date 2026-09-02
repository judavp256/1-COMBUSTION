"""
Motor de Estabilidad de Llama, Emisiones de CO Neutro y Rendimiento Térmico.
Cumplimiento normativo NTC 2832-1 y NTC 2832-2.
"""

import math
from typing import Dict, Any


def evaluate_flame_stability(
    v_port_m_s: float,
    lambda_primary: float,
    gas_type: str = "G20_GAS_NATURAL"
) -> Dict[str, Any]:
    """
    Evalúa la estabilidad de la llama en función de la velocidad en los puertos
    y la relación de aire primario.
    """
    # Velocidades de referencia promedio según familia de gas
    is_lpg = "G30" in gas_type or "G31" in gas_type
    s_l = 0.43 if is_lpg else 0.38
    
    # Límites críticos
    v_flashback_limit = s_l * 0.95
    v_lifting_limit = s_l * 4.20
    lambda_yellow_tip_limit = 0.45 if not is_lpg else 0.52
    
    status = "ESTABLE (LLAMA AZUL UNIFORME)"
    code = "OK"
    risk_level = "NINGUNO"
    
    if lambda_primary < lambda_yellow_tip_limit:
        status = "ALERTA: PUNTAS AMARILLAS / HOLLÍN (Deficiencia de Aire Primario)"
        code = "YELLOW_TIPPING"
        risk_level = "ALTO"
    elif v_port_m_s < v_flashback_limit:
        status = "PELIGRO: RETORNO DE LLAMA (Flashback a la Garganta Venturi)"
        code = "FLASHBACK"
        risk_level = "CRÍTICO"
    elif v_port_m_s > v_lifting_limit:
        status = "ALERTA: DESPRENDIMIENTO / SOPLADO DE LLAMA (Lifting)"
        code = "LIFTING"
        risk_level = "MEDIO"
        
    return {
        "status": status,
        "code": code,
        "risk_level": risk_level,
        "v_port_m_s": round(v_port_m_s, 3),
        "v_flashback_limit": round(v_flashback_limit, 3),
        "v_lifting_limit": round(v_lifting_limit, 3),
        "lambda_primary": round(lambda_primary, 3)
    }


def estimate_co_emissions_and_efficiency(
    power_kw: float,
    lambda_primary: float,
    h_pot_mm: float = 22.0,
    is_oven: bool = False
) -> Dict[str, Any]:
    """
    Estimación de emisiones de CO neutro (ppm corregido a 0% O2)
    y rendimiento térmico considerando el quenching térmico con la base del recipiente.
    """
    # Quenching por proximidad al recipiente (distancia crítica ~ 2.2 mm de dardo)
    h_critical_mm = 18.0
    h_factor = 1.0
    
    if h_pot_mm < h_critical_mm:
        # Incremento exponencial de CO por enfriamiento rápido de la llama
        h_factor = math.exp((h_critical_mm - h_pot_mm) / 3.0)
        
    # Estimación de CO neutro base (ppm)
    # CO neutro bajo aire adecuado ~ 150-250 ppm. Sube si lambda < 0.5 o hay quenching
    base_co = 180.0
    lambda_penalty = 1.0 if lambda_primary >= 0.55 else math.pow(0.55 / max(lambda_primary, 0.1), 2.2)
    
    co_neutral_ppm = base_co * lambda_penalty * h_factor
    
    # Rendimiento Térmico Estimado (%)
    # Depende de la altura de la parrilla y el exceso de aire
    base_efficiency = 58.5 if not is_oven else 72.0
    efficiency_pct = base_efficiency - (0.15 * max(0, h_pot_mm - 20.0)) - (5.0 * max(0, lambda_primary - 0.7))
    
    # Límites Normativos NTC 2832-1
    # CO neutro max = 1000 ppm (0.10% vol) en condiciones normales
    co_limit_ppm = 1000.0 if not is_oven else 2000.0
    min_eff_limit = 52.0 if not is_oven else 60.0
    
    co_compliant = co_neutral_ppm <= co_limit_ppm
    eff_compliant = efficiency_pct >= min_eff_limit
    
    return {
        "co_neutral_ppm": round(co_neutral_ppm, 1),
        "co_neutral_pct_vol": round(co_neutral_ppm / 10000.0, 4),
        "co_limit_ppm": co_limit_ppm,
        "co_compliant": co_compliant,
        "efficiency_pct": round(efficiency_pct, 2),
        "min_efficiency_limit": min_eff_limit,
        "efficiency_compliant": eff_compliant,
        "h_pot_mm": h_pot_mm,
        "quenching_risk": h_pot_mm < h_critical_mm
    }
