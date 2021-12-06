"""



   _____ _            _                    __  __      _                       _             _              _____ ______ _______      ________ _____  
  / ____| |          (_)                  |  \/  |    | |                     | |           (_)            / ____|  ____|  __ \ \    / /  ____|  __ \ 
 | (___ | |_ __ _ _____  ___  _ __   ___  | \  / | ___| |_ ___  ___  _ __ ___ | | ___   __ _ _  ___ __ _  | (___ | |__  | |__) \ \  / /| |__  | |__) |
  \___ \| __/ _` |_  / |/ _ \| '_ \ / _ \ | |\/| |/ _ \ __/ _ \/ _ \| '__/ _ \| |/ _ \ / _` | |/ __/ _` |  \___ \|  __| |  _  / \ \/ / |  __| |  _  / 
  ____) | || (_| |/ /| | (_) | | | |  __/ | |  | |  __/ ||  __/ (_) | | | (_) | | (_) | (_| | | (_| (_| |  ____) | |____| | \ \  \  /  | |____| | \ \ 
 |_____/ \__\__,_/___|_|\___/|_| |_|\___| |_|  |_|\___|\__\___|\___/|_|  \___/|_|\___/ \__, |_|\___\__,_| |_____/|______|_|  \_\  \/   |______|_|  \_\
                                                                                        __/ |                                                         
                                                                                       |___/                                                          



"""

""" _______________________INCLUSIONE LIBRERIE________________________"""

from flask import Flask, render_template, jsonify
import threading
from pathlib import Path
import logzero
import requests
import sqlite3
import time
from mega import Mega
import datetime
import os
import subprocess

""" //////////////////////////////////////////////////////////////// """


""" ______________________DEFINIZIONE VARIABILI_____________________ """

#           DELAY          #
SECONDI_TRA_AGGIORNAMENTO_DATI = 60*1
# ------------------------ #

#           LOCK           #
blocco_thread = threading.Lock()
# ------------------------ #

#   ACCESSO ACCOUNT MEGA   #
email = "..."
password = "..."
# ------------------------ #

#          SOCKET          #
SERVER_ADDRESS = "0.0.0.0"
SERVER_PORT = 4000
TIPO_SITO = "http"
# ------------------------ #

#    PERCORSO CARTELLA     #
dir_path = str(Path(__file__).parent.resolve())
print(dir_path)
# ------------------------ #

#      FILE PER ERRORI     #
file_info_error= logzero.setup_logger(name='file_info_error', logfile=f"{dir_path}/log/file_info_error.csv") 
# ------------------------ #

#      DATI STAZIONI       #
stazioni_elenco_ID = []
stazioni_sensori = {}
stazioni_address = {}
elenco_tipi_dati_sensori = {}
# ------------------------ #

#     OPZIONI POSSIBILI    #
altre_opzioni = ["dati_attuali"]
# ------------------------ #

#            DATI          #
dati_raggruppati_annuali = {}
dati_raggruppati_attuali = {}
# ------------------------ #
""" //////////////////////////////////////////////////////////////// """



""" ____________________DEFINIZIONI ROUTE FLASK_____________________ """

app = Flask(__name__)

@app.route("/stazioni-meteorologiche/<numero_stazione>/html/<pagina_richiesta>")
def inviaPagina(numero_stazione, pagina_richiesta):
    try:
        numero_stazione = int(numero_stazione)
        if numero_stazione in stazioni_elenco_ID and pagina_richiesta in stazioni_sensori[numero_stazione]: return render_template(f'{pagina_richiesta}.html', dati_della_stazione_meteorologica=[f"{TIPO_SITO}{SERVER_ADDRESS}:{SERVER_PORT}",numero_stazione])
        elif numero_stazione in stazioni_elenco_ID and pagina_richiesta == "index": return render_template("index.html", dati_della_stazione_meteorologica=[f"{TIPO_SITO}://{SERVER_ADDRESS}:{SERVER_PORT}",numero_stazione])
        else: return render_template("pagina_non_trovata.html")
    except:
        file_info_error.error("error web page")
        return render_template("pagina_di_errore.html")


@app.route("/stazioni-meteorologiche/<numero_stazione>/dato/<dato_richiesto>")
def inviaDato(numero_stazione, dato_richiesto):
    try:
        numero_stazione = int(numero_stazione)
        if numero_stazione in stazioni_elenco_ID and (dato_richiesto in stazioni_sensori[numero_stazione] or dato_richiesto in altre_opzioni):
            if dato_richiesto == altre_opzioni[0]:
                return jsonify(dati_raggruppati_attuali[numero_stazione])
            else:
                return jsonify({"data_ora_stazione":dati_raggruppati_annuali[numero_stazione]["data_ora_stazione"],"dato_richiesto":dati_raggruppati_annuali[numero_stazione][dato_richiesto]})
        else:
            return render_template("dato_non_trovato.html")
    except:
        file_info_error.error("error web page")
        return render_template("pagina_di_errore.html")
    

""" //////////////////////////////////////////////////////////////// """

""" _________________SPECIALIZZAZIONI CLASSI THREAD_________________ """

class OttenimentoDati(threading.Thread):
    """
    Questo thread permette di acquisire i dati dalle varie stazioni
    """
    def __init__(self):
        threading.Thread.__init__(self)
        self.running = True

    def run(self):
        global dati_raggruppati_attuali

        while True:

            with blocco_thread:

                conn = sqlite3.connect(f"{dir_path}/database/dati_sensori_stazioni.db", timeout=20) # connessione al database
                cur = conn.cursor()

                for n in stazioni_elenco_ID:   

                    try:
                        dict_ricevuto = eval(requests.get(f"{stazioni_address[n]}/stazione-meteorologica/dato/sensori-attuali").text) # richiesta di invio dati
                        # anche se ci sono degli / di troppo tra stazioni_address[n] e link della risorsa non importa

                        print(f"salvataggio dati_stazione_{n} su database")

                        data_ora_server = str(datetime.datetime.utcnow())
                        data_ora_stazione = dict_ricevuto["data_ora_stazione"]

                        dati_raggruppati_attuali[n] = dict_ricevuto.copy()

                        del dict_ricevuto["data_ora_stazione"]

                        # CARICAMENTO DATI SU DATABASE
                        nomi_colonne = "data_ora_server,data_ora_stazione,"
                        for nome_sensore in stazioni_sensori[n]:
                            nomi_colonne += f"\"{nome_sensore}\","


                        sql = f"INSERT INTO dati_stazione_{n} ({nomi_colonne[:-1]}) VALUES (\"{data_ora_server}\",\"{data_ora_stazione}\","

                        for tipo_dato, nome_sensore in zip(elenco_tipi_dati_sensori[n], stazioni_sensori[n]):
                            virgolette = ""
                            if tipo_dato == "TEXT": virgolette = "\""

                            sql += f"{virgolette}{dict_ricevuto[nome_sensore]}{virgolette},"

                        sql = sql[:-1]
                        sql += ")"

                        cur.execute(sql)
                        
                        conn.commit()
                        
                        time.sleep(SECONDI_TRA_AGGIORNAMENTO_DATI)

                    except:
                        file_info_error.error("error in saving data on database")

                conn.close()

            time.sleep(SECONDI_TRA_AGGIORNAMENTO_DATI)



class RaggruppamentoDati(threading.Thread):
    """
    Questo thread raggruppa per tipo tutti i dati fino ad ora caricati sul database
    """
    def __init__(self):
        threading.Thread.__init__(self)
        self.running = True

    def run(self):
        global dati_raggruppati_annuali

        while True:

            with blocco_thread:

                conn = sqlite3.connect(f"{dir_path}/database/dati_sensori_stazioni.db", timeout=20) # connessione al database
                cur = conn.cursor()

                for n in stazioni_elenco_ID:    

                    try:
                        dict_dati_annuali = {}

                        dict_dati_annuali["data_ora_server"] = []
                        dict_dati_annuali["data_ora_stazione"] = []

                        for tipo_sensore in stazioni_sensori[n]:
                            dict_dati_annuali[tipo_sensore] = []

                        for row in cur.execute(f"SELECT * FROM dati_stazione_{n}"):
                            dict_dati_annuali["data_ora_server"].append(row[1])
                            dict_dati_annuali["data_ora_stazione"].append(row[2])
                            for numero_sensore, tipo_sensore in enumerate(stazioni_sensori[n]):
                                dict_dati_annuali[tipo_sensore].append(row[numero_sensore+3])  # +3 perché salto la chiave primaria e le due date

                        dati_raggruppati_annuali[n] = dict_dati_annuali.copy()

                    except:
                        file_info_error.error("error in extract data from database")

                conn.close()
            
            time.sleep(SECONDI_TRA_AGGIORNAMENTO_DATI)



class EliminazioneDatiVecchi(threading.Thread):
    """
    Questo thread permette di caricare su cloud, eliminare e ricreare il databse 
    """
    def __init__(self):
        threading.Thread.__init__(self)
        self.running = True
    
    def run(self):
        parametro_backup = datetime.datetime.utcnow().year
        parametro_backup_precedente = datetime.datetime.utcnow().year

        while self.running:

            data_ora_corrente = datetime.datetime.utcnow()
            parametro_backup = data_ora_corrente.year
            

            if parametro_backup != parametro_backup_precedente:
                with blocco_thread:

                    try: 
                        errore = False    
                        
                        # rinominazione database
                        subprocess.run(["mv", f"{dir_path}/database/dati_sensori_stazioni.db", f"{dir_path}/database/{data_ora_corrente}.db"])

                        try:
                            mega = Mega()
                            m = mega.login(email, password)
                            
                            # SALVATAGGIO DATABASE SU CLOUD
                            print("salvataggio dati su cloud")

                            folder = m.find('StazioneMeteorologica/database', exclude_deleted=True)
                            m.upload(f"{dir_path}/database/{data_ora_corrente}.db", folder[0])
                        except:
                            file_info_error.error("error upload mega")
                            errore = True

                        if errore == False:
                            # se è successo un errore non elimino il database
                            print("eliminazione dati")
                            subprocess.run(["rm", f"{dir_path}/database/{data_ora_corrente}.db"])

                    except:
                        file_info_error.error("error in the EliminazioneDatiVecchi thread")

                    # ricreo il database
                    inizializzazioneStazioniMeteorologiche()
                    
            parametro_backup_precedente = parametro_backup
            time.sleep(60)  



class GestioneComandi(threading.Thread):
    """
    Questo thread permette di gestire il programma del server con alcuni comandi
    """
    def __init__(self):
        threading.Thread.__init__(self)
        self.running = True
    
    def run(self):
        while self.running:
        
            comando = input("")

            if comando == "refresh":
                with blocco_thread:
                    inizializzazioneStazioniMeteorologiche()
                print("\nREFRESH EFFETTUATO\n")
            elif "delete:" in comando:
                stz_id = int(comando.split(":")[1])
                if stazioni_elenco_ID.count(stz_id) == 0:
                    print(f"\nID: {stz_id}, NON PRESENTE NELLA LISTA DI ID_STAZIONI\n")
                else:
                    i = stazioni_elenco_ID.index(stz_id)
                    with blocco_thread:
                        stazioni_elenco_ID.pop(i)
                    print(f"\nID: {stz_id}, ELIMINATO DALLA LISTA DI ID_STAZIONI\n")
            elif comando == "list":
                print(stazioni_elenco_ID)
                print("\n")
            elif comando == "data":
                print("\n")
                for n in stazioni_elenco_ID:
                    print("|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|")
                    print(f"ID: {n}")
                    print(f"Elenco sensori: {stazioni_sensori[n]}")
                    print(f"Elenco dei tipi dei dati restituiti dai sensori: {elenco_tipi_dati_sensori}")
                    print(f"Address: {stazioni_address[n]}")
                    print("|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|")
                print("\n")
            elif comando == "help":
                print("\nCOMANDI:\n")
                print("- refresh --> serve per aggiornare il server quando si aggiungono nuove stazioni meteorologiche\n")
                print("- delete:ID --> serve per eliminare dal server una stazione con l'ID specificato\n")
                print("- list --> serve per mostrare la lista degli id delle stazioni meteorologiche attive \n")
                print("- data --> serve per mostrare i dati che il server sa sulle stazioni meteorologiche\n")
                print("- help --> serve per mostrare i comandi possibili con le loro spiegazioni\n")
                print("\n")
            else: print("\nCOMANDO NON RICONOSCIUTO\n")

            
        
""" //////////////////////////////////////////////////////////////// """

def inizializzazioneStazioniMeteorologiche():
    """
    Questa funzione legge il contenuto dei file presenti nella cartella dati_stazioni, ne estrapola il contenuto
    e va ad aggiornale le strutture dati presenti nel programma
    """

    global stazioni_elenco_ID
    global stazioni_sensori
    global stazioni_address
    global elenco_tipi_dati_sensori

    stazioni_elenco_ID = []
    stazioni_sensori = {}
    stazioni_address = {}
    elenco_tipi_dati_sensori = {}
    
    id = -1

    for _, _, files in os.walk(f"{dir_path}/dati_stazioni"):

        con = sqlite3.connect(f"{dir_path}/database/dati_sensori_stazioni.db", timeout=20)
        cur = con.cursor()
        
        for file in files:

            try:
                with open(f"{dir_path}/dati_stazioni/{file}") as config_file_stazione:
                    righe = config_file_stazione.readlines()
                    
                    # estrazione ID
                    id = int(righe[2].replace("\n",""))
                    stazioni_elenco_ID.append(id)

                    # estrazione elenco_sensori e tipi_sensori
                    stazioni_sensori[id] = righe[0].replace("\n","").split(",")   # aggiungo ["data_ora_server"] per poi potere memoriazzare l'ora di salvataggio dei dati
                    
                    elenco_tipi_dati_sensori[id] = righe[1].replace("\n","").split(",")
                    # estrazione address_stazione

                    stazioni_address[id] = righe[3].replace("\n","")

                    # creazione tabella
                    stringa_creazione_tabella = f"CREATE TABLE if not exists \"dati_stazione_{id}\" (\"ID_misurazioni\" INTEGER NOT NULL, \"data_ora_server\" TEXT, \"data_ora_stazione\" TEXT, "
                    

                    for sensore, tipo in zip(stazioni_sensori[id], elenco_tipi_dati_sensori[id]):
                        stringa_creazione_tabella += f"\"{sensore}\" {tipo}, "

                    stringa_creazione_tabella += "PRIMARY KEY(\"ID_misurazioni\" AUTOINCREMENT))"
                    cur.execute(stringa_creazione_tabella)

                    con.commit()
            
            except:
                file_info_error.error(f"error in creating the weather station")
        
        con.close()




""" ------------------MAIN------------------ """

def main():

    inizializzazioneStazioniMeteorologiche()

    ottenimento_dati = OttenimentoDati()
    ottenimento_dati.start()
    raggruppamento_dati = RaggruppamentoDati()
    raggruppamento_dati.start()
    eliminazione_dati_vecchi = EliminazioneDatiVecchi()
    eliminazione_dati_vecchi.start()
    gestione_comandi = GestioneComandi()
    gestione_comandi.start()

    app.run(host=SERVER_ADDRESS, port=SERVER_PORT)

""" --------------------------------------- """

if __name__ == "__main__":
    main()