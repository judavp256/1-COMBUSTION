"""
Motor de Intercambiabilidad de Gases - Índices de Weaver y Diagrama de Delbourg
Basado en GASURE UdeA (Doc. 6 - Prof. Andrés Amell A.) y Normativa NTC 2832-1
"""

import math
from typing import Dict, Any

# Gas de Referencia Predeterminado: Gas Natural Comercial G20
REF_GAS = {
    "name": "Gas Natural G20 (Referencia)",
    "dr": 0.555,
    "pcs": 10.49,
    "sl": 0.38,
    "ch_ratio": 0.25, # C/H ratio para Metano CH4 (1/4)
    "wobbe": 10.49 / math.sqrt(0.555)
}

GAS_DATABASE = {
    "G20_GAS_NATURAL": REF_GAS,
    "G23_GAS_NATURAL_ALTO_CO2": {
        "name": "Gas Natural Rico en Inertes (G23)",
        "dr": 0.610,
        "pcs": 9.50,
        "sl": 0.36,
        "ch_ratio": 0.26,
        "wobbe": 9.50 / math.sqrt(0.610)
    },
    "G30_BUTANO": {
        "name": "Butano Comercial (G30)",
        "dr": 2.070,
        "pcs": 34.30,
        "sl": 0.40,
        "ch_ratio": 0.40, # C4H10 (4/10)
        "wobbe": 34.30 / math.sqrt(2.070)
    },
    "G31_PROPANO": {
        "name": "Propano Comercial (G31)",
        "dr": 1.550,
        "pcs": 25.99,
        "sl": 0.43,
        "ch_ratio": 0.375, # C3H8 (3/8)
        "wobbe": 25.99 / math.sqrt(1.550)
    }
}


def calculate_weaver_interchangeability(
    target_gas_key: str,
    ref_gas_key: str = "G20_GAS_NATURAL"
) -> Dict[str, Any]:
    """
    Calcula los 4 Índices de Intercambiabilidad de Weaver (I_L, I_F, I_Y, I_I)
    al sustituir el gas de referencia por un gas objetivo.
    """
    gas_ref = GAS_DATABASE.get(ref_gas_key, REF_GAS)
    gas_target = GAS_DATABASE.get(target_gas_key, GAS_DATABASE["G31_PROPANO"])
    
    # 1. Índice de Combustión Incompleta (I_I) - Relación de Wobbe
    i_incomplete = gas_target["wobbe"] / gas_ref["wobbe"]
    
    # 2. Índice de Retorno de Llama (I_F) - Flashback Index
    i_flashback = (gas_target["sl"] / gas_ref["sl"]) * math.sqrt(gas_ref["dr"] / gas_target["dr"])
    
    # 3. Índice de Desprendimiento / Soplado (I_L) - Lifting Index
    i_lifting = (gas_target["sl"] / gas_ref["sl"]) * math.sqrt(gas_ref["dr"] / gas_target["dr"]) * (gas_target["wobbe"] / gas_ref["wobbe"])
    
    # 4. Índice de Puntas Amarillas (I_Y) - Yellow Tip Index
    i_yellow = (gas_target["ch_ratio"] / gas_ref["ch_ratio"]) * math.sqrt(gas_ref["dr"] / gas_target["dr"])
    
    # Evaluación de Tolerancias Normativas Weaver / NTC 2832-1
    # Límites aceptables de intercambiabilidad segura:
    # I_I: 0.90 a 1.10
    # I_F: <= 1.20 (Si > 1.20 hay alto riesgo de retorno)
    # I_L: >= 0.80 (Si < 0.80 hay alto riesgo de soplado)
    # I_Y: <= 1.35 (Si > 1.35 hay riesgo de hollín)
    
    pass_incomplete = 0.90 <= i_incomplete <= 1.10
    pass_flashback = i_flashback <= 1.20
    pass_lifting = i_lifting >= 0.80
    pass_yellow = i_yellow <= 1.35
    
    interchangeable_direct = pass_incomplete and pass_flashback and pass_lifting and pass_yellow
    
    recommendation = "INTERCAMBIO DIRECTO PERMITIDO SIN CAMBIOS"
    if not interchangeable_direct:
        if "G31" in target_gas_key or "G30" in target_gas_key:
            recommendation = "REQUIERE CAMBIO DE INYECTOR (Conversión a GLP/Propano)"
        else:
            recommendation = "REQUIERE AJUSTE DE PRESIÓN O REGULACIÓN DE VENTURI"

    return {
        "reference_gas": gas_ref["name"],
        "target_gas": gas_target["name"],
        "weaver_indices": {
            "i_incomplete_combustion": round(i_incomplete, 3),
            "i_flashback_retrollama": round(i_flashback, 3),
            "i_lifting_desprendimiento": round(i_lifting, 3),
            "i_yellow_puntas_amarillas": round(i_yellow, 3)
        },
        "limits_eval": {
            "incomplete_ok": pass_incomplete,
            "flashback_ok": pass_flashback,
            "lifting_ok": pass_lifting,
            "yellow_tip_ok": pass_yellow
        },
        "is_direct_interchangeable": interchangeable_direct,
        "recommendation": recommendation
    }
