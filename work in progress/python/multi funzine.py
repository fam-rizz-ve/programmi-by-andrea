dizionario = {
    "nome": "mario",
    "cognome": "rossi",
    "eta": 25
}
operazioni = ("aggiungere","modificare","eliminare","mostra dizionario")
def start():
    operazione = input("cosa vuoi fare? ")
    if operazione == operazioni[0]:
        articolo = input("inserire chiave e valore separati da una virgola")
        aggiungere(articolo.split(","))
    elif operazione == operazioni[1]:
        articolo = input("scrivi la chiave del oggetto da modificare  e il nuovo valore separati da una virgola ")
        modifica(articolo.split(","))
    elif operazione == operazioni[2]:
        rimuovere(input("chiave da eliminare "))
    elif operazione == operazioni[3]:
        print(dizionario)
    else:
        print("operazione non trovata")

def aggiungere(articolo):
    chiave = articolo[0]
    valore = articolo[1]
    dizionario[chiave] = valore

def rimuovere(articolo):
    del dizionario[articolo]

def modifica(articolo):
    chiave = articolo[0]
    valore = articolo[1]
    dizionario[chiave] = valore
while True:
    start()