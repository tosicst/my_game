from pgzero.actor import Actor
import math

WIDTH = 800
HEIGHT = 600

class Bullet:
    def __init__(self, x, y, target_x, target_y, is_enemy=False):
        self.actor = Actor("bullet")
        self.actor.pos = (x, y)
        self.is_enemy = is_enemy
        
        # Calculate direction
        dx = target_x - x
        dy = target_y - y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            self.vx = (dx / distance) * 6
            self.vy = (dy / distance) * 6
        else:
            self.vx = 0
            self.vy = -6
    
    def update(self):
        self.actor.x += self.vx
        self.actor.y += self.vy
    
    def is_off_screen(self):
        return (self.actor.x < 0 or self.actor.x > WIDTH or 
                self.actor.y < 0 or self.actor.y > HEIGHT)
    
    def draw(self):
        self.actor.draw()