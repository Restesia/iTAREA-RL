/*-----------------MAIN METHODS-----------------*/



function saveAllFile() {
    filename = nameFile();
    saveFile(resultData);
}

function saveAssignmentFile(){
    filename = nameFile();
    assignmentsText = getAssignment(resultData)
    saveFile(assignmentsText);
}

function saveConfigAndAssignmentFile(nodes_string, tasks_string){

    filename = nameFile();
    input = toStringInput(nodes_string, tasks_string);
    assignmentsText = getAssignment(resultData);
    result = input + "\n" + "\n" + assignmentsText;
    saveFile(result);

}

function savePDF() {
    filename = nameFile();
    print()
}

function saveInputConfig() {

    // Busca la línea que contiene la entrada que deseas
    var startIndex = resultData.indexOf("[[");
    var endIndex = resultData.indexOf("]]");

    if (startIndex !== -1 && endIndex !== -1) {
        var entradaRecortada = resultData.substring(startIndex, endIndex + 2);
        console.log(entradaRecortada)
        return entradaRecortada;
    } else {
        console.log("No se encontró la parte de la entrada que deseas.");
        return null; // Opcionalmente, puedes devolver null u otro valor predeterminado si la entrada no se encuentra
    }
}

function saveConfig(nodes_string, tasks_string) {

    filename = nameFile();
    const output = toStringInput(nodes_string, tasks_string);
    saveFile(output)

}

function toStringInput(nodes_string, tasks_string) {
    const nodes = JSON.parse(nodes_string);
    const tasks = JSON.parse(tasks_string);
    json_array = nodes.concat(tasks);
    const output = JSON.stringify(json_array);
    return output;
}

/*-----------------AUX METHODS-----------------*/

function getAssignment(resultData){

  var lines = resultData.split('\n');
  var assignment_text = "";
  for (var i = 0; i < lines.length; i++) {
    var linea = lines[i];
    if (linea.startsWith("Task") || linea.startsWith("CPU assigned")) {
      assignment_text += linea + "\n";
    }
  }
  return assignment_text;
}

function nameFile(){
    var now = new Date();
    var day = String(now.getDate()).padStart(2, "0");
    var month = String(now.getMonth() + 1).padStart(2, "0");
    var year = String(now.getFullYear()).slice(-2);
    var hours = String(now.getHours()).padStart(2, "0");
    var minutes = String(now.getMinutes()).padStart(2, "0");
    var filename = `${day}-${month}-${year}_${hours}.${minutes}.txt`;
    return filename
}

function saveFile(result){
    var blob = new Blob([result], { type: "text/plain" });
    var url = URL.createObjectURL(blob);
    var link = document.createElement("a");
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}
