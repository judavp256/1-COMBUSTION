# 🔥 Laboratorio Virtual de Combustión & Metrología
### Plataforma de Simulación Físico-Matemática y Certificación Normativa NTC 2832-1 / NTC 2832-2

Plataforma integral para el análisis, diseño, optimización y certificación técnica de sistemas de combustión atmosféricos para gasodomésticos residenciales (cubiertas, cocinas y hornos) a Gas Natural y Propano/GLP.

---

## 🧰 Módulos Incluidos

1. **Simulador R&D y Físico 0D/1D (`frontend/index.html`):**
   - Ecuaciones de Bernoulli e inyección corregidas por densidad de gas y presión atmosférica del sitio de ensayo.
   - Evaluación de arrastre Venturi, velocidad en puertos y límites de estabilidad (Llama Azul, Retorno/Flashback, Desprendimiento/Lifting, Puntas Amarillas).
   - Modelo de quenching térmico por recipientes, emisiones de CO neutro e indicador de eficiencia energética ($\eta\%$).
   - Dictamen automático de certificación NTC 2832-1 (Tolerancia $\pm 8\%$, CO $< 1000\text{ ppm}$, $\eta \ge 52\%$).

2. **🎯 Ventana de Operación Segura & DoE Virtual:**
   - Barrido matricial de $25 \times 25 = 625$ combinaciones paramétricas (Diámetro del Inyector vs Presión de Suministro).
   - Generación de Mapa de Calor 2D (Heatmap) con delimitación de la Zona Verde Apta NTC 2832.
   - Buscador automático del **Centroide de Diseño Óptimo** para máxima robustez ante variaciones de presión de gas.

3. **🔀 Matriz de Intercambiabilidad de Gases - Índices de Weaver:**
   - Evaluación de la sustitución entre familias de gas (G20, G23, G30, G31).
   - Cálculo de los 4 Índices de Weaver: Combustión Incompleta ($I_I$), Retrollama ($I_F$), Desprendimiento ($I_L$) y Puntas Amarillas ($I_Y$).

4. **🍞 Simulación 1D de Quemadores Tubulares de Horno:**
   - Distribución hidráulica de velocidad y presión puerto a puerto a lo largo del tubo quemador.
   - Cálculo del Porcentaje de Uniformidad de Llama.

5. **💨 Módulo de Equivalencia Neumática (Test de Aire Frío):**
   - Conversión de caudal de aire medido en banco frío de control de calidad a potencia nominal esperada con gas combustible ($Q_{air} \to Q_{gas}$).

6. **📊 Motor Estadístico & Metrología R&R (ISO 5725):**
   - Repetibilidad, test de Grubbs para outliers e Incertidumbre Expandida al 95% ($U_{95}$).
   - Recomendador del valor de potencia nominal a declarar en la placa de características según la banda del $\pm 8\%$.

7. **📄 Generador de Reportes Técnicos en Formato Artículo IEEE:**
   - Inyección dinámica de datos simulados/medidos en un plantilla en formato artículo científico IEEE (2 columnas, tipografía formal, encabezados numerados y tablas oficiales) para exportar o imprimir en PDF.

---

## 📁 Estructura del Proyecto

```
1-COMBUSTION/
├── frontend/
│   └── index.html               # Dashboard Web interactivo y Generador IEEE
├── backend/
│   ├── physics/
│   │   ├── combustion_engine.py # Ecuaciones de Bernoulli, altitud y potencia
│   │   ├── stability_emissions.py # Estabilidad de llama, CO y eficiencia
│   │   ├── doe_engine.py        # Barrido DoE 25x25 y punto óptimo
│   │   ├── interchangeability_engine.py # Índices de Weaver
│   │   └── oven_manifold_engine.py # Simulación 1D de hornos
│   ├── statistics/
│   │   └── metrology_engine.py  # ISO 5725 R&R, Grubbs e Incertidumbre
│   ├── normativity/
│   │   └── ntc2832_rules.py     # Reglas de certificación NTC 2832-1
│   ├── main.py                  # API REST con FastAPI
│   └── requirements.txt
├── gasure_extracted_data.json   # Base de datos de modelos teóricos extraída
└── README.md
```

---

## 🚀 Instalación y Uso

### Frontend (Dashboard Standalone)
No requiere instalación de servidores. Simplemente abre `frontend/index.html` en cualquier navegador moderno.

### Backend (API REST en Python)
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

---

## 📜 Normativa y Estándares de Referencia
- **NTC 2832-1:** Gasodomésticos para la cocción de alimentos. Aspectos de seguridad y métodos de ensayo.
- **NTC 2832-2:** Aspectos de uso racional de energía (URE) y eficiencia térmica.
- **ISO/IEC 17025:** Requisitos generales para la competencia de los laboratorios de ensayo y calibración.
