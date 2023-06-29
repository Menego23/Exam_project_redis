import redis

# Connessione al database

r = redis.Redis(
  host='redis-12114.c293.eu-central-1-1.ec2.cloud.redislabs.com',
  port=12114,
  password='3FYHn60i42mOmITHT7CnlJI4SoYyoX4P')

db = r
##############################################################################################################
# VEDERE LE PROPOSTE
##############################################################################################################
def mostra_proposte():
    proposte = db.zrevrangebyscore('voti_proposte', '+inf', '-inf', withscores=True)#La funzione db.zrevrangebyscore è un metodo di Redis utilizzato per ottenere un insieme ordinato di elementi da un set ordinato (sorted set) in base ai loro punteggi (scores) in ordine decrescente.
    print("Proposte attuali:")
    for i, (proposta, voti) in enumerate(proposte, start=1):
        proponenti = ', '.join(db.smembers(f"proponenti:{proposta}"))
        print(f"{i}. {proposta.decode()} ({proponenti}): {int(voti)} voti")


##############################################################################################################
# NUOVE PROOSTE
##############################################################################################################
def nuova_proposta():
    descrizione = input("Descrivi la proposta: ")
    proponenti = input("Chi sono i proponenti? (separati da virgola): ").split(",")
    proposta_id = db.incr('proposta_id')
    db.hmset(f"proposta:{proposta_id}", {"descrizione": descrizione})
    for proponente in proponenti:
        db.sadd(f"proponenti:proposta:{proposta_id}", proponente.strip())
    db.zadd('voti_proposte', {f"proposta:{proposta_id}": 0})



##############################################################################################################
# VOTARE UNA PROPOSTA
##############################################################################################################
def vota_proposta():
    nome_studente = input("Chi sei? ")
    mostra_proposte()
    proposta_voto = input(
        "Che proposta voti? (inserisci il numero corrispondente o '0' per tornare al menu principale): ")
    if proposta_voto == '0':
        return

    proposte = db.zrevrangebyscore('voti_proposte', '+inf', '-inf', withscores=True)
    if proposta_voto.isdigit() and 1 <= int(proposta_voto) <= len(proposte):
        proposta = proposte[int(proposta_voto) - 1]
        proposta_id = proposta[0].decode()

        if not db.sismember(f"votanti:{proposta_id}", nome_studente):
            db.sadd(f"votanti:{proposta_id}", nome_studente)
            db.zincrby('voti_proposte', 1, proposta_id)
            print("Voto registrato!")
        else:
            print("Hai già votato questa proposta.")
    else:
        print("Selezione non valida.")


##############################################################################################################
# TOP PROPOSTE
##############################################################################################################
def mostra_top_proposte():
    n = input("Quante proposte vuoi visualizzare? ")
    proposte = db.zrevrangebyscore('voti_proposte', '+inf', '-inf', withscores=True, start=0, num=int(n))
    print(f"Le {n} proposte con il maggior numero di voti sono:")
    for i, (proposta, voti) in enumerate(proposte, start=1):
        proponenti = ', '.join(db.smembers(f"proponenti:{proposta}"))
        print(f"{i}. {proposta.decode()} ({proponenti}): {int(voti)} voti")




##############################################################################################################
# RICERCA PROPOSTE
##############################################################################################################
def ricerca_proposte():
    parola_chiave = input("Inserisci una parola chiave per la ricerca: ")
    proposte = db.zrevrangebyscore('voti_proposte', '+inf', '-inf', withscores=True)
    
    proposte_filtrate = []
    for proposta, voti in proposte:
        proponenti = ', '.join(db.smembers(f"proponenti:{proposta}"))
        descrizione = db.hget(f"proposta:{proposta}", "descrizione").decode()
        if parola_chiave.lower() in descrizione.lower() or parola_chiave.lower() in proponenti.lower():
            proposte_filtrate.append((proposta, voti))
    
    if proposte_filtrate:
        print("Risultati della ricerca:")
        for i, (proposta, voti) in enumerate(proposte_filtrate, start=1):
            proponenti = ', '.join(db.smembers(f"proponenti:{proposta}"))
            print(f"{i}. {proposta.decode()} ({proponenti}): {int(voti)} voti")
    else:
        print("Nessun risultato trovato per la parola chiave inserita.")


