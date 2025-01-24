#def Random_word():

def Life():
    word_to_guess = Random_word()
    guessed_letters = set()
    hp = 6

def display_word(word, guessed_letters):
    display = ""
    for letter in word:
        if letter in guessed_letters:
            display += letter
        else:
            display += "_"
    return display

def hangman():
    print("Welcome to the Hangman game!")
    print(display_word(word_to_guess, guessed_letters))

    while hp > 0:
        guess = input("Guess a letter: ").lower()

        if guess in guessed_letters:
            print("You have already guessed this letter. Try another one.")
            continue

        guessed_letters.add(guess)

        if guess in word_to_guess:
            print("Good guess!")
        else:
            hp -= 1
            print(f"Wrong guess. You have {hp} hit points left.")

        print(display_word(word_to_guess, guessed_letters))

        if all(letter in guessed_letters for letter in word_to_guess):
            print("Congratulations! You guessed the word.")
            break
    else:
        print(f"Sorry, you have run out of hit points. The word was '{word_to_guess}'.")

hangman()

