"""
Script para extraer texto e inspeccionar el contenido técnico de los PDFs 1 a 8 y NTC 2832
"""

import os
import sys

def parse_pdfs():
    workspace = os.path.dirname(os.path.abspath(__file__))
    pdf_files = [
        "1_Estimación de las propiedades de combustión de combustibles gaseosos (Falta numeración).pdf",
        "2_Fenómenos de flujo de fluidos en sistemas de combustión gaseosos.pdf",
        "3_Diagnóstico de combustión.pdf",
        "4_Diagnóstico de combustión 2.pdf",
        "5_ Fenómenos de combustión llama no premezclada.pdf",
        "6_Fenómenos de Combustión en Llamas de Premezcla.pdf",
        "7_Introducción a la turbulencia.pdf",
        "8_Problemas resueltos llamas no premezclada.pdf",
        "NTC-2832-1-5ta [2020-03-18].pdf",
        "NTC-2832-2-2da [2019-11-20].pdf"
    ]
    
    try:
        import pypdf
        print("Biblioteca 'pypdf' disponible.")
        for fname in pdf_files:
            fpath = os.path.join(workspace, fname)
            if os.path.exists(fpath):
                reader = pypdf.PdfReader(fpath)
                num_pages = len(reader.pages)
                print(f"\n--- FILE: {fname} ({num_pages} páginas) ---")
                text_sample = ""
                for p in range(min(3, num_pages)):
                    text_sample += reader.pages[p].extract_text() or ""
                print(text_sample[:400].replace('\n', ' '))
    except ImportError:
        print("pypdf no instalado. Intentando pypdf2 / pdfplumber...")
        try:
            import PyPDF2
            for fname in pdf_files:
                fpath = os.path.join(workspace, fname)
                if os.path.exists(fpath):
                    reader = PyPDF2.PdfReader(fpath)
                    print(f"\n--- FILE: {fname} ({len(reader.pages)} páginas) ---")
                    text_sample = reader.pages[0].extract_text() or ""
                    print(text_sample[:300].replace('\n', ' '))
        except ImportError:
            print("Instalar pypdf o pdfplumber")

if __name__ == "__main__":
    parse_pdfs()
