import json


def score(json_fich, resultat):
    with open(json_fich, "r") as f:
        content = json.load(f)
        a = content['exchanges']
        b = content['ips']
        c = content['response_avg']
        M = content['ports']
        time = content['total_duration']
    rat = a / time
    score = 0
    ech = 0
    if 5 >= rat > 0:  # en fonction du nombre de trame par seconde
        ech += rat
    elif 5 < rat <= 100:
        ech += (2 * rat) / 95 + (93 / 19)
    elif 100 < rat <= 1000:
        ech += (rat / 300) + 20 / 3
    elif 1000 < rat <= 1850:
        ech += 213 / 17 - (3 * rat) / 850

    taille = 0
    if b <= 5:
        taille += (3 / 5) * b  # petite architecture
    elif 5 < b <= 25:
        taille += b / 5 + 2  # architecture moyenne
    elif 25 < b <= 50:
        taille += (2 * b) / 50 + 5
    elif b > 50:
        taille += 10  # grosse architecture

    rep = 0
    if c < 0.7:
        rep += (50 / 7) * c  # taux de reponse moyens
    elif 0.7 <= c < 1.5:
        rep += ((50 * c) / 8) + 0.625  # bon taux de reponse
    elif 1.5 <= c < 3:
        rep += (-2 * c) + 6

    with open('src/port_list.json', 'r') as f:
        content = json.load(f)
        L = content['ports']

    # verifier le pourcentage de présence dans M de L
    cont = len(set(M) & set(L))
    ratio = (cont / len(L) * 10)  # on ajoute au score la présence des ports à surveiller entre 0 et 10

    score += ratio + taille + ech + rep
    return [score, ratio, taille, ech, rep, time]
