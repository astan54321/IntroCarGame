import pygame
import random
import shelve

pygame.init()
d = shelve.open('HighScores.txt')

FPS = 60

display_width = 800
display_height = 600

black = (0, 0, 0)
white = (255, 255, 255)
red = (150, 0, 0)
green = (0, 150, 0)
bred = (255, 0, 0)
bgreen = (0, 255, 0)
blue = (0, 0, 255)

biggening_factor_car = 6
carw = 12 * biggening_factor_car
carh = 16 * biggening_factor_car
turn_angle = 7

biggening_factor_back = 50
backImg = pygame.image.load('Background.png')
backImg = pygame.transform.scale(backImg, (display_width, display_height))

carImg = pygame.image.load('Car.png')
carImg = pygame.transform.scale(carImg, (carw, carh))  # image resized to 96 x 96
leftCarImg = pygame.transform.rotate(carImg, turn_angle)
rightCarImg = pygame.transform.rotate(carImg, -turn_angle)

expImg = pygame.image.load('Explosion.png')
expImg = pygame.transform.scale(expImg, (carw * 2, carh * 2))

enemyImg = pygame.image.load('Enemy.png')
enemyImg = pygame.transform.scale(enemyImg, (carw, carh))

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Car Game')
clock = pygame.time.Clock()

pause = False


def score_disp(score):
    font = pygame.font.SysFont(None, 100)
    text = font.render(str(score), True, black)
    gameDisplay.blit(text, (display_width / 2 - 20, 0))


def things(thingx, thingy):
    gameDisplay.blit(enemyImg, [thingx, thingy])


def back(backx, backy):
    gameDisplay.blit(backImg, (backx, backy))
    gameDisplay.blit(backImg, (backx, backy - display_height))


def car(x, y, crashed):
    if crashed:
        gameDisplay.blit(expImg, (x - carw / 2, y - carh / 2))
    else:
        gameDisplay.blit(carImg, (x, y))


def text_objects(text, font):
    text_surface = font.render(text, True, black)
    return text_surface, text_surface.get_rect()


def message_display(text, x, y):
    font = pygame.font.SysFont(None, 115)
    text_surf, text_rect = text_objects(text, font)
    text_rect.center = (x, y)
    gameDisplay.blit(text_surf, text_rect)

    pygame.display.update()


def crash():
    crashed = True

    while crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit_game()
                if event.key == pygame.K_RETURN:
                    game_loop()

        font = pygame.font.SysFont(None, 115)
        text_surf, text_rect = text_objects("You Crashed!", font)
        text_rect.center = (display_width / 2, display_height / 2)
        gameDisplay.blit(text_surf, text_rect)

        button("Restart", 150, 450, 100, 50, green, bgreen, game_loop)
        button("Exit", 550, 450, 100, 50, red, bred, quit_game)
        pygame.display.update()
        clock.tick(FPS)


def button(msg, x, y, w, h, i_color, a_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, a_color, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()

    else:
        pygame.draw.rect(gameDisplay, i_color, (x, y, w, h))

    small_text = pygame.font.SysFont(None, 20)
    text_surf, text_rect = text_objects(msg, small_text)
    text_rect.center = (x + w / 2, y + h / 2)
    gameDisplay.blit(text_surf, text_rect)


def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit_game()
                if event.key == pygame.K_RETURN:
                    game_loop()

        gameDisplay.fill(white)
        font = pygame.font.SysFont(None, 115)
        text_surf, text_rect = text_objects("Race Game", font)
        text_rect.center = (display_width / 2, display_height / 2)
        gameDisplay.blit(text_surf, text_rect)

        button("Start", 150, 450, 100, 50, green, bgreen, game_loop)
        button("Exit", 550, 450, 100, 50, red, bred, quit_game)
        pygame.display.update()
        clock.tick(FPS)


def unpause():
    global pause
    pause = False


def pause_screen():
    global pause

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    unpause()
                if event.key == pygame.K_RETURN:
                    quit_game()

        gameDisplay.fill(white)
        font = pygame.font.SysFont(None, 115)
        text_surf, text_rect = text_objects("Paused", font)
        text_rect.center = (display_width / 2, display_height / 2)
        gameDisplay.blit(text_surf, text_rect)

        button("Resume", 150, 450, 100, 50, green, bgreen, unpause)
        button("Exit", 550, 450, 100, 50, red, bred, quit_game)
        pygame.display.update()
        clock.tick(FPS)


def quit_game():
    pygame.quit()
    quit()


def game_loop():
    global pause

    score = 0

    carx = (display_width / 2 - carw / 2)
    cary = (display_height * 0.8)

    deltacar = 9

    back_starty = 0

    thing_startx = random.randrange(50 + carw, display_width - (50 + carw))
    thing_starty = -600
    thing_speed = 7

    game_exit = False

    while not game_exit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause = True
                    pause_screen()

        # Movement controls
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_LEFT]:
            carx -= deltacar
        if keys_pressed[pygame.K_RIGHT]:
            carx += deltacar

        # gameDisplay.fill(white)  # make background white
        back(0, back_starty)

        # things(thingx, thingy)
        things(thing_startx, thing_starty)
        thing_starty += thing_speed
        back_starty += thing_speed * 2
        car(carx, cary, False)  # draws car not crashed
        score_disp(score)

        if carx > display_width - 50 - carw or carx < 50:
            car(carx, cary, True)
            crash()

        if back_starty > display_height:
            back_starty = 0

        if thing_starty > display_height:
            thing_starty = 0 - carh
            thing_startx = random.randrange(50 + carw, display_width - (50 + carw))
            score += 1
            if thing_speed < 25:
                thing_speed += 0.3

        if thing_starty + carh > cary and thing_starty < cary + carh:
            if thing_startx < carx + carw and thing_startx + carw > carx:
                car(carx, cary, True)
                crash()

        pygame.display.update()
        clock.tick(FPS)


game_intro()
game_loop()
quit_game()
