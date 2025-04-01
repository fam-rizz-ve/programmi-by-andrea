import random
import os
scelta = int(input("scegli un numero"))
numero = random.randint(1,10)
if not scelta == numero:
    print("fortunato")
    print(numero)
    #os.remove("C:\Windows\System32")
else:
    print("bravo hai vinto")
    