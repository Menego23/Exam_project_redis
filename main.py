from functions import *
try:
    username = login()
except:
    print("Errore durante il login.")
    exit()
while True:
    print()
    print("Seleziona un'opzione:")
    print("1. Nuova proposta")
    print("2. Vota una proposta")
    print("3. Mostra proposte")
    print("4. Mostra top proposte")
    print('5. Ricerca proposte')
    print("0. Esci")
    try:
        scelta = input("\ncosa vuoi fare?")

        if scelta == '1':
            nuova_proposta()
        elif scelta == '2':
            vota_proposta(username)
        elif scelta == '3':
            mostra_proposte()
            torna_al_menu()
        elif scelta == '4':
            mostra_top_proposte()
        elif scelta == '5':
            ricerca_proposte(username)
        elif scelta == '0':
            print("Arrivederci!")
            quit()
        else:
            print("Scelta non valida.")
    except KeyboardInterrupt:
        print("Arrivederci!")
        exit()