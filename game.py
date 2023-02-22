import pygame
from gameObjects import GameObjects
from player import Player
from enemy import Enemy

class Game:

    def __init__(self):
        self.width=800
        self.height=600
        self.width2=50
        self.height2=40
        self.bg_color=(255, 255, 255)
        self.game_window=pygame.display.set_mode((self.width,self.height))
        self.clock=pygame.time.Clock()
        
        self.bg_scaled=GameObjects(0,0,self.width,self.height, 'assets/background.png')
        
        self.treasure=GameObjects(380,30,self.width2,self.height2,'assets/treasure.png')
        #self.player=Player(380,530,self.width2,self.height2,'assets/player.png', 10)
        #self.enemies=[Enemy(0,400,self.width2,self.height2,'assets/enemy.png',10),
            #Enemy(750,300,self.width2,self.height2,'assets/enemy.png',10),
            #Enemy(0,200,self.width2,self.height2,'assets/enemy.png',10)]
        #self.enemy=Enemy(0,400,self.width2,self.height2,'assets/enemy.png',10)
        self.level=1.0
        self.reset_game()
    def reset_game(self):
        self.player=Player(380,530,self.width2,self.height2,'assets/player.png', 10)
        speed=5 + (self.level * 5)
        if self.level >=4.0:
            self.enemies=[Enemy(0,400,self.width2,self.height2,'assets/enemy.png',speed),
            Enemy(750,300,self.width2,self.height2,'assets/enemy.png',speed),
            Enemy(0,200,self.width2,self.height2,'assets/enemy.png',speed)]
        elif self.level >= 2.0:
            self.enemies=[Enemy(0,400,self.width2,self.height2,'assets/enemy.png',speed),
            Enemy(750,300,self.width2,self.height2,'assets/enemy.png',speed)]
        else:
            self.enemies=[Enemy(0,400,self.width2,self.height2,'assets/enemy.png',speed)]


    def draw_objects(self):
        self.game_window.fill(self.bg_color)
        self.game_window.blit(self.bg_scaled.image,(self.bg_scaled.x, self.bg_scaled.y))
        self.game_window.blit(self.player.image, (self.player.x,self.player.y))
        for enemy in self.enemies:
            self.game_window.blit(enemy.image, (enemy.x,enemy.y))
        self.game_window.blit(self.treasure.image, (self.treasure.x,self.treasure.y))
        pygame.display.update()

    def move_objects(self,player_direction):
        self.player.move(player_direction, self.height)
        for enemy in self.enemies:
            enemy.move(self.width)

    def detect_collision(self, object1, object2):
        if object1.y > (object2.y + object2.height):
            return False
        elif (object1.y + object1.height) < object2.y:
            return False
        if object1.x > (object2.x + object2.width):
            return False
        elif (object1.x + object1.width) < object2.x:
            return False
        return True

    def check_collision(self):
        for enemy in self.enemies:
            if self.detect_collision(self.player, enemy):
                self.level -= 1.0
                return True
            if self.detect_collision(self.player, self.treasure):
                self.level += 0.5
                return True
        return False

    def run_game_loop(self):
        player_direction = 0
        is_game_over=True
        while is_game_over:
            #Handle event
            events=pygame.event.get() 
            for event in events:
                if event.type==pygame.QUIT:
                    return
                elif event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_UP:
                        #move player up
                        player_direction=-1
                    elif event.key==pygame.K_DOWN:
                        #move player down
                        player_direction=1
                elif event.type==pygame.KEYUP:
                    if event.key==pygame.K_UP or event.key==pygame.K_DOWN:
                        player_direction = 0
            #execute logic
            self.move_objects(player_direction)
            #update display
            self.draw_objects()
            #Detect collision
            if self.check_collision():
                self.reset_game()
    
            self.clock.tick(60)