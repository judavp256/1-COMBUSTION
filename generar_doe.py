from docx import Document
from docx.shared import Pt, Cm, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import copy

doc = Document()

# ── Márgenes ──────────────────────────────────────────────────────────────────
for section in doc.sections:
    section.top_margin    = Cm(2.5)
    section.bottom_margin = Cm(2.5)
    section.left_margin   = Cm(3.0)
    section.right_margin  = Cm(2.5)

# ── Helpers ───────────────────────────────────────────────────────────────────
AZUL_OSCURO  = RGBColor(0x1A, 0x3A, 0x5C)
AZUL_CLARO   = RGBColor(0xDE, 0xEA, 0xF4)
VERDE_CLARO  = RGBColor(0xD4, 0xED, 0xDA)
AMARILLO     = RGBColor(0xFF, 0xF3, 0xCD)
BLANCO       = RGBColor(0xFF, 0xFF, 0xFF)
GRIS_FILA    = RGBColor(0xF2, 0xF2, 0xF2)

def set_cell_bg(cell, rgb: RGBColor):
    tc   = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd  = OxmlElement('w:shd')
    hex_color = f"{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}"
    shd.set(qn('w:val'),   'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'),  hex_color)
    tcPr.append(shd)

def cell_font(cell, bold=False, size=10, color=None, center=False):
    for para in cell.paragraphs:
        if center:
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in para.runs:
            run.bold      = bold
            run.font.size = Pt(size)
            if color:
                run.font.color.rgb = color
        if not para.runs and para.text:
            run = para.runs[0] if para.runs else para.add_run(para.text)
            run.bold      = bold
            run.font.size = Pt(size)
            if color:
                run.font.color.rgb = color

def add_heading(doc, text, level=1, color=AZUL_OSCURO, size=13):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(text)
    run.bold           = True
    run.font.size      = Pt(size)
    run.font.color.rgb = color
    # Subrayado por borde inferior en el párrafo
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'),   'single')
    bottom.set(qn('w:sz'),    '6')
    bottom.set(qn('w:space'), '4')
    bottom.set(qn('w:color'), f"{color[0]:02X}{color[1]:02X}{color[2]:02X}")
    pBdr.append(bottom)
    pPr.append(pBdr)
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after  = Pt(6)
    return p

def add_body(doc, text, bold=False, italic=False, size=11, justify=True):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY if justify else WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(text)
    run.bold        = bold
    run.italic      = italic
    run.font.size   = Pt(size)
    p.paragraph_format.space_after = Pt(6)
    return p

def add_bullet(doc, text, size=11):
    p = doc.add_paragraph(style='List Bullet')
    run = p.add_run(text)
    run.font.size = Pt(size)
    p.paragraph_format.space_after = Pt(3)
    return p

def add_formula(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text)
    run.italic    = True
    run.font.size = Pt(11)
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after  = Pt(6)
    return p

def style_header_row(table, rgb=AZUL_OSCURO):
    for cell in table.rows[0].cells:
        set_cell_bg(cell, rgb)
        for para in cell.paragraphs:
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in para.runs:
                run.bold           = True
                run.font.size      = Pt(9)
                run.font.color.rgb = BLANCO

def add_page_break(doc):
    doc.add_page_break()

# ══════════════════════════════════════════════════════════════════════════════
# PORTADA
# ══════════════════════════════════════════════════════════════════════════════
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("PLAN DE DISEÑO EXPERIMENTAL (DoE)")
run.bold = True; run.font.size = Pt(16); run.font.color.rgb = AZUL_OSCURO

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("OPTIMIZACIÓN DE EFICIENCIA TÉRMICA Y EMISIONES EN QUEMADOR ATMOSFÉRICO ABIERTO DOMÉSTICO")
run.bold = True; run.font.size = Pt(14); run.font.color.rgb = AZUL_OSCURO
p.paragraph_format.space_after = Pt(20)

doc.add_paragraph()

info = [
    ("Normativa de Referencia",      "NTC 2832-1  /  ISO 23550"),
    ("Tipo de Diseño",               "Diseño Central Compuesto (CCD) de Segundo Orden — 3 Factores"),
    ("Método de Análisis",           "Superficie de Respuesta (RSM) + Función de Deseabilidad Multiobjetivo"),
    ("Objetivo",                     "Incrementar Eficiencia Térmica ≥ 62.5%  |  CO ≤ 450 ppm"),
]
for label, val in info:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r1 = p.add_run(f"{label}: "); r1.bold = True; r1.font.size = Pt(11)
    r2 = p.add_run(val);          r2.font.size = Pt(11)
    p.paragraph_format.space_after = Pt(4)

doc.add_paragraph()
add_body(doc, "CONFIGURACIÓN BASE DEL QUEMADOR ENSAYADO", bold=True, justify=False).alignment = WD_ALIGN_PARAGRAPH.CENTER

datos_base = [
    "Diámetro del Inyector: 0.99 mm  |  Cd = 0.853",
    "Tubo Venturi Cónico: Ø10 mm → Ø12.7 mm  |  Longitud total: 57 mm",
    "Ventana de Aire Primario: 25.25 mm de longitud (desde x = 0, inicio garganta)",
    "Presión de Ensayo: 20.0 mbar  (Gas de Referencia G20 – NTC 2832-1)",
    "Resultado de Referencia Medido:  η ≈ 58.0 %  |  CO ≈ 260 ppm  |  H_pot actual = 14.0 mm",
]
for d in datos_base:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(d); r.font.size = Pt(10.5)
    p.paragraph_format.space_after = Pt(3)

doc.add_paragraph()

# Firmas
tbl = doc.add_table(rows=3, cols=2)
tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
tbl.style = 'Table Grid'
labels_firma = ["Elaborado por:", "Revisado por:", "Cargo:", "Cargo:", "Firma:", "Firma:"]
for i, row in enumerate(tbl.rows):
    for j, cell in enumerate(row.cells):
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(labels_firma[i*2+j])
        run.bold = (i == 0)
        run.font.size = Pt(10)
        cell.paragraphs[0].paragraph_format.space_after = Pt(18)

# ══════════════════════════════════════════════════════════════════════════════
# SECCIÓN 1: OBJETIVO
# ══════════════════════════════════════════════════════════════════════════════
add_page_break(doc)
add_heading(doc, "1.  OBJETIVO Y ALCANCE DEL ESTUDIO", level=1)

add_body(doc,
    "El presente plan de ensayos establece la metodología formal para el estudio sistemático de los factores "
    "geométricos y operativos del quemador atmosférico abierto descrito en la portada, con el propósito de "
    "identificar la configuración de diseño que maximice la eficiencia térmica y minimice las emisiones de "
    "monóxido de carbono (CO) dentro de los límites exigidos por la norma colombiana NTC 2832-1.")

add_body(doc,
    "Los resultados previos del laboratorio establecen las condiciones de referencia: eficiencia térmica medida "
    "de ≈ 58.0 % y concentración de CO de ≈ 260 ppm. El objetivo cuantificado del estudio es alcanzar una "
    "eficiencia ≥ 62.5 % sin superar el límite normativo de 1000 ppm de CO (con una meta técnica conservadora "
    "de ≤ 450 ppm).")

add_body(doc,
    "NOTA IMPORTANTE: Este diseño experimental permite encontrar el punto óptimo de operación con un número mínimo "
    "de ensayos (15 corridas), evitando el maquinado de prototipos innecesarios y reduciendo el tiempo total de "
    "desarrollo del producto.", bold=False, italic=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECCIÓN 2: FUNDAMENTACIÓN TEÓRICA
# ══════════════════════════════════════════════════════════════════════════════
add_heading(doc, "2.  FUNDAMENTACIÓN TEÓRICA DE LAS VARIABLES SELECCIONADAS", level=1)

add_body(doc,
    "Las tres variables de entrada del DoE fueron seleccionadas con base en la teoría de transferencia de calor, "
    "mecánica de fluidos de eyectores y cinética química de combustión, con soporte en los fundamentos de la "
    "NTC 2832-1. A continuación se documenta la relación física causal de cada variable con las respuestas de interés.")

# --- Variable 1 ---
add_heading(doc, "Variable 1 (X₁): Altura del Quemador a la Base de la Olla — H_pot (mm)", level=2, size=11)

add_body(doc, "¿Cómo se modifica en el banco?", bold=True)
add_body(doc,
    "Mediante suplementos o arandelas de espesor calibrado colocadas bajo la base de la olla sobre la parrilla "
    "de ensayo. Modificación en segundos, sin alterar ninguna parte del quemador.")

add_body(doc, "Relación teórica con la Eficiencia Térmica (η):", bold=True)
add_body(doc,
    "La tasa de transferencia de calor desde los productos de combustión hacia la base de la olla se rige por "
    "los mecanismos de convección forzada y radiación térmica:")
add_formula(doc,
    "q_útil = h · A_olla · (T_gases − T_olla)  +  ε · σ · A_olla · (T_gases⁴ − T_olla⁴)")
add_body(doc,
    "Al reducir H_pot, la trayectoria del chorro caliente de gases de combustión disminuye, el coeficiente de "
    "transferencia convectiva (h) aumenta por mayor velocidad de impacto, y se reduce la mezcla de los gases "
    "calientes con el aire frío ambiental lateral. El resultado neto es una mayor cantidad de calor absorbida "
    "por la olla y un incremento en la eficiencia térmica.")

add_body(doc, "Relación teórica con las Emisiones de CO:", bold=True)
add_body(doc,
    "La reacción de oxidación CO + ½O₂ → CO₂ es sensible a la temperatura según la cinética de Arrhenius. "
    "Si H_pot se reduce por debajo de la altura del cono interno de llama, la pared fría de la olla interrumpe "
    "abruptamente la zona de reacción, congelando la conversión CO→CO₂. Este fenómeno se denomina Thermal "
    "Quenching (Apagado Térmico) y genera picos de CO que pueden superar el límite normativo de 1000 ppm.")
add_body(doc, "Grado de Impacto Esperado: CRÍTICO — Variable dominante tanto sobre la eficiencia como sobre las emisiones.", bold=True, italic=True)

# --- Variable 2 ---
add_heading(doc, "Variable 2 (X₂): Apertura Efectiva de la Ventana de Aire Primario — A_vent (%)", level=2, size=11)

add_body(doc, "¿Cómo se modifica en el banco?", bold=True)
add_body(doc,
    "Mediante obturación parcial de la ventana de 25.25 mm con cinta metálica de aluminio de alta temperatura, "
    "aplicada desde los bordes de la ventana hacia el centro. Los niveles se expresan como porcentaje del área "
    "libre: 50%, 67%, 83%, 100%.")

add_body(doc, "Relación teórica con la Eficiencia Térmica (η) y las Emisiones de CO:", bold=True)
add_body(doc,
    "En un quemador atmosférico abierto, el caudal de aire primario succionado por el efecto eyector del chorro "
    "de gas depende del área efectiva de paso por la ventana:")
add_formula(doc, "ṁ_aire = Cd · A_vent · √( 2 · ρ_aire · ΔP_succión )")
add_body(doc,
    "La relación de aire primario (λ_prim) define el tipo de llama y la temperatura adiabática de combustión. "
    "El rango teórico óptimo para quemadores atmosféricos residenciales de tipo venturi es λ_prim ≈ 0.65 – 0.72:")

add_bullet(doc,
    "Si A_vent < 50% libre: déficit de aire primario (λ_prim < 0.55), llama rica en combustible no quemado, "
    "producción de hollín y aumento severo de emisiones de CO por combustión incompleta.")
add_bullet(doc,
    "Si A_vent ≥ 70% libre: el área deja de ser el cuello de botella, el quemador opera en el rango "
    "estequiométrico primario óptimo, temperatura adiabática de llama es máxima y las emisiones de CO son mínimas.")
add_body(doc, "Grado de Impacto Esperado: ALTO sobre emisiones de CO; MEDIO-ALTO sobre la eficiencia térmica.", bold=True, italic=True)

# --- Variable 3 ---
add_heading(doc, "Variable 3 (X₃): Posición Axial del Inyector respecto a la Garganta — x_inj (mm)", level=2, size=11)

add_body(doc, "¿Cómo se modifica en el banco?", bold=True)
add_body(doc,
    "Desplazando axialmente el inyector sobre su guía roscada o soporte deslizante. Los valores positivos (+mm) "
    "corresponden a alejar (retirar) el inyector hacia atrás, aumentando la distancia libre entre la punta del "
    "inyector y la entrada de la garganta de Ø10 mm. El valor 0.0 mm corresponde a la posición a ras de la entrada "
    "de la garganta.")

add_body(doc, "Relación teórica:", bold=True)
add_body(doc,
    "El chorro de gas genera un cono de expansión con ángulo de apertura natural θ ≈ 12°–15°. Al alejarse "
    "de la garganta (x_inj > 0), el chorro recorre una mayor distancia libre en contacto con el aire antes "
    "de entrar al tubo. Esta mayor distancia incrementa el área interfacial de cizallamiento entre el gas y "
    "el aire, aumentando el momento transferido al aire primario y, por consiguiente, el caudal de succión "
    "(λ_prim aumenta). Existe un límite físico: si x_inj supera la distancia crítica (≈ 5–6 mm para este "
    "inyector), parte del gas se derrama al exterior reduciendo la eficiencia de inducción.")
add_body(doc, "Grado de Impacto Esperado: MEDIO — Permite ajuste fino de λ_prim sin restricciones geométricas.", bold=True, italic=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECCIÓN 3: HIPÓTESIS
# ══════════════════════════════════════════════════════════════════════════════
add_page_break(doc)
add_heading(doc, "3.  HIPÓTESIS ESTADÍSTICAS DEL ESTUDIO", level=1)

add_body(doc,
    "El análisis estadístico se realizará mediante Análisis de Varianza (ANOVA) con nivel de significancia "
    "α = 0.05 (95% de confianza estadística). Las hipótesis formales son:")

add_heading(doc, "3.1  Hipótesis para Y₁: Eficiencia Térmica (η %)", level=2, size=11)

tbl_h1 = doc.add_table(rows=3, cols=2)
tbl_h1.style = 'Table Grid'
style_header_row(tbl_h1)
hdr = tbl_h1.rows[0].cells
hdr[0].paragraphs[0].add_run("Hipótesis")
hdr[1].paragraphs[0].add_run("Enunciado")
filas_h1 = [
    ("H₀,η  (Nula)",
     "Ninguno de los factores de diseño (H_pot, A_vent, x_inj) ni sus interacciones o efectos cuadráticos "
     "tienen un efecto estadísticamente significativo sobre la eficiencia térmica. Todos los coeficientes del "
     "modelo de superficie de respuesta son iguales a cero:\n"
     "β₁ = β₂ = β₃ = β₁₁ = β₂₂ = β₃₃ = β₁₂ = β₁₃ = β₂₃ = 0"),
    ("H₁,η  (Alternativa)",
     "Al menos uno de los factores principales, sus interacciones o sus efectos cuadráticos tiene un efecto "
     "estadísticamente significativo sobre la eficiencia térmica. Existe curvatura en la superficie de respuesta "
     "(βᵢⱼ ≠ 0 para algún par i,j), lo que confirma la necesidad de un modelo de segundo orden para encontrar el óptimo."),
]
for i, (hip, desc) in enumerate(filas_h1):
    r = tbl_h1.rows[i+1]
    r.cells[0].paragraphs[0].add_run(hip).bold = True
    r.cells[1].paragraphs[0].add_run(desc)
    # Celdas de datos: fondo blanco
for row in tbl_h1.rows:
    for cell in row.cells:
        for para in cell.paragraphs:
            for run in para.runs:
                run.font.size = Pt(10)

doc.add_paragraph()

add_heading(doc, "3.2  Hipótesis para Y₂: Emisiones de Monóxido de Carbono (CO ppm)", level=2, size=11)

tbl_h2 = doc.add_table(rows=3, cols=2)
tbl_h2.style = 'Table Grid'
style_header_row(tbl_h2)
hdr2 = tbl_h2.rows[0].cells
hdr2[0].paragraphs[0].add_run("Hipótesis")
hdr2[1].paragraphs[0].add_run("Enunciado")
filas_h2 = [
    ("H₀,CO  (Nula)",
     "Ninguno de los factores de diseño ni sus interacciones tienen un efecto estadísticamente significativo "
     "sobre la concentración de emisiones de monóxido de carbono. Todos los coeficientes del modelo son "
     "iguales a cero: β₁ = β₂ = β₃ = β₁₁ = β₂₂ = β₃₃ = β₁₂ = β₁₃ = β₂₃ = 0"),
    ("H₁,CO  (Alternativa)",
     "Al menos uno de los factores tiene un efecto significativo sobre la concentración de CO. Se espera "
     "particularmente un efecto cuadrático significativo del factor H_pot (β₁₁ ≠ 0), asociado al fenómeno "
     "de Thermal Quenching que genera un pico de emisiones cuando H_pot se reduce por debajo de la altura "
     "crítica del cono de llama."),
]
for i, (hip, desc) in enumerate(filas_h2):
    r = tbl_h2.rows[i+1]
    r.cells[0].paragraphs[0].add_run(hip).bold = True
    r.cells[1].paragraphs[0].add_run(desc)
    # Celdas de datos: fondo blanco
for row in tbl_h2.rows:
    for cell in row.cells:
        for para in cell.paragraphs:
            for run in para.runs:
                run.font.size = Pt(10)

doc.add_paragraph()
add_body(doc,
    "Criterio de decisión: si el P-valor calculado en el ANOVA para un factor o interacción es P < 0.05, "
    "se rechaza la hipótesis nula y se confirma que dicho factor influye significativamente sobre la respuesta. "
    "El modelo final deberá cumplir R² ≥ 0.90.", italic=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECCIÓN 4: FACTORES Y NIVELES
# ══════════════════════════════════════════════════════════════════════════════
add_heading(doc, "4.  DEFINICIÓN DE FACTORES Y NIVELES DEL CCD", level=1)

headers4 = ["Factor", "Parámetro", "Nivel −α\n(Axial Mín)", "Nivel −1\n(Bajo)", "Nivel 0\n(Centro)", "Nivel +1\n(Alto)", "Nivel +α\n(Axial Máx)"]
rows4 = [
    ["X₁", "Altura a la Olla\nH_pot (mm)\n[Suplementos/arandelas]",       "11.5 mm", "12.5 mm", "14.0 mm *", "15.5 mm", "16.5 mm"],
    ["X₂", "Apertura Ventana Aire\nA_vent (%)\n[Cinta metálica aluminio]", "50 %",    "67 %",    "83 %",       "100 %",   "100 % **"],
    ["X₃", "Posición Inyector\nx_inj (mm)\n[Desplazamiento axial]",        "0.0 mm",  "1.0 mm",  "2.5 mm",     "4.0 mm",  "5.0 mm"],
]
tbl4 = doc.add_table(rows=len(rows4)+1, cols=len(headers4))
tbl4.style = 'Table Grid'
style_header_row(tbl4)
for j, h in enumerate(headers4):
    tbl4.rows[0].cells[j].paragraphs[0].add_run(h)
for i, row_data in enumerate(rows4):
    row = tbl4.rows[i+1]
    for j, val in enumerate(row_data):
        cell = row.cells[j]
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = cell.paragraphs[0].add_run(val)
        r.font.size = Pt(9.5)
        if j == 4:  # Columna Centro
            r.bold = True
            set_cell_bg(cell, VERDE_CLARO)
        # Resto de celdas: fondo blanco
doc.add_paragraph()
add_body(doc, "* Punto Central = Configuración de inicio del espacio de diseño experimental.", italic=True, size=10)
add_body(doc, "** El nivel axial máximo de X₂ coincide con el nivel +1 ya que el 100% representa el límite físico absoluto.", italic=True, size=10)

# ══════════════════════════════════════════════════════════════════════════════
# SECCIÓN 5: MATRIZ EXPERIMENTAL
# ══════════════════════════════════════════════════════════════════════════════
add_page_break(doc)
add_heading(doc, "5.  MATRIZ DE ENSAYOS — PLAN DE EJECUCIÓN PARA EL TÉCNICO", level=1)

add_body(doc,
    "INSTRUCCIÓN AL TÉCNICO: Ejecutar los ensayos en el orden exacto indicado. El orden está aleatorizado "
    "para evitar sesgos por calentamiento progresivo del quemador o de los instrumentos. Registrar los valores "
    "medidos en las columnas Y₁, Y₂ e Y₃ inmediatamente después de cada ensayo. Estabilizar el quemador por "
    "mínimo 3 minutos antes de tomar cada medición.", italic=True)

headers5 = ["N°", "Tipo de Punto", "X₁\nH_pot\n(mm)", "X₂\nVentana\nAire (%)", "X₃\nPos. Inyector\n(mm)", "Y₁\nEficiencia\nη (%)", "Y₂\nCO\n(ppm)", "Y₃\nPotencia\n(kW)", "Observaciones"]
ensayos = [
    ["1",  "Factorial",                    "12.5", "67 %\n(1/3 tapada)",   "1.0\n(casi raz)", "", "", "", ""],
    ["2",  "Factorial",                    "15.5", "67 %\n(1/3 tapada)",   "1.0\n(casi raz)", "", "", "", ""],
    ["3",  "Factorial",                    "12.5", "100 %\n(abierta)",     "1.0\n(casi raz)", "", "", "", ""],
    ["4",  "Factorial",                    "15.5", "100 %\n(abierta)",     "1.0\n(casi raz)", "", "", "", ""],
    ["5",  "Factorial",                    "12.5", "67 %\n(1/3 tapada)",   "4.0\n(retirado)", "", "", "", ""],
    ["6",  "Factorial",                    "15.5", "67 %\n(1/3 tapada)",   "4.0\n(retirado)", "", "", "", ""],
    ["7",  "Factorial",                    "12.5", "100 %\n(abierta)",     "4.0\n(retirado)", "", "", "", ""],
    ["8",  "Factorial",                    "15.5", "100 %\n(abierta)",     "4.0\n(retirado)", "", "", "", ""],
    ["9",  "Axial (Lím. Mín X₁)",         "11.5", "83 %\n(cinta leve)",   "2.5\n(centro)",   "", "", "", ""],
    ["10", "Axial (Lím. Máx X₁)",         "16.5", "83 %\n(cinta leve)",   "2.5\n(centro)",   "", "", "", ""],
    ["11", "Axial (Lím. Mín X₂)",         "14.0", "50 %\n(mitad tapada)", "2.5\n(centro)",   "", "", "", ""],
    ["12", "Axial (Lím. Máx X₂)",         "14.0", "100 %\n(abierta)",     "2.5\n(centro)",   "", "", "", ""],
    ["13", "Axial (Lím. Mín X₃)",         "14.0", "83 %\n(cinta leve)",   "0.0\n(raz)",       "", "", "", ""],
    ["14", "Axial (Lím. Máx X₃)",         "14.0", "83 %\n(cinta leve)",   "5.0\n(muy retirado)", "", "", "", ""],
    ["15", "PUNTO CENTRAL\n(Base Actual)", "14.0", "83 %",                 "2.5\n(centro)",   "", "", "", ""],
]

tbl5 = doc.add_table(rows=len(ensayos)+1, cols=len(headers5))
tbl5.style = 'Table Grid'
style_header_row(tbl5)
for j, h in enumerate(headers5):
    tbl5.rows[0].cells[j].paragraphs[0].add_run(h)
    tbl5.rows[0].cells[j].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

for i, row_data in enumerate(ensayos):
    row = tbl5.rows[i+1]
    es_axial  = "Axial" in row_data[1]
    es_centro = "CENTRAL" in row_data[1]
    for j, val in enumerate(row_data):
        cell = row.cells[j]
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = cell.paragraphs[0].add_run(val)
        r.font.size = Pt(8.5)
        if es_centro:
            r.bold = True
            set_cell_bg(cell, VERDE_CLARO)
        elif es_axial:
            set_cell_bg(cell, AMARILLO)
        # Factoriales: fondo blanco

doc.add_paragraph()
add_body(doc, "Convención de colores de la tabla:", bold=True, size=10)
add_body(doc, "  Verde: Punto Central (Configuración Base de Referencia)   |   Amarillo: Puntos Axiales (Límites del Espacio de Diseño)", italic=True, size=10)

# ══════════════════════════════════════════════════════════════════════════════
# SECCIÓN 6: PROTOCOLO DE MEDICIÓN
# ══════════════════════════════════════════════════════════════════════════════
add_page_break(doc)
add_heading(doc, "6.  PROTOCOLO DE MEDICIÓN EN BANCO (NTC 2832-1)", level=1)

add_heading(doc, "6.1  Condiciones Estándar del Ensayo", level=2, size=11)
condiciones = [
    "Gas de ensayo: Gas Natural de Referencia G20 (Metano ≥ 99.5% pureza).",
    "Presión nominal de ensayo: 20.0 mbar ± 0.5 mbar (verificar con manómetro calibrado antes de cada corrida).",
    "Temperatura del agua inicial: T₁ = 15°C ± 2°C.",
    "Temperatura ambiente del laboratorio: 15°C – 25°C (registrar al inicio de cada ensayo).",
    "Presión barométrica del laboratorio: registrar el valor del barómetro al inicio de cada jornada de ensayos.",
]
for c in condiciones:
    add_bullet(doc, c)

add_heading(doc, "6.2  Procedimiento Paso a Paso por Ensayo", level=2, size=11)
pasos = [
    "Verificar la presión de suministro de gas en 20.0 mbar y registrar en la hoja de datos.",
    "Configurar el quemador según los valores de X₁, X₂ y X₃ indicados para el ensayo:\n"
    "   • X₁ (Altura H_pot): Colocar suplementos de la altura indicada bajo la olla. Verificar con calibrador Vernier.\n"
    "   • X₂ (Ventana de Aire): Aplicar cinta metálica desde los bordes hasta cubrir el porcentaje indicado. Verificar el área libre con regla o galga.\n"
    "   • X₃ (Posición Inyector): Desplazar el inyector la distancia indicada ALEJÁNDOLO de la garganta del tubo. Verificar con calibrador de profundidad.",
    "Aplicar el procedimiento de medición de eficiencia térmica según NTC 2832-1.",
    "Medir la concentración de CO en los productos de combustión usando la sonda de análisis de gases en la campana de muestreo. Expresar en ppm (base seca, referida a 0% O₂).",
    "Registrar Y₁ (Eficiencia Térmica), Y₂ (CO ppm) e Y₃ (Potencia kW) en la Tabla de la Sección 5 y en la Hoja de Registro de Campo. Anotar observaciones visuales de la llama.",
]
for i, paso in enumerate(pasos):
    p = doc.add_paragraph(style='List Number')
    r = p.add_run(paso); r.font.size = Pt(10.5)
    p.paragraph_format.space_after = Pt(4)

add_heading(doc, "6.3  Cálculo de la Eficiencia Térmica", level=2, size=11)
add_formula(doc,
    "η (%) = [ (m_agua · Cp_agua · ΔT)  +  (m_olla · Cp_olla · ΔT) ]  /  (V_gas_std · PCS)  ×  100 %")
add_body(doc, "Donde:")
terminos = [
    "m_agua = masa de agua en la olla normalizada (kg)",
    "Cp_agua = 4.186 kJ / (kg · °C)",
    "ΔT = T₂ − T₁  (°C)",
    "m_olla, Cp_olla = masa y calor específico del recipiente normalizado de ensayo",
    "V_gas_std = volumen de gas corregido a 15°C y 1013.25 mbar (m³)",
    "PCS = Poder Calorífico Superior del gas G20 (MJ/m³)",
]
for t in terminos:
    add_bullet(doc, t, size=10.5)

# ══════════════════════════════════════════════════════════════════════════════
# SECCIÓN 7: ANÁLISIS ESTADÍSTICO
# ══════════════════════════════════════════════════════════════════════════════
add_heading(doc, "7.  PLAN DE ANÁLISIS ESTADÍSTICO DE RESULTADOS", level=1)

add_heading(doc, "7.1  Modelo de Superficie de Respuesta (Segundo Orden)", level=2, size=11)
add_body(doc,
    "Una vez completados los 15 ensayos, los datos se procesarán mediante el siguiente modelo polinomial "
    "de segundo orden (Metodología de Superficie de Respuesta — RSM):")
add_formula(doc,
    "Y = β₀ + β₁X₁ + β₂X₂ + β₃X₃ + β₁₁X₁² + β₂₂X₂² + β₃₃X₃² + β₁₂X₁X₂ + β₁₃X₁X₃ + β₂₃X₂X₃ + ε")
add_body(doc,
    "Este modelo se ajustará por separado para Y₁ (Eficiencia) y Y₂ (CO), generando las ecuaciones predictivas "
    "de ambas respuestas en función de los tres factores de diseño.")

add_heading(doc, "7.2  Criterios de Validación del Modelo", level=2, size=11)
headers7 = ["Criterio Estadístico", "Valor Requerido", "Interpretación"]
rows7 = [
    ["Coeficiente de Determinación (R²)", "≥ 0.90", "El modelo explica al menos el 90% de la variabilidad observada"],
    ["Falta de Ajuste (P-valor)",          "P > 0.05", "El modelo no presenta falta de ajuste significativa"],
    ["P-Valor Factores Significativos",    "P < 0.05", "El factor o interacción tiene un efecto estadístico real sobre la respuesta"],
    ["R² Predictivo vs R² Ajustado",       "Diferencia < 0.20", "El modelo no está sobreajustado y predice correctamente nuevas observaciones"],
]
tbl7 = doc.add_table(rows=len(rows7)+1, cols=3)
tbl7.style = 'Table Grid'
style_header_row(tbl7)
for j, h in enumerate(headers7):
    tbl7.rows[0].cells[j].paragraphs[0].add_run(h)
for i, row_data in enumerate(rows7):
    row = tbl7.rows[i+1]
    for j, val in enumerate(row_data):
        cell = row.cells[j]
        r = cell.paragraphs[0].add_run(val)
        r.font.size = Pt(10)
        if j != 0:
            cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        # Fondo blanco en celdas de datos

add_heading(doc, "7.3  Optimización por Función de Deseabilidad Multiobjetivo", level=2, size=11)
add_body(doc,
    "Se aplicará la Función de Deseabilidad de Derringer-Suich para optimizar simultáneamente ambas respuestas:")
metas = [
    "Y₁ (Eficiencia η): MAXIMIZAR — Meta: η ≥ 62.5 %",
    "Y₂ (CO ppm): MINIMIZAR — Meta: CO ≤ 450 ppm",
    "Y₃ (Potencia kW): MANTENER EN RANGO — Meta: 1.65 ≤ P ≤ 1.90 kW",
]
for m in metas:
    add_bullet(doc, m)
add_body(doc,
    "El resultado final será un conjunto de coordenadas (H_pot*, A_vent*, x_inj*) que representa la "
    "configuración de quemador que maximiza la deseabilidad global, definida como el punto donde η es "
    "máxima y CO es mínima simultáneamente.")

# ══════════════════════════════════════════════════════════════════════════════
# SECCIÓN 8: HOJA DE REGISTRO
# ══════════════════════════════════════════════════════════════════════════════
add_page_break(doc)
add_heading(doc, "8.  HOJA DE REGISTRO DE CAMPO — PARA USO DEL TÉCNICO EN BANCO", level=1)

add_body(doc,
    "Esta hoja debe imprimirse y llenarse durante la ejecución de cada ensayo. Al finalizar los 15 ensayos, "
    "entregar esta hoja al responsable del laboratorio para el análisis estadístico.", italic=True)

p = doc.add_paragraph()
for label in ["Fecha: _______________   ", "Técnico: _______________________   ", "Equipo de Gases: _______________"]:
    run = p.add_run(label); run.font.size = Pt(10)
p = doc.add_paragraph()
for label in ["Presión Barométrica Lab.: _______ mbar   ", "T° Ambiente: _______ °C   ", "Humedad Relativa: _______ %"]:
    run = p.add_run(label); run.font.size = Pt(10)

doc.add_paragraph()

headers8 = ["N°", "H_pot\n(mm)\nVerif.", "Ventana\n(% Libre)\nVerif.", "x_inj\n(mm)\nVerif.", "T₁\n(°C)", "T₂\n(°C)", "Δt\n(seg)", "V_gas\n(m³ std)", "η Y₁\n(%)", "CO Y₂\n(ppm)", "Pot. Y₃\n(kW)", "Observaciones"]
ensayos8 = [
    ["1","12.5","67%","1.0","","","","","","","",""],
    ["2","15.5","67%","1.0","","","","","","","",""],
    ["3","12.5","100%","1.0","","","","","","","",""],
    ["4","15.5","100%","1.0","","","","","","","",""],
    ["5","12.5","67%","4.0","","","","","","","",""],
    ["6","15.5","67%","4.0","","","","","","","",""],
    ["7","12.5","100%","4.0","","","","","","","",""],
    ["8","15.5","100%","4.0","","","","","","","",""],
    ["9","11.5","83%","2.5","","","","","","","",""],
    ["10","16.5","83%","2.5","","","","","","","",""],
    ["11","14.0","50%","2.5","","","","","","","",""],
    ["12","14.0","100%","2.5","","","","","","","",""],
    ["13","14.0","83%","0.0","","","","","","","",""],
    ["14","14.0","83%","5.0","","","","","","","",""],
    ["15","14.0","83%","2.5","","","","","","","",""],
]
tbl8 = doc.add_table(rows=len(ensayos8)+1, cols=len(headers8))
tbl8.style = 'Table Grid'
style_header_row(tbl8)
for j, h in enumerate(headers8):
    tbl8.rows[0].cells[j].paragraphs[0].add_run(h)
    tbl8.rows[0].cells[j].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

for i, row_data in enumerate(ensayos8):
    row = tbl8.rows[i+1]
    es_axial  = i >= 8 and i <= 13
    es_centro = i == 14
    for j, val in enumerate(row_data):
        cell = row.cells[j]
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = cell.paragraphs[0].add_run(val)
        r.font.size = Pt(8)
        if es_centro:
            r.bold = True
            set_cell_bg(cell, VERDE_CLARO)
        elif es_axial:
            set_cell_bg(cell, AMARILLO)

doc.add_paragraph()
p = doc.add_paragraph()
r = p.add_run("Firma del Técnico: ________________________________     Firma de Revisión: ________________________________")
r.font.size = Pt(10)

# ── Guardar ──────────────────────────────────────────────────────────────────
output_path = r"C:\Users\User\Documents\Dev\1-COMBUSTION\DOE_Quemador_Plan_Ensayos.docx"
doc.save(output_path)
print(f"Documento guardado exitosamente en:\n{output_path}")
