const fs = require('fs');
const path = require('path');
const PDFParser = require('pdf-parse/lib/pdf-parse.js');

const files = [
  "1_Estimación de las propiedades de combustión de combustibles gaseosos (Falta numeración).pdf",
  "2_Fenómenos de flujo de fluidos en sistemas de combustión gaseosos.pdf",
  "3_Diagnóstico de combustión.pdf",
  "4_Diagnóstico de combustión 2.pdf",
  "5_ Fenómenos de combustión llama no premezclada.pdf",
  "6_Fenómenos de Combustión en Llamas de Premezcla.pdf",
  "7_Introducción a la turbulencia.pdf",
  "8_Problemas resueltos llamas no premezclada.pdf"
];

async function parseAll() {
  console.log("=== EXTRACCIÓN DE CONTENIDO TÉCNICO DE PDFS DE UNIVERSIDAD ===");
  for (const file of files) {
    const filePath = path.join(__dirname, file);
    if (fs.existsSync(filePath)) {
      try {
        const dataBuffer = fs.readFileSync(filePath);
        const data = await PDFParser(dataBuffer);
        console.log(`\n==================================================`);
        console.log(`📄 DOCUMENTO: ${file}`);
        console.log(`Páginas: ${data.numpages}`);
        console.log(`--------------------------------------------------`);
        const cleanText = data.text.replace(/\s+/g, ' ').trim();
        console.log(cleanText.substring(0, 600));
      } catch (err) {
        console.error(`Error leyendo ${file}:`, err.message);
      }
    }
  }
}

parseAll();
