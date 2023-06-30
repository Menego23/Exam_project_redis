from functions import *

while True:
    print()
    print("Seleziona un'opzione:")
    print("1. Nuova proposta")
    print("2. Vota una proposta")
    print("3. Mostra proposte attuali")
    print("4. Mostra top proposte")
    print('5. Ricerca proposte')
    print("0. Esci")
    scelta = input("\ncosa vuoi fare?")

    if scelta == '1':
        nuova_proposta()
    elif scelta == '2':
        vota_proposta()
    elif scelta == '3':
        mostra_proposte()
    elif scelta == '4':
        mostra_top_proposte()
    elif scelta == '5':
        ricerca_proposte()
    else:
        print("Scelta non valida.")
