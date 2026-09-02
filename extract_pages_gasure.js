const fs = require('fs');
const path = require('path');

const data = JSON.parse(fs.readFileSync(path.join(__dirname, 'gasure_extracted_data.json'), 'utf-8'));

function getPages(docKey, pageStart, pageEnd) {
  const text = data[docKey] || "";
  console.log(`\n==========================================================`);
  console.log(` 📖 EXTRAIENDO PÁGINAS ${pageStart} A ${pageEnd} DE: ${docKey}`);
  console.log(`==========================================================`);

  for (let p = pageStart; p <= pageEnd; p++) {
    const pageMarker = `-- ${p} of `;
    const idx = text.indexOf(pageMarker);
    if (idx !== -1) {
      const nextIdx = text.indexOf(`-- ${p+1} of `, idx);
      const pageText = nextIdx !== -1 ? text.substring(idx, nextIdx) : text.substring(idx, idx + 2500);
      console.log(`\n>>> PÁGINA ${p}:`);
      console.log(pageText.replace(/\s+/g, ' ').trim());
    } else {
      console.log(`Página ${p} no encontrada.`);
    }
  }
}

// Extraer páginas de Inestabilidad (Retrollama, Desprendimiento, Puntas Amarillas) de Doc 6
getPages("6_Fenómenos de Combustión en Llamas de Premezcla.pdf", 28, 36);

// Extraer páginas de Coeficiente de Descarga e Inyectores de Doc 2
getPages("2_Fenómenos de flujo de fluidos en sistemas de combustión gaseosos.pdf", 9, 13);
