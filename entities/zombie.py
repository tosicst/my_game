from pgzero.actor import Actor
import random

from entities.bullet import WIDTH, HEIGHT

class ZombieEnemy:
    def __init__(self):
        self.actor = Actor("zombie_walk1")
        self.actor.pos = (random.randint(40, WIDTH - 40), random.randint(-150, -40))
        self.speed = 1
        self.health = 2

        self.walk_images = ["zombie_walk1", "zombie_walk2"]
        self.walk_frame = 0

        self.hurt_image = "zombie_hurt"

        self.frame_timer = 0
        
    def update(self, player_pos=None):
        self.actor.y += self.speed

        # Keep enemy within horizontal bounds
        if self.actor.x < 50:
            self.actor.x = 50
        elif self.actor.x > WIDTH - 50:
            self.actor.x = WIDTH - 50

        # Keep enemy from going too far up
        if self.actor.y < 30:
            self.actor.y = 30

        self.frame_timer += 1
        if self.frame_timer > 5: 
            self.walk_frame = (self.walk_frame + 1) % len(self.walk_images)
            self.actor.image = self.walk_images[self.walk_frame]
            self.frame_timer = 0
    
    def draw(self):
        self.actor.draw()
    
    def hit(self, sound_enabled, sounds):
        self.actor.image = self.hurt_image
        self.health -= 1
        if sound_enabled:
            sounds.hit.play()
        return self.health <= 0
    
    def is_off_screen(self):
        return self.actor.y > HEIGHT + 20