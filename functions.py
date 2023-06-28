import redis

# Connessione al database Redis
db = redis.Redis()

def mostra_proposte():
    proposte = db.zrevrangebyscore('voti_proposte', '+inf', '-inf', withscores=True)
    print("Proposte attuali:")
    for i, (proposta, voti) in enumerate(proposte, start=1):
        proponenti = ', '.join(db.smembers(f"proponenti:{proposta}"))
        print(f"{i}. {proposta.decode()} ({proponenti}): {int(voti)} voti")

def nuova_proposta():
    descrizione = input("Descrivi la proposta: ")
    proponenti = input("Chi sono i proponenti? (separati da virgola): ").split(",")
    proposta_id = db.incr('proposta_id')
    db.hmset(f"proposta:{proposta_id}", {"descrizione": descrizione})
    for proponente in proponenti:
        db.sadd(f"proponenti:proposta:{proposta_id}", proponente.strip())
    db.zadd('voti_proposte', {f"proposta:{proposta_id}": 0})