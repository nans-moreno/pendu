import pygame
from helpers import get_random_word, enter_new_word, get_user, write_user_score, display_score

class RenderGame: #parameters for the display
    def __init__(self, screen_width, screen_height, game_name):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption(game_name)
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.red = (255, 0, 0)
        self.blue = (0, 0, 255)

        self.font = pygame.font.Font(None, 36)
        self.letter_font = pygame.font.Font(None, 28)
        self.keyboard = self.create_keyboard()

        self.hangman_parts =[
            (300, 450, 150, 10),  # Base
            (300, 200, 10, 250),  # vertical pole
            (300, 200, 100, 10),  # horizontal pole
            ((400, 200), (400, 230)),    # rope
            (400, 250, 20),       # head
            ((400, 270), (400, 350)),  # body
            ((400, 300), (370, 330)),  # left arm
            ((400, 300), (430, 330)),  # right arm
            ((400, 350), (370, 390)),  # left leg
            ((400, 350), (430, 390)),  # right leg
        ]

        self.menu_options = [
            {"text": "Play", "rect": pygame.Rect(300, 200, 200, 50), "action": "hangman_game"},
            {"text": "Score", "rect": pygame.Rect(300, 300, 200, 50), "action": "score"},
            {"text": "Add a word", "rect": pygame.Rect(300, 400, 200, 50), "action": "add_word"}
        ]



    def draw_score_screen(self):
        scores = display_score()
        
        sorted_scores = sorted(scores.values(), key=lambda x: x["victory"], reverse=True)
        
        self.screen.fill(self.white)
        self.draw_text("Score", 20, 20, self.black)
        
        y_offset = 150 
        for player in sorted_scores:
            score_text = f"{player['name']}: {player['victory']} victories, {player['defeat']} defeats, {player['nb_game_played']} played games"
            self.draw_text(score_text, 100, y_offset, self.black)
            y_offset += 30 

 

    def draw_menu_screen(self):
        for option in self.menu_options:
            pygame.draw.rect(self.screen, self.black, option["rect"])
            text_surface = self.font.render(option["text"], True, self.white)
            text_rect = text_surface.get_rect(center=option["rect"].center)
            self.screen.blit(text_surface, text_rect)

    def draw_hangman_game_screen(self, attempts, guessed_letters, word_to_guess, player):
        self.screen.fill(self.white)
        self.draw_text(player.get("name"), 20, 20, self.blue)
        self.draw_word(guessed_letters, word_to_guess)
        self.draw_hangman(attempts)
        self.draw_keyboard()


    def draw_add_word_screen(self, current_word):
        self.screen.fill(self.white)
        self.draw_text("Add a word", 300, 50, self.black)
        self.draw_text(f"Current word : {current_word}", 200, 200, self.blue)
        self.draw_text("Press enter to validate", 200, 400, self.red)

    def draw_enter_name_screen(self, current_name):
        self.screen.fill(self.white)
        self.draw_text("Enter your name", 300, 50, self.black)
        self.draw_text(f"Current name : {current_name}", 200, 200, self.blue)
        self.draw_text("Press enter to validate", 200, 400, self.red)

    def create_keyboard(self):
        rows = ["ABCDEFGHIJKLM", "NOPQRSTUVWXYZ"]
        keyboard = []
        x_start = 50
        y_start = 500
        button_width = 40
        button_height = 40  
        spacing = 10

        for row_index, row in enumerate(rows):
            for col_index, letter in enumerate(row):
                x = x_start + col_index * (button_width + spacing)
                y = y_start + row_index * (button_height + spacing)
                keyboard.append({
                    "rect": pygame.Rect(x, y, button_width, button_height),
                    "letter": letter,
                    "clicked": False
                })

        return keyboard
    
    def handle_menu_events(self, pos, word_to_guess):
        for option in self.menu_options:
            if option["rect"].collidepoint(pos):
                if option["action"] == "hangman_game":
                    self.draw_hangman_game_screen(0, {}, word_to_guess, {})
                elif option["action"] == "score":
                    self.draw_score_screen()
                elif option["action"] == "add_word":
                    self.draw_add_word_screen("")
                return option["action"]


    def handle_mouse_click(self, pos):
      for key in self.keyboard:
          if key["rect"].collidepoint(pos) and not key["clicked"]:
              key["clicked"] = True  # register the button as clicked
              return key.get("letter")

    def draw_text(self, text, x, y, color):
        label = self.font.render(text, True, color)
        self.screen.blit(label, (x, y))

    def draw_hangman(self, attempts):
        for i in range(attempts):
            part = self.hangman_parts[i]
            if i < 3:  # Rectangle (base, poles)
                pygame.draw.rect(self.screen, self.black, part)
            elif i == 3:  # Rope  (line)
                pygame.draw.line(self.screen, self.black, part[0], part[1], 2)
            elif i == 4:  # Head (circle)
                pygame.draw.circle(self.screen, self.black, (part[0], part[1]), part[2], 2)
            elif i >= 5:  # Lines (body, arms, legs)
                pygame.draw.line(self.screen, self.black, part[0], part[1], 2)


    def draw_word(self, guessed_letters, word_to_guess):
        display_word = " ".join([letter if letter in guessed_letters else "_" for letter in word_to_guess.upper()])
        self.draw_text(display_word, 300, 100, self.black)
        return display_word

    def draw_keyboard(self):
        for key in self.keyboard:
            color = self.blue if key["clicked"] else self.black
            pygame.draw.rect(self.screen, color, key["rect"], 2)
            letter_surface = self.letter_font.render(key["letter"], True, color)
            letter_rect = letter_surface.get_rect(center=key["rect"].center)
            self.screen.blit(letter_surface, letter_rect)

        
class HangmanGame: #Containt game rules and the run
    _game_instance = None  # Design pattern Singleton allows to have one instance of the game if we launch two time the same class

    def __new__(cls, *args, **kwargs):
        if cls._game_instance is None:
            # Create an instance if none is existing
            cls._game_instance = super().__new__(cls)
        return cls._game_instance

    def __init__(self):
        pygame.init()
        self.state = "menu"
        self.word_to_guess = ""
        self.guessed_word = ""
        self.guessed_letters = set()
        self.max_attempts = 10
        self.attempts = 0
        self.render_game = RenderGame(800, 600, "Hangman Game")
        self.player = {}

    def lose_game(self):
        return self.attempts == self.max_attempts
    
    def game_status(self):
        if self.attempts == self.max_attempts:
            return "lose"
        elif self.guessed_word.lower() == self.word_to_guess.lower():
            return "victory"
        else: return "ongoing"
    
    def word_attempt(self, letter):
        if letter.lower() in self.word_to_guess:
            self.guessed_letters.add(letter)
            self.guessed_word = self.render_game.draw_word(self.guessed_letters, self.word_to_guess).replace(" ", "")

        else:
            self.attempts += 1
            
    
    def run(self): #Game loop
        running = True
        current_word = ""
        current_name = ""

        while running:
            self.render_game.screen.fill(self.render_game.white)
                
            if self.state == "menu":
                self.render_game.draw_menu_screen()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.word_to_guess = get_random_word()
                        self.guessed_word = ""
                        self.guessed_letters = set()
                        self.attempts = 0
                        self.render_game.keyboard = self.render_game.create_keyboard()
                        
                        self.state = self.render_game.handle_menu_events(event.pos, self.word_to_guess)

            elif self.state == "enter_name":
                self.render_game.draw_enter_name_screen(current_name)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            if current_name.strip():
                                self.player[current_name] = {"name": current_name, "victory": 0, "defeat": 0, "nb_game_played": 0}
                                self.player = get_user(self.player)

                                current_name = ""
                                self.state = "hangman_game"
                        elif event.key == pygame.K_BACKSPACE:
                            current_name = current_name[:-1]
                        elif event.unicode.isalpha():
                            current_name += event.unicode

            elif self.state == "hangman_game":
                if not self.player:
                    self.state = "enter_name"
                    continue

                self.render_game.screen.fill(self.render_game.white)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        letter = self.render_game.handle_mouse_click(event.pos)
                        if letter:
                            self.word_attempt(letter)
                self.render_game.draw_hangman_game_screen(self.attempts, self.guessed_letters, self.word_to_guess, self.player)

                game_status = self.game_status()
                if game_status == "lose":
                    self.render_game.draw_text(f"You lose, the word was : {self.word_to_guess}", 300, 150, self.render_game.red)
                    
                    self.player["defeat"] += 1 
                    self.player["nb_game_played"] += 1 

                    write_user_score(self.player.get("name"), self.player)
                    pygame.display.flip()
                    pygame.time.wait(6000)
                    self.state = "menu"
                    self.player = {}
                    self.render_game.draw_menu_screen()

                elif game_status == "victory":
                    self.render_game.draw_text("You won !", 300, 150, self.render_game.blue)

                    self.player["victory"] += 1
                    self.player["nb_game_played"] += 1 

                    write_user_score(self.player.get("name"), self.player)


                    pygame.display.flip()
                    pygame.time.wait(6000)
                    self.state = "menu"

                    self.player = {}
                    self.render_game.draw_menu_screen()

            elif self.state == "score":
                self.render_game.draw_score_screen()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.state = "menu"
                        self.render_game.draw_menu_screen()

            elif self.state == "add_word":
                self.render_game.draw_add_word_screen(current_word)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.state = "menu"
                        self.render_game.draw_menu_screen()

                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN: 
                            if current_word.strip(): 
                                self.word_to_guess = current_word.lower()
                                enter_new_word(current_word.lower())
                                current_word = "" 
                                self.state = "menu"
                        elif event.key == pygame.K_BACKSPACE: 
                            current_word = current_word[:-1]
                        elif event.unicode.isalpha():
                            current_word += event.unicode


 

            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    game = HangmanGame()
    game.run()