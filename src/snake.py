
import pygame
import sys 
import random

from Functions.draw_menu import draw_menu


pygame.init()

SW, SH = 800, 800

BLOCK_SIZE = 50
FONT = pygame.font.Font("font.ttf", BLOCK_SIZE*2)

screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Snake!")
draw_menu(BLOCK_SIZE,screen,SW,SH)

clock = pygame.time.Clock()

menu_running = True

while menu_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            menu_running = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                menu_running = False
    
    pygame.display.update()
    clock.tick(5)


class Snake:
    def __init__(self):
        self.x, self.y = BLOCK_SIZE, BLOCK_SIZE
        self.xdir = 1
        self.ydir = 0
        self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
        self.body = [pygame.Rect(self.x-BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)]
        self.dead = False
    
    def update(self):
        global apple
        
        for square in self.body:
            if self.head.x == square.x and self.head.y == square.y:
                self.dead = True
            if self.head.x not in range(0, SW) or self.head.y not in range(0, SH):
                self.dead = True
        
        if self.dead:
            self.x, self.y = BLOCK_SIZE, BLOCK_SIZE
            self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
            self.body = [pygame.Rect(self.x-BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)]
            self.xdir = 1
            self.ydir = 0
            self.dead = False
            apple = Apple()
        
        self.body.append(self.head)
        for i in range(len(self.body)-1):
            self.body[i].x, self.body[i].y = self.body[i+1].x, self.body[i+1].y
        self.head.x += self.xdir * BLOCK_SIZE
        self.head.y += self.ydir * BLOCK_SIZE
        self.body.remove(self.head)

class Apple:
    def __init__(self):
        self.x = int(random.randint(0, SW)/BLOCK_SIZE) * BLOCK_SIZE
        self.y = int(random.randint(0, SH)/BLOCK_SIZE) * BLOCK_SIZE
        self.rect = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
    
    def update(self):
        pygame.draw.rect(screen, "orange", self.rect)

class BadApple:
    def __init__(self):
        self.x = random.randint(0, SW/BLOCK_SIZE - 1) * BLOCK_SIZE
        self.y = random.randint(0, SH/BLOCK_SIZE - 1) * BLOCK_SIZE
        self.rect = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
        self.speed = BLOCK_SIZE/2

    def update(self):
        direction = random.choice([(self.speed, 0), (-self.speed, 0), (0, self.speed), (0, -self.speed)])
        self.rect.move_ip(direction)
          # Verificar si la manzana está fuera del área de juego
        if self.rect.left < 0 or self.rect.right > SW or self.rect.top < 0 or self.rect.bottom > SH:
            self.x = random.randint(0, SW/BLOCK_SIZE - 1) * BLOCK_SIZE
            self.y = random.randint(0, SH/BLOCK_SIZE - 1) * BLOCK_SIZE
            self.rect.topleft = (self.x, self.y)
            
        self.x, self.y = self.rect.topleft

def drawGrid():
    for x in range(0, SW, BLOCK_SIZE):
        for y in range(0, SH, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, "#3c3c3b", rect, 1)



score = FONT.render("1", True, "white")
score_rect = score.get_rect(center=(SW/2, SH/20))
menu_running = True

while menu_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            menu_running = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                menu_running = False
    
    pygame.display.update()
    clock.tick(5)

bad_apple = BadApple()
apple = Apple()
snake = Snake()

game_running = True

score = 0
score_surface = FONT.render(f"Score: {score}", True, "white")

while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                snake.ydir = 1
                snake.xdir = 0
            elif event.key == pygame.K_UP:
                snake.ydir = -1
                snake.xdir = 0
            elif event.key == pygame.K_RIGHT:
                snake.ydir = 0
                snake.xdir = 1
            elif event.key == pygame.K_LEFT:
                snake.ydir = 0
                snake.xdir = -1
 
    snake.update()
    
    screen.fill('black')
    drawGrid()

    apple.update()

    bad_apple.update()
    pygame.draw.rect(screen, "red", bad_apple.rect)

    pygame.draw.rect(screen, "green", snake.head)

    for square in snake.body:
        pygame.draw.rect(screen, "green", square)

    screen.blit(score_surface, (10, 10))

    if snake.head.x == apple.x and snake.head.y == apple.y:
        snake.body.append(pygame.Rect(square.x, square.y, BLOCK_SIZE, BLOCK_SIZE))
        apple = Apple()
        score += 1
        score_surface = FONT.render(f"Score: {score}", True, "white") 

    if snake.head.colliderect(bad_apple.rect):
        snake.body.pop()
        score -= 1
        score_surface = FONT.render(f"Score: {score}", True, "white")

    pygame.display.update()
    clock.tick(5)