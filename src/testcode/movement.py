import pygame as pg
import math

pg.init()
screen = pg.display.set_mode((1920, 1080))
clock = pg.time.Clock()

running = True
x, y = 400, 300 
speed = 5

class Player:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.alive = True
        self.turns_since_move = 500
        self.angle_to_tgt = 0

    def add_target(self, target):
        self.target = target

    def angle_to_target(self):
        return math.atan2(self.target.y - self.y, self.target.x - self.x)

    def distance_to_target(self):
        return math.sqrt((self.target.x - self.x)**2 + (self.target.y - self.y)**2)

    def move(self):


        if self.target is None:
            return
        
        self.angle_to_tgt = self.angle_to_target()
        self.x += math.cos(self.angle_to_tgt) * self.speed
        self.y += math.sin(self.angle_to_tgt) * self.speed

        self.turns_since_move += 1

        if self.distance_to_target() < 5:
            self.kill_target()
    
    

    
    def kill_target(self):
        self.target.die()
        self.target = None
        
    

class Player2:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.alive = True

    def move(self):
        self.x += self.speed
    
    def die(self):
        self.alive = False


player = Player(400, 900, 3)
player2 = Player2(200, 300, 1)

player.add_target(player2)

def display_players():
    if player2.alive:
        pg.draw.rect(screen, (0, 0, 255), (player2.x, player2.y, 10, 10))
    pg.draw.rect(screen, (255, 0, 0), (player.x, player.y, 10, 10)) 

players = [player, player2]

while running:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_q:
                running = False


    for ply in players:
        if player.alive:
            ply.move()
        else:
            players.remove(ply)



    screen.fill((0, 0, 0))
    display_players()
    pg.display.flip()
    clock.tick(30)
