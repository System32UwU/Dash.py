import pygame
import sys
import time

pygame.init()

screen_info = pygame.display.Info()
WIDTH, HEIGHT = screen_info.current_w, screen_info.current_h
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dash.py")
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()
is_fullscreen = False

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
CYAN = (64, 224, 208)

game_font = pygame.font.Font("fonts/font.ttf", 23)
title_font = pygame.font.Font("fonts/font.ttf", 72)
button_font = pygame.font.Font("fonts/font.ttf", 36)

LEVEL1_WIDTH = 5000
LEVEL2_WIDTH = 10000
player_width, player_height = 50, 50
start_x, start_y = 100, HEIGHT - 150
player = pygame.Rect(start_x, start_y, player_width, player_height)
player_velocity_x = 0
player_velocity_y = 0
gravity = 0.5
jump_power = -10
on_ground = False
facing_right = True
camera_x = 0

player_img_right = pygame.image.load("sprites/player_right.png").convert_alpha()
player_img_right = pygame.transform.scale(player_img_right, (player_width, player_height))
player_img_left = pygame.image.load("sprites/player_left.png").convert_alpha()
player_img_left = pygame.transform.scale(player_img_left, (player_width, player_height))
heart_img = pygame.image.load("sprites/heart.png").convert_alpha()
heart_img = pygame.transform.scale(heart_img, (32, 32))
enemy_img_right = pygame.image.load("sprites/enemy_right.png").convert_alpha()
enemy_img_right = pygame.transform.scale(enemy_img_right, (50, 50))
enemy_img_left = pygame.image.load("sprites/enemy_left.png").convert_alpha()
enemy_img_left = pygame.transform.scale(enemy_img_left, (50, 50))
gun_img_right = pygame.image.load("sprites/gun_right.png").convert_alpha()
gun_img_right = pygame.transform.scale(gun_img_right, (30, 20))
gun_img_left = pygame.image.load("sprites/gun_left.png").convert_alpha()
gun_img_left = pygame.transform.scale(gun_img_left, (30, 20))
bullet_img = pygame.image.load("sprites/bullet.png").convert_alpha()
bullet_img = pygame.transform.scale(bullet_img, (10, 10))
spike_img = pygame.image.load("sprites/spike.png").convert_alpha()
spike_img = pygame.transform.scale(spike_img, (50, 50))
background_img1 = pygame.image.load("images/bg.jpg").convert()
background_img1 = pygame.transform.scale(background_img1, (WIDTH, HEIGHT))
background_img2 = pygame.image.load("images/bg2.jpg").convert()
background_img2 = pygame.transform.scale(background_img2, (WIDTH, HEIGHT))
logo_img = pygame.image.load("images/logo.png").convert_alpha()
logo_img = pygame.transform.scale(logo_img, (500, 300))
door_img = pygame.image.load("sprites/door.png").convert_alpha()
door_img = pygame.transform.scale(door_img, (60, 60))

death_sfx = pygame.mixer.Sound("sfx/death.wav")
gameover_sfx = pygame.mixer.Sound("sfx/game_over.wav")
gun_equip_sfx = pygame.mixer.Sound("sfx/gun_equip.wav")
gnushot_sfx = pygame.mixer.Sound("sfx/gunshot.wav")

platforms1 = [
    pygame.Rect(100, HEIGHT - 150, 150, 20),
    pygame.Rect(350, HEIGHT - 250, 150, 20),
    pygame.Rect(600, HEIGHT - 350, 300, 20),
    pygame.Rect(1200, HEIGHT - 450, 150, 20),
    pygame.Rect(1600, HEIGHT - 550, 150, 20),
    pygame.Rect(2000, HEIGHT - 350, 150, 20),
    pygame.Rect(2500, HEIGHT - 250, 150, 20),
    pygame.Rect(2700, HEIGHT - 300, 150, 20),
    pygame.Rect(2900, HEIGHT - 350, 150, 20),
    pygame.Rect(3100, HEIGHT - 430, 150, 20),
    pygame.Rect(2900, HEIGHT - 520, 150, 20),
    pygame.Rect(2700, HEIGHT - 570, 150, 20),
    pygame.Rect(2500, HEIGHT - 620, 150, 20),
    pygame.Rect(2500, HEIGHT - 740, 750, 20),
    pygame.Rect(3750, HEIGHT - 200, 1000, 20),
    pygame.Rect(4750, HEIGHT - 300, 150, 20),
    pygame.Rect(4750, HEIGHT - 420, 150, 20),
    pygame.Rect(4750, HEIGHT - 540, 150, 20),
]
enemies1 = [
    [pygame.Rect(450, HEIGHT - 300, 50, 50), -2, 320, HEIGHT - 300],
]
bullets1 = []
gun_collected1 = False
gun_rect1 = pygame.Rect(200, HEIGHT - 180, 30, 20)
spikes1 = [
    pygame.Rect(650, HEIGHT - 400, 50, 50),
    pygame.Rect(3180, HEIGHT - 480, 50, 50),
    pygame.Rect(2520, HEIGHT - 670, 50, 50),
]
door_rect = pygame.Rect(LEVEL1_WIDTH - 205, HEIGHT - 600, 50, 80)

platforms2 = [
    pygame.Rect(0, HEIGHT - 40, LEVEL2_WIDTH, 40),
    pygame.Rect(300, HEIGHT - 150, 150, 20),
    pygame.Rect(600, HEIGHT - 250, 150, 20),
    pygame.Rect(900, HEIGHT - 250, 150, 20),
    pygame.Rect(1200, HEIGHT - 350, 150, 20),
    pygame.Rect(1700, HEIGHT - 450, 200, 20),
    pygame.Rect(2200, HEIGHT - 250, 200, 20),
    pygame.Rect(2600, HEIGHT - 350, 120, 20),
    pygame.Rect(3000, HEIGHT - 450, 120, 20),
    pygame.Rect(3300, HEIGHT - 550, 250, 20),
    pygame.Rect(4000, HEIGHT - 450, 180, 20),
    pygame.Rect(4600, HEIGHT - 350, 180, 20),
    pygame.Rect(5000, HEIGHT - 250, 180, 20),
    pygame.Rect(5400, HEIGHT - 150, 180, 20),
    pygame.Rect(6000, HEIGHT - 250, 180, 20),
    pygame.Rect(6500, HEIGHT - 350, 180, 20),
    pygame.Rect(7000, HEIGHT - 450, 250, 20),
    pygame.Rect(8000, HEIGHT - 350, 180, 20),
    pygame.Rect(9000, HEIGHT - 250, 200, 20),
    pygame.Rect(9500, HEIGHT - 150, 200, 20),
]
enemies2 = [
    [pygame.Rect(320, HEIGHT - 90, 50, 50), 2, 320, HEIGHT - 90],
    [pygame.Rect(1000, HEIGHT - 300, 50, 50), -2, 1000, HEIGHT - 300],
    [pygame.Rect(1900, HEIGHT - 500, 50, 50), 2, 1900, HEIGHT - 500],
    [pygame.Rect(2600, HEIGHT - 370, 50, 50), -2, 2600, HEIGHT - 370],
    [pygame.Rect(3400, HEIGHT - 570, 50, 50), 2, 3400, HEIGHT - 570],
    [pygame.Rect(4100, HEIGHT - 470, 50, 50), -2, 4100, HEIGHT - 470],
    [pygame.Rect(5100, HEIGHT - 270, 50, 50), 2, 5100, HEIGHT - 270],
    [pygame.Rect(6000, HEIGHT - 270, 50, 50), -2, 6000, HEIGHT - 270],
    [pygame.Rect(7000, HEIGHT - 470, 50, 50), 2, 7000, HEIGHT - 470],
    [pygame.Rect(9000, HEIGHT - 270, 50, 50), -2, 9000, HEIGHT - 270],
]
bullets2 = []
gun_collected2 = False
gun_rect2 = pygame.Rect(700, HEIGHT - 270, 30, 20)
spikes2 = [
    pygame.Rect(200, HEIGHT - 90, 50, 50),
    pygame.Rect(600, HEIGHT - 90, 50, 50),
    pygame.Rect(1200, HEIGHT - 90, 50, 50),
    pygame.Rect(1800, HEIGHT - 90, 50, 50),
    pygame.Rect(2200, HEIGHT - 90, 50, 50),
    pygame.Rect(2600, HEIGHT - 90, 50, 50),
    pygame.Rect(3200, HEIGHT - 90, 50, 50),
    pygame.Rect(3800, HEIGHT - 90, 50, 50),
    pygame.Rect(4500, HEIGHT - 90, 50, 50),
    pygame.Rect(5100, HEIGHT - 90, 50, 50),
    pygame.Rect(5700, HEIGHT - 90, 50, 50),
    pygame.Rect(6300, HEIGHT - 90, 50, 50),
    pygame.Rect(6900, HEIGHT - 90, 50, 50),
    pygame.Rect(7500, HEIGHT - 90, 50, 50),
    pygame.Rect(8000, HEIGHT - 90, 50, 50),
    pygame.Rect(9000, HEIGHT - 90, 50, 50),
    pygame.Rect(9500, HEIGHT - 90, 50, 50),
]

level = 1

level_songs = {
    1: "music/bgm.mp3",
    2: "music/bgm2.mp3",
}

def get_level_data():
    if level == 1:
        return [platforms1, enemies1, bullets1, gun_collected1, gun_rect1, spikes1, LEVEL1_WIDTH, door_rect]
    else:
        return [platforms2, enemies2, bullets2, gun_collected2, gun_rect2, spikes2, LEVEL2_WIDTH, door_rect2]
    
door_rect2 = pygame.Rect(LEVEL2_WIDTH - 200, HEIGHT - 98, 50, 80)

def get_level_background():
    return background_img1 if level == 1 else background_img2

def get_level_song():
    return level_songs.get(level, "music/bgm.mp3")

player_lives = 3

def demo_end_screen():
    selected = 0
    options = ["Return to Main Menu", "Quit"]
    running_demo = True

    pygame.mixer.music.pause()

    while running_demo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if selected == 0:
                        pygame.mixer.music.stop()
                        reset_game()
                        main_menu()
                        pygame.mixer.music.load(get_level_song())
                        pygame.mixer.music.play(-1, 0.0)
                        running_demo = False
                    elif selected == 1:
                        pygame.quit()
                        sys.exit()
        
        screen.fill(BLACK)
        thank_you = title_font.render("Thank you for playing the demo!", True, YELLOW)
        screen.blit(thank_you, (WIDTH // 2 - thank_you.get_width() // 2, HEIGHT // 3))

        more_levels = game_font.render("More levels will be added to Dash.py soon.", True, WHITE)
        screen.blit(more_levels, (WIDTH // 2 - more_levels.get_width() // 2, HEIGHT // 2 - 20))

        for i, option in enumerate(options):
            color = YELLOW if i == selected else WHITE
            label = button_font.render(option, True, color)
            screen.blit(label, (WIDTH // 2 - label.get_width() // 2, HEIGHT // 2 + 50 + i * 60))
        
        pygame.display.flip()

def respawn():
    global player, player_velocity_x, player_velocity_y, on_ground, bullets1, bullets2
    player = pygame.Rect(start_x, start_y, player_width, player_height)
    player_velocity_x = 0
    player_velocity_y = 0
    on_ground = False
    bullets1.clear()
    bullets2.clear()
    for enemies in [enemies1, enemies2]:
        for enemy in enemies:
            enemy[0].x, enemy[0].y = enemy[2], enemy[3]

def pause_menu():
    global running
    paused = True
    selected = 0
    options = ["Resume", "Return to Main Menu", "Quit"]
    pygame.mixer.music.pause()

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if selected == 0:
                        paused = False
                        pygame.mixer.music.unpause()
                    elif selected == 1:
                        pygame.mixer.music.stop()
                        reset_game()
                        main_menu()
                        pygame.mixer.music.play(-1, 0.0)
                        paused = False
                    elif selected == 2:
                        pygame.quit()
                        sys.exit()
                elif event.key == pygame.K_ESCAPE:
                    paused = False
                    pygame.mixer.music.unpause()

        screen.fill(BLACK)
        title = title_font.render("PAUSED", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3))

        for i, option in enumerate(options):
            color = YELLOW if i == selected else WHITE
            label = button_font.render(option, True, color)
            screen.blit(label, (WIDTH // 2 - label.get_width() // 2, HEIGHT // 2 + i * 60))

        pygame.display.flip()

def reset_game():
    global player_lives, gun_collected1, gun_collected2, level
    player_lives = 3
    gun_collected1 = False
    gun_collected2 = False
    level = 1
    respawn()

def game_over_menu():
    selected = 0
    options = ["Try Again", "Quit"]
    while True:
        screen.fill(BLACK)
        title = title_font.render("GAME OVER", True, RED)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3))

        for i, option in enumerate(options):
            color = YELLOW if i == selected else WHITE
            label = button_font.render(option, True, color)
            screen.blit(label, (WIDTH // 2 - label.get_width() // 2, HEIGHT // 2 + i * 60))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if selected == 0:
                        return True
                    else:
                        pygame.quit()
                        sys.exit()

def show_message(text, duration=3, color=RED):
    start_time = time.time()
    while time.time() - start_time < duration:
        screen.fill(BLACK)
        message = title_font.render(text, True, color)
        screen.blit(message, (WIDTH // 2 - message.get_width() // 2, HEIGHT // 2 - message.get_height() // 2))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def main_menu():
    selected = 0
    options = ["Start Game", "Quit"]

    while True:
        screen.fill(BLACK)

        screen.blit(logo_img, (WIDTH // 2 - logo_img.get_width() // 2, HEIGHT // 8))

        credit_text = game_font.render("Made by System32UwU", True, WHITE)
        screen.blit(credit_text, (10, 10))

        version_text = game_font.render("Demo ver. 0.1.0", True, WHITE)
        screen.blit(version_text, (WIDTH - version_text.get_width() - 10, 10))

        for i, option in enumerate(options):
            color = YELLOW if i == selected else WHITE
            label = button_font.render(option, True, color)
            screen.blit(label, (WIDTH // 2 - label.get_width() // 2, HEIGHT // 2 + 150 + i * 60))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if selected == 0:
                        return
                    elif selected == 1:
                        pygame.quit()
                        sys.exit()

main_menu()
running = True
pygame.mixer.music.load(get_level_song())
pygame.mixer.music.play(-1, 0.0)
current_song = get_level_song()

while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pause_menu()
            elif event.key == pygame.K_F11:
                is_fullscreen = not is_fullscreen
                if is_fullscreen:
                    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    platforms, enemies, bullets, gun_collected, gun_rect, spikes, cur_level_width, maybe_door = get_level_data()

    if get_level_song() != current_song:
        pygame.mixer.music.load(get_level_song())
        pygame.mixer.music.play(-1, 0.0)
        current_song = get_level_song()

    sprint_speed = 8

    keys = pygame.key.get_pressed()
    player_velocity_x = 0
    if keys[pygame.K_a]:
        player_velocity_x = -5
        if keys[pygame.K_LSHIFT]:
            player_velocity_x = -sprint_speed
        facing_right = False
    if keys[pygame.K_d]:
        player_velocity_x = 5
        if keys[pygame.K_LSHIFT]:
            player_velocity_x = sprint_speed
        facing_right = True
    if keys[pygame.K_SPACE] and on_ground:
        player_velocity_y = jump_power
        on_ground = False

    if level == 1 and gun_collected1 and pygame.mouse.get_pressed()[0]:
        if len(bullets1) < 10:
            direction = 10 if facing_right else -10
            bullet = pygame.Rect(player.centerx, player.centery, 10, 5)
            bullet.x += 20 if facing_right else -20
            bullets1.append([bullet, direction])
            gnushot_sfx.play()
    elif level == 2 and gun_collected2 and pygame.mouse.get_pressed()[0]:
        if len(bullets2) < 10:
            direction = 10 if facing_right else -10
            bullet = pygame.Rect(player.centerx, player.centery, 10, 5)
            bullet.x += 20 if facing_right else -20
            bullets2.append([bullet, direction])
            gnushot_sfx.play()

    player_velocity_y += gravity
    player.x += player_velocity_x
    player.x = max(0, min(player.x, cur_level_width - player.width))
    player.y += player_velocity_y
    on_ground = False

    for platform in platforms:
        if player.colliderect(platform):
            if player_velocity_y > 0:
                player.bottom = platform.top
                player_velocity_y = 0
                on_ground = True

    if not gun_collected and player.colliderect(gun_rect):
        if level == 1:
            gun_collected1 = True
        else:
            gun_collected2 = True
        gnushot_sfx.play()

    for enemy in enemies[:]:
        rect, velocity, _, _ = enemy
        rect.x += velocity
        if rect.left <= 0 or rect.right >= cur_level_width:
            enemy[1] = -velocity
        rect.y += gravity
        for platform in platforms:
            if rect.colliderect(platform):
                rect.bottom = platform.top

    if level == 1:
        for bullet in bullets1[:]:
            bullet[0].x += bullet[1]
            if bullet[0].x < 0 or bullet[0].x > cur_level_width:
                bullets1.remove(bullet)
                continue
            for enemy in enemies[:]:
                if bullet[0].colliderect(enemy[0]):
                    enemies.remove(enemy)
                    if bullet in bullets1:
                        bullets1.remove(bullet)
                    break
    else:
        for bullet in bullets2[:]:
            bullet[0].x += bullet[1]
            if bullet[0].x < 0 or bullet[0].x > cur_level_width:
                bullets2.remove(bullet)
                continue
            for enemy in enemies[:]:
                if bullet[0].colliderect(enemy[0]):
                    enemies.remove(enemy)
                    if bullet in bullets2:
                        bullets2.remove(bullet)
                    break

    for spike in spikes:
        if player.colliderect(spike):
            player_lives -= 1
            pygame.mixer.music.pause()
            death_sfx.play()
            show_message("YOU DIED", 1)
            pygame.mixer.music.unpause()
            if player_lives <= 0:
                pygame.mixer.music.pause()
                gameover_sfx.play()
                if game_over_menu():
                    reset_game()
                    pygame.mixer.music.play(-1, 0.0)
                    break
                else:
                    running = False
            else:
                respawn()
            break

    for enemy in enemies:
        if player.colliderect(enemy[0]):
            player_lives -= 1
            pygame.mixer.music.pause()
            death_sfx.play()
            show_message("YOU DIED", 3)
            pygame.mixer.music.unpause()
            if player_lives <= 0:
                pygame.mixer.music.pause()
                gameover_sfx.play()
                if game_over_menu():
                    reset_game()
                    pygame.mixer.music.play(-1, 0.0)
                    break
                else:
                    running = False
            else:
                respawn()
            break

    if level == 1 and player.y > HEIGHT:
        player_lives -= 1
        pygame.mixer.music.pause()
        death_sfx.play()
        show_message("YOU DIED", 1)
        pygame.mixer.music.unpause()
        if player_lives <= 0:
            pygame.mixer.music.pause()
            gameover_sfx.play()
            if game_over_menu():
                reset_game()
                pygame.mixer.music.play(-1, 0.0)
                continue
            else:
                running = False
        else:
            respawn()
        continue

    if level == 1 and player.colliderect(door_rect):
        pygame.mixer.music.pause()
        show_message("LEVEL 2!", 2, color=YELLOW)
        pygame.mixer.music.unpause()
        level = 2
        respawn()
        continue

    if level == 2 and player.colliderect(door_rect2):
        demo_end_screen()
        continue

    camera_x = player.x - WIDTH // 2
    camera_x = max(0, min(camera_x, cur_level_width - WIDTH))

    screen.blit(get_level_background(), (0, 0))

    if (level == 1 and maybe_door) or (level == 2 and maybe_door):
        adjusted_door = pygame.Rect(maybe_door.x - camera_x, maybe_door.y, maybe_door.width, maybe_door.height)
        screen.blit(door_img, (adjusted_door.x, adjusted_door.y))

    for platform in platforms:
        adjusted = pygame.Rect(platform.x - camera_x, platform.y, platform.width, platform.height)
        pygame.draw.rect(screen, CYAN, adjusted)

    adjusted_player = pygame.Rect(player.x - camera_x, player.y, player.width, player.height)
    player_img = player_img_right if facing_right else player_img_left
    screen.blit(player_img, (adjusted_player.x, adjusted_player.y))

    if (level == 1 and gun_collected1) or (level == 2 and gun_collected2):
        gun_offset_x = 10 if facing_right else -20
        gun_offset_y = 5
        adjusted_gun = pygame.Rect(adjusted_player.x + gun_offset_x, adjusted_player.y + gun_offset_y, gun_img_right.get_width(), gun_img_right.get_height())
        gun_img_to_use = gun_img_right if facing_right else gun_img_left
        screen.blit(gun_img_to_use, (adjusted_gun.x, adjusted_gun.y))

    if (level == 1 and not gun_collected1) or (level == 2 and not gun_collected2):
        adjusted_gun_rect = pygame.Rect(gun_rect.x - camera_x, gun_rect.y, gun_rect.width, gun_rect.height)
        screen.blit(gun_img_right, (adjusted_gun_rect.x, adjusted_gun_rect.y))

    for enemy in enemies:
        adjusted_enemy = pygame.Rect(enemy[0].x - camera_x, enemy[0].y, enemy[0].width, enemy[0].height)
        enemy_img = enemy_img_right if enemy[1] > 0 else enemy_img_left
        screen.blit(enemy_img, (adjusted_enemy.x, adjusted_enemy.y))

    if level == 1:
        for bullet in bullets1:
            adjusted_bullet = pygame.Rect(bullet[0].x - camera_x, bullet[0].y, bullet[0].width, bullet[0].height)
            screen.blit(bullet_img, adjusted_bullet)
    else:
        for bullet in bullets2:
            adjusted_bullet = pygame.Rect(bullet[0].x - camera_x, bullet[0].y, bullet[0].width, bullet[0].height)
            screen.blit(bullet_img, adjusted_bullet)

    for spike in spikes:
        adjusted_spike = pygame.Rect(spike.x - camera_x, spike.y, spike.width, spike.height)
        screen.blit(spike_img, (adjusted_spike.x, adjusted_spike.y))

    if level == 1:
        adjusted_door = pygame.Rect(door_rect.x - camera_x, door_rect.y, door_rect.width, door_rect.height)
        screen.blit(door_img, (adjusted_door.x, adjusted_door.y))

    for i in range(player_lives):
        screen.blit(heart_img, (10 + i * 40, 10))

    level_text = game_font.render(f"Level {level}", True, YELLOW)
    screen.blit(level_text, (WIDTH - level_text.get_width() - 10, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()

# 53 6F 6D 65 6F 6E 65 20 69 73 20 77 61 74 63 68 69 6E 67 20 6D 65 20 66 72 6F 6D 20 74 68 65 20 73 68 61 64 6F 77 73