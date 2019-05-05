import pygame
import json
import requests

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
        url = "http://127.0.0.1:8080/init"
        r = requests.post(url, json.dumps(game_dict))

    def set_player(self, x, y):
        pos = {
            "x": x,
            "y": y
        }
        url = "http://127.0.0.1:8080/set_player"
        r = requests.post(url, json.dumps(pos))

    def update_redzone_pos(self):
        url = "http://127.0.0.1:8080/update_redzone_pos"
        r = requests.post(url, None)

    def get_redzone_pos(self):
        url = "http://127.0.0.1:8080/get_redzone_pos"
        r = requests.get(url)
        r_dict = r.json()
        return pygame.Rect(r_dict['r_left'], r_dict['r_top'], r_dict['r_width'], r_dict['r_height'])

    def get_player_pos(self):
        url = "http://127.0.0.1:8080/get_player_pos"
        r = requests.get(url)
        p_dict = r.json()
        return pygame.Rect(p_dict['p_left'], p_dict['p_top'], p_dict['p_width'], p_dict['p_height'])

    def is_player_in_redzone(self):
        url = "http://127.0.0.1:8080/is_player_in_redzone"
        r = requests.get(url)
        return r.json()

    def change_player_speed(self, x, y):
        url = "http://127.0.0.1:8080/change_player_speed"
        pos = {
            "change_x": x,
            "change_y": y
        }
        r = requests.post(url, json.dumps(pos))

    def move_player(self):
        url = "http://127.0.0.1:8080/move_player"
        r = requests.post(url, None)

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
