from source.game import Game
import pygame

if __name__ == "__main__":
    game = Game()
    game.fruit_generate()
    game.game_loop()
    pygame.quit()