const fs = require('fs');
const path = require('path');

const data = JSON.parse(fs.readFileSync(path.join(__dirname, 'gasure_extracted_data.json'), 'utf-8'));

console.log("==========================================================");
console.log("   EXTRACCIÓN DETALLADA DE ECUACIONES GASURE (DOC 2 & 6)  ");
console.log("==========================================================");

function searchInDoc(docKey, terms) {
  const text = data[docKey] || "";
  console.log(`\n🔍 BUSCANDO EN: ${docKey}`);
  
  terms.forEach(term => {
    console.log(`\n--- Término: "${term}" ---`);
    const idxs = [];
    let pos = text.indexOf(term);
    while (pos !== -1) {
      idxs.push(pos);
      pos = text.indexOf(term, pos + 1);
    }
    
    console.log(`Encontradas ${idxs.length} ocurrencias.`);
    idxs.slice(0, 4).forEach((p, i) => {
      const start = Math.max(0, p - 100);
      const end = Math.min(text.length, p + 350);
      const snippet = text.substring(start, end).replace(/\s+/g, ' ').trim();
      console.log(`  [${i+1}] ... ${snippet} ...`);
    });
  });
}

searchInDoc("2_Fenómenos de flujo de fluidos en sistemas de combustión gaseosos.pdf", [
  "descarga", "inyector", "garganta", "Venturi", "Bernoulli"
]);

searchInDoc("6_Fenómenos de Combustión en Llamas de Premezcla.pdf", [
  "DESPRENDIMIENTO", "RETROLLAMA", "PUNTAS AMARILLAS", "velocidad", "aire primario"
]);
