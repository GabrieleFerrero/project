var id_aggiornamento_dati;
var percorso = ""; //più il resto del percorso

/*creo un dizionario dati che contiene come chiave i nomi dei sensori e come valore gli 
ultimi dati richiesti al server*/
var dati = {
    "generale": "",
    "temperatura": 0,
    "giroscopio": "0#0#0"
};

//creo un dizionario dati che contiene come chiave i nomi dei sensori e come valore i loro canvas
var canvas_sensori = {
    "temperatura": ""
}
/*----------------FUNZIONI PER AGGIORNARE I DATI DELLA TABELLA NELLA PAGINA PRINCIPALE---------------- */
function aggiornaDati() {
    $.ajax({
        url: percorso+"dato/dati_attuali",
        type: "GET",
        dataType: "json",
        success: function(dati_sensori) {
            dati["generale"] = dati_sensori;
            aggiornaPagina(dati_sensori);
            
          }
      });
}

function aggiornaPaginaPrincipale(){
    aggiornaDati()
}

function inizializzazionePaginaPrincipale(id_della_stazione_meteorologica){
    calcolaPercorso(id_della_stazione_meteorologica)
    aggiornaPaginaPrincipale();
    id_aggiornamento_dati = setInterval(aggiornaPaginaPrincipale, 10000);
}

function inizializzazionePagineSensori(id_della_stazione_meteorologica, sensore, unita_di_misura){
    calcolaPercorso(id_della_stazione_meteorologica)
    onLoadSensore(sensore, unita_di_misura)
}

function aggiornaPagina(dati_sensori){
    paragrafo = document.getElementById("ora_dati");
    tblSensori = document.getElementById("tblSensori");
    tblSensori.innerHTML = "<tr><th class=\"thSensori\">Nome Sensore</th><th class=\"thSensori\">Valore</th></tr>";
    for(const [key, value] of Object.entries(dati_sensori)){
        if(key == "data_ora_stazione"){
            var data_paragrafo = value.split(":");
            if(data_paragrafo[1].length < 2){
                data_paragrafo[1] = "0" + data_paragrafo[1];
            }
            if(data_paragrafo[2].length < 2){
                data_paragrafo[2] = "0" + data_paragrafo[2];
            }
            paragrafo.innerHTML = "Dati aggiornati il "+data_paragrafo[0] + ":" + data_paragrafo[1] + ":" + data_paragrafo[2];
        }
        else{
            tblSensori.innerHTML += "<tr><td class=\"tdSensori\">"+key+"</td><td class=\"tdSensori\">+"+value+"</td></tr>"
        }
    }
    tblSensori.innerHTML += ""
}


/*------------------------------------------------------------------------------------------- */


/*---------------------FUNZIONE PER RICAVARE I DATI DI UN SENSORE-------------------------------- */
//Quando carico la pagina di uno dei sensori creo un primo canvas vuoto e chiedo i dati del sensore specifico
function onLoadSensore(sensore, unitaMisura){
    if(sensore != "giroscopio"){
         canvas_sensori[sensore] = new Chart(
    document.getElementById('grafico'),
    );
    ottieniDati(sensore, unitaMisura);
    }
    else{
        ottieniDatiGiroscopio();
        setInterval(ottieniDatiGiroscopio, 10000);
    }
    
}

function ottieniDatiGiroscopio(){
    $.ajax({
        url: percorso+"dato/giroscopio",
        type: "GET",
        dataType: "json",
        success: function(dati_sensori){
            console.log("Aggiornamento in immagine effettuato")
            dati["giroscopio"] = dati_sensori["dato_richiesto"][dati_sensori["dato_richiesto"].length -1];
            document.getElementById("valoreAttualeX").innerHTML = "X: "+dati["giroscopio"].split("#")[0]+"°/s";
            document.getElementById("valoreAttualeY").innerHTML = "Y: "+dati["giroscopio"].split("#")[1]+"°/s";
            document.getElementById("valoreAttualeZ").innerHTML = "Z: "+dati["giroscopio"].split("#")[2]+"°/s";
        }
});
//aggiornaImmagine();
}

//Ottengo i dati del sensore richiesti dal serer e chiamo la funzione per visualizzarli
function ottieniDati(sensore, unitaMisura){
    $.ajax({
        url: percorso+"dato/"+sensore,
        type: "GET",
        dataType: "json",
        success: function(dati_sensori) {
            if(sensore != "giroscopio"){
                dati[sensore] = dati_sensori;
                var dati_da_eliminare = [];
            
                for(let a = 0; a < dati[sensore]["dato_richiesto"].length; a++){
                    if(dati[sensore]["dato_richiesto"][a]== 9999.9 || dati[sensore]["dato_richiesto"][a]== 8888.8){
                      dati_da_eliminare.append(a);
                    }
                }
                for(let a = 0; a < dati_da_eliminare.length;a++){
                    delete dati[sensore]["dato_richiesto"][a];
                    delete dati[sensore]["data_ora_stazione"][a];
                }
                visualizzaDati(sensore, 'Valori '+sensore + "("+unitaMisura+")", unitaMisura);
            }
          
          }
      });
}

/*------------------------------------------------------------------------------------------- */

/*----------------FUNZIONI CHE VENGONO CHIAMATE PER POTER REALIZZARE I GRAFICI---------------------- */

function visualizzaDati(sensore, etichetta, unitaMisura){
    let dato_attuale = dati[sensore]["dato_richiesto"][dati[sensore]["dato_richiesto"].length - 1]
    document.getElementById("valoreAttuale").innerHTML = (Math.round(dato_attuale*10)/10) + unitaMisura;
    //formato = 2021/6/5 15.10.7
    //Questa funzione ritorna un array contenete i valori che devo rappresentare nel grafico
    var dati_necessari = opzioneSelezionata(dati[sensore]["data_ora_stazione"]);

    const labels = dati_necessari;
    const data = {
        labels: dati_necessari,
        datasets: [{
          label: etichetta,
          backgroundColor: 'rgb(255,140,20)',
          
          data: trovaDatiNecessari(sensore, dati_necessari.length),
          borderColor: function(context) {
            const chart = context.chart;
            const {ctx, chartArea} = chart;
    
            if (!chartArea) {
              // This case happens on initial chart load
              return null;
            }
            return getGradient(ctx, chartArea);
          },
        }]
      };
      const config = {
        type: 'line',
        data,
        options: {}
      };
      
      //Distruggo il vecchio canvas e ne creo un altro
      canvas_sensori[sensore].destroy();
      canvas_sensori[sensore] = new Chart(
      document.getElementById('grafico'),
      config
      );

}

let width, height, gradient;
function getGradient(ctx, chartArea) {
  const chartWidth = chartArea.right - chartArea.left;
  const chartHeight = chartArea.bottom - chartArea.top;
  if (gradient === null || width !== chartWidth || height !== chartHeight) {
    // Create the gradient because this is either the first render
    // or the size of the chart has changed
    width = chartWidth;
    height = chartHeight;
    gradient = ctx.createLinearGradient(0, chartArea.bottom, 0, chartArea.top);
    gradient.addColorStop(0, '#FBEF59');
    gradient.addColorStop(0.5, '#FF8C14');
    gradient.addColorStop(1, '#FF390D');
  }

  return gradient;
}

//Controllo quale delle seguenti opzioni e selezionati e ritorno l'array contentente di dati che mi interessano
function opzioneSelezionata(dati_sensori){
    var opzione = document.getElementById("arco_temporale").value;
    var mese = ricavaMese(dati_sensori);
    if(opzione == "optgiorno"){
        var oggi = dati_sensori[dati_sensori.length-1].split(" ")[0];
        return dati_sensori.filter(dato => dato.startsWith(oggi)).map(dato => dato.split(" ")[1]);
    }
    else if(opzione == "optmese"){
        return (mese.filter(dato => dato.split("-")[1]==dati_sensori[dati_sensori.length-1].split("-")[1])).map(dato => dato.split(" ")[0].split("-")[2]+"-"+dato.split("-")[1]);
    }
    else {
        return ricavaAnno(mese).map(dato => dato.split("-")[1]+"-"+dato.split("-")[0]);
    }
}
//Ricava tutti i mesi dei dati
function ricavaAnno(mese){
    dati_mensili = []
    if(mese.length > 0){dati_mensili.push(mese[0]);}
    for(let a = 0; a < mese.length; a++){
        if(mese[a].split("-")[1]!=dati_mensili[dati_mensili.length-1].split("-")[1]){
            dati_mensili.push(mese[a]);
        }
    }
    return dati_mensili;
}

//Ricava tutti i giorni del mese che sono stati registrati
function ricavaMese(dati_sensori){
    dati_finali = [];
    if(dati_sensori>=0){dati_finali.push(dati_sensori[0].split(" ")[0]);}
    for(let a = 0; a < dati_sensori.length; a++){
        if((dati_sensori[a].startsWith(dati_finali[dati_finali.length-1]))==false){
            dati_finali.push(dati_sensori[a].split(" ")[0]);
        }
    }
    return dati_finali;
}

//Trova i dati necessari in base al tipo di grafico che è stato selezionato
function trovaDatiNecessari(sensore, n_dati_necessari){
    var opzione = document.getElementById("arco_temporale").value;
    
    if(opzione == "optgiorno"){
        return dati[sensore]["dato_richiesto"].filter(dato => dati[sensore]["dato_richiesto"].indexOf(dato) >= dati[sensore]["dato_richiesto"].length-n_dati_necessari);
    }
    else if(opzione == "optmese"){
        dati_finali = calcolaMediaGiornaliera(sensore);
        return dati_finali.filter(dato => dati_finali.indexOf(dato) >= dati_finali.length - n_dati_necessari);
    }
    else {
        return dati_finali = calcolaMediaMensile(sensore);
    }
}

//Calcola la media giornaliera dei dati
function calcolaMediaGiornaliera(sensore){
    let somma = 0;
    let substringIniziale = "";
    let indice = 0;
    if (dati[sensore]["dato_richiesto"].length >=0){
        substringIniziale = dati[sensore]["data_ora_stazione"][0].split(" ")[0];
    }
    dati_finali = []
    for(let a = 0; a < dati[sensore]["dato_richiesto"].length; a++){
        if(dati[sensore]["data_ora_stazione"][a].startsWith(substringIniziale)){
            indice++;
            somma +=dati[sensore]["dato_richiesto"][a];
        }
        else{
            dati_finali.push(somma/indice);
            indice = 0;
            somma = 0;
            substringIniziale = dati[sensore]["data_ora_stazione"][a].split(" ")[0];
        }
    }
    dati_finali.push(somma/indice);
    return dati_finali;
}

//Calcola la media mensile dei dati
function calcolaMediaMensile(sensore){
    let somma = 0;
    let substringIniziale = "";
    let indice = 0;
    if (dati[sensore]["dato_richiesto"].length >=0){
        substringIniziale = dati[sensore]["data_ora_stazione"][0].split("-")[1];
    }
    dati_finali = []
    for(let a = 0; a < dati[sensore]["dato_richiesto"].length; a++){
        if(dati[sensore]["data_ora_stazione"][a].split("-")[1] == substringIniziale){
            indice++;
            somma +=dati[sensore]["dato_richiesto"][a];
        }
        else{
            console.log("Aggiungo il dato : " +somma)
            dati_finali.push(somma/indice);
            indice = 0;
            somma = 0;
            substringIniziale = dati[sensore]["data_ora_stazione"][a].split("-  ")[1];
        }
    }
    dati_finali.push(somma/indice);
    return dati_finali;
}

/*------------------------------------------------------------------------------------------ */

/*------------------FUNZIONI CHE COLORANO E DECOLORANO LE ICONE------------------------------*/
function coloraIcona(nome){
    var img = document.getElementById("img_"+nome).src = "/static/img/"+nome+"_red.png";
}

function decoloraIcona(nome){
    var img = document.getElementById("img_"+nome).src = "/static/img/"+nome+".png";
}
/*------------------------------------------------------------------------------------------ */

/*------------------FUNZIONI CHE SI OCCUPANO DEL GIROSCOPIO------------------------------*/
function salvaNuoveCoordinateGiroscopio(){
    console.log(dati["giroscopio"])
    return dati["giroscopio"].split("#");
}

function cambiaModelloImmagineGiroscopio(id_mostra, id_nascosto){
    document.getElementById(id_mostra).style.display = "block";
    document.getElementById(id_nascosto).style.display = "none";
}

/*------------------------------------------------------------------------------------------ */

function calcolaPercorso(numero_stazione){
    percorso = "/stazioni-meteorologiche/"+numero_stazione+"/"
    console.log(numero_stazione);
}