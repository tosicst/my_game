from pgzero.actor import Actor

from entities.bullet import Bullet, WIDTH, HEIGHT

class Player:
    def __init__(self):
        self.actor = Actor("hero_idle1")
        self.actor.pos = (WIDTH // 2, HEIGHT - 120)
        self.speed = 5
        self.lives = 3
        self.bullets = []
        self.shoot_cooldown = 0
        self.last_direction = 0

        self.walk_images = ["hero_walk1", "hero_walk2"]
        self.walk_images_mirror = ["hero_walk1_mirror", "hero_walk2_mirror"]
        self.walk_frame = 0

        self.idle_images = ["hero_idle1", "hero_idle2"]
        self.idle_images_mirror = ["hero_idle1_mirror", "hero_idle2_mirror"]
        self.idle_frame = 0

        self.hurt_image = "hero_hurt"

        self.frame_timer = 0
        
    def update(self, keyboard, sound_enabled):
        moving = False

        # Movement
        if keyboard.left and self.actor.x > 20:
            self.actor.x -= self.speed
            self.actor.angle = 15 
            self.last_direction = -1
            moving = True
        if keyboard.right and self.actor.x < WIDTH - 20:
            self.actor.x += self.speed
            self.actor.angle = -15  
            self.last_direction = 1
            moving = True
        if keyboard.up and self.actor.y > 20:
            self.actor.y -= self.speed
            moving = True
        if keyboard.down and self.actor.y < HEIGHT - 20:
            self.actor.y += self.speed
            moving = True
            
        if not (keyboard.left or keyboard.right):
            self.actor.angle = 0
        
        # Shooting
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
            
        # Update bullets
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.is_off_screen():
                self.bullets.remove(bullet)

        self.frame_timer += 1
        if moving:
            if self.frame_timer > 5: 
                if self.last_direction == 1:
                    self.walk_frame = (self.walk_frame + 1) % len(self.walk_images)
                    self.actor.image = self.walk_images[self.walk_frame]
                    self.frame_timer = 0
                else:
                    self.walk_frame = (self.walk_frame + 1) % len(self.walk_images_mirror)
                    self.actor.image = self.walk_images_mirror[self.walk_frame]
                    self.frame_timer = 0
        else:
            if self.frame_timer > 10:  
                if self.last_direction == 1:
                    self.idle_frame = (self.idle_frame + 1) % len(self.idle_images)
                    self.actor.image = self.idle_images[self.idle_frame]
                    self.frame_timer = 0
                else:
                    self.idle_frame = (self.idle_frame + 1) % len(self.idle_images_mirror)
                    self.actor.image = self.idle_images_mirror[self.idle_frame]
                    self.frame_timer = 0
    
    def shoot(self, sounds, sound_enabled, target_x=0, target_y=0):
        if self.shoot_cooldown == 0:
            bullet = Bullet(self.actor.x, self.actor.y, target_x, target_y, False)
            self.bullets.append(bullet)
            self.shoot_cooldown = 15
            if sound_enabled:
                sounds.arrow.play()

    
    def draw(self):
        self.actor.draw()
        for bullet in self.bullets:
            bullet.draw()
    
    def hit(self, sounds, sound_enabled):
        self.actor.image = self.hurt_image
        self.lives -= 1
        if sound_enabled:
            sounds.hit.play()