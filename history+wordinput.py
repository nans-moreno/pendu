def enter_new_word():
    try:
        with open("mots.txt", "r") as f :
            text = f.read()
        with open("mots.txt","w") as f:
            word= input("enter a new word:")
            new_entry=f"{word}\n"
            f.write(new_entry + text)
    except FileNotFoundError:
        print("The file mots.txt does not exist !")

def display_history():
    try:
        with open("mots.txt", "r") as f :
            text = f.read()
            print(text)
    except FileNotFoundError:
        print("The file mots.txt does not exist !")

def reset_history():
    try:
        with open("mots.txt","w") as f :
            f.write("")
            print("History succesfully cleared")
    except FileNotFoundError:
        print("The file mots.txt does not exist !")

def menu() :
    print("""
    MENU :
    press 1. Enter a new word in the list.
    press 2. Display the words history.
    press 3. Reset the words history.
    """)
    player_choice=input("choose a mode (1,2,3):")
    if player_choice=="1":
        enter_new_word()
    elif player_choice=="2":
        display_history()
    elif player_choice=="3":
        reset_history()
    else:
        print("Invalid answer !")
    return player_choice

##########################################

nb_victory=0
nb_defeat=0

nb_player=0

def create_username (nb_player,nb_victory,nb_defeat):
    name = input("Enter an username :")
    # history.append(
    history={
            "player":nb_player,
            "name": name,
            "victory":nb_victory,
            "defeat":nb_defeat,
            "nb_game_played":nb_defeat+nb_victory
    }
    return history

def export_txt(history):
    try:
        with open('score.txt','r') as f :
            text=f.read()
        with open('score.txt', 'w') as f: 
            f.write(f"{history}\n")
            f.write(f"{text}\n")
    except FileNotFoundError:
        print("File is inexistant !")

    # try:
    #     with open("score.txt","r") as f :
    #         text=f.read
    # # except FileNotFoundError:
    # #     text=""
    # # history_text = "\n".join(f"{key}: {value}" for key, value in history.items())
    # # with open("score.txt", "w") as f:
    # #     f.write(history_text + "\n\n" + text)
    #     full_history=text.append(history)
    #     with open("score.txt", 'w') as f:
    #         f.write(full_history)
    # except FileNotFoundError:
    #     print("File is inexistant !")

def display_score():
    try:
        with open("score.txt","r") as f:
            text= f.read()
            print(text)
    except FileNotFoundError:
        print("File is inexistant !")

def clear_score():
    try:
        with open("score.txt","w") as f:
            f.write("")
            print("Score table successfully cleared")
    except FileNotFoundError:
        print("File is inexistant! ")
        
while True:
    history=create_username(nb_player,nb_victory,nb_defeat)
    nb_player+=1
    export_txt(history)
    display_score()
# while True:
#     menu()
# clear_score()
