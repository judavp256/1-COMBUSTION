const fs = require('fs');
const path = require('path');

const data = JSON.parse(fs.readFileSync(path.join(__dirname, 'gasure_extracted_data.json'), 'utf-8'));

console.log("=================================================================");
console.log("   ANÁLISIS DE FÓRMULAS Y CORRELACIONES UdeA (GASURE)            ");
console.log("=================================================================");

const keywords = [
  "Wobbe", "inyección", "inyector", "coeficiente de descarga", "arrastre",
  "venturi", "aire primario", "premezcla", "velocidad de llama", "retorno",
  "desprendimiento", "soplado", "puntas amarillas", "CO", "exceso de aire", "eficiencia"
];

for (const [docName, text] of Object.entries(data)) {
  console.log(`\n📄 --- ANALIZANDO: ${docName} (${text.length} chars) ---`);
  
  const lines = text.split('\n');
  const matchingSnippets = [];
  
  keywords.forEach(kw => {
    const regex = new RegExp(`([^.!?]*?\\b${kw}\\b[^.!?]*?[.!?])`, 'gi');
    let match;
    let count = 0;
    while ((match = regex.exec(text)) !== null && count < 3) {
      const snippet = match[0].replace(/\s+/g, ' ').trim();
      if (snippet.length > 30 && snippet.length < 250) {
        matchingSnippets.push(` [kw: ${kw}] -> ${snippet}`);
        count++;
      }
    }
  });

  console.log(` Muestras de términos clave encontrados (${matchingSnippets.length}):`);
  matchingSnippets.slice(0, 8).forEach(s => console.log(s));
}
