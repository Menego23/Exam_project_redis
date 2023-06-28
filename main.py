from functions import *

while True:
    print()
    print("Scegli:")
    print("1. Nuova proposta")
    print("2. Vota una proposta")
    print("3. Mostra proposte attuali")
    print("4. Mostra top proposte")
    print("0. Esci")
    scelta = input()

    if scelta == '1':
        nuova_proposta()
    elif scelta == '2':
        vota_proposta()
    elif scelta == '3':
        mostra_proposte()
    elif scelta == '4':
        mostra_top_proposte()
    elif scelta == '0':
        break
    else:
        print("Scelta non valida.")
