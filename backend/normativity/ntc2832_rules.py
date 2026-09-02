"""
Evaluador de Reglas de Certificación NTC 2832-1 y NTC 2832-2
"""

from typing import Dict, Any

def check_full_ntc2832_compliance(
    power_pcs_kw: float,
    declared_power_kw: float,
    co_neutral_ppm: float,
    efficiency_pct: float,
    flame_status_code: str,
    is_oven: bool = False
) -> Dict[str, Any]:
    """
    Realiza la evaluación normativa integral de un ensayo o simulación.
    """
    # 1. Tolerancia de Potencia Nominal (±8%)
    power_diff_pct = ((power_pcs_kw - declared_power_kw) / declared_power_kw) * 100.0
    power_pass = abs(power_diff_pct) <= 8.0
    
    # 2. Higiene de la Combustión (CO neutro <= 1000 ppm en cubiertas, <= 2000 ppm en hornos)
    max_co_ppm = 1000.0 if not is_oven else 2000.0
    co_pass = co_neutral_ppm <= max_co_ppm
    
    # 3. Rendimiento Térmico (>= 52% en cubiertas, >= 60% en hornos)
    min_eff = 52.0 if not is_oven else 60.0
    eff_pass = efficiency_pct >= min_eff
    
    # 4. Estabilidad de Llama
    flame_pass = flame_status_code == "OK"
    
    global_certified = power_pass and co_pass and eff_pass and flame_pass
    
    return {
        "global_certified": global_certified,
        "evaluations": {
            "power_nominal": {
                "measured_kw": power_pcs_kw,
                "declared_kw": declared_power_kw,
                "deviation_pct": round(power_diff_pct, 2),
                "tolerance_limit_pct": 8.0,
                "passed": power_pass
            },
            "co_emissions": {
                "co_neutral_ppm": co_neutral_ppm,
                "max_allowed_ppm": max_co_ppm,
                "passed": co_pass
            },
            "thermal_efficiency": {
                "efficiency_pct": efficiency_pct,
                "min_required_pct": min_eff,
                "passed": eff_pass
            },
            "flame_stability": {
                "status_code": flame_status_code,
                "passed": flame_pass
            }
        }
    }
