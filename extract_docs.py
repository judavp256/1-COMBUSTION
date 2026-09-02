"""
Script Extractor y Analizador de Documentos Universitarios (1 al 8) y Normas NTC 2832-1 / 2832-2.
"""

import os
import re

def scan_pdf_documents():
    docs_dir = os.path.dirname(os.path.abspath(__file__))
    files = [f for f in os.listdir(docs_dir) if f.endswith('.pdf')]
    print(f"Documentos PDF detectados ({len(files)}):")
    for f in sorted(files):
        size_mb = os.path.getsize(os.path.join(docs_dir, f)) / (1024 * 1024)
        print(f" -> {f} ({size_mb:.2f} MB)")

if __name__ == "__main__":
    scan_pdf_documents()
