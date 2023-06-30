import redis
import json
from tabulate import tabulate

#da fixare:
# - visualizzazione top proposte
# - ricerca proposte
#    - ricerca proposte, gestire l'eventualità in cui l'utente non inserisce un caBBo
# - vota proposte non funziona correttamente


db = redis.Redis(
  host='redis-17800.c55.eu-central-1-1.ec2.cloud.redislabs.com',
  port=17800,
  password='R0xoNRNdiq8KTklL7Y4mfzeOVq40btc4')


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
    for posizione, (titolo, autori) in enumerate(proposte.items(), start=1):
        if not titolo.decode().endswith('_voti'):
            voti_key = f'{titolo.decode()}_voti'.encode()
            num_voti = proposte.get(voti_key, b'0').decode()
            table.append([posizione, titolo.decode(), autori.decode(), num_voti])

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
    proposte = db.hgetall('proposta')
    mostra_proposte()

    proposta_voto = input("Quale proposta vuoi votare? \n(inserisci il numero corrispondente o '0' per tornare al menu principale): ")
    torna_al_menu()

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
        torna_al_menu()

        # Incrementa il valore del voto di uno
        voto_attuale = int(proposte[proposta_id])
        db.hset('proposta', proposta_id, voto_attuale + 1)
        print("Valore del voto incrementato di uno.")
    else:
        print(f"Hai già votato la proposta: {proposta_id}")
        torna_al_menu()


##############################################################################################################
# TOP PROPOSTE
##############################################################################################################
def mostra_top_proposte():
    proposte = db.hgetall('proposta')

    print(proposte)
    return
    # Dizionario per memorizzare il numero di voti per ogni proposta
    proposte_voti = proposte 
    for titolo, voto in proposte.items():
        if not titolo.decode().endswith('_voti'):
            titolo_proposta = titolo.decode()
            try:
                num_voti = int(voto)
                proposte_voti[titolo_proposta] = num_voti
            except ValueError:
                continue

    proposte_ordinate = sorted(proposte_voti.items(), key=lambda x: x[1], reverse=True)

    print('Proposte attuali (ordine decrescente di voti):')
    
    table = []
    for posizione, (titolo, num_voti) in enumerate(proposte_ordinate, start=1):
        autori_key = f'{titolo}_autori'.encode()
        autori = proposte.get(autori_key, b'').decode()
        table.append([posizione, titolo, autori, num_voti])

    print(tabulate(table, headers=['Posizione', 'Titolo', 'Autori', 'Numero di voti'], tablefmt='fancy_grid'))

    torna_al_menu()


##############################################################################################################
# RICERCA PROPOSTE
##############################################################################################################
def ricerca_proposte(username):
    mostra_proposte()

    proposta_voto = input("Quale proposta vuoi votare? \n(inserisci il numero corrispondente o '0' per tornare al menu principale): ")
    if proposta_voto == '0':
        return

    proposte = db.hgetall('proposta')
    proposta_voto = int(proposta_voto)
    if proposta_voto < 1 or proposta_voto > len(proposte):
        print('Scelta non valida.')
        return

    proposta_selezionata = list(proposte.keys())[proposta_voto - 1]
    proposta_id = proposta_selezionata.decode()
    votanti_key = f"votanti:{proposta_id}"

    if not db.sismember(votanti_key, username):
        db.sadd(votanti_key, username)
        db.hincrby('proposta', f'{proposta_id}_voti', amount=1)
        print("Voto registrato!")

        # Verifica se la chiave proposta_id esiste nel dizionario proposte
        if proposta_id in proposte:
            voto_attuale = int(proposte[proposta_id])
            db.hset('proposta', proposta_id, voto_attuale + 1)
            print("Valore del voto incrementato di uno.")
        else:
            print("La proposta selezionata non esiste.")
    else:
        print("Hai già votato questa proposta.")



##############################################################################################################
# LOG IN O SIGN IN
##############################################################################################################
def login():
    print("Benvenuto nel sistema di votazione di proposte di ricerca!\nseleziona tra le seguenti opzioni:")
    azione = int(input('0)Login\n1)Sign up\n '))
    if azione == 1:
        username = input('Inserisci username: ')
        password = input('Inserisci password: ')
        email = input('Inserisci email: ')

        if db.hexists('users', username):
            print('Username già esistente. Si prega di effettuare il login.')
            
        else:
            # Creazione di un nuovo account
            user_data = {'password': password, 'email': email}
            user_data_str = json.dumps(user_data)  # Converti il dizionario in una stringa JSON
            db.hset('users', username, user_data_str)
            print('Account creato correttamente.')
            return

    else:
        username = input('Inserisci username: ')
        password = input('Inserisci password: ')

        if db.hexists('users', username):
            user_data_str = db.hget('users', username)
            user_data = json.loads(user_data_str)  # Converti la stringa JSON in un dizionario

            if user_data['password'] == password:
                print('Accesso effettuato correttamente.')
            else:
                print('Password errata. Accesso negato.')
                quit()
        else:
            print('Account non trovato.')
    return username


'''

print('---------------------------------------------------------------------------------------------------------------------')
print("Account utente registrati:")
user_accounts = db.hgetall('users')

for username, user_data in user_accounts.items():
    user_data = eval(user_data)  # Converti la stringa in un dizionario
    print(f"Username: {username.decode()}, Password: {user_data['password']}, Email: {user_data['email']}")

print('---------------------------------------------------------------------------------------------------------------------')

proposte = db.hgetall('proposta')

print('Proposte attuali:')
for posizione, (titolo, autori) in enumerate(proposte.items(), start=1):
    if not titolo.decode().endswith('_voti'):
        voti_key = f'{titolo.decode()}_voti'.encode()
        num_voti = proposte.get(voti_key, b'0').decode()  # Decodifica il valore da byte a stringa
        print(f'Proposta: {posizione}\nTitolo: {titolo.decode()}\nAutori: {autori.decode()}\nNumero di voti: {num_voti}\n---')
'''