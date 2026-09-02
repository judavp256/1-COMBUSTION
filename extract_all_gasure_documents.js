const fs = require('fs');
const path = require('path');
const { PDFParse } = require('pdf-parse');

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

async function extractAll() {
  console.log("==========================================================");
  console.log("   EXTRACCIÓN DE DOCUMENTOS CIENTÍFICOS - GASURE UdeA     ");
  console.log("==========================================================");

  const results = {};

  for (const fileName of files) {
    const filePath = path.join(__dirname, fileName);
    if (!fs.existsSync(filePath)) {
      console.log(`❌ No se encontró: ${fileName}`);
      continue;
    }

    try {
      const buffer = fs.readFileSync(filePath);
      const parser = new PDFParse(new Uint8Array(buffer));
      const res = await parser.getText();
      
      const fullText = res.text;
      results[fileName] = fullText;

      console.log(`\n✅ Extraído: ${fileName}`);
      console.log(`   Longitud de Texto: ${fullText.length} caracteres`);
      console.log(`   Muestra del Contenido:`);
      console.log(`   "${fullText.substring(0, 350).replace(/\s+/g, ' ')}..."`);

    } catch (err) {
      console.error(`❌ Error al procesar ${fileName}:`, err.message);
    }
  }

  // Guardar todo el texto extraído en un JSON consolidado
  const outputPath = path.join(__dirname, 'gasure_extracted_data.json');
  fs.writeFileSync(outputPath, JSON.stringify(results, null, 2), 'utf-8');
  console.log(`\n🎉 Extracción completa guardada en: ${outputPath}`);
}

extractAll();
