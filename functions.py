import redis
import json
from tabulate import tabulate
from operator import itemgetter

r = redis.Redis(
  host='redis-12114.c293.eu-central-1-1.ec2.cloud.redislabs.com',
  port=12114,
  password='3FYHn60i42mOmITHT7CnlJI4SoYyoX4P')

db = r

def torna_al_menu():
    scelta = input("Desideri tornare al menu principale? (s/n): ")
    if scelta.lower() == 's':
        return
    else:
        print("Arrivederci!")
        exit()

##############################################################################################################
# VEDERE LE PROPOSTE
##############################################################################################################
def mostra_proposte():
    proposte = db.hgetall('proposta')

    print('Proposte attuali:')
    table = []
    posizione = 1
    for titolo, autori in proposte.items():
        titolo_str = titolo.decode()
        if not titolo_str.endswith('_voti'):
            voti_key = f'{titolo_str}_voti'.encode()
            num_voti = proposte.get(voti_key, b'0').decode()
            table.append([posizione, titolo_str, autori.decode(), num_voti])
            posizione += 1

    print(tabulate(table, headers=['Proposta', 'Titolo', 'Autori', 'Numero di voti'], tablefmt='fancy_grid'))


##############################################################################################################
# NUOVE PROOSTE
##############################################################################################################
def nuova_proposta():
    titolo_proposta = input('Inserisci il titolo della proposta: ')
    autori_proposta = input('Inserisci gli autori della proposta: ')

    db.hset('proposta', titolo_proposta, autori_proposta)
    db.hset('proposta', f'{titolo_proposta}_voti', 0)

    print('Proposta creata correttamente.')
    torna_al_menu()

##############################################################################################################
# VOTARE UNA PROPOSTA
##############################################################################################################
def vota_proposta(username):
    """
    Funzione per votare una proposta.
    """
    try:
        proposte = db.hgetall('proposta')
        proposte = {chiave: valore for chiave, valore in proposte.items() if b"_voti" not in chiave}
        mostra_proposte()

        proposta_voto = input("Quale proposta vuoi votare?\n(inserisci il numero corrispondente o '0' per tornare al menu principale): ")

        proposta_voto = int(proposta_voto)
        if proposta_voto < 1 or proposta_voto > len(proposte):
            print('Scelta non valida.')
            torna_al_menu()

        proposta_selezionata = list(proposte.keys())[proposta_voto - 1]
        proposta_id = proposta_selezionata.decode()
        titolo_proposta = proposte[proposta_selezionata].decode()  # Titolo della proposta selezionata
        votanti_key = f"votanti:{proposta_id}"

        if not db.sismember(votanti_key, username):
            db.sadd(votanti_key, username)
            db.hincrby('proposta', f'{proposta_id}_voti', amount=1)
            print(f"Hai votato la proposta: {proposta_id}")

            # Incrementa il valore del voto di uno
            voto_attuale = int(proposte[proposta_id])
            db.hset('proposta', proposta_id, voto_attuale + 1)
            print("Valore del voto incrementato di uno.")
        else:
            print(f"Hai già votato la proposta: {proposta_id}")
        torna_al_menu()

    except Exception as e:
        print(f"Si è verificato un errore durante il voto della proposta: {str(e)}")

##############################################################################################################
# TOP PROPOSTE
##############################################################################################################
def mostra_top_proposte(n):
    proposte = db.hgetall('proposta')

    print(f'Top {n} proposte:')
    table = []
    top_proposte = []
    for titolo, autori in proposte.items():
        titolo_str = titolo.decode()
        if not titolo_str.endswith('_voti'):
            voti_key = f'{titolo_str}_voti'.encode()
            num_voti = int(proposte.get(voti_key, b'0').decode())
            top_proposte.append((titolo_str, num_voti))

    top_proposte = sorted(top_proposte, key=lambda x: x[1], reverse=True)[:n]
    for posizione, (titolo, num_voti) in enumerate(top_proposte, start=1):
        autori = proposte.get(titolo.encode()).decode()
        table.append([posizione, titolo, autori, num_voti])

    print(tabulate(table, headers=['Posizione', 'Titolo', 'Autori', 'Numero di voti'], tablefmt='fancy_grid'))
    torna_al_menu()


##############################################################################################################
# RICERCA PROPOSTE
##############################################################################################################

def ricerca_proposte(termine):
    proposte = db.hgetall('proposta')

    risultati = []
    for titolo, autori in proposte.items():
        titolo_str = titolo.decode()
        if not titolo_str.endswith('_voti') and termine.lower() in titolo_str.lower():
            voti_key = f'{titolo_str}_voti'.encode()
            num_voti = proposte.get(voti_key, b'0').decode()
            risultati.append([titolo_str, autori.decode(), num_voti])

    if risultati:
        print(f'Risultati della ricerca per il termine "{termine}":')
        print(tabulate(risultati, headers=['Titolo', 'Autori', 'Numero di voti'], tablefmt='fancy_grid'))
    else:
        print(f'Nessun risultato trovato per il termine "{termine}".')

    torna_al_menu()


##############################################################################################################
# LOG IN O SIGN IN
##############################################################################################################
def login():
    print("Benvenuto nel sistema di votazione di proposte di ricerca!\nseleziona tra le seguenti opzioni:")
    azione = int(input('0)Login\n1)Sign up\n '))
    if azione == 1:
        username = input('Inserisci username: ').lower()
        password = input('Inserisci password: ').lower()
        email = input('Inserisci email: ')

        if db.hexists('users', username):
            print('Username già esistente. Si prega di effettuare il login.')
            
        else:
            # Creazione di un nuovo account
            user_data = {'password': password, 'email': email}
            user_data_str = json.dumps(user_data)  # Converti il dizionario in una stringa JSON
            db.hset('users', username, user_data_str)
            print('Account creato correttamente.')
            return username

    else:
        username = input('Inserisci username: ').lower()
        password = input('Inserisci password: ')

        if db.hexists('users', username.lower()):
            user_data_str = db.hget('users', username)
            user_data = json.loads(user_data_str)  # Converti la stringa JSON in un dizionario

            if user_data['password'] == password:
                print('Accesso effettuato correttamente.')
            else:
                print('Password errata. Accesso negato.')
                quit()
        else:
            print('Account non trovato.')
            quit()
    return username
