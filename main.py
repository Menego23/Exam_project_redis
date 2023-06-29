from functions import *

while True:
    login()
    print()
    print("Scegli:")
    print("1. Nuova proposta")
    print("2. Vota una proposta")
    print("3. Mostra proposte attuali")
    print("4. Mostra top proposte")
    print('5. Ricerca proposte')
    print("0. Esci")
    scelta = input()

    match scelta:
        case '1':
            nuova_proposta()
            break
        case '2':
            vota_proposta()
            break
        case '3':
            mostra_proposte()
            break
        case '4':
            mostra_top_proposte()
            break
        case '5':
            ricerca_proposte()
            break
        case _:
            print("Scelta non valida.")
