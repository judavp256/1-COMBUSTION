from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

doc = Document()

# ── Márgenes ajustados para caber en 2 páginas ─────────────────────────────
for section in doc.sections:
    section.top_margin    = Cm(1.8)
    section.bottom_margin = Cm(1.8)
    section.left_margin   = Cm(2.5)
    section.right_margin  = Cm(2.0)

# ── Colores ────────────────────────────────────────────────────────────────
AZUL      = RGBColor(0x1A, 0x3A, 0x5C)
VERDE     = RGBColor(0xD4, 0xED, 0xDA)
AMARILLO  = RGBColor(0xFF, 0xF3, 0xCD)
BLANCO    = RGBColor(0xFF, 0xFF, 0xFF)

def set_bg(cell, rgb):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'),   'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'),  f"{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}")
    tcPr.append(shd)

def header_row(table):
    """Solo el encabezado va en azul oscuro; las celdas de datos quedan blancas."""
    for cell in table.rows[0].cells:
        set_bg(cell, AZUL)
        for para in cell.paragraphs:
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in para.runs:
                run.bold = True
                run.font.size = Pt(8.5)
                run.font.color.rgb = BLANCO

def p_add(doc, text, bold=False, italic=False, size=10, align='justify', space_after=4, color=None):
    p = doc.add_paragraph()
    p.alignment = {'justify': WD_ALIGN_PARAGRAPH.JUSTIFY,
                   'center':  WD_ALIGN_PARAGRAPH.CENTER,
                   'left':    WD_ALIGN_PARAGRAPH.LEFT}[align]
    r = p.add_run(text)
    r.bold = bold; r.italic = italic; r.font.size = Pt(size)
    if color: r.font.color.rgb = color
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after  = Pt(space_after)
    return p

def heading(doc, text, size=11.5):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.bold = True; r.font.size = Pt(size); r.font.color.rgb = AZUL
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bot = OxmlElement('w:bottom')
    bot.set(qn('w:val'), 'single'); bot.set(qn('w:sz'), '4')
    bot.set(qn('w:space'), '3'); bot.set(qn('w:color'), '1A3A5C')
    pBdr.append(bot); pPr.append(pBdr)
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after  = Pt(4)

# ══════════════════════════════════════════════════════════════════════════════
# ENCABEZADO
# ══════════════════════════════════════════════════════════════════════════════
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("PLAN DE ENSAYOS — QUEMADOR ATMOSFÉRICO ABIERTO")
r.bold = True; r.font.size = Pt(14); r.font.color.rgb = AZUL
p.paragraph_format.space_after = Pt(2)

p_add(doc,
    "Objetivo: Encontrar la configuración que mejore la eficiencia térmica (≥ 62.5%) y reduzca el CO (≤ 450 ppm) "
    "sin modificar partes del quemador.",
    italic=True, size=9.5, space_after=6)

# ══════════════════════════════════════════════════════════════════════════════
# SECCIÓN 1: POR QUÉ ESTAS VARIABLES
# ══════════════════════════════════════════════════════════════════════════════
heading(doc, "1.  ¿POR QUÉ ESTAS TRES VARIABLES?")

tbl_v = doc.add_table(rows=4, cols=3)
tbl_v.style = 'Table Grid'
tbl_v.alignment = WD_TABLE_ALIGNMENT.CENTER
header_row(tbl_v)
for j, h in enumerate(["Variable", "¿Qué hace físicamente?", "Impacto esperado"]):
    tbl_v.rows[0].cells[j].paragraphs[0].add_run(h)

vars_data = [
    (
        "X₁ — Altura de la olla\n(H_pot, mm)\nSuplementos bajo la olla",
        "Controla cuánto calor llega a la olla. Si está muy cerca, la pared fría apaga la llama antes "
        "de que el CO se queme completamente (efecto «Thermal Quenching»). Si está muy lejos, el calor "
        "se pierde al ambiente antes de llegar al fondo de la olla.",
        "CRÍTICO para eficiencia y emisiones de CO. Es la variable más importante del ensayo."
    ),
    (
        "X₂ — Apertura de la ventana de aire\n(A_vent, %)\nCinta metálica de aluminio",
        "Controla cuánto aire primario entra al tubo venturi antes de la llama. Con poca apertura, "
        "hay poco oxígeno y la llama es amarilla y rica en CO. Con apertura total, la llama es azul "
        "y la combustión es completa.",
        "ALTO impacto en emisiones de CO. Medio-alto en eficiencia térmica."
    ),
    (
        "X₃ — Posición del inyector\n(x_inj, mm)\nDesplazamiento axial hacia atrás",
        "Al retirar el inyector de la garganta del tubo, el chorro de gas arrastra más aire antes "
        "de entrar al tubo. Es un ajuste fino de la mezcla gas-aire. Valor 0 = inyector a ras de "
        "la garganta. Valor positivo = inyector más alejado hacia atrás.",
        "MEDIO. Permite afinar la mezcla sin cambiar piezas."
    ),
]
for i, (var, desc, imp) in enumerate(vars_data):
    row = tbl_v.rows[i+1]
    for j, txt in enumerate([var, desc, imp]):
        cell = row.cells[j]
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.LEFT
        r = cell.paragraphs[0].add_run(txt)
        r.font.size = Pt(8.5)
        if j == 0: r.bold = True
        # Celdas de datos: fondo blanco (sin set_bg → Word default = blanco)

# ══════════════════════════════════════════════════════════════════════════════
# SECCIÓN 2: HIPÓTESIS
# ══════════════════════════════════════════════════════════════════════════════
heading(doc, "2.  HIPÓTESIS DE LOS ENSAYOS")

p_add(doc,
    "Antes de empezar, planteamos dos preguntas formales que los datos deberán responder "
    "(nivel de confianza estadística del 95%):", size=10, space_after=3)

tbl_h = doc.add_table(rows=5, cols=2)
tbl_h.style = 'Table Grid'
tbl_h.alignment = WD_TABLE_ALIGNMENT.CENTER
header_row(tbl_h)
tbl_h.rows[0].cells[0].paragraphs[0].add_run("Hipótesis")
tbl_h.rows[0].cells[1].paragraphs[0].add_run("Enunciado en términos simples")

hip_data = [
    ("H₀ para la Eficiencia (η)",
     "Ninguna de las tres variables cambia la eficiencia de forma significativa. "
     "Todos los ensayos darían el mismo resultado."),
    ("H₁ para la Eficiencia (η)  ✔ Lo que esperamos",
     "Al menos una variable SÍ afecta significativamente la eficiencia. "
     "Existe una combinación óptima que supera el 62.5%."),
    ("H₀ para las Emisiones de CO",
     "Ninguna de las variables cambia las emisiones de CO de forma significativa. "
     "Todos los ensayos darían el mismo nivel de CO."),
    ("H₁ para las Emisiones de CO  ✔ Lo que esperamos",
     "Al menos una variable SÍ reduce significativamente el CO. En especial, acercar demasiado "
     "la olla (X₁ muy bajo) generaría un pico de CO por apagado térmico de la llama."),
]
for i, (h, desc) in enumerate(hip_data):
    row = tbl_h.rows[i+1]
    row.cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.LEFT
    row.cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r0 = row.cells[0].paragraphs[0].add_run(h)
    r1 = row.cells[1].paragraphs[0].add_run(desc)
    r0.font.size = Pt(8.5); r0.bold = True
    r1.font.size = Pt(8.5)
    # Solo las filas H₁ reciben fondo verde; las H₀ quedan blancas
    if "esperamos" in h:
        set_bg(row.cells[0], VERDE)
        set_bg(row.cells[1], VERDE)

# ══════════════════════════════════════════════════════════════════════════════
# SECCIÓN 3: NIVELES DE CADA VARIABLE
# ══════════════════════════════════════════════════════════════════════════════
heading(doc, "3.  NIVELES DE CADA VARIABLE EN EL BANCO")

tbl_n = doc.add_table(rows=4, cols=6)
tbl_n.style = 'Table Grid'
tbl_n.alignment = WD_TABLE_ALIGNMENT.CENTER
header_row(tbl_n)
for j, h in enumerate(["Variable", "Mínimo extremo", "Bajo", "CENTRO (★)", "Alto", "Máximo extremo"]):
    tbl_n.rows[0].cells[j].paragraphs[0].add_run(h)

niv_data = [
    ["X₁  H_pot (mm)",  "11.5 mm", "12.5 mm", "14.0 mm ★", "15.5 mm", "16.5 mm"],
    ["X₂  Ventana (%)", "50%\n(mitad tapada)", "67%\n(1/3 tapada)", "83%\n(cinta leve) ★", "100%\n(abierta total)", "100%\n(abierta total)"],
    ["X₃  x_inj (mm)",  "0.0 mm\n(a ras)",    "1.0 mm",            "2.5 mm ★",            "4.0 mm",              "5.0 mm\n(muy retirado)"],
]
for i, row_d in enumerate(niv_data):
    row = tbl_n.rows[i+1]
    for j, val in enumerate(row_d):
        cell = row.cells[j]
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = cell.paragraphs[0].add_run(val)
        r.font.size = Pt(8.5)
        if j == 3:
            r.bold = True
            set_bg(cell, VERDE)   # Solo la columna CENTRO en verde; resto blanco

p_add(doc, "★ = Punto de inicio / configuración base del ensayo.", italic=True, size=8.5, space_after=4)

# ══════════════════════════════════════════════════════════════════════════════
# SECCIÓN 4: MATRIZ DE 15 ENSAYOS  (con columna Observaciones)
# ══════════════════════════════════════════════════════════════════════════════
heading(doc, "4.  MATRIZ DE 15 ENSAYOS — ORDEN DE EJECUCIÓN")

p_add(doc,
    "Ejecutar en el orden indicado. Aplicar el procedimiento de medición NTC 2832-1 en cada corrida. "
    "Registrar Y₁, Y₂ e Y₃ al finalizar cada ensayo y anotar observaciones en la última columna.",
    italic=True, size=9, space_after=3)

hdrs_m = ["N°", "Tipo", "X₁\nH_pot\n(mm)", "X₂\nVentana\n(%)", "X₃\nx_inj\n(mm)",
          "Y₁\nη (%)", "Y₂\nCO\n(ppm)", "Y₃\nPot.\n(kW)", "Observaciones"]

ensayos = [
    ["1",  "Factorial", "12.5", "67%",  "1.0", "", "", "", ""],
    ["2",  "Factorial", "15.5", "67%",  "1.0", "", "", "", ""],
    ["3",  "Factorial", "12.5", "100%", "1.0", "", "", "", ""],
    ["4",  "Factorial", "15.5", "100%", "1.0", "", "", "", ""],
    ["5",  "Factorial", "12.5", "67%",  "4.0", "", "", "", ""],
    ["6",  "Factorial", "15.5", "67%",  "4.0", "", "", "", ""],
    ["7",  "Factorial", "12.5", "100%", "4.0", "", "", "", ""],
    ["8",  "Factorial", "15.5", "100%", "4.0", "", "", "", ""],
    ["9",  "Axial",     "11.5", "83%",  "2.5", "", "", "", ""],
    ["10", "Axial",     "16.5", "83%",  "2.5", "", "", "", ""],
    ["11", "Axial",     "14.0", "50%",  "2.5", "", "", "", ""],
    ["12", "Axial",     "14.0", "100%", "2.5", "", "", "", ""],
    ["13", "Axial",     "14.0", "83%",  "0.0", "", "", "", ""],
    ["14", "Axial",     "14.0", "83%",  "5.0", "", "", "", ""],
    ["15", "CENTRO ★",  "14.0", "83%",  "2.5", "", "", "", ""],   # sin datos precargados
]

tbl_m = doc.add_table(rows=16, cols=9)
tbl_m.style = 'Table Grid'
tbl_m.alignment = WD_TABLE_ALIGNMENT.CENTER
header_row(tbl_m)
for j, h in enumerate(hdrs_m):
    tbl_m.rows[0].cells[j].paragraphs[0].add_run(h)

for i, row_d in enumerate(ensayos):
    row = tbl_m.rows[i+1]
    es_axial  = row_d[1] == "Axial"
    es_centro = "CENTRO" in row_d[1]
    for j, val in enumerate(row_d):
        cell = row.cells[j]
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = cell.paragraphs[0].add_run(val)
        r.font.size = Pt(8.5)
        # Colores solo para indicar tipo de punto; interior siempre legible
        if es_centro:
            r.bold = True
            set_bg(cell, VERDE)
        elif es_axial:
            set_bg(cell, AMARILLO)
        # Factoriales y celdas de resultados: fondo blanco

p_add(doc,
    "Verde ★ = Punto Central (configuración inicial de referencia).   "
    "Amarillo = Puntos Axiales (límites extremos del espacio de diseño).",
    italic=True, size=8.5, space_after=4)

# ══════════════════════════════════════════════════════════════════════════════
# SECCIÓN 5: CHECKLIST PARA CADA ENSAYO
# ══════════════════════════════════════════════════════════════════════════════
heading(doc, "5.  CHECKLIST PARA CADA ENSAYO")

checks = [
    "Verificar presión de gas = 20.0 mbar antes de arrancar.",
    "Configurar H_pot con suplementos calibrados bajo la olla. Verificar con calibrador Vernier.",
    "Configurar la ventana de aire con cinta metálica de aluminio. Verificar el área libre con regla.",
    "Configurar posición del inyector desplazándolo HACIA ATRÁS el valor indicado. "
    "Verificar con calibrador de profundidad.",
    "Aplicar el procedimiento de medición de eficiencia térmica según NTC 2832-1.",
    "Registrar CO (ppm) con la sonda de análisis de gases en la campana de muestreo.",
    "Anotar cualquier anomalía visual de la llama (color, inestabilidad, desprendimiento) "
    "en la columna 'Observaciones' de la tabla.",
]
for c in checks:
    p = doc.add_paragraph(style='List Number')
    r = p.add_run(c); r.font.size = Pt(9.5)
    p.paragraph_format.space_after  = Pt(2)
    p.paragraph_format.space_before = Pt(0)

# ── Guardar ──────────────────────────────────────────────────────────────────
output = r"C:\Users\User\Documents\Dev\1-COMBUSTION\DOE_Quemador_Tecnico_Resumido.docx"
doc.save(output)
print(f"Documento técnico resumido guardado en:\n{output}")
