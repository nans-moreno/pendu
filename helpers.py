import random
import json

def enter_new_word(new_entry):
    try:
        with open("mots.txt", "r") as f :
            text = f.read()
        with open("mots.txt","w") as f:
            f.write(new_entry + "\n" + text)
    except FileNotFoundError:
        print("The file mots.txt does not exist !")

def display_dictionnary():
    try:
        with open("mots.txt", "r") as f :
            text = f.read().splitlines()
            return text
            
    except FileNotFoundError:
        print("The file mots.txt does not exist !")

def get_random_word():
    random_number = random.randint(0, len(display_dictionnary()))

    word = display_dictionnary()[random_number]
    return word

def reset_history():
    try:
        with open("mots.txt","w") as f :
            f.write("")
            print("History succesfully cleared")
    except FileNotFoundError:
        print("The file mots.txt does not exist !")

##########################################


def get_user(user):
    """Récupère un utilisateur dans scores.txt ou le crée s'il n'existe pas."""

    name = next(iter(user))
    try:
        # Lire le fichier scores.txt
        with open("scores.txt", "r") as f:
            users = json.load(f)
    except FileNotFoundError:
        # Si le fichier n'existe pas, on initialise un dictionnaire vide
        users = {}

    # Vérifier si l'utilisateur existe
    if name in users:
        return users[name]

    # Si l'utilisateur n'existe pas, le créer
    users.update(user) 

    # Écrire la mise à jour dans le fichier
    with open("scores.txt", "w") as f:
        json.dump(users, f, indent=4)

    return users[name]

def write_user_score(name, user):
    """Met à jour les données d'un utilisateur en ajoutant une victoire ou une défaite."""
    try:
        # Lire le fichier scores.txt
        with open("scores.txt", "r") as f:
            users = json.load(f)
    except FileNotFoundError:
        raise Exception("Le fichier scores.txt est introuvable.")

    # Vérifier si l'utilisateur existe
    if name not in users:
        raise Exception(f"L'utilisateur {name} n'existe pas.")

    users[name] = user

    # Écrire la mise à jour dans le fichier
    with open("scores.txt", "w") as f:
        json.dump(users, f, indent=4)


def export_txt(history):
    try:
        with open('score.txt','r') as f :
            text=f.read()
        with open('score.txt', 'w') as f: 
            f.write(f"{history}\n")
            f.write(f"{text}\n")
    except FileNotFoundError:
        print("File is inexistant !")


def display_score():
    # tableau des scores trié du 1er sur le nb de victoire, afficher le ratio a cote
    try:
        with open("scores.txt", "r") as f:
            scores = json.load(f)
            return scores
    except FileNotFoundError:
        print("File is inexistant !")

def clear_score():
    try:
        with open("scores.txt","w") as f:
            f.write("")
            print("Score table successfully cleared")
    except FileNotFoundError:
        print("File is inexistant! ")
        

name="Nans"
user="Nans"
write_user_score(name, user)