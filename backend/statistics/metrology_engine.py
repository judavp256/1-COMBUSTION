"""
Motor Estadístico y Metrológico Integrado (ISO 5725, GUM, NTC 2832-1)
Análisis de Repetibilidad, Reproducibilidad (R&R), Grubbs Outliers y Rotulado.
"""

import math
from typing import List, Dict, Any, Optional


def grubb_outlier_test(data: List[float], alpha: float = 0.05) -> Dict[str, Any]:
    """
    Test de Grubbs para detectar lecturas anómalas (outliers) en datos de ensayo.
    """
    n = len(data)
    if n < 3:
        return {"has_outlier": False, "cleaned_data": data, "outliers": []}
        
    mean = sum(data) / n
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in data) / (n - 1))
    
    if std_dev == 0:
        return {"has_outlier": False, "cleaned_data": data, "outliers": []}
        
    # Valor crítico G aproximado para alpha=0.05 (n entre 3 y 30)
    g_critical_table = {
        3: 1.153, 4: 1.463, 5: 1.672, 6: 1.822, 7: 1.938, 8: 2.032, 9: 2.110, 10: 2.176
    }
    g_crit = g_critical_table.get(n, 2.2 + 0.02 * (n - 10))
    
    max_diff = 0.0
    suspect_val = None
    for x in data:
        diff = abs(x - mean) / std_dev
        if diff > max_diff:
            max_diff = diff
            suspect_val = x
            
    is_outlier = max_diff > g_crit
    cleaned = [x for x in data if x != suspect_val] if is_outlier else data
    
    return {
        "has_outlier": is_outlier,
        "g_calculated": round(max_diff, 3),
        "g_critical": round(g_crit, 3),
        "outliers": [suspect_val] if is_outlier else [],
        "cleaned_data": cleaned
    }


def analyze_repeatability_and_labeling(
    power_measurements_kw: List[float],
    target_declared_kw: Optional[float] = None,
    tolerance_pct: float = 8.0
) -> Dict[str, Any]:
    """
    Analiza una serie de mediciones de potencia en laboratorio,
    evalúa la variabilidad estadística y recomienda el valor a rotular según NTC 2832-1.
    """
    outlier_res = grubb_outlier_test(power_measurements_kw)
    clean_data = outlier_res["cleaned_data"]
    n = len(clean_data)
    
    if n < 2:
        raise ValueError("Se requieren al menos 2 mediciones válidas para el análisis estadístico.")
        
    mean_val = sum(clean_data) / n
    variance = sum((x - mean_val) ** 2 for x in clean_data) / (n - 1)
    std_dev = math.sqrt(variance)
    cv_pct = (std_dev / mean_val) * 100.0 if mean_val > 0 else 0
    
    # Incertidumbre expandida Tipo A (k=2, 95% confianza)
    u_type_a = std_dev / math.sqrt(n)
    u_expanded_95 = 2.0 * u_type_a
    
    # Recomendación del valor nominal a rotular en la placa
    recommended_label_kw = round(mean_val, 2)
    min_allowed_kw = round(recommended_label_kw * (1.0 - (tolerance_pct / 100.0)), 3)
    max_allowed_kw = round(recommended_label_kw * (1.0 + (tolerance_pct / 100.0)), 3)
    
    # Verificación de cumplimiento si hay un valor declarado objetivo
    target_compliant = True
    if target_declared_kw is not None:
        lower_bound = target_declared_kw * (1.0 - (tolerance_pct / 100.0))
        upper_bound = target_declared_kw * (1.0 + (tolerance_pct / 100.0))
        if mean_val < lower_bound or mean_val > upper_bound:
            target_compliant = False

    return {
        "n_samples_valid": n,
        "mean_power_kw": round(mean_val, 3),
        "std_dev_kw": round(std_dev, 4),
        "cv_repeatability_pct": round(cv_pct, 2),
        "expanded_uncertainty_95_kw": round(u_expanded_95, 4),
        "recommended_label_power_kw": recommended_label_kw,
        "tolerance_band_kw": [min_allowed_kw, max_allowed_kw],
        "target_declared_kw": target_declared_kw,
        "ntc2832_8pct_compliant": target_compliant,
        "outlier_analysis": outlier_res
    }
