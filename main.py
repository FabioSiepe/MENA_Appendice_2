import PySimpleGUI as sg
import pymysql
import Costanti as API

USER = API.USER
PASSWORD = API.PASSWORD

font = ("Arial", 15)
layout = [
    [sg.Text('Benvenuto Sul Bot!')],
    [sg.Text('Visualizza Domande:', font=font), sg.Button('Visualizza', size=(8,2))],
    [sg.Exit()]]

window = sg.Window('Window that stays open', layout, size=(300, 170))


def open_visualizza():
    colonne =["id", "Domanda", "Opzione 1" ,"Opzione 2" ,"Opzione 3" ,"Opzione 4" ,"Vera" ,"Tempo" ,"Difficolta","Argomento"]
    connection = pymysql.connect(host='localhost',
                                 user=USER,
                                 password=PASSWORD,
                                 database='botdb',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    print("csadasasdads")
    with connection:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "SELECT * FROM `domande`"
            cursor.execute(sql)
        connection.commit()
        domande = cursor.fetchall()
    print(domande)
    data = []
    for domanda in domande:
        data.append([domanda["id"], domanda["domanda"], domanda["opz1"], domanda["opz2"], domanda["opz3"], domanda["opz4"], int(domanda["opzCorrect"]) + 1, domanda["period"], domanda["difficolta"], domanda["argomento"]])
    layout_Tabella = [
        [sg.Text("Elenco delle Domande")],
        [sg.Text("Cerca domanda:")],
        [sg.Text("argomento"), sg.InputText(key="argomento"), sg.Button("Cerca", key="argomento_cerca")],
        [sg.Button("Visualizza Tutte", key="all") , sg.Button("Aggiungi Domanda", key="aggiungi")],
        [sg.Table(values=data, headings=colonne,
                        auto_size_columns=False,
                        col_widths= [4, 25, 25, 25, 25, 25, 4, 5, 10],
                        row_height=50,
                        background_color='lightblue',
                        alternating_row_color='white',
                        text_color='black',
                        justification='center',
                        key='-TABLE-',
                        selected_row_colors='red on yellow',
                        enable_events=True,
                        expand_x=True,
                        expand_y=True,
                        vertical_scroll_only=False,
                        enable_click_events=True,  # Comment out to not enable header and other clicks
                        tooltip='Clicca su una riga per modificarla o cancellarla')]]
    window = sg.Window("Second Window", layout_Tabella, modal=True)
    while True:
        event, values = window.read()
        print("Evento: " + str(event) + " Valori:" + str(values))
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "argomento_cerca":
            data=[]
            connection.ping()
            with connection:
                with connection.cursor() as cursor:
                    # Create a new record
                    sql = "SELECT * FROM `domande` WHERE `argomento`=%s"
                    cursor.execute(sql,(values["argomento"]))
                connection.commit()
                domande = cursor.fetchall()
            for domanda in domande:
                data.append([domanda["id"], domanda["domanda"], domanda["opz1"], domanda["opz2"], domanda["opz3"],
                             domanda["opz4"],int(domanda["opzCorrect"]) + 1, domanda["period"],domanda["difficolta"], domanda["argomento"]])
            window['-TABLE-'].update(data)
            window.refresh()
        if event == "all":

            print("ALL")
            data=[]
            connection.ping()
            with connection:
                with connection.cursor() as cursor:
                    # Create a new record
                    sql = "SELECT * FROM `domande`"
                    cursor.execute(sql)
                connection.commit()
                domande = cursor.fetchall()
            for domanda in domande:
                data.append([domanda["id"], domanda["domanda"], domanda["opz1"], domanda["opz2"], domanda["opz3"],
                             domanda["opz4"], domanda["opzCorrect"] + 1 , domanda["period"],domanda["difficolta"],  domanda["argomento"]])
            window['-TABLE-'].update(data)
            window.refresh()
            continue
        if event == "aggiungi":
                open_inserisci()
        if event == "-TABLE-" and values["-TABLE-"]:
            print("asdasd")
            #print("CLIKED: " + str(data[values["-TABLE-"][0]]))
            open_modifica_cancella(data[values["-TABLE-"][0]])

    window.close()

def open_modifica_cancella(elemento):
    print("modifica/cancella")
    layout_aggiungi = [
        [sg.Text("Domanda:  "), sg.InputText(key="domanda", size=128, default_text=elemento[1])],
        [sg.Text("Opzione 1: "), sg.Input(key="opz1", size=128, default_text=elemento[2])],
        [sg.Text("Opzione 2: "), sg.Input(key="opz2", size=128, default_text=elemento[3])],
        [sg.Text("Opzione 3: "), sg.Input(key="opz3", size=128, default_text=elemento[4])],
        [sg.Text("Opzione 4: "), sg.Input(key="opz4", size=128, default_text=elemento[5])],
        [sg.Text("Opzione corretta: "), sg.Combo(["1", "2", "3", "4"], key="corretta" ,  default_value=elemento[6])],
        [sg.Text("Tempo per domanda (in secondi, MIN:5 MAX:500): "), sg.Input(key="secondi", size=3, default_text=elemento[7])],
        [sg.Text("Difficoltà: "), sg.Combo(["1", "2", "3", "4", "5"], key="difficolta", default_value=elemento[8])],
        [sg.Text("Argomento"), sg.Input(key="argomento", default_text=elemento[9])],
        [sg.Button("Aggiorna"), sg.Button("Elimina")]
    ]
    window = sg.Window("Agiorna/Elimina", layout_aggiungi, modal=True)
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "Aggiorna":
            connection = pymysql.connect(host='localhost',
                                         user=USER,
                                         password=PASSWORD,
                                         database='botdb',
                                         charset='utf8mb4',
                                         cursorclass=pymysql.cursors.DictCursor)
            with connection:
                with connection.cursor() as cursor:
                    sql = "UPDATE domande SET `domanda`=%s, `opz1`=%s, `opz2`=%s, `opz3`=%s, `opz4`=%s," \
                          "`opzCorrect`=%s, `period`=%s, `difficolta`=%s, `argomento`=%s WHERE `id`=%s"
                    try:
                        if values["corretta"] == "1" or values["corretta"] == "2" or values["corretta"] == "3" \
                                or values["corretta"] == "4":
                            if 5 <= int(values["secondi"]) <= 500:
                                if 1 <= int(values["difficolta"]) <= 5:
                                    cursor.execute(sql, (values["domanda"],
                                                         values["opz1"],
                                                         values["opz2"],
                                                         values["opz3"],
                                                         values["opz4"],
                                                         int(values["corretta"]) -1,
                                                         values["secondi"],
                                                         values["difficolta"],
                                                         values["argomento"],
                                                         int(elemento[0]),
                                                         ))
                                    connection.commit()
                                    sg.popup("Domanda Aggiornata Correttamente")
                                else:
                                    raise Exception
                            else:
                                raise Exception
                        else:
                            raise Exception
                    except Exception as e:
                        print(e)
                        sg.popup("Errore nell'aggiornamento ri-controllare i campi")
        if event == "Elimina":
            connection = pymysql.connect(host='localhost',
                                         user=USER,
                                         password=PASSWORD,
                                         database='botdb',
                                         charset='utf8mb4',
                                         cursorclass=pymysql.cursors.DictCursor)
            with connection:
                with connection.cursor() as cursor:
                    sql = "DELETE FROM domande WHERE `id`=%s"
                    cursor.execute(sql, (int(elemento[0]),
                                         ))
                    connection.commit()
            break

    window.close()

def open_inserisci():
    layout_aggiungi = [
        [sg.Text("Domanda:  "), sg.Input(key="domanda" , size=128)],
        [sg.Text("Opzione 1: "), sg.Input(key="opz1" , size=128)],
        [sg.Text("Opzione 2: "), sg.Input(key="opz2" , size=128)],
        [sg.Text("Opzione 3: "), sg.Input(key="opz3" , size=128)],
        [sg.Text("Opzione 4: "), sg.Input(key="opz4" , size=128)],
        [sg.Text("Opzione corretta: ") ,sg.Combo(["1","2","3","4"], key="corretta")],
        [sg.Text("Tempo per domanda (in secondi, MAX:500): ") ,sg.Input(key="secondi" , size=3)],
        [sg.Text("Difficoltà: "), sg.Combo(["1", "2", "3", "4", "5"], key="difficolta")],
        [sg.Text("Argomento"), sg.Input(key="argomento")],
        [sg.Button("aggiungi")]
    ]
    window = sg.Window("Aggiungi", layout_aggiungi, modal=True)

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "aggiungi":
            connection = pymysql.connect(host='localhost',
                                         user=USER,
                                         password=PASSWORD,
                                         database='botdb',
                                         charset='utf8mb4',
                                         cursorclass=pymysql.cursors.DictCursor)
            with connection:
                with connection.cursor() as cursor:
                    sql = "INSERT INTO `domande` (`domanda`, `opz1`, `opz2`, `opz3`, `opz4`, " \
                          "`opzCorrect`, `period`, `difficolta`, `argomento`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    try:
                        if values["corretta"] == "1" or values["corretta"] == "2" or values["corretta"] == "3" or values["corretta"] == "4":
                            if 5 <= int(values["secondi"]) <= 500:
                                cursor.execute(sql, (values["domanda"],
                                                     values["opz1"],
                                                     values["opz2"],
                                                     values["opz3"],
                                                     values["opz4"],
                                                     int(values["corretta"]) -1,
                                                     values["secondi"],
                                                     values["difficolta"],
                                                     values["argomento"],
                                                     ))

                                connection.commit()
                                sg.popup("Domanda Inserita Correttamente")
                            else:
                                raise Exception
                        else:
                            raise Exception
                    except Exception as e:
                        print(e)
                        sg.popup("Errore nell'inserimento ri-controllare i campi")

    window.close()

while True:                             # The Event Loop

    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Visualizza':
        open_visualizza()
window.close()