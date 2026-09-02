"""
Motor de Diseño de Experimentos Virtual (DoE) y Ventana de Operación Segura
Genera matrices paramétricas para eliminar el ensayo y error en el laboratorio.
"""

from typing import Dict, Any, List
from physics.combustion_engine import calculate_gasure_injection_and_power, calculate_venturi_entrainment
from physics.stability_emissions import evaluate_flame_stability, estimate_co_emissions_and_efficiency
from normativity.ntc2832_rules import check_full_ntc2832_compliance


def run_virtual_doe_sweep(
    d_inj_min: float = 0.80,
    d_inj_max: float = 1.50,
    p_sup_min: float = 10.0,
    p_sup_max: float = 30.0,
    steps: int = 20,
    gas_type: str = "G20_GAS_NATURAL",
    c_d: float = 0.90,
    d_throat_mm: float = 12.0,
    a_ports_mm2: float = 180.0,
    h_pot_mm: float = 22.0,
    declared_power_kw: float = 2.0,
    p_atm_mbar: float = 1013.25,
    is_oven: bool = False
) -> Dict[str, Any]:
    """
    Ejecuta un barrido matricial DoE completo (steps x steps) y determina
    la Ventana de Operación Segura (Zona Verde de Cumplimiento NTC 2832).
    """
    grid = []
    green_points = []
    
    d_step = (d_inj_max - d_inj_min) / (steps - 1)
    p_step = (p_sup_max - p_sup_min) / (steps - 1)
    
    for i in range(steps):
        d_inj = d_inj_min + (i * d_step)
        row = []
        for j in range(steps):
            p_sup = p_sup_min + (j * p_step)
            
            # 1. Inyección y Potencia UdeA
            flow = calculate_gasure_injection_and_power(d_inj, p_sup, gas_type, c_d, p_atm_mbar)
            
            # 2. Venturi
            venturi = calculate_venturi_entrainment(flow["q_gas_std_l_h"], d_inj, d_throat_mm, a_ports_mm2, gas_type)
            
            # 3. Estabilidad
            stability = evaluate_flame_stability(venturi["v_port_m_s"], venturi["lambda_primary"], gas_type)
            
            # 4. Emisiones y Eficiencia
            emissions = estimate_co_emissions_and_efficiency(flow["power_pcs_kw"], venturi["lambda_primary"], h_pot_mm, is_oven)
            
            # 5. Evaluación NTC 2832
            compliance = check_full_ntc2832_compliance(
                flow["power_pcs_kw"], declared_power_kw, emissions["co_neutral_ppm"], emissions["efficiency_pct"], stability["code"], is_oven
            )
            
            zone = "RED"
            if compliance["global_certified"]:
                zone = "GREEN"
                green_points.append({
                    "d_inj_mm": round(d_inj, 3),
                    "p_sup_mbar": round(p_sup, 2),
                    "power_kw": flow["power_pcs_kw"],
                    "co_ppm": emissions["co_neutral_ppm"],
                    "efficiency_pct": emissions["efficiency_pct"],
                    "margin_safety_pct": round(8.0 - abs(compliance["evaluations"]["power_nominal"]["deviation_pct"]), 2)
                })
            elif abs(compliance["evaluations"]["power_nominal"]["deviation_pct"]) <= 12.0 and emissions["co_neutral_ppm"] <= 1500.0:
                zone = "YELLOW"
                
            cell = {
                "d_inj_mm": round(d_inj, 3),
                "p_sup_mbar": round(p_sup, 2),
                "power_kw": flow["power_pcs_kw"],
                "co_ppm": emissions["co_neutral_ppm"],
                "efficiency_pct": emissions["efficiency_pct"],
                "zone": zone,
                "passed": compliance["global_certified"]
            }
            row.append(cell)
        grid.append(row)
        
    # Buscar el punto óptimo central dentro de la Zona Verde
    optimum_point = None
    if green_points:
        # Ordenar por máximo margen de seguridad
        green_points.sort(key=lambda x: x["margin_safety_pct"], reverse=True)
        optimum_point = green_points[0]

    return {
        "sweep_summary": {
            "total_points_evaluated": steps * steps,
            "green_compliant_points": len(green_points),
            "green_percentage": round((len(green_points) / (steps * steps)) * 100.0, 1),
            "optimum_recommended_design": optimum_point
        },
        "grid_matrix": grid
    }
