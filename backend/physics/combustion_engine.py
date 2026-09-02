"""
Motor Físico-Matemático de Combustión para Gasodomésticos
Modelo de Inyección y Transferencia Térmica GASURE (UdeA) - Prof. Andrés Amell A.
Basado en NTC 2832-1, NTC 2832-2 y Documentos de Investigación UdeA 1 a 8.
"""

import math
from typing import Dict, Any

# Propiedades Físicas Estándar de Gases (a T* = 15°C / 288.15 K, P* = 1013.25 mbar)
GAS_PROPERTIES = {
    "G20_GAS_NATURAL": {
        "name": "Gas Natural Comercial (G20)",
        "density_relative": 0.555,      # dr respecto al aire
        "pcs_kwh_m3": 10.49,             # PCS (kWh/m³ std)
        "pci_kwh_m3": 9.45,              # PCI (kWh/m³ std)
        "stoich_air_ratio": 9.52,        # m³ aire / m³ gas estequiométrico
        "laminar_speed_m_s": 0.38,       # S_L (m/s)
        "viscosity_pa_s": 1.10e-5
    },
    "G23_GAS_NATURAL_ALTO_CO2": {
        "name": "Gas Natural Rico en Inertes (G23)",
        "density_relative": 0.610,
        "pcs_kwh_m3": 9.50,
        "pci_kwh_m3": 8.56,
        "stoich_air_ratio": 8.60,
        "laminar_speed_m_s": 0.36,
        "viscosity_pa_s": 1.12e-5
    },
    "G30_BUTANO": {
        "name": "Butano Comercial (G30)",
        "density_relative": 2.070,
        "pcs_kwh_m3": 34.30,
        "pci_kwh_m3": 31.62,
        "stoich_air_ratio": 30.94,
        "laminar_speed_m_s": 0.40,
        "viscosity_pa_s": 0.74e-5
    },
    "G31_PROPANO": {
        "name": "Propano Comercial (G31)",
        "density_relative": 1.550,
        "pcs_kwh_m3": 25.99,
        "pci_kwh_m3": 23.95,
        "stoich_air_ratio": 23.81,
        "laminar_speed_m_s": 0.43,
        "viscosity_pa_s": 0.82e-5
    }
}

# Constantes Fundamentales (GASURE UdeA)
AIR_DENSITY_STD = 1.225      # kg/m³ a T* = 288.15 K, P* = 1013.25 mbar
P_STD_MBAR = 1013.25         # Presión Estándar (mbar)
T_STD_K = 288.15             # Temperatura Estándar (15°C en Kelvin)


def calculate_gasure_injection_and_power(
    d_inj_mm: float,
    delta_p_mbar: float,
    gas_type: str = "G20_GAS_NATURAL",
    c_d: float = 0.90,
    p_atm_mbar: float = 1013.25,
    t_site_c: float = 15.0
) -> Dict[str, Any]:
    """
    Ecuaciones exactas del Modelo UdeA - GASURE (Prof. Andrés Amell A. - Doc. 2):
    P_T = A * Cd * sqrt(2 * p / (rho_aire* * dr)) * (T*/T) * ((Patm + p) / P*) * PCS
    P_T = A * Cd * sqrt(2 * p / rho_aire*) * (T*/T) * ((Patm + p) / P*) * Wobbe
    """
    if gas_type not in GAS_PROPERTIES:
        raise ValueError(f"Gas no reconocido: {gas_type}")
        
    prop = GAS_PROPERTIES[gas_type]
    dr = prop["density_relative"]
    pcs = prop["pcs_kwh_m3"]
    pci = prop["pci_kwh_m3"]
    
    # Índice de Wobbe Superior (kWh/m³)
    wobbe_index = pcs / math.sqrt(dr)
    
    # Conversión de temperatura a Kelvin y presión a Pa
    t_site_k = t_site_c + 273.15
    delta_p_pa = delta_p_mbar * 100.0
    area_inj_m2 = (math.pi / 4.0) * ((d_inj_mm / 1000.0) ** 2)
    
    # Densidad del gas a condiciones de sitio (Ecuación 12 GASURE)
    # rho_sitio = ((Patm + delta_p) / P*) * (T* / T_sitio) * rho_aire* * dr
    pressure_ratio = (p_atm_mbar + delta_p_mbar) / P_STD_MBAR
    temp_ratio = T_STD_K / t_site_k
    rho_gas_site = pressure_ratio * temp_ratio * AIR_DENSITY_STD * dr
    
    # Velocidad de inyección teórica y real
    v_inj = math.sqrt((2.0 * delta_p_pa) / rho_gas_site)
    
    # Caudal Volumétrico Estándar Equivalente Q* (Ecuación 13 GASURE)
    # Q* = A * Cd * sqrt(2*p / (rho_aire* * dr)) * (T*/T) * ((Patm + p) / P*)
    v_ideal_std = math.sqrt((2.0 * delta_p_pa) / (AIR_DENSITY_STD * dr))
    q_std_m3_s = area_inj_m2 * c_d * v_ideal_std * temp_ratio * pressure_ratio
    q_std_m3_h = q_std_m3_s * 3600.0
    q_std_l_h = q_std_m3_h * 1000.0
    
    # Flujo másico de gas descargado (kg/h) (Ecuación 13' GASURE)
    m_dot_kg_h = c_d * area_inj_m2 * math.sqrt(2.0 * delta_p_pa * rho_gas_site) * 3600.0
    
    # Potencia Térmica Nominal Superior e Inferior (kW) (Ecuaciones 14 y 15 GASURE)
    power_pcs_kw = q_std_m3_h * pcs
    power_pci_kw = q_std_m3_h * pci
    
    return {
        "gas_name": prop["name"],
        "d_inj_mm": d_inj_mm,
        "delta_p_mbar": delta_p_mbar,
        "p_atm_mbar": p_atm_mbar,
        "t_site_c": t_site_c,
        "v_inj_m_s": round(v_inj, 2),
        "q_gas_std_l_h": round(q_std_l_h, 2),
        "q_gas_std_m3_h": round(q_std_m3_h, 4),
        "m_dot_kg_h": round(m_dot_kg_h, 4),
        "power_pcs_kw": round(power_pcs_kw, 3),
        "power_pci_kw": round(power_pci_kw, 3),
        "wobbe_index": round(wobbe_index, 2),
        "rho_gas_site_kg_m3": round(rho_gas_site, 4)
    }


def convert_air_cold_test_gasure(
    q_air_l_h: float,
    delta_p_air_mbar: float,
    delta_p_gas_mbar: float,
    gas_type: str = "G20_GAS_NATURAL",
    d_inj_mm: float = 1.15,
    c_d: float = 0.90
) -> Dict[str, Any]:
    """
    Equivalencia neumática basada en modelo impulsivo y dinámica de fluidos GASURE.
    """
    prop = GAS_PROPERTIES[gas_type]
    dr = prop["density_relative"]
    
    # Relación de caudales por conservación de momentum e incompresibilidad a baja presión
    q_gas_l_h_est = q_air_l_h * math.sqrt(1.0 / dr) * math.sqrt(delta_p_gas_mbar / delta_p_air_mbar)
    q_gas_m3_h_est = q_gas_l_h_est / 1000.0
    
    power_pcs_kw_est = q_gas_m3_h_est * prop["pcs_kwh_m3"]
    
    # Diámetro efectivo real de orificio
    v_air = math.sqrt((2.0 * delta_p_air_mbar * 100.0) / AIR_DENSITY_STD)
    area_eff_m2 = (q_air_l_h / 3600000.0) / (c_d * v_air)
    d_eff_mm = math.sqrt(area_eff_m2 * 4.0 / math.pi) * 1000.0
    
    return {
        "q_air_cold_l_h": q_air_l_h,
        "delta_p_air_mbar": delta_p_air_mbar,
        "delta_p_gas_mbar": delta_p_gas_mbar,
        "target_gas": prop["name"],
        "q_gas_est_l_h": round(q_gas_l_h_est, 2),
        "power_pcs_est_kw": round(power_pcs_kw_est, 3),
        "d_effective_mm": round(d_eff_mm, 3),
        "d_diff_pct": round(((d_eff_mm - d_inj_mm) / d_inj_mm) * 100.0, 2)
    }
