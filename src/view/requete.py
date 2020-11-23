import sqlite3

try:
    conn = sqlite3.connect('resultat.db')
    cur = conn.cursor()
    print("Connexion réussie à SQLite")
    sql = "SELECT * FROM resultats"
    cur.execute(sql)
    res = cur.fetchall()
    for row in res:
        print("sha256: ", row[0])
        print("nom: ", row[1])
        print("score: ", row[2])
        print("nombre_ip: ", row[3])
        print("nombre_port: ", row[4])
        print("taux_de_reponse: ", row[5])
        print("variance_ip_life: ", row[6])
        print("debut_de_capture: ", row[7])
        print("fin_de_capture: ", row[8])
        print("temps_analyse_en_sec: ", row[9])
        print("\n")

    cur.close()
    conn.close()
    print("Connexion SQLite est fermée")
except sqlite3.Error as error:
    print("Erreur lors du sélection à partir de la table person", error)
