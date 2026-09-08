"""
Evaluador de Reglas de Certificación NTC 2832-1 y NTC 2832-2
"""

from typing import Dict, Any

def get_ntc_power_tolerance(declared_power_kw: float, d_inj_mm: float = 1.0) -> Dict[str, Any]:
    """
    Tolerancias de Potencia según NTC 2832-1 (Numeral 7.3.1.2.1.2):
    - d_inj <= 0.3 mm: ±20%
    - 0.3 < d_inj <= 0.5 mm: ±10%
    - Qn <= 2.25 kW: ±8%
    - 2.25 < Qn <= 3.6 kW: ±0.177 kW (fijo)
    - Qn > 3.6 kW: ±5%
    """
    if declared_power_kw <= 0:
        return {"delta_kw": 0.0, "label": "±8.0%", "pct": 8.0}
        
    if d_inj_mm <= 0.30:
        pct = 20.0
        delta = declared_power_kw * 0.20
        label = "±20.0% (d ≤ 0.3mm)"
    elif d_inj_mm <= 0.50:
        pct = 10.0
        delta = declared_power_kw * 0.10
        label = "±10.0% (d ≤ 0.5mm)"
    elif declared_power_kw <= 2.25:
        pct = 8.0
        delta = declared_power_kw * 0.08
        label = "±8.0%"
    elif declared_power_kw <= 3.60:
        delta = 0.177
        pct = (delta / declared_power_kw) * 100.0
        label = "±0.177 kW (fijo NTC)"
    else:
        pct = 5.0
        delta = declared_power_kw * 0.05
        label = "±5.0%"
        
    return {"delta_kw": delta, "label": label, "pct": round(pct, 2)}


def check_full_ntc2832_compliance(
    power_pcs_kw: float,
    declared_power_kw: float,
    co_neutral_ppm: float,
    efficiency_pct: float,
    flame_status_code: str,
    d_inj_mm: float = 1.0,
    is_oven: bool = False
) -> Dict[str, Any]:
    """
    Realiza la evaluación normativa integral de un ensayo o simulación.
    """
    # 1. Tolerancia de Potencia Nominal (Escalonada según NTC 2832-1)
    tol = get_ntc_power_tolerance(declared_power_kw, d_inj_mm)
    power_diff_kw = power_pcs_kw - declared_power_kw
    power_diff_pct = (power_diff_kw / declared_power_kw) * 100.0 if declared_power_kw > 0 else 0.0
    power_pass = abs(power_diff_kw) <= (tol["delta_kw"] + 1e-4)
    
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
                "deviation_kw": round(power_diff_kw, 3),
                "tolerance_limit_pct": tol["pct"],
                "tolerance_label": tol["label"],
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
