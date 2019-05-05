import pygame
import random
import json
import bottle

class GameInterface(object):
    def __init__(self, g_dict):
        self.game = Game(pygame.Rect(g_dict['p_left'], g_dict['p_top'], g_dict['p_width'], g_dict['p_height']), g_dict['m_width'])

    def set_player(self, ppos_dict):
        self.game.player.startpos(ppos_dict['x'], ppos_dict['y'])

    def update_redzone_pos(self):
        self.game.redzone.update_redzone_pos()

    def get_redzone_pos(self):
        return self.game.redzone.get_redzone_pos()

    def get_player_pos(self):
        return self.game.player.get_player_pos()

    def is_player_in_redzone(self):
        return self.game.is_player_in_redzone()

    def change_player_speed(self, pspeed_dict):
        self.game.change_player_speed(pspeed_dict['change_x'], pspeed_dict['change_y'])

    def move_player(self):
        self.game.move_player()


class Game(object):
    def __init__(self, p_rect, m_width):
        self.player = Player(p_rect)
        self.redzone = Redzone(m_width)

    def update_redzone_pos(self):
        self.redzone.update_redzone_pos()

    def get_redzone_pos(self):
        return self.redzone.get_redzone_pos()

    def set_player(self, x, y):
        self.player.startpos(x, y)

    def get_player_pos(self):
        return self.player.get_player_pos()

    def change_player_speed(self, x, y):
        self.player.changespeed(x, y)

    def move_player(self):
        self.player.move()

    def is_player_in_redzone(self):
        p_rect = self.get_player_pos()
        r_rect = self.get_redzone_pos()
        if p_rect.left > r_rect.left and p_rect.right < r_rect.right \
                and p_rect.top > r_rect.top and p_rect.bottom < r_rect.bottom:
            return True
        return False


class Redzone(object):
    def __init__(self, m_width):
        self.max_width = m_width
        self.rect = pygame.Rect(m_width, random.randrange(0, 400),
                                random.randrange(300, 1500), random.randrange(200, 1000))

    def get_redzone_pos(self):
        return self.rect

    def update_redzone_pos(self):
        self.rect.centerx -= 20
        if self.rect.left < 0:
            self.rect.width -= 20
            if self.rect.width < 0:
                self.rect.left = self.max_width
                self.rect.width = random.randrange(300, 1500)
                self.rect.height = random.randrange(200, 1000)
                self.rect.top = random.randrange(0, 400)


class Player(object):
    def __init__(self, p_rect):
        # set speed vector
        self.change_x = 0
        self.change_y = 0
        self.rect = p_rect

    def get_player_pos(self):
        return self.rect

    def startpos(self, x, y):
        # Make our top-left corner the passed-in location.
        self.rect.x = x
        self.rect.y = y

    def changespeed(self, x, y):
        self.change_x += x
        self.change_y += y

    def move(self):
        # Move left/right
        self.rect.x += self.change_x
        # Move up/down
        self.rect.y += self.change_y


game = None

@bottle.post('/init')
def do_init():
    global game
    content = bottle.request.body.read().decode()
    content = json.loads(content)
    game = GameInterface(content)
    return json.dumps(True)

@bottle.post('/update_redzone_pos')
def do_update_redzone_pos():
    if game == None:
        return json.dumps(False)
    game.update_redzone_pos()
    return json.dumps(True)

@bottle.route('/get_redzone_pos')
def do_get_redzone_pos():
    if game == None:
        return json.dumps(None)
    r_rect = game.get_redzone_pos()
    r_dict = {
        "r_left": r_rect.left,
        "r_top": r_rect.top, 
        "r_width": r_rect.width, 
        "r_height": r_rect.height
    }
    return json.dumps(r_dict)

@bottle.post('/set_player')
def do_set_player():
    if game == None:
        return json.dumps(False)
    content = bottle.request.body.read().decode()
    ppos_dict = json.loads(content)
    game.set_player(ppos_dict)
    return json.dumps(True)

@bottle.route('/get_player_pos')
def do_get_player_pos():
    if game == None:
        return json.dumps(None)
    p_rect = game.get_player_pos()
    p_dict = {
        "p_left": p_rect.left,
        "p_top": p_rect.top, 
        "p_width": p_rect.width, 
        "p_height": p_rect.height
    }
    return json.dumps(p_dict)

@bottle.route('/is_player_in_redzone')
def do_is_player_in_redzone():
    if game == None:
        return json.dumps(False)
    return json.dumps(game.is_player_in_redzone())

@bottle.post('/change_player_speed')
def do_change_player_speed():
    if game == None:
        return json.dumps(False)
    content = bottle.request.body.read().decode()
    pspeed_dict = json.loads(content)
    game.change_player_speed(pspeed_dict)
    return json.dumps(True)

@bottle.post('/move_player')
def do_move_player():
    if game == None:
        return json.dumps(False)
    game.move_player()
    return json.dumps(True)

bottle.run(host='127.0.0.1', port=8080)
#bottle.run(host='localhost', port=8080, debug=True)
