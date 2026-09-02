const fs = require('fs');
const path = require('path');

const data = JSON.parse(fs.readFileSync(path.join(__dirname, 'gasure_extracted_data.json'), 'utf-8'));

console.log("==========================================================");
console.log("   EXTRACCIÓN DE SECCIONES CRÍTICAS (DOC 6 & DOC 2)       ");
console.log("==========================================================");

const doc6Text = data["6_Fenómenos de Combustión en Llamas de Premezcla.pdf"] || "";

const startRetrollama = doc6Text.indexOf("LIMITE CRÍTICO DE RETROLLAMA");
if (startRetrollama !== -1) {
  console.log("\n--- SECCIÓN RETROLLAMA, DESPRENDIMIENTO Y PUNTAS AMARILLAS (DOC 6) ---");
  console.log(doc6Text.substring(startRetrollama, startRetrollama + 3500));
}

const doc2Text = data["2_Fenómenos de flujo de fluidos en sistemas de combustión gaseosos.pdf"] || "";
const startInyector = doc2Text.indexOf("Coeficientes de descarga según la geometría del inyector");
if (startInyector !== -1) {
  console.log("\n--- SECCIÓN COEFICIENTES DE DESCARGA DE INYECTOR (DOC 2) ---");
  console.log(doc2Text.substring(startInyector, startInyector + 2500));
}
