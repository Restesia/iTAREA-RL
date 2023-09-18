/*-----------------MAIN METHODS-----------------*/



function saveAllFile() {
    filename = nameFile();
    saveFile(resultData);
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

function saveConfig(nodes, tasks) {

    filename = nameFile()
    output = nodes + tasks
    saveFile(output)

}

/*-----------------AUX METHODS-----------------*/
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
