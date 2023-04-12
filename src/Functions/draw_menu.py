import pygame

def draw_menu(BLOCK_SIZE,screen,SW,SH):
    title_font = pygame.font.Font("font.ttf", BLOCK_SIZE*3)
    title = title_font.render("Snake Menu", True, "white")
    title_rect = title.get_rect(center=(SW/2, SH/5))

    menu_font = pygame.font.Font("font.ttf", BLOCK_SIZE*1)
    start_text = menu_font.render("Press SPACE to Start", True, "white")
    start_rect = start_text.get_rect(center=(SW/2, SH/2))

    controls_text = menu_font.render("Use arrow keys to move", True, "white")
    controls_rect = controls_text.get_rect(center=(SW/2, SH*2/3))

    screen.fill("black")
    screen.blit(title, title_rect)
    screen.blit(start_text, start_rect)
    screen.blit(controls_text, controls_rect)