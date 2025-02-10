class gestore_magazzino:
    def __init__(self,costo_magazzino):
        self.costo_magazzino = costo_magazzino
        self.prodotti = {}
    def aggiungi_prodotto(self,nome):
        self.prodotti[nome.nome]
    def romuovi_prodotto(self,nome):
        self.prodotti.pop(nome.nome)
    def calcola_costi_magazzino(self):
        costo = self.costo_magazzino
        for prodotto in self.prodotti:
            self.costo_magazzino += prodotto.costo
        print(self.costo_magazzino)
        self.costo_magazzino = costo
        del costo
class prodotto:
    def __init__(self, nome, costo, quantità):
        self.nome = nome
        self.costo = costo
        self.quantità = quantità
prodotto1 = prodotto("sciampo",350,75)
magazzino1 = gestore_magazzino(500)
prodotto2 = prodotto("nokia",800,30)
magazzino1.aggiungi_prodotto(prodotto1)
magazzino1.aggiungi_prodotto(prodotto2)
magazzino1.romuovi_prodotto("sciampo")
magazzino1.calcola_costi_magazzino()