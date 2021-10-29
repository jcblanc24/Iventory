'pas encore resourdew'
# position = input("Entrez une position: ")
# lettre = position[0]
# chiffre = int(position[1])
#
# if chiffre % 2 == 0 and lettre in 'aceg':
#     print("blanc")
# else:
#     print("noir")
#
# if chiffre % 2 != 0 and lettre in 'aceg':
#     print("blanc")
# else:
#     print("noir")
""""
nmbre = int(input("entrez plusieurs nombres et zero pour arreter: "))
compteur = 0
accumulateur = 0
while nmbre != 0:
    compteur += 1
    accumulateur += nmbre
    nmbre = int(input("entrez plusieurs nombres: "))

moyenne = accumulateur/compteur
print(f"la moyenne est: ",{moyenne})
"""

dik = {"A+": 4.0, "A": 4.0, "A-": 3.7, "B+": 3.3, "B": 3.0, "B-": 2.7, "C+": 2.3, "C": 2.0, "C-": 1.7, "D+": 1.3,
       "D": 1.0, "F": 0}

lettre = input("Entrer une lettre: ")
if lettre not in dik:
    print("Error")
compt = 0
accu = 0
while lettre != "":
    compt += 1
    accu += dik[lettre]
    lettre = input("Entrer une lettre: ")

moyenne = accu / compt
print(f"la moyenne est: {moyenne}")
