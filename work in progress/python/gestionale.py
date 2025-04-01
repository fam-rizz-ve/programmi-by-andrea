prodotti_creati = {}

class magazzino():

    def __init__(self,nome,affitto):
        self.nome = nome
        self.affitto = affitto
        self.prodotti = {}
        self.quantita_prodotti = {}

    def aggiungi_prodotto(self,prodotto,quantità):
        try:
            x = prodotto.nome
        except:
            pass
            #riporta al loop
        self.prodotti[prodotto.nome] = prodotto
        self.quantita_prodotti[prodotto.nome] = quantità
    def rimuovi_prodotto(self,prodotto,quantità):
        try:
            x = prodotto.nome
        except:
            pass
            #riporta al loop
        if quantità == "all":
            self.prodotti.pop(prodotto.nome)
            self.quantita_prodotti.pop(prodotto.nome)
        elif self.quantita_prodotti[prodotto.nome] - quantità == 0:
            self.prodotti.pop(prodotto.nome)
            self.quantita_prodotti.pop(prodotto.nome)
        elif quantità < self.quantita_prodotti[prodotto.nome]:
            self.quantita_prodotti[prodotto.nome] -= quantità
        else:
            print("non hai a disposizione abbastanza prodotti")


class prodotto():
    def __init__(self,nome,costo):
        self.nome = nome
        self.costo = costo


lista_magazzini = {}
lista_magazzini["mondo"] = magazzino("ceggia",300)
prodotos = prodotto("palla",22)
lista_magazzini["mondo"].aggiungi_prodotto(prodotos,300)
lista_magazzini["mondo"].rimuovi_prodotto(prodotos,5545)
print(lista_magazzini["mondo"].prodotti)
print(lista_magazzini["mondo"].quantita_prodotti)

def loop_principale():
    print("su cosa vuoi lavorare?")
    print("-magazzini")
    print("-articoli")
    input_utente = input()
    if input_utente == "magazzini":

def scelte_magazzini():
    print("cosa vuoi fare?")
    scelte = list()