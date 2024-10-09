import random
import termtables
import sys


# Anzahl der Spieler
def anzahl_spieler():
    # Funktion, die den User nach der Anzahl der Spieler fragt
    # gibt die Anzahl der Spieler aus
    player_count_input = 0
    while (2 <= player_count_input <= 8) is False:
        try:
            player_count_input = int(input("Wie viele möchten spielen(2-8)?: "))
        except ValueError:
            print("Bitte gib eine Zahl von 2 bis 8 ein!")
            continue
        if (2 <= player_count_input <= 8) is False:
            print("Bitte gib eine Zahl von 2 bis 8 ein!")
            continue
    return player_count_input


def game_start():
    # Funktion, den Spieler nach Spielstart oder Spielerlistenänderung fragt
    # gibt den jeweiligen status zurück
    gm_start = None
    while gm_start != "s" and gm_start != "ä":
        try:
            gm_start = input("Möchten Sie die Spielerliste ändern oder das Spiel starten?(ä/s): ")
        except ValueError:
            print("Bitte geben Sie 'ä' oder 's' ein!")
    return gm_start


# Gewinnkarte
def gewinnkarte(punkte, bonus):
    # Funktion, die die Punkte des Spielers in einer Gewinnkarte ausgibt.
    # benötigt die Spielerliste, welche den Spielernamen und deren Punkte beinhaltet
    # und die Funktion zum Berechnen der Bonus/Gesamtpunkte
    header = [punkte[0], "Kategorie", "Punkte"]
    data1 = [
        [1, "Nur Einser zählen", punkte[1]],
        [2, "Nur Zweier zählen", punkte[2]],
        [3, "Nur Dreier zählen", punkte[3]],
        [4, "Nur Vierer zählen", punkte[4]],
        [5, "Nur Fünfer zählen", punkte[5]],
        [6, "Nur Sechser zählen", punkte[6]],
        ["gesamt", "->", bonus[0]],
        ["Bonus bei 63 oder mehr", "plus 35", bonus[1]],
        ["gesamt oberer Teil", "->", bonus[2]],
    ]
    termtables.print(
        data1,
        header=header,
        style=termtables.styles.double_thin
    )

    data2 = [
        [7, "Dreierpasch", punkte[7]],
        [8, "Viererpasch", punkte[8]],
        [9, "Full-House", punkte[9]],
        [10, "Kleine Straße", punkte[10]],
        [11, "Große Straße", punkte[11]],
        [12, "Kniffel", punkte[12]],
        ["13 Chance", "alle Augen zählen ", punkte[13]],
        ["gesamt unterer Teil   ", "->", bonus[3]],
        ["gesamt oberer Teil", "->", bonus[2]],
        ["Endsumme", "->", bonus[4]]
    ]
    header = [punkte[0], "Kategorie", "Punkte"]
    termtables.print(
        data2,
        header=header,
        style=termtables.styles.double_thin
    )


def print_p_list(plr_list):
    # Funktion, um nur die Namen der Spielerliste abzurufen und auszugeben
    # benötigt die Spielerliste
    print("Spielerliste: ")
    for p in range(len(plr_list)):
        print(f"Spieler{p + 1}: {list(plr_list[f"Spieler{p + 1}"])[0]}")


# Würfeln 1-5 Würfel
def roll_dices(saved_dice):
    # Funktion, die eine Liste mit 5 Würfeln ausgibt
    # benötigt die Liste der gespeicherten Würfel
    # um wieder auf 5 Würfel neu zu generieren
    for dices in range(5 - len(saved_dice)):
        dice_list.append(random.randint(1, 6))
    dices = [dice_list[:]]
    termtables.print(
        dices,
        style=termtables.styles.double_thin
    )
    return dice_list


# Auswahl der Würfel
def pick_dices(rolled_dices, p_liste, playername):
    # Funktion, die den Spieler fragt, welche Würfel er behalten möchte
    # gibt auch die Möglichkeit die Runde zu beenden oder die Gewinnkarte anzeigen zu lassen
    # benötigt die Liste der gewürfelten Würfel, die gesamte Spielerliste und den derzeitigen Spieler
    # Rückgabewert ist eine Liste der Würfel die beibehalten werden,
    # die Abfrage nach der Gewinnkategorie oder das anzeigen der Gewinnkarte
    while True:
        keep_dices = input("Welche Würfel möchtest du behalten? Tippe 1-5 hintereinander, 0, 'e', 'k' oder 'x':")
        if keep_dices == "x":
            exit_g = input("Sicher das Sie das Spiel abbrechen wollen? Bestätigen Sie durch die Eingabe 'exit': ")
            if exit_g == "exit":
                sys.exit("Der Spieler hat das Spiel abgebrochen!")
        elif keep_dices == "0":
            rolled_dices.clear()
            return rolled_dices
        elif keep_dices == "e":
            karte_abfrage(rolled_dices, p_liste, playername)
            gewinnkarte(player_list.get(key), bonus_points(p_liste.get(key)))
            return "endTurn"
        elif keep_dices == "k":
            gewinnkarte(player_list.get(key), bonus_points(p_liste.get(key)))
            dices = [dice_list[:]]
            termtables.print(
                dices,
                style=termtables.styles.double_thin
            )
        elif keep_dices.isdigit() and (len(keep_dices) == len(set(keep_dices))):

            for char in keep_dices:
                if char in "07689":
                    return pick_dices(rolled_dices, p_liste, playername)
            for char in keep_dices:
                if char in "12345":
                    for index in range(5):
                        if f"{5 - index}" not in keep_dices:
                            rolled_dices.pop(4 - index)
                    return rolled_dices
        else:
            continue


# Eintragen in Gewinnkarte
def karte_abfrage(rolled_dices, pl_liste, player_n):
    # Funktion, die den Spieler fragt, in welche Kategorie der Wurf eingetragen werden soll
    # und die Punkte dafür berechnet und die Punkteliste des Spieler einträgt
    # benötigt die aktuellen Würfel, die Spielerliste für die Punkte und den aktuellen Spieler
    kategorie_auswahl = 0
    while (1 <= kategorie_auswahl <= 13) is False:
        kategorie_auswahl = (
            input(f"Auf welcher Position möchtest du die Punkte eintragen lassen(1-13)? 'k' für Gewinnkarte: "))
        if kategorie_auswahl == "x":
            exit_g = input("Sicher das Sie das Spiel abbrechen wollen? Bestätigen Sie durch die Eingabe 'exit': ")
            if exit_g == "exit":
                sys.exit("Der Spieler hat das Spiel abgebrochen!")
        try:
            kategorie_auswahl = int(kategorie_auswahl)
        except ValueError:
            print("Gib die Zahl der Position zwischen 1-13 an!")
            if kategorie_auswahl == "k":
                gewinnkarte(pl_liste.get(player), bonus_points(pl_liste.get(player)))
                dices = [dice_list[:]]
                termtables.print(
                    dices,
                    style=termtables.styles.double_thin
                )
            kategorie_auswahl = 0
            continue
        except TypeError:
            print("Gib eine gültige Eingabe ein!")
            kategorie_auswahl = 0
            continue
        else:
            if not 1 <= kategorie_auswahl <= 13:
                print("Gib die Zahl der Position zwischen 1-13 an!")
                kategorie_auswahl = 0
                continue
        if pl_liste.get(player_n)[kategorie_auswahl] != "-":
            print("Die Kategorie ist schon belegt!")
            kategorie_auswahl = 0
            continue
    if kategorie_auswahl == 1:
        pl_liste.get(player_n)[1] = nur_einser(rolled_dices)
    elif kategorie_auswahl == 2:
        pl_liste.get(player_n)[2] = nur_zweier(rolled_dices)
    elif kategorie_auswahl == 3:
        pl_liste.get(player_n)[3] = nur_dreier(rolled_dices)
    elif kategorie_auswahl == 4:
        pl_liste.get(player_n)[4] = nur_vierer(rolled_dices)
    elif kategorie_auswahl == 5:
        pl_liste.get(player_n)[5] = nur_fuenfer(rolled_dices)
    elif kategorie_auswahl == 6:
        pl_liste.get(player_n)[6] = nur_sechser(rolled_dices)
    elif kategorie_auswahl == 7:
        pl_liste.get(player_n)[7] = dreier_pasch(rolled_dices)
    elif kategorie_auswahl == 8:
        pl_liste.get(player_n)[8] = vierer_pasch(rolled_dices)
    elif kategorie_auswahl == 9:
        pl_liste.get(player_n)[9] = full_house(rolled_dices)
    elif kategorie_auswahl == 10:
        pl_liste.get(player_n)[10] = kleine_strasse(rolled_dices)
    elif kategorie_auswahl == 11:
        pl_liste.get(player_n)[11] = grosse_strasse(rolled_dices)
    elif kategorie_auswahl == 12:
        pl_liste.get(player_n)[12] = kniffel(rolled_dices)
    elif kategorie_auswahl == 13:
        pl_liste.get(player_n)[13] = chance(rolled_dices)
    if kniffel(rolled_dices) == 50 and kategorie_auswahl != 12:
        if pl_liste.get(player_n)[14] == "-":
            pl_liste.get(player_n)[14] = 50
        else:
            pl_liste.get(player_n)[14] += 50


def nur_einser(rolled_dices):
    # Funktion, um die Punkte für die Kategorie 1 zu berechnen und auszugeben
    points = 0
    for dice in rolled_dices:
        if dice == 1:
            points += 1
    if kniffel(rolled_dices) == 50:
        points = 6
    return points


def nur_zweier(rolled_dices):
    # Funktion, um die Punkte für die Kategorie 2 zu berechnen und auszugeben
    points = 0
    for dice in rolled_dices:
        if dice == 2:
            points += 2
    if kniffel(rolled_dices) == 50:
        points = 10
    return points


def nur_dreier(rolled_dices):
    # Funktion, um die Punkte für die Kategorie 3 zu berechnen und auszugeben
    points = 0
    for dice in rolled_dices:
        if dice == 3:
            points += 3
    if kniffel(rolled_dices) == 50:
        points = 15
    return points


def nur_vierer(rolled_dices):
    # Funktion, um die Punkte für die Kategorie 4 zu berechnen und auszugeben
    points = 0
    for dice in rolled_dices:
        if dice == 4:
            points += 4
    if kniffel(rolled_dices) == 50:
        points = 20
    return points


def nur_fuenfer(rolled_dices):
    # Funktion, um die Punkte für die Kategorie 5 zu berechnen und auszugeben
    points = 0
    for dice in rolled_dices:
        if dice == 5:
            points += 5
    if kniffel(rolled_dices) == 50:
        points = 25
    return points


def nur_sechser(rolled_dices):
    # Funktion, um die Punkte für die Kategorie 6 zu berechnen und auszugeben
    points = 0
    for dice in rolled_dices:
        if dice == 6:
            points += 6
    if kniffel(rolled_dices) == 50:
        points = 30
    return points


def dreier_pasch(rolled_dices):
    # Funktion, um die Punkte für die Kategorie 7 zu berechnen und auszugeben
    points = 0
    for dices in range(1, 7):
        if kniffel(rolled_dices) == 50:
            points = 30
            break
        if rolled_dices.count(dices) >= 3:
            points = sum(rolled_dices)
            break
    return points


def vierer_pasch(rolled_dices):
    # Funktion, um die Punkte für die Kategorie 8 zu berechnen und auszugeben
    points = 0
    for dices in range(1, 7):
        if kniffel(rolled_dices) == 50:
            points = 30
            break
        if rolled_dices.count(dices) >= 4:
            points = sum(rolled_dices)
            break
    return points


def full_house(rolled_dices):
    # Funktion, um die Punkte für die Kategorie 9 zu berechnen und auszugeben
    points = 0
    rolled_dices.sort()
    if rolled_dices.count(rolled_dices[0]) == 3 and rolled_dices.count(rolled_dices[-1]) == 2 \
            or rolled_dices.count(rolled_dices[0]) == 2 and rolled_dices.count(rolled_dices[-1]) == 3:
        points = 25
    if kniffel(rolled_dices) == 50:
        points = 30
    return points


def kleine_strasse(rolled_dices):
    # Funktion, um die Punkte für die Kategorie 10 zu berechnen und auszugeben
    points = 0
    if kniffel(rolled_dices) == 50:
        points = 30
    else:
        rolled_dices.sort()
        rolled_dices = str(set(rolled_dices))
        if "1, 2, 3, 4" in rolled_dices or "2, 3, 4, 5" in rolled_dices or "3, 4, 5, 6" in rolled_dices:
            points = 30
    return points


def grosse_strasse(rolled_dices):
    # Funktion, um die Punkte für die Kategorie 11 zu berechnen und auszugeben
    points = 0
    if kniffel(rolled_dices) == 50:
        points = 30
    else:
        rolled_dices.sort()
        rolled_dices = str(set(rolled_dices))
        if "1, 2, 3, 4, 5" in rolled_dices or "2, 3, 4, 5, 6" in rolled_dices:
            points = 40
    return points


def kniffel(rolled_dices):
    # Funktion, um die Punkte für die Kategorie 12 zu berechnen und auszugeben
    points = 0
    for dices in range(1, 7):
        if rolled_dices.count(dices) == 5:
            points = 50
            break
    return points


def chance(rolled_dices):
    # Funktion, um die Punkte für die Kategorie 13 zu berechnen und auszugeben
    points = sum(rolled_dices)
    if kniffel(rolled_dices) == 50:
        points = 30
    return points


def bonus_points(points):
    # Funktion, um die Bonuspunkte auswertet und Gesamtpunkte ausgibt
    # benötigt die Spielerliste um auf die Punkte des Spielers zu zugreifen
    bonus_punkte = [0, 0, 0, 0, 0]
    temp_points = points[:]
    for ind in range(len(temp_points)):
        if temp_points[ind] == "-":
            temp_points[ind] = 0
    bonus_punkte[0] = sum(temp_points[1:7])
    if bonus_punkte[0] > 62:
        bonus_punkte[1] = 35
    if bonus_punkte[1] == 35:
        bonus_punkte[2] = sum(bonus_punkte[0:2])
    else:
        bonus_punkte[2] = bonus_punkte[0]
    bonus_punkte[3] = sum(temp_points[7:14])
    bonus_punkte[4] = sum(bonus_punkte[2:4]) + temp_points[14]
    return bonus_punkte


# Gewinnerplatzierung
def placement(pla_list):
    # Funktion, um die Spieler nach ihrem Punktestand zu sortieren und die Gewinnerliste auszugeben
    # benötigt die Spielerliste
    placements = {}
    for players in pla_list:
        placements[pla_list.get(players)[0]] = (bonus_points(pla_list.get(players)))[4]
    final_placement = dict(sorted(placements.items(), key=lambda item: item[1], reverse=True))
    for rank in range(len(list(final_placement))):
        print(f"Platz {rank + 1} ist {list(final_placement)[rank]} mit {list(final_placement.values())[rank]} Punkten!")


# Start des Programmes
print("Wilkommen bei Kniffel 5000!!!! Das beste Kniffel Spiel das je programmiert wurde!!!")
print("Wenn du an der Reihe bist, kannst du deine Würfel anhand der Position des Würfels 1-5 speichern.")
print("Würfel die du nicht auswählst, werden neu gewürfelt! Mit Eingabe durch '0' werden alle Würfel neu gewürfelt.")
print("Du kannst durch Eingabe von 'e' deinen Zug vorzeitig beenden und Punkte eintragen!")
print("Mit Eingabe von 'k' kannst du dir jederzeit deine Gewinnkarte anzeigen lassen!")
print("Wenn du das Spiel abbrechen möchtest, kannst du das durch die Eingabe von 'x' durchführen!")
print("Viel Spaß und viel Glück beim Kniffel spielen!")

# Namen der Spieler eintragen
player_list = {}
player_count = anzahl_spieler()
for i in range(player_count):
    player_list[f"Spieler{i + 1}"] = [input(f"Wie heißt Spieler {i + 1}: "), "-", "-", "-", "-", "-", "-", "-", "-",
                                      "-", "-", "-", "-", "-", "-"]
print_p_list(player_list)

# Anfrage nach Spielstart
g_start = game_start()

# Abfrage nach Änderung der Spielerliste
if g_start == "ä":
    p_number = 0
    while g_start == "ä":
        while (1 <= p_number <= len(player_list)) is False:
            try:
                p_number = int(input("Welchen Spieler möchten Sie ändern?: "))
            except ValueError:
                print("Bitte gib die Zahl des Spielers ein, dessen Namen du ändern möchtest!")
                continue
            if (1 <= p_number <= player_count) is False:
                print("Bitte gib die Zahl des Spielers ein, dessen Namen du ändern möchtest!")
                continue
        player_list.get(f"Spieler{p_number}")[0] = input("Wie soll der Spieler heißen?: ")
        print_p_list(player_list)
        g_start = game_start()
        p_number = 0

# Beginn des Spiels
if g_start == "s":
    running = True
    while running:
        for i in range(13):
            for key in player_list:
                print(f"Der Spieler {(list(player_list.get(key))[0])} ist an der Reihe!")
                player = key
                dice_list = []
                while True:
                    for turn in range(3):
                        dice_list = roll_dices(dice_list)
                        if turn == 2:
                            karte_abfrage(dice_list, player_list, player)
                            gewinnkarte(player_list.get(player), bonus_points(player_list.get(player)))
                            break
                        dice_list = pick_dices(dice_list, player_list, player)
                        if dice_list == "endTurn":
                            break
                    break
        placement(player_list)
        print("Das Spiel ist zu Ende!")
        break