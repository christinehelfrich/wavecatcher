import arcade
import os
import random



# --- Constants ---
PATH = os.path.dirname(os.path.abspath(__file__))
SPRITE_SCALING_PLAYER = .2
SPRITE_SCALING_ENEMY = .15
ENEMY_COUNT = 2

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Wave Catcher"

ENEMY_VELOCITY = .8


class Enemy(arcade.Sprite):
    """
    This class represents the enemies on our screen. It is a child class of
    the arcade library's "Sprite" class.
    """

    def reset_pos(self):

        # Reset the enemy to a random spot above the screen
        self.center_y = random.randrange(SCREEN_HEIGHT + 20,
                                         SCREEN_HEIGHT + 100)
        self.center_x = random.randrange(SCREEN_WIDTH)

    def update(self):

        # Move the enemy
        self.center_y -= ENEMY_VELOCITY

        # See if the enemy has fallen off the bottom of the screen.
        # If so, reset it.
        if self.top < 0:
            # self.reset_pos()
            self.remove_from_sprite_lists()


class GameView(arcade.Window):
    """ Our custom Window Class"""

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Variables that will hold sprite lists
        self.player_list = None
        self.enemy_list = None

        # Set up the player info
        self.player_sprite = None
        self.score = 0

        # Don't show the mouse cursor
        self.set_mouse_visible(False)

        arcade.set_background_color(arcade.color.BLUE_SAPPHIRE)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()

        # Score
        self.score = 0

        # Set up the player
        # Character image from kenney.nl
        img = os.path.join(PATH, "./sprites/surfer.png")
        self.player_sprite = arcade.Sprite(img, SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)



    def on_draw(self):
        """ Draw everything """
        arcade.start_render()
        self.enemy_list.draw()
        self.player_list.draw()

        # Put the text on the screen.
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

    def on_mouse_motion(self, x, y, dx, dy):
        """ Handle Mouse Motion """

        # Move the center of the player sprite to match the mouse x, y
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.enemy_list.update()

        # Generate a list of all sprites that collided with the player.
        enemy_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                              self.enemy_list)

        # Loop through each colliding sprite, remove it, and add to the score.
        for enemy in enemy_hit_list:
            enemy.remove_from_sprite_lists()
            self.score += 1
        self.spawn_enemies(delta_time)

    def spawn_enemies(self, delta_time):

        for i in range(ENEMY_COUNT):
            # Have a random 1 in 200 change of shooting each 1/60th of a second
            odds = 40

            # Adjust odds based on delta-time
            adj_odds = int(odds * (1 / 60) / delta_time)


            if random.randrange(adj_odds) == 0:
                randoNum = random.randint(1, 100)

                if randoNum % 3 == 0:
                    # Set up virus
                    enemy = Enemy(os.path.join(PATH, "./sprites/wave.png"), SPRITE_SCALING_ENEMY)

                            # Set its position to a random position at the top of the screen
                    enemy.left = random.randint(60, SCREEN_WIDTH - 75)
                    enemy.top = SCREEN_HEIGHT
                    enemy.radius = 30
                    self.enemy_list.append(enemy)
                    
                else: 
                    # Set up karen
                    enemy = Enemy(os.path.join(PATH, "./sprites/wave.png"), SPRITE_SCALING_ENEMY)
        
                            # Set its position to a random position at the top of the screen
                    enemy.left = random.randint(60, SCREEN_WIDTH - 75)
                    enemy.top = SCREEN_HEIGHT
                    enemy.radius = 30
                    self.enemy_list.append(enemy)



def main():
    """ Main method """
    window = GameView()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()