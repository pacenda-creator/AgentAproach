from tools import get_invoice, get_tariff

question = input("Napiš dotaz: ")

if "faktura" in question.lower():
    print(get_invoice())

elif "tarif" in question.lower():
    print(get_tariff())

else:
    print("Nerozumím dotazu")