from Game import *

def main(width=600, height=800, fps=30):
    random.seed()
    pygame.init()

    utils.load_music('bgm.mid')
    # Loop play the BGM
    pygame.mixer.music.play(-1, 0.0)

    # Initialize the game window
    pygame.display.set_mode((width, height), 0, 32)
    pygame.display.set_caption(Game.name)

    # Load resources
    Game.fonts = utils.load_game_fonts()
    Game.sounds = utils.load_game_sounds()
    Game.images = utils.load_game_images()
    Player.images = utils.load_player_images()
    Bubble.images = utils.load_bubble_images()

    game = Game()
    while game.is_running():
        game.update(fps)
        game.draw()

    pygame.quit()
    exit()


if __name__ == '__main__':
    main()
