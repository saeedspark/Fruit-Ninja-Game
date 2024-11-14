import pygame, sys
import os
import random



class Game:
    def __init__(self):
        pygame.init()
        # initialize Variables
        self.player_lives = 3                                                #keep track of lives
        self.score = 0                                                       #keeps track of score
        self.fruits = ['melon', 'orange', 'pomegranate', 'guava', 'bomb']
        self.first_round = True
        self.game_over = True        #terminates the game While loop if more than 3-Bombs are cut
        self.game_running = True     #used to manage the game loop
        
        # Define colors
        self.WHITE = (255,255,255)
        self.BLACK = (0,0,0)
        self.RED = (255,0,0)
        self.GREEN = (0,255,0)
        self.BLUE = (0,0,255)
        

        self.font = pygame.font.Font(os.path.join(os.getcwd(), 'font/comic.ttf'), 42)
        self.font_name = pygame.font.match_font('font/comic.ttf')
        self.background = pygame.image.load('images/back.jpg')                                  #game background
        self.score_text = self.font.render('Score : ' + str(self.score), True, (255, 255, 255))    #score display
        lives_icon = pygame.image.load('images/white_lives.png')
        
        # initialize pygame and create window
        self.WIDTH = 800
        self.HEIGHT = 500
        self.FPS = 12                                                 #controls how often the gameDisplay should refresh. In our case, it will refresh every 1/12th second
        

        pygame.display.set_caption('Fruit Ninja')
        self.gameDisplay = pygame.display.set_mode((self.WIDTH, self.HEIGHT))   #setting game display size
        self.clock = pygame.time.Clock()
        
        # Generic method to draw fonts on the screen
        
        

        
    # Generalized structure of the fruit Dictionary
    def generate_random_fruits(self, fruit):
        fruit_path = "images/" + fruit + ".png"
        self.data[fruit] = {
            'img': pygame.image.load(fruit_path),
            'x' : random.randint(100,500),          #where the fruit should be positioned on x-coordinate
            'y' : 800,
            'speed_x': random.randint(-10,10),      #how fast the fruit should move in x direction. Controls the diagonal movement of fruits
            'speed_y': random.randint(-80, -60),    #control the speed of fruits in y-directionn ( UP )
            'throw': False,                         #determines if the generated coordinate of the fruits is outside the gameDisplay or not. If outside, then it will be discarded
            't': 0,                                 #manages the
            'hit': False,
        }

        if random.random() >= 0.75:     #Return the next random floating point number in the range [0.0, 1.0) to keep the fruits
            self.data[fruit]['throw'] = True
        else:
            self.data[fruit]['throw'] = False
                
    def fruit_generate(self):
        self.data = {}
        for fruit in self.fruits:
            self.generate_random_fruits(fruit)
              
    def hide_cross_lives(self, x, y):
        self.gameDisplay.blit(pygame.image.load("images/red_lives.png"), (x, y))
        
    def draw_text(self, display, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.gameDisplay.blit(text_surface, text_rect)
        
    def draw_lives(self,display, x, y, lives, image):
        for i in range(self.player_lives):
            img = pygame.image.load("images/white_lives.png")
            img_rect = img.get_rect()
            img_rect.x = x + 30 * i
            img_rect.y = y
            self.gameDisplay.blit(img, img_rect)
            
    # show game over display & front display
    def show_gameover_screen(self):
        self.gameDisplay.blit(self.background, (0,0))
        self.draw_text(self.gameDisplay, "FRUIT NINJA", 90, self.WIDTH / 2, self.HEIGHT / 4)
        if not self.game_over:
            self.draw_text(self.gameDisplay,"Score : " + str(self.score), 50, self.WIDTH / 2, self.HEIGHT /2)
            
        self.draw_text(self.gameDisplay, "Press a Key to Play Again", 64, self.WIDTH / 2, self.HEIGHT * 3 / 4)
        pygame.display.flip()
        waiting = True
        while waiting:
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYUP:
                    waiting = False
                    
    # Main game loop
    def game_loop(self):
        while self.game_running :
            if self.game_over :
                if self.first_round:
                    self.show_gameover_screen()
                    self.first_round = False
                self.game_over = False
                self.player_lives = 3
                self.draw_lives(self.gameDisplay, 690, 5, self.player_lives, 'images/red_lives.png')
                self.score = 0

            for event in pygame.event.get():
                # checking for closing window
                if event.type == pygame.QUIT:
                    self.game_running = False

            self.gameDisplay.blit(self.background, (0, 0))
            self.gameDisplay.blit(self.score_text, (0, 0))
            self.draw_lives(self.gameDisplay, 690, 5, self.player_lives, 'images/red_lives.png')

            for key, value in self.data.items():
                if value['throw']:
                    value['x'] += value['speed_x']          #moving the fruits in x-coordinates
                    value['y'] += value['speed_y']          #moving the fruits in y-coordinate
                    value['speed_y'] += (1 * value['t'])    #increasing y-corrdinate
                    value['t'] += 1                         #increasing speed_y for next loop

                    if value['y'] <= 800:
                        self.gameDisplay.blit(value['img'], (value['x'], value['y']))    #displaying the fruit inside screen dynamically
                    else:
                        self.generate_random_fruits(key)

                    current_position = pygame.mouse.get_pos()   #gets the current coordinate (x, y) in pixels of the mouse

                    if not value['hit'] and current_position[0] > value['x'] and current_position[0] < value['x']+60 \
                        and current_position[1] > value['y'] and current_position[1] < value['y']+60:
                        if key == 'bomb':
                            self.player_lives -= 1
                            if self.player_lives == 0:
                                self.hide_cross_lives(690, 15)
                            elif self.player_lives == 1 :
                                self.hide_cross_lives(725, 15)
                            elif self.player_lives == 2 :
                                self.hide_cross_lives(760, 15)
                            #if the user clicks bombs for three time, GAME OVER message should be displayed and the window should be reset
                            if self.player_lives <= 0 :
                                self.show_gameover_screen()
                                self.game_over = True
                                self.score = 0

                            half_fruit_path = "images/explosion.png"
                        else:
                            half_fruit_path = "images/" + "half_" + key + ".png"

                        value['img'] = pygame.image.load(half_fruit_path)
                        value['speed_x'] += 10
                        if key != 'bomb' :
                            self.score += 1
                        self.score_text = self.font.render('Score : ' + str(self.score), True, (255, 255, 255))
                        value['hit'] = True
                else:
                    self.generate_random_fruits(key)

            pygame.display.update()
            self.clock.tick(self.FPS)