//Limpiar la tabla primero
const removedata = ()=> {
    var delElements = document.getElementsByClassName("tr");
    var delElementsLength = delElements.length;
    if (delElementsLength !== 0){
        for (let j=0; j<delElementsLength;j++){
            let element=document.querySelector(".tr")
            element.remove();
        }
    }
}

//crear la tabla    
const createdata = (filter_data) => {
    const table = document.getElementById("tbody");
    for (var i=0; i<filter_data.length; i++){
        //Creamos la hilera por cada elemento de la lista y le damos un nombre de clase apra poder borrarla luego
        var hilera = document.createElement("tr")
        hilera.className = "tr";
        //Creamos los diferentes elementos de cada casilla
        let firstname = document.createElement("td");
        let lastname = document.createElement("td");
        let adminName = document.createElement("td");
        let serviceName = document.createElement("td");
        //añadimos los datos de cada persona
        firstname.innerHTML=filter_data[i]["firstName"];
        lastname.innerHTML=filter_data[i]["lastName"];
        if (filter_data[i]["accessLevels"]["projectAdmin"]){
            adminName.innerHTML="Admin";
        }
        let accesslevels = '';
        let services = filter_data[i]["services"];
        for (let element in services){
            const access = services[element]["serviceName"] + " : " + services[element]["access"];
            accesslevels = accesslevels + access + ", ";
        }
        serviceName.innerHTML=accesslevels;
        //Asociamos los elementos a su hilera padre y luego la hilera a la tabla 
        hilera.appendChild(firstname);
        hilera.appendChild(lastname);
        hilera.appendChild(adminName);
        hilera.append(serviceName);
        table.appendChild(hilera);
        }
    }



//Create CSV file
const createcsv = (filter_data) => {
    let csv = 'FirstName,LastName,AccesLevel,documentManagement,projectAdministration,fieldManagement,designCollaboration,modelCoordination,insight,plan,glue\n';
    for (let element in filter_data){
        //Metemos nombre y apellido
        csv = csv + filter_data[element]["firstName"] +","+filter_data[element]["lastName"]+",";
        //Metemos si es o no project Admin
        if(filter_data[element]['accessLevels']['projectAdmin'] === true) {
            csv = csv + "Admin,";
        } else {
            csv=csv+"Normal,";
        };
        //Verificamos todos los accesos
        const acceschecker = (accessName) => {
            let name = "";
            for(let access in filter_data[element]['services']){
                if (filter_data[element]['services'][access]["serviceName"]===accessName){
                    name = filter_data[element]['services'][access]["access"];
                }
            }
            return name
        }
        
        csv = csv + acceschecker("documentManagement") + "," + acceschecker("projectAdministration") + "," + acceschecker("fieldManagement") + "," + acceschecker("designCollaboration") + "," + acceschecker("modelCoordination") + "," + acceschecker("insight") + "," + acceschecker("plan") + "," + acceschecker("glue") + "\n";
    }
    //Eliminamos elemento de referencia anterior
    if (document.getElementById("reference")){
        let deleted = document.getElementById("reference");
        deleted.remove();
    }
    
    //Creamos la referencia para descargar el csv
    var hiddenElement = document.createElement('a');
    hiddenElement.id = "reference";
    hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(csv);
    hiddenElement.target = '_blank';
    hiddenElement.download = 'users.csv';
    var button = document.getElementById("csv");
    button.appendChild(hiddenElement);
}


//download csv file

const downcsv = () =>{
    var clickElement = document.getElementById("reference");
    clickElement.click();
}


async function loadUsers(event) {

    // Acemos la peticion de los datos de usuarios
    var documentId = event.currentTarget.id;
    var header = {'Content-Type': 'application/json','Content-ID': documentId};
    const response = await fetch('http://127.0.0.1:8000/Users/', {headers: header});
    const data = await response.json();
    const filter_data = await data['Users']['results'];

    await removedata();
    await createdata(filter_data);
    await createcsv(filter_data);

}