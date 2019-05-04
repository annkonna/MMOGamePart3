import pygame
import json

import model.surviv_model


class Controller(object):

    def __init__(self, p_rect, m_width):
        self.game_over = False
        game_dict = {
            "p_left": p_rect.left,
            "p_top": p_rect.top, 
            "p_width": p_rect.width, 
            "p_height": p_rect.height,
            "m_width": m_width
        }
        self.game = model.surviv_model.GameInterface(json.dumps(game_dict))
#        self.game = model.surviv_model.Game(p_rect, m_width)


    def set_player(self, x, y):
        ppos_dict = {
            "x": x,
            "y": y
        }
        self.game.set_player(json.dumps(ppos_dict))
#        self.game.set_player(x, y)

    def update_redzone_pos(self):
        self.game.update_redzone_pos()

    def get_redzone_pos(self):
        json_r_dict = self.game.get_redzone_pos()
        r_dict = json.loads(json_r_dict)
        return pygame.Rect(r_dict['r_left'], r_dict['r_top'], r_dict['r_width'], r_dict['r_height'])
#      return self.game.get_redzone_pos()

    def get_player_pos(self):
        json_p_dict = self.game.get_player_pos()
        p_dict = json.loads(json_p_dict)
        return pygame.Rect(p_dict['p_left'], p_dict['p_top'], p_dict['p_width'], p_dict['p_height'])
#        return self.game.get_player_pos()

    def is_player_in_redzone(self):
        return json.loads(self.game.is_player_in_redzone())
#        return self.game.is_player_in_redzone()

    def change_player_speed(self, x, y):
        pspeed_dict = {
            "change_x": x,
            "change_y": y
        }
        self.game.change_player_speed(json.dumps(pspeed_dict))
#        self.game.change_player_speed(x,y)

    def move_player(self):
        self.game.move_player()

    @staticmethod
    def process_welcome_events(rect):
        done = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = 1
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if rect.left < pos[0] < rect.right and rect.top < pos[1] < rect.bottom:
                    done = 2  # Play Solo button pressed.
        return done

    def process_game_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.change_player_speed(-5, 0)
                if event.key == pygame.K_RIGHT:
                    self.change_player_speed(5, 0)
                if event.key == pygame.K_UP:
                    self.change_player_speed(0, -5)
                if event.key == pygame.K_DOWN:
                    self.change_player_speed(0, 5)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.change_player_speed(5, 0)
                if event.key == pygame.K_RIGHT:
                    self.change_player_speed(-5, 0)
                if event.key == pygame.K_UP:
                    self.change_player_speed(0, 5)
                if event.key == pygame.K_DOWN:
                    self.change_player_speed(0, -5)

        self.move_player()
        return False
