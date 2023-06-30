# Sistema di votazione di proposte di ricerca

Questo repository contiene un sistema di votazione per proposte di ricerca scritto in Python. Il sistema utilizza Redis come database per memorizzare le proposte e i voti associati.

## Dipendenze

Assicurarsi di avere le seguenti dipendenze installate prima di eseguire il codice:

- Redis (python-redis)
- Tabulate (tabulate)



## Configurazione

Il sistema utilizza un'istanza di Redis, utilizzare quella corrente su cui si sono fatti i test o inserire la propria da redislab. Assicurarsi di aver configurato correttamente l'host, la porta e la password del database Redis nel codice sorgente.


## Funzionalità principali:
Il sistema offre le seguenti funzionalità:

- Visualizzazione delle proposte attuali
- Creazione di nuove proposte
- Voto per una proposta
- Visualizzazione delle top proposte
- Ricerca di proposte per termine

## Utilizzo
Assicurarsi di avere Redis in esecuzione e configurato correttamente prima di eseguire il codice. Avviare il sistema eseguendo il file Python main.py.


python main.py
Seguire le istruzioni sullo schermo per utilizzare le diverse funzionalità del sistema.

### Autori
Questo sistema è stato sviluppato da:

Gianluca Meneghetti
Gabriele Laguna
Stefano Bonfanti
Giulio Nocco