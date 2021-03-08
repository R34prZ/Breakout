import pygame, sys, random
from pygame.locals import *
from functionalities import *
from button import *

pygame.init()
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

WIN_SIZE = width, height = 640, 480
screen = pygame.display.set_mode(WIN_SIZE)

def main_menu():

    btn_color = WHITE
    bg_color = BLACK

    start_button_rect = pygame.Rect(width//2 - 50, height//2 - 50, 70, 70)

    while True:

        screen.fill(bg_color)

        mx, my = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.draw.polygon(screen, btn_color, [[width//2-40, height // 2-40],
                    [width// 2 + 40, height // 2], [width//2-40, height // 2+40]])

        if start_button_rect.collidepoint((mx, my)):
            btn_color = BLACK
            bg_color = WHITE
            if click[0]:
                main()
        else:
            btn_color = WHITE
            bg_color = BLACK

        clock.tick(60)
        pygame.display.flip()

def main():

    player_rect = pygame.Rect(width / 2 - 50, height - 50, 100, 10)
    ball_rect = pygame.Rect(width / 2 - 5, height / 2 + 50, 10, 10)
    
    def generate_blocks():
        blocks = []
        block_width = random.randrange(5, 100, 10)
        block_height = random.randrange(5, 100, 10)

        main_wall = [(50, width - 50), (50, 250)]

        cols = (main_wall[0][1] - main_wall[0][0]) // block_width
        rows = (main_wall[1][1] - main_wall[1][0]) // block_height
        
        for i in range(rows):
            for j in range(cols):
                blocks.append(pygame.Rect(main_wall[0][0] + j * block_width, main_wall[1][0] + i * block_height,
                                block_width, block_height))

        return blocks

    ball_velocity = [3, 3]

    def player():

        pygame.draw.rect(screen, WHITE, player_rect)

        player_movement = 0
        if moving_left:
            player_movement = -5
        elif moving_right:
            player_movement = 5
        
        player_rect.x += player_movement

        if player_rect.left >= width:
            player_rect.x = 0
        elif player_rect.right <= 0:
            player_rect.x = width
    
    global lives, starting
    def ball():
        global lives, starting

        pygame.draw.circle(screen, WHITE, (ball_rect.x + 5, ball_rect.y + 5), 6)

        if ball_rect.left >= width:
           ball_velocity[0] = -ball_velocity[0]
        elif ball_rect.right <= 0:
            ball_velocity[0] = -ball_velocity[0]
        elif ball_rect.top <= 0:
            ball_velocity[1] = -ball_velocity[1]
        elif ball_rect.bottom  >= height:
            lives -= 1
            ball_rect.x, ball_rect.y = width / 2 - 5, height / 2 + 50
            player_rect.x, player_rect.y = width / 2 - 50, height - 50
            starting = True
            
        ball_rect.x += ball_velocity[0]
        ball_rect.y += ball_velocity[1]

        if ball_rect.colliderect(player_rect):
            ball_velocity[1] = -ball_velocity[1]

    moving_left = False
    moving_right = False
    
    def option_bar():

        option_bar = pygame.Surface((150, 150))
        option_bar.fill(RED)
        option_bar.set_alpha(20)
        screen.blit(option_bar, (width // 2 - option_bar.get_width() // 2, height // 2 - option_bar.get_height() // 2))

        blit_text(screen, 'Menu', width // 2 - option_bar.get_width() // 2,  height // 2 - option_bar.get_height() // 2 - 50, BLACK, True, screen_size=WIN_SIZE)
        
        continue_button = Button(screen, width // 2 - option_bar.get_width() // 2,  height // 2 - option_bar.get_height() // 2, 150, 50)
        continue_button.makeButton(BLACK, 50)
        continue_button.buttonAction(BLUE, 50, main)
        continue_button.textHandler('Reset', WHITE)
        continue_button.update()

        menu_button = Button(screen, width // 2 - option_bar.get_width() // 2,  height // 2 - option_bar.get_height() // 2 + 50, 150, 50)
        menu_button.makeButton(BLACK, 50)
        menu_button.buttonAction(BLUE, 50, main_menu)
        menu_button.textHandler('Main Menu', WHITE)
        menu_button.update()

        quit_button = Button(screen, width // 2 - option_bar.get_width() // 2, height // 2 - option_bar.get_height() // 2 + 100, 150, 50)
        quit_button.makeButton(BLACK, 50)
        quit_button.buttonAction(BLUE, 50, pygame.quit)
        quit_button.textHandler('Exit', WHITE)
        quit_button.update()

    def game_over_screen():

        blit_text(screen, 'Game Over!', 0, 0, BLACK, True, True, WIN_SIZE)

        menu_button = Button(screen, width / 2 - 100, height / 2 + 50, 100, 50)
        menu_button.makeButton(BLACK, 50)
        menu_button.buttonAction(BLUE, 25, main_menu)
        menu_button.textHandler('Menu', WHITE)
        menu_button.update()

        reset_button = Button(screen, width / 2, height / 2 + 50, 100, 50)
        reset_button.makeButton(BLACK, 50)
        reset_button.buttonAction(BLUE, 25, main)
        reset_button.textHandler('Restart', WHITE)
        reset_button.update()

    show_option_bar = False
    paused = False
    starting = True
    game_over = False
    show_fps = False

    bg_color = BLACK

    level = 1
    lives = 10

    blocks = generate_blocks()

    while True:

        screen.fill(bg_color)
        blit_text(screen, f'Level: {level}', 20, 10, WHITE, screen_size=WIN_SIZE)
        blit_text(screen, f'Lives: {lives}', width - 120, 10, WHITE, screen_size=WIN_SIZE)

        if len(blocks) == 0:
            ball_rect.x, ball_rect.y = width / 2 - 5, height / 2 + 50
            level += 1
            blocks = generate_blocks()
            starting = True

        if lives == 0:
            paused = True
            game_over = True
        
        if game_over:
            screen.fill(WHITE)
            game_over_screen()

        for block in blocks:
            pygame.draw.rect(screen, (255, 255, 255), block, 3)
            if ball_rect.colliderect(block):
                play_sound('./snd/hit.wav')
                ball_velocity[1] = -ball_velocity[1]
                blocks.remove(block)

        if starting:
            paused = True
            player_rect.x, player_rect.y = width / 2 - 50, height - 50
            blit_text(screen, 'Press SPACE!', 0, height - 200, WHITE, True, screen_size=WIN_SIZE)

        if not paused:
            player()
            ball()

        if show_option_bar:
            option_bar()
            bg_color = WHITE
            paused = True
        else:
            bg_color = BLACK
            paused = False

        if show_fps:
            blit_text(screen,f'FPS: {fps}', player_rect.x, player_rect.y, BLACK, screen_size=WIN_SIZE, font_size=20)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_a:
                    moving_left = True
                elif event.key == K_d:
                    moving_right = True
                elif event.key == K_ESCAPE:
                    show_option_bar = not show_option_bar
                elif event.key == K_SPACE:
                    if starting:
                        starting = False
                elif event.key == K_TAB:
                    show_fps = not show_fps
            elif event.type == KEYUP:
                if event.key == K_a:
                    moving_left = False
                elif event.key == K_d:
                    moving_right = False

        fps = clock.get_fps()
        pygame.display.set_caption(f'Breakout | FPS: {fps}')
        clock.tick(60)
        pygame.display.flip()

if __name__ == '__main__':
    main_menu()