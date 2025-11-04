import random
from pgzero.actor import Actor

from entities.bullet import Bullet, WIDTH, HEIGHT

class SoldierEnemy:
    def __init__(self):
        self.actor = Actor("soldier_walk1")
        self.actor.pos = (random.randint(30, WIDTH - 30), random.randint(-100, -30))
        self.speed = random.randint(2, 4)
        self.direction = random.choice([-1, 1])
        self.health = 1
        self.bullets = []
        self.shoot_cooldown = random.randint(60, 120)

        self.walk_images = ["soldier_walk1", "soldier_walk2"]
        self.walk_images_mirror = ["soldier_walk1_mirror", "soldier_walk2_mirror"]
        self.walk_frame = 0

        self.hurt_image = "soldier_hurt"

        self.frame_timer = 0
        
    def update(self, player_pos, sound_enabled, sounds):
        self.actor.y += self.speed
        self.actor.x += self.direction * 2

        # Keep enemy within screen bounds
        if self.actor.x < 40:
            self.actor.x = 40
            self.direction = 1
        elif self.actor.x > WIDTH - 40:
            self.actor.x = WIDTH - 40
            self.direction = -1
        
        # Keep enemy from going too far up
        if self.actor.y < 20:
            self.actor.y = 20

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        else:
            if self.actor.y > 0 and self.actor.y < HEIGHT - 100:
                self.shoot(sound_enabled, sounds, player_pos)
                self.shoot_cooldown = random.randint(80, 150)

        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.is_off_screen():
                self.bullets.remove(bullet)

        self.frame_timer += 1
        if self.frame_timer > 5: 
            if self.direction == 1:
                self.walk_frame = (self.walk_frame + 1) % len(self.walk_images)
                self.actor.image = self.walk_images[self.walk_frame]
                self.frame_timer = 0
            else:
                self.walk_frame = (self.walk_frame + 1) % len(self.walk_images_mirror)
                self.actor.image = self.walk_images_mirror[self.walk_frame]
                self.frame_timer = 0

    def shoot(self, sound_enabled, sounds, target_pos):
        bullet = Bullet(self.actor.x, self.actor.y, target_pos[0], target_pos[1], True)
        self.bullets.append(bullet)
        if sound_enabled:
            sounds.arrow.play()
    
    def draw(self):
        self.actor.draw()
        for bullet in self.bullets:
            bullet.draw()
    
    def is_off_screen(self):
        return self.actor.y > HEIGHT + 20

    def hit(self, sound_enabled, sounds):
        self.actor.image = self.hurt_image
        self.health -= 1
        if sound_enabled:
            sounds.hit.play()
        return self.health <= 0