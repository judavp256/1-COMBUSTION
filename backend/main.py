"""
Servidor API REST - Laboratorio Virtual de Combustión y Metrología NTC 2832-1 / 2832-2
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from physics.combustion_engine import (
    calculate_gas_flow_and_power,
    convert_air_cold_test_to_gas,
    calculate_venturi_entrainment
)
from physics.stability_emissions import (
    evaluate_flame_stability,
    estimate_co_emissions_and_efficiency
)
from statistics.metrology_engine import analyze_repeatability_and_labeling
from normativity.ntc2832_rules import check_full_ntc2832_compliance

app = FastAPI(
    title="API Laboratorio Virtual de Combustión para Gasodomésticos",
    description="Motor de Simulación Físico-Matemático y Metrología NTC 2832-1 / NTC 2832-2",
    version="1.0.0"
)

# Habilitar CORS para conexión con Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SimulationRequest(BaseModel):
    d_inj_mm: float = 1.15
    delta_p_mbar: float = 18.0
    gas_type: str = "G20_GAS_NATURAL"
    c_d: float = 0.90
    d_throat_mm: float = 12.0
    a_ports_mm2: float = 180.0
    h_pot_mm: float = 22.0
    declared_power_kw: float = 2.0
    is_oven: bool = False


class AirEquivalenceRequest(BaseModel):
    q_air_l_h: float = 140.0
    delta_p_air_mbar: float = 10.0
    delta_p_gas_mbar: float = 18.0
    gas_type: str = "G20_GAS_NATURAL"
    d_inj_mm: float = 1.15


class MetrologyRequest(BaseModel):
    power_measurements_kw: List[float]
    target_declared_kw: Optional[float] = None
    tolerance_pct: float = 8.0


@app.get("/")
def read_root():
    return {
        "status": "Servidor del Laboratorio Virtual de Combustión Operativo",
        "normas_aplicadas": ["NTC 2832-1 (5ta actualización)", "NTC 2832-2 (2da actualización)"],
        "modulos": ["Bernoulli Inyección", "Venturi Arrastre", "Equivalencia Neumática Aire-Gas", "R&R Estadístico", "Certificación NTC"]
    }


@app.post("/api/simulate")
def run_full_simulation(req: SimulationRequest):
    """
    Ejecuta una simulación completa de combustión: Potencia, Arrastre Venturi, Estabilidad, Emisiones y Verificación NTC.
    """
    # 1. Bernoulli e Inyección
    flow_power = calculate_gas_flow_and_power(req.d_inj_mm, req.delta_p_mbar, req.gas_type, req.c_d)
    
    # 2. Arrastre Venturi
    venturi = calculate_venturi_entrainment(
        flow_power["q_gas_l_h"], req.d_inj_mm, req.d_throat_mm, req.a_ports_mm2, req.gas_type
    )
    
    # 3. Estabilidad de Llama
    stability = evaluate_flame_stability(venturi["v_port_m_s"], venturi["lambda_primary"], req.gas_type)
    
    # 4. Emisiones y Eficiencia
    emissions = estimate_co_emissions_and_efficiency(
        flow_power["power_pcs_kw"], venturi["lambda_primary"], req.h_pot_mm, req.is_oven
    )
    
    # 5. Evaluación Normativa NTC 2832
    compliance = check_full_ntc2832_compliance(
        flow_power["power_pcs_kw"],
        req.declared_power_kw,
        emissions["co_neutral_ppm"],
        emissions["efficiency_pct"],
        stability["code"],
        req.is_oven
    )
    
    return {
        "input_parameters": req.dict(),
        "power_flow": flow_power,
        "venturi": venturi,
        "stability": stability,
        "emissions_efficiency": emissions,
        "ntc2832_compliance": compliance
    }


@app.post("/api/air-equivalence")
def run_air_equivalence(req: AirEquivalenceRequest):
    """
    Calcula la equivalencia neumática aire-gas a partir de prueba en frío.
    """
    return convert_air_cold_test_to_gas(
        req.q_air_l_h, req.delta_p_air_mbar, req.delta_p_gas_mbar, req.gas_type, req.d_inj_mm
    )


@app.post("/api/metrology-rr")
def run_metrology_analysis(req: MetrologyRequest):
    """
    Ejecuta el análisis R&R, detección de outliers y recomendación de rotulado.
    """
    try:
        return analyze_repeatability_and_labeling(
            req.power_measurements_kw, req.target_declared_kw, req.tolerance_pct
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
