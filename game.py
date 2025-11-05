import pgzrun
import random
import math

from entities.bullet import WIDTH, HEIGHT
from entities.player import Player
from entities.soldier import SoldierEnemy
from entities.zombie import ZombieEnemy

# Game settings
TITLE = "Defender"
MAX_ENEMIES = 10

# Game state
class GameState:
    MENU = "menu"
    PLAYING = "playing"
    GAME_OVER = "game_over"
    WIN = "win"

current_state = GameState.MENU
sound_enabled = True
score = 0
current_music = None
WIN_SCORE = 200

def play_music(music_name):
    global current_music

    if sound_enabled and current_music != music_name:
        music.play(music_name)
        current_music = music_name

def stop_music():
    global current_music

    music.stop()
    current_music = None

# Game objects
player = Player()
soldier_enemies = []
zombie_enemies = []
spawn_timer = 0

# Menu buttons
play_button = Rect((WIDTH // 2 - 100, HEIGHT // 2 - 30), (200, 60))
sound_button = Rect((WIDTH // 2 - 100, HEIGHT // 2 + 50), (200, 60))
exit_button = Rect((WIDTH // 2 - 100, HEIGHT // 2 + 130), (200, 60))

def reset_game():
    global player, soldier_enemies, zombie_enemies, score, spawn_timer, current_state
    player = Player()
    soldier_enemies = []
    zombie_enemies = []
    score = 0
    spawn_timer = 0
    current_state = GameState.PLAYING

def check_enemy_collisions():
    global score
    
    for soldier_e in soldier_enemies[:]:
        for zombie_e in zombie_enemies[:]:
            if soldier_e.actor.colliderect(zombie_e.actor._rect.inflate(-20, -20)):
                if soldier_e.hit(sound_enabled, sounds):
                    if soldier_e in soldier_enemies:
                        soldier_enemies.remove(soldier_e)
                        score += 5
                if zombie_e.hit(sound_enabled, sounds):
                    if zombie_e in zombie_enemies:
                        zombie_enemies.remove(zombie_e)
                        score += 10
                break

def update():
    global spawn_timer, score, current_state
    
    if current_state == GameState.PLAYING:
        # Update player
        player.update(keyboard, sound_enabled)
        
        # Spawn enemies
        spawn_timer += 1
        if spawn_timer > 60:
            spawn_timer = 0
            if random.random() < 0.7:
                soldier_enemies.append(SoldierEnemy())
            else:
                zombie_enemies.append(ZombieEnemy())
        
        # Update soldier enemies
        for enemy in soldier_enemies[:]:
            enemy.update(player.actor.pos, sound_enabled, sounds)
            if enemy.is_off_screen():
                soldier_enemies.remove(enemy)
            elif enemy.actor.colliderect(player.actor._rect.inflate(0, 0)):
                soldier_enemies.remove(enemy)
                player.hit(sounds, sound_enabled)
            else:
                # Check bullet collisions
                for bullet in player.bullets[:]:
                    if enemy.actor.colliderect(bullet.actor._rect.inflate(0, 0)):
                        player.bullets.remove(bullet)
                        if enemy.hit(sound_enabled, sounds):
                            soldier_enemies.remove(enemy)
                            score += 10
                        break

                # Check enemy bullet collisions with player
                for bullet in enemy.bullets[:]:
                    if bullet.actor.colliderect(player.actor._rect.inflate(0, 0)):
                        enemy.bullets.remove(bullet)
                        player.hit(sounds, sound_enabled)
        
        # Update zombie enemies
        for enemy in zombie_enemies[:]:
            enemy.update()
            if enemy.is_off_screen():
                zombie_enemies.remove(enemy)
                player.hit(sounds, sound_enabled)
            elif enemy.actor.colliderect(player.actor._rect.inflate(0, 0)):
                zombie_enemies.remove(enemy)
                player.hit(sounds, sound_enabled)
            else:
                # Check bullet collisions
                for bullet in player.bullets[:]:
                    if enemy.actor.colliderect(bullet.actor._rect.inflate(0, 0)):
                        player.bullets.remove(bullet)
                        if enemy.hit(sound_enabled, sounds):
                            zombie_enemies.remove(enemy)
                            score += 25
                        break
        
        check_enemy_collisions()

        # Check win condition
        if score >= WIN_SCORE:
            current_state = GameState.WIN
            play_music("win")

        # Check game over
        if player.lives <= 0:
            current_state = GameState.GAME_OVER
            play_music("game_over")

def draw():
    screen.clear()
    
    if current_state == GameState.MENU:
        # Draw menu
        screen.fill((10, 10, 40))
        screen.draw.text("DEFENDER", center=(WIDTH // 2, HEIGHT // 3), 
                        fontsize=60, color="white", shadow=(2, 2))

        play_music("intro")
        
        # Play button
        screen.draw.filled_rect(play_button, (50, 150, 50))
        screen.draw.text("PLAY", center=play_button.center, 
                        fontsize=40, color="white")
        
        # Sound button
        sound_color = (50, 150, 50) if sound_enabled else (150, 50, 50)
        screen.draw.filled_rect(sound_button, sound_color)
        sound_text = "SOUND: ON" if sound_enabled else "SOUND: OFF"
        screen.draw.text(sound_text, center=sound_button.center, 
                        fontsize=30, color="white")

        # Exit button
        screen.draw.filled_rect(exit_button, (50, 150, 50))
        screen.draw.text("EXIT", center=exit_button.center, 
                        fontsize=30, color="white")

                        
        
        screen.draw.text("Use ARROW KEYS to move, Left Mouse Button to shoot", 
                        center=(WIDTH // 2, HEIGHT - 80), 
                        fontsize=20, color="gray")
    
    elif current_state == GameState.PLAYING:
        # Draw game
        screen.blit("background", (-20, -10))
        
        player.draw()
        
        for enemy in soldier_enemies:
            enemy.draw()
        
        for enemy in zombie_enemies:
            enemy.draw()
        
        # Draw HUD
        screen.draw.text(f"Score: {score}", topleft=(10, 10), 
                        fontsize=30, color="white")
        screen.draw.text(f"Lives: {player.lives}", topright=(WIDTH - 10, 10), 
                        fontsize=30, color="white")
    
    elif current_state == GameState.GAME_OVER:
        screen.fill((20, 0, 0))
        screen.draw.text("GAME OVER", center=(WIDTH // 2, HEIGHT // 2 - 50), 
                        fontsize=70, color="red", shadow=(3, 3))
        screen.draw.text(f"Final Score: {score}", center=(WIDTH // 2, HEIGHT // 2 + 30), 
                        fontsize=40, color="white")
        screen.draw.text("Click to return to menu", center=(WIDTH // 2, HEIGHT // 2 + 100), 
                        fontsize=25, color="gray")

    elif current_state == GameState.WIN:
        screen.fill((0, 20, 40))
        screen.draw.text("YOU WIN!!!", center=(WIDTH // 2, HEIGHT // 2 - 50), 
                        fontsize=70, color="yellow", shadow=(3, 3))
        screen.draw.text(f"Final Score: {score}", center=(WIDTH // 2, HEIGHT // 2 + 30), 
                        fontsize=40, color="white")
        screen.draw.text("Click to return to menu", center=(WIDTH // 2, HEIGHT // 2 + 130), 
                        fontsize=25, color="gray")

def on_mouse_down(pos):
    global current_state, sound_enabled
    
    if current_state == GameState.MENU:
        if play_button.collidepoint(pos):
            reset_game()
        elif sound_button.collidepoint(pos):
            sound_enabled = not sound_enabled
            if not sound_enabled:
                stop_music()
            else:
                play_music("intro")
        elif exit_button.collidepoint(pos):
            import sys
            sys.exit()

    elif current_state == GameState.PLAYING:
        player.shoot(sounds, sound_enabled, pos[0], pos[1])
    
    elif current_state == GameState.GAME_OVER:
        current_state = GameState.MENU

    elif current_state == GameState.WIN:
        current_state = GameState.MENU

pgzrun.go()