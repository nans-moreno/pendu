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
    """Select an user in scores.txt or add a new one."""

    name = next(iter(user))
    try:
        with open("scores.txt", "r") as f:
            users = json.load(f)
    except FileNotFoundError:
        # add an empty dictionnarie if the file doesn't exist
        users = {}

    # Verify the user is existant
    if name in users:
        return users[name]

    # creat new user if it inexistant
    users.update(user) 

    with open("scores.txt", "w") as f:
        json.dump(users, f, indent=4)

    return users[name]

def write_user_score(name, user):
    """Refresh user score by adding a victory or a defeat."""
    try:
        with open("scores.txt", "r") as f:
            users = json.load(f)
    except FileNotFoundError:
        raise Exception("The file scores.txt is inexistant.")

    if name not in users:
        raise Exception(f"User {name} is inexistant.")

    users[name] = user

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
    # display the score table with also the ratio
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
        