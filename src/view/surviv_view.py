import pygame
import os
import controller.surviv_controller
import random

DARK_GREEN = (0, 100, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIME = (0, 255, 0)
LIGHT_GREEN = (144, 238, 144)
GRAY = (128, 128, 128)
LIGHT_GRAY = (211, 211, 211)
DARK_GRAY = (169, 169, 169)
RED = (255, 0, 0)


class View(object):
    display_width = 0

    def __init__(self):

        pygame.init()
        pygame.font.init()

        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 50)

        # Set the width and height of the screen [width,height]
        info = pygame.display.Info()
        self.display_width = info.current_w
        self.display_height = info.current_h - 100
        self.screen = pygame.display.set_mode((self.display_width, self.display_height))

        pygame.display.set_caption("surviv.io clone - 2d Battle Royale game")

        self.score = 0
        self.game_over = False
        self.elapsed_time = 0
        self.redzone_time = 0
        self.scorefont = None
        self.h1_font = None
        self.h2_font = None
        self.menu_font = None
        self.game_controller = None
        self.score_surface = None
        self.h1_surface = None
        self.h2_surface = None
        self.m1_surface = None
        self.m2_surface = None
        self.m3_surface = None
        self.m4_surface = None
        self.rz_surface = None
        self.menu_rect = None
        self.background_image = None
        self.player_image = None

    def main_loop(self):
        done = 0

        # Frame rate is set using clock in the program loop
        clock = pygame.time.Clock()

        self.player_image = pygame.image.load("view\\player.gif").convert()
        self.player_image.set_colorkey((0, 0, 0))  # may not need it for BLACK as it is default
        print(self.player_image.get_rect())
        self.game_controller = controller.surviv_controller.Controller(self.player_image.get_rect(), self.display_width)

        self.h1_font = pygame.font.SysFont('serif', 32)
        self.h1_font.set_bold(True)
        self.h2_font = pygame.font.SysFont('serif', 24)
        self.h2_font.set_bold(True)
        self.menu_font = pygame.font.SysFont('times new roman', 14)

        while not done:
            done = self.game_controller.process_welcome_events(self.menu_rect)
            if done == 2:
                break  # play game
            self.welcome_logic()
            self.draw_welcome_frame()
            self.display_frame()
            # Pause for the next frame
            clock.tick(20)

        if done == 1:
            pygame.quit()
            return

        done = 0
        self.background_image = pygame.image.load("view\\game_background.gif").convert()
        self.background_image = pygame.transform.scale(self.background_image, (self.display_width, self.display_height))

        self.scorefont = pygame.font.SysFont('Comic Sans MS', 30)

        self.game_controller.set_player(random.randrange(self.display_width), random.randrange(self.display_height))

        game_over_flag = False
        while not done:
            done = self.game_controller.process_game_events()
            ret = self.game_logic()
            if not game_over_flag:
                self.draw_game_frame()
                self.display_frame()
            game_over_flag = ret
            clock.tick(20)  # max 20 frames per second.

        pygame.quit()

    def welcome_logic(self):
        self.h1_surface = self.h1_font.render('SURVIV.IO CLONE', True, WHITE)
        self.h2_surface = self.h2_font.render('BATTLE ROYALE', True, LIME)
        self.m1_surface = self.menu_font.render('Enter your name here.', True, DARK_GRAY)
        self.m2_surface = self.menu_font.render('Number of Players: 10', True, BLACK)
        self.m3_surface = self.menu_font.render('Play Solo', True, BLACK)
        self.m4_surface = self.menu_font.render('How to Play', True, BLACK)

    def draw_welcome_frame(self):
        # draw background
        self.screen.fill(DARK_GREEN)
        # draw menu background
        menu_rect = pygame.Rect(0, 0, self.display_width/5, self.display_height/3)
        menu_rect.center = (self.display_width/2, self.display_height*5/12)
        self.screen.fill(BLACK, menu_rect)
        # draw "Enter your name here" Edit Box
        menu_rect.centery += 25
        menu_rect.centerx += 15
        menu_rect.height = menu_rect.height/6
        menu_rect.width -= 30
        self.screen.fill(WHITE, menu_rect)
        self.screen.blit(self.m1_surface, self.m1_surface.get_rect(center=(menu_rect.centerx, menu_rect.centery)))
        # draw "Number of Players" Text Box
        menu_rect.centery += 45
        self.screen.fill(WHITE, menu_rect)
        self.screen.blit(self.m2_surface, self.m2_surface.get_rect(center=(menu_rect.centerx, menu_rect.centery)))
        # draw "Play Solo" button
        menu_rect.centery += 45
        self.screen.fill(LIGHT_GREEN, menu_rect)
        self.screen.blit(self.m3_surface, self.m3_surface.get_rect(center=(menu_rect.centerx, menu_rect.centery)))
        # draw "How to Play" button
        menu_rect.centery += 45
        self.screen.fill(LIGHT_GRAY, menu_rect)
        self.screen.blit(self.m4_surface, self.m4_surface.get_rect(center=(menu_rect.centerx, menu_rect.centery)))

        # set the menu rectangle to be that of the play solo button.
        menu_rect.centery -= 45
        self.menu_rect = menu_rect

        self.screen.blit(self.h1_surface, self.h1_surface.get_rect(center=(self.display_width / 2, 50)))
        self.screen.blit(self.h2_surface, self.h2_surface.get_rect(center=(self.display_width / 2, 100)))

    def game_logic(self):
        """
        The time spent by player in the redzone and the elapsed time are tracked to determine
        game status (won, done, continue).
        """
        if self.game_controller.is_player_in_redzone():
            self.redzone_time += 1

        self.elapsed_time += 1
        if self.elapsed_time/20 > 30:
            self.score_surface = \
                self.scorefont.render('You Won!! Survival Time (Secs): ' + str(round(self.elapsed_time / 20, 2)),
                                      False, (0, 0, 0))
            return True
        elif self.redzone_time/20 > 5:
            self.score_surface = \
                self.scorefont.render('Game Over!! Survival Time (Secs): ' + str(round(self.elapsed_time / 20, 2)),
                                      False, (0, 0, 0))
            return True
        else:
            self.score_surface = \
                self.scorefont.render('Survival Time (Secs): ' + str(round(self.elapsed_time / 20, 2)),
                                      False, (0, 0, 0))
            return False

    def draw_game_frame(self):
        self.screen.fill(WHITE)
        self.screen.blit(self.background_image, [0, 0])
        self.game_controller.update_redzone_pos()
        self.screen.fill(RED, self.game_controller.get_redzone_pos())
        p_rect = self.game_controller.get_player_pos()
        self.screen.blit(self.player_image, [p_rect.x, p_rect.y])
        self.screen.blit(self.score_surface, (self.display_width / 3, 10))

    @staticmethod
    def display_frame():
        """ Display the drawing which contains the game/welcome screen """
        pygame.display.flip()
