operazioni = ["+","-","*","/","^"]
while True:
    formula = input("scrivi la formula").split(" ")
    try:
            a = float(formula[0])
    except ValueError:
        if formula[0].upper == "ANS":
            formula[0] = risultato
        elif formula[2].upper == "ANS":
            formula[2] = risultato
        else:
            print("valori non corretti")
            continue
    if formula[1] == "+":
        risultato = float(formula[0]) + float(formula[2])
    elif formula[1] == "-":
        risultato = float(formula[0]) - float(formula[2])
    elif formula[1] == "*":
        risultato = float(formula[0]) * float(formula[2])
    elif formula[1] == "/":
        try:
            prova = float(formula[0]) / float(formula[2])
        except ZeroDivisionError:
            print("non puoi dividere per 0") 
            continue
        else:
            risultato = float(formula[0]) / float(formula[2])
    elif formula[1] == "^":
        risultato = float(formula[0]) ** float(formula[2])
    else:
        print("operazione non valida")
        continue
    print(risultato)