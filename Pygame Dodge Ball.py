import pygame
import random
import time
from datetime import datetime

pygame.init()

#            R    G    B
GRAY     = (100, 100, 100) #button color not highlighted
NAVYBLUE = ( 60,  60, 100) #background color
RED      = (255,   0,   0) #enemy ball color
GREEN    = (  0, 255,   0) #food color
YELLOW   = (255, 255,   0) #button color highlighted
BLACK    = (  0,   0,   0) #text color
HOTPINK  = (255, 105, 180) #player color

SCREENWIDTH = 600
SCREENHEIGHT = 600
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption("Pygame Dodge Ball by Murcsik Tamáska")
FPS = 40
BALL_RADIUS = 15

class EnemyBall():
    "Enemy ball class. The goal is to avoid collision with enemy balls."

    def __init__(self):
        self.radius = BALL_RADIUS
        self.color = RED
        self.position_x = 40
        self.position_y = 40
        self.x_change = random.randint(-5, 5)
        self.y_change = random.randint(-5, 5)

    def move(self):
        self.position_x += self.x_change
        self.position_y += self.y_change
        if self.position_x >= SCREENWIDTH - BALL_RADIUS or self.position_x <= 0 + BALL_RADIUS:
            self.x_change *= -1
        if self.position_y >= SCREENHEIGHT - BALL_RADIUS or self.position_y <= 0 + BALL_RADIUS:
            self.y_change *= -1

    def draw_enemy_ball(self):
        pygame.draw.circle(SCREEN, self.color, (self.position_x, self.position_y), self.radius)

    def check_collision(self):
        mouse_pos = pygame.mouse.get_pos()
        distance_x =  abs(self.position_x - mouse_pos[0])
        distance_y = abs(self.position_y - mouse_pos[1])
        distance = (distance_x**2 + distance_y**2) ** 0.5
        if distance <= BALL_RADIUS * 2:
            game_over_sound()
            write_score_history(score)
            game_over()

class Player:
    "Player class which can be moved by mouse cursor."
    def __init__(self):
        self.radius = BALL_RADIUS
        self.color = HOTPINK

    def draw_player(self):
        pos = pygame.mouse.get_pos()
        pygame.draw.circle(SCREEN, self.color, (pos[0], pos[1]), self.radius)

class Food:
    "Creating food. Goal is to get food to gain score."
    def __init__(self):
        self.radius = BALL_RADIUS
        self.position_x = random.randint(100, 500)
        self.position_y = random.randint(100, 500)
        self.color = GREEN

    def draw_food(self):
        pygame.draw.circle(SCREEN, self.color, (self.position_x, self.position_y), self.radius)

    def check_food_collision(self):
        mouse_pos = pygame.mouse.get_pos()
        distance_x =  abs(self.position_x - mouse_pos[0])
        distance_y = abs(self.position_y - mouse_pos[1])
        distance = (distance_x**2 + distance_y**2) ** 0.5
        if distance <= BALL_RADIUS * 2:
            self.position_x = random.randint(100, 500)
            self.position_y = random.randint(100, 500)
            return True

def start_game():
    FPSCLOCK = pygame.time.Clock()
    SCREEN.fill(NAVYBLUE)
    #GAME OVER FONT
    gameover_font = pygame.font.SysFont("bahnschrift", 100)
    gameover_text = gameover_font.render("DODGE BALL", True, BLACK)
    gameover_text_obj = gameover_text.get_rect()
    gameover_text_obj.center = (SCREENWIDTH / 2, SCREENHEIGHT / 2 - 200)
    #PLAY AGAIN "BUTTON"
    BUTTON_WIDTH = 150
    BUTTON_HEIGHT = 70
    playagain_rect = pygame.Rect(100, 300, BUTTON_WIDTH, BUTTON_HEIGHT)
    playagain_font = pygame.font.SysFont("bahnschrift", 25)
    playagain_text = playagain_font.render("START GAME", True, BLACK)
    playagain_text_obj = playagain_text.get_rect()
    playagain_text_obj.center = (100 + BUTTON_WIDTH / 2, 300 + BUTTON_HEIGHT / 2)
    #EXIT "BUTTON"
    exit_rect = pygame.Rect(SCREENWIDTH - BUTTON_WIDTH - 100, 300, BUTTON_WIDTH, BUTTON_HEIGHT)
    exit_font = pygame.font.SysFont("bahnschrift", 25)
    exit_text = exit_font.render("EXIT", True, BLACK)
    exit_text_obj = exit_text.get_rect()
    exit_text_obj.center = (SCREENWIDTH - BUTTON_WIDTH / 2 - 100, 300 + BUTTON_HEIGHT / 2)
    #SCORE FONT
    max_score_font = pygame.font.SysFont("bahnschrift", 32)

    start_game = True
    while start_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if 100 <= mouse_pos[0] <= 100 + BUTTON_WIDTH and 300 <= mouse_pos[1] <= 300 + BUTTON_HEIGHT:
                    game_loop()
                if SCREENWIDTH - BUTTON_WIDTH - 100 <= mouse_pos[0] <= SCREENWIDTH - 100 and 300 <= mouse_pos[1] <= 300 + BUTTON_HEIGHT:
                    pygame.quit()
                    quit()

        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.rect(SCREEN, GRAY, playagain_rect)
        pygame.draw.rect(SCREEN, GRAY, exit_rect)
        # change the button rect color when the cursor is on
        if 100 <= mouse_pos[0] <= 100 + BUTTON_WIDTH and 300 <= mouse_pos[1] <= 300 + BUTTON_HEIGHT:
            pygame.draw.rect(SCREEN, YELLOW, playagain_rect)
        if SCREENWIDTH - BUTTON_WIDTH - 100 <= mouse_pos[0] <= SCREENWIDTH - 100 and 300 <= mouse_pos[1] <= 300 + BUTTON_HEIGHT:
            pygame.draw.rect(SCREEN, YELLOW, exit_rect)

        # DISPLAY MAX SCORE AND TIME
        score_file = open("score history.txt", "r")
        content = score_file.readlines()
        a = "a"
        score_list = []
        for i in content:
            a_index = i.find(a)
            score_list.append(int(i[19:a_index]))
        max_score = max(score_list)
        max_index = score_list.index(max_score)
        max_score_time = content[max_index]
        max_score_time_format = max_score_time[0:19]
        score_file.close()
        max_score_text = max_score_font.render("Record: {0} {1}".format(max_score, max_score_time_format), True,
                                                   BLACK)
        max_score_text_object = max_score_text.get_rect()
        max_score_text_object.center = (300, 450)
        SCREEN.blit(max_score_text, max_score_text_object)
        SCREEN.blit(gameover_text, gameover_text_obj)
        SCREEN.blit(playagain_text, playagain_text_obj)
        SCREEN.blit(exit_text, exit_text_obj)
        pygame.display.update()
        FPSCLOCK.tick()

def game_over():
    FPSCLOCK = pygame.time.Clock()
    SCREEN.fill(NAVYBLUE)
    #GAME OVER FONT
    gameover_font = pygame.font.SysFont("bahnschrift", 100)
    gameover_text = gameover_font.render("GAME OVER", True, BLACK)
    gameover_text_obj = gameover_text.get_rect()
    gameover_text_obj.center = (SCREENWIDTH / 2, SCREENHEIGHT / 2 - 200)
    #PLAY AGAIN "BUTTON"
    BUTTON_WIDTH = 150
    BUTTON_HEIGHT = 70
    playagain_rect = pygame.Rect(100, 300, BUTTON_WIDTH, BUTTON_HEIGHT)
    playagain_font = pygame.font.SysFont("bahnschrift", 25)
    playagain_text = playagain_font.render("PLAY AGAIN", True, BLACK)
    playagain_text_obj = playagain_text.get_rect()
    playagain_text_obj.center = (100 + BUTTON_WIDTH / 2, 300 + BUTTON_HEIGHT / 2)
    #EXIT "BUTTON"
    exit_rect = pygame.Rect(SCREENWIDTH - BUTTON_WIDTH - 100, 300, BUTTON_WIDTH, BUTTON_HEIGHT)
    exit_font = pygame.font.SysFont("bahnschrift", 25)
    exit_text = exit_font.render("EXIT", True, BLACK)
    exit_text_obj = exit_text.get_rect()
    exit_text_obj.center = (SCREENWIDTH - BUTTON_WIDTH / 2 - 100, 300 + BUTTON_HEIGHT / 2)
    #SCORE TEXT
    score_font = pygame.font.SysFont("bahnschrift", 32)
    score_text = score_font.render("Score: {}".format(score), True, BLACK)
    score_text_obj = score_text.get_rect()
    score_text_obj.center = (150 + BUTTON_WIDTH, 200)
    max_score_font = pygame.font.SysFont("bahnschrift", 32)

    game_over = True
    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if 100 <= mouse_pos[0] <= 100 + BUTTON_WIDTH and 300 <= mouse_pos[1] <= 300 + BUTTON_HEIGHT:
                    game_loop()
                if SCREENWIDTH - BUTTON_WIDTH - 100 <= mouse_pos[0] <= SCREENWIDTH - 100 and 300 <= mouse_pos[1] <= 300 + BUTTON_HEIGHT:
                    pygame.quit()
                    quit()

        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.rect(SCREEN, GRAY, playagain_rect)
        pygame.draw.rect(SCREEN, GRAY, exit_rect)
        # change the button rect color when the cursor is on
        if 100 <= mouse_pos[0] <= 100 + BUTTON_WIDTH and 300 <= mouse_pos[1] <= 300 + BUTTON_HEIGHT:
            pygame.draw.rect(SCREEN, YELLOW, playagain_rect)
        if SCREENWIDTH - BUTTON_WIDTH - 100 <= mouse_pos[0] <= SCREENWIDTH - 100 and 300 <= mouse_pos[1] <= 300 + BUTTON_HEIGHT:
            pygame.draw.rect(SCREEN, YELLOW, exit_rect)

        # DISPLAY MAX SCORE AND TIME
        score_file = open("score history.txt", "r")
        content = score_file.readlines()
        a = "a"
        score_list = []
        for i in content:
            a_index = i.find(a)
            score_list.append(int(i[19:a_index]))
        max_score = max(score_list)
        max_index = score_list.index(max_score)
        max_score_time = content[max_index]
        max_score_time_format = max_score_time[0:19]
        score_file.close()
        max_score_text = max_score_font.render("Record: {0} {1}".format(max_score, max_score_time_format), True,
                                                   BLACK)
        max_score_text_object = max_score_text.get_rect()
        max_score_text_object.center = (300, 450)
        SCREEN.blit(max_score_text, max_score_text_object)

        SCREEN.blit(gameover_text, gameover_text_obj)
        SCREEN.blit(playagain_text, playagain_text_obj)
        SCREEN.blit(exit_text, exit_text_obj)
        SCREEN.blit(score_text, (200 ,200))
        pygame.display.update()
        FPSCLOCK.tick()

def display_score(score):
    score_font = pygame.font.SysFont("bahnschrift", 20)
    score_text = score_font.render("Score: {}". format(score), True, YELLOW)
    SCREEN.blit(score_text, (10, 10))

def game_over_sound():
    game_over_sound = pygame.mixer.Sound("GameOver.wav")
    game_over_sound.play()

def pickup_sound():
    pickup_sound = pygame.mixer.Sound("pickup.mp3")
    pickup_sound.play()

def display_time(t):
    time_font = pygame.font.SysFont("bahnschrift", 20)
    time_text = time_font.render("Time: {}".format(t), True, YELLOW)
    SCREEN.blit(time_text, (10, 30))

def write_score_history(score):
    now = datetime.now()
    now_str = now.strftime("%Y/%m/%d %H:%M:%S")
    score_file = open("score history.txt", "a")
    score_file.write(now_str)
    score_file.write("{}a\n".format(score))
    score_file.close()

def game_loop():
    global score

    initial_ball_number = 1
    enemy_ball_list = []
    t0 = round(time.time())
    for ball in range(initial_ball_number):
        ball = EnemyBall()
        enemy_ball_list.append(ball)
    player = Player()
    food = Food()
    score = 0
    run = True
    while run:
        t1 = round(time.time())
        dt = t1 - t0
        SCREEN.fill(NAVYBLUE)
        FPSCLOCK = pygame.time.Clock()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        for balls in enemy_ball_list:
            balls.move()
            balls.draw_enemy_ball()
            balls.check_collision()
        player.draw_player()
        food.draw_food()
        if food.check_food_collision():
            pickup_sound()
            score += 1
            next_ball = EnemyBall()
            enemy_ball_list.append(next_ball)
        display_score(score)
        display_time(dt)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

start_game()