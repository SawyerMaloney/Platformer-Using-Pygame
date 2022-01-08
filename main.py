import pygame
from sys import exit
from Player import Player
from Ground import Ground
from HighscoreWindow import HighscoreWindow
from random import randint
from Input import Input

pygame.init()


class ground_data:
    def __init__(self, onGround, position):
        self.onGround = onGround
        self.position = position


class Screen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.size = (width, height)


def checkGround():
    for sprite in ground:
        if (
            sprite.rect.top <= player.sprite.rect.bottom
            and sprite.rect.bottom >= player.sprite.rect.bottom
        ):
            if (
                sprite.rect.left <= player.sprite.rect.right
                and sprite.rect.right >= player.sprite.rect.left
            ):
                data = ground_data(True, sprite.rect.top)
                return data
    data = ground_data(False, 0)
    return data


def check_scroll(player):
    if player.rect.y < 400:
        return 400 - player.rect.y
    return 0


def check_spawn_new_obstacle():
    offset = 25
    if len(ground.sprites()) < 8:
        previous = ground.sprites()[-1].rect
        previous_centerx = previous.centerx
        if (previous_centerx - offset + 400) % 400 > (
            previous_centerx + offset + 400
        ) % 400:
            ground.add(
                Ground(
                    (
                        randint(
                            (previous_centerx + offset + 400) % 400,
                            (previous_centerx - offset + 400) % 400,
                        ),
                        previous.centery - 200,
                    ),
                    (50, 30),
                )
            )
        else:
            ground.add(
                Ground(
                    (
                        randint(
                            (previous_centerx - offset + 400) % 400,
                            (previous_centerx + offset + 400) % 400,
                        ),
                        previous.centery - 200,
                    ),
                    (50, 30),
                )
            )


def check_game_over():
    if player.sprite.rect.y > 1000:
        highscore_bool = restart()
        return False, highscore_bool
    return True, False


def restart():
    highscore_bool = check_highscore(score)
    player.empty()
    player.add(Player(SCREEN))

    ground.empty()
    ground.add(Ground((SCREEN.width / 2, SCREEN.height - 50), (50, 30)))

    while len(ground.sprites()) < 8:
        previous = ground.sprites()[-1].rect.centery
        ground.add(Ground((randint(75, SCREEN.width - 75), previous - 200), (50, 30)))
    return highscore_bool


def display_score():
    font = pygame.font.SysFont("verdana", 25)
    score_text = font.render(f"{round(score, 2)}", True, "white")
    score_text_rect = score_text.get_rect(center=(200, 50))
    screen.blit(score_text, score_text_rect)


def print_highscores():
    font = pygame.font.SysFont("verdana", 20)
    # print 'highscore' text
    highscore_text = font.render("Top Five", True, "black")
    highscore_text_rect = highscore_text.get_rect(center=(200, 325))
    screen.blit(highscore_text, highscore_text_rect)
    highscores = []
    offset = 0
    with open("highscores.txt", "r") as f:
        highscores = [line.strip() for line in f.readlines()]
    for i in range(5):
        highscore = highscores[i].split(",")
        highscore = font.render(f"{highscore[0]} -- {highscore[1]}", True, "black")
        highscore_rect = highscore.get_rect(center=(200, 355 + offset))
        screen.blit(highscore, highscore_rect)
        offset += 25


def check_highscore(player_score):
    with open("highscores.txt", "r") as f:
        highscores = [line.strip().split(",") for line in f.readlines()]
        highscore_bool = False
        for i in range(5):
            if player_score > int(
                highscores[i][1]
            ):  # we have a new highscore, lets deal with it
                highscore_bool = True
                break
    return highscore_bool


def check_score(score):
    for sprite in ground.sprites():
        if sprite.rect.top > 600 and not sprite.counted:
            score += 1
            sprite.counted = True

    return score


def update_highscore(name, score):
    with open("highscores.txt", "r") as f:
        highscores = [line.strip().split(",") for line in f.readlines()]
        for i in range(5):
            if score > int(highscores[i][1]):
                highscores.insert(i, [f"{name}", f"{score}"])
                highscores.pop()
                break
        with open("highscores.txt", "w") as f:
            for line in highscores:
                f.write(f"{line[0]},{line[1]}\n")


SCREEN = Screen(400, 600)
screen = pygame.display.set_mode(SCREEN.size)
pygame.display.set_caption("Jumper")
scroll_speed = 5
game_active = True  # SHOULD BE TRUE
score = 0
highscore_bool = False  # SHOULD BE FALSE

# handling text input
pygame.key.stop_text_input()

# fonts
font = pygame.font.SysFont("verdana", 50)
clock = pygame.time.Clock()

# groups
player = pygame.sprite.GroupSingle()
player.add(Player(SCREEN))

ground = pygame.sprite.Group()
ground.add(Ground((SCREEN.width / 2, SCREEN.height - 50), (50, 30)))

# timers
score_timer = pygame.USEREVENT + 1
pygame.time.set_timer(score_timer, 100)

# input
Input = Input((350, 50), (200, 300))

while len(ground.sprites()) < 8:
    previous = ground.sprites()[-1].rect.centery
    ground.add(Ground((randint(75, SCREEN.width - 75), previous - 200), (50, 30)))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if highscore_bool:
            if event.type == pygame.MOUSEBUTTONDOWN:
                Input.clicked(pygame.mouse.get_pos())
            if event.type == pygame.TEXTINPUT:
                Input.type(event.text)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                Input.backspace()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                highscore_name = Input.enter()
                update_highscore(highscore_name, score)
                highscore_bool = False

    if (
        pygame.key.get_pressed()[pygame.K_SPACE]
        and not game_active
        and not highscore_bool
    ):
        score = 0
        game_active = True

    if game_active:

        screen.fill("black")
        scroll_distance = check_scroll(player.sprite)

        player.draw(screen)
        data = checkGround()
        player.sprite.apply_gravity(data.onGround, data.position)
        player.update(data.onGround, scroll_distance, scroll_speed)

        ground.draw(screen)
        ground.update(scroll_distance, scroll_speed)
        check_spawn_new_obstacle()
        score = check_score(score)
        display_score()
        game_active, highscore_bool = check_game_over()

    else:
        if highscore_bool:

            screen.fill("white")
            highscore_reached_text = font.render("! HIGHSCORE !", True, "black")
            highscore_reached_text_rect = highscore_reached_text.get_rect(
                center=(200, 100)
            )
            screen.blit(highscore_reached_text, highscore_reached_text_rect)
            Input.draw(screen)

        else:
            screen.fill("white")
            score_text = font.render(f"SCORE: {score}", True, "black")
            score_text_rect = score_text.get_rect(center=(200, 25))
            game_over_text = font.render("GAME OVER", True, "black")
            game_over_text_rect = game_over_text.get_rect(center=(200, 100))
            space_text = font.render("PRESS SPACE", True, "black")
            space_text_rect = space_text.get_rect(center=(200, 200))
            restart_text = font.render("TO RESTART", True, "black")
            restart_text_rect = restart_text.get_rect(center=(200, 275))
            screen.blit(space_text, space_text_rect)
            screen.blit(restart_text, restart_text_rect)
            screen.blit(game_over_text, game_over_text_rect)
            screen.blit(score_text, score_text_rect)

            # handle printing highscores
            print_highscores()

    clock.tick(60)
    pygame.display.update()
