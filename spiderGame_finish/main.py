import pygame
import random
import sys
from button import ImageButton

# Константы
WIDTH = 800
HEIGHT = 600
BACKGROUND_SPEED = 5
FPS = 30
GRAVITY = 2
GREEN = (1, 50, 32)

# Инициализация pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu test")
main_backround = pygame.image.load('images/backround1.jpg')


def main_menu():
    """отображение главого меню"""
    main_backround = pygame.image.load('images/backround1.jpg')
    start_button = ImageButton(
        WIDTH/2-(175/2), 260, 200, 100,
        '', 'images/new_game.png', 'images/new_game_light.png'
    )
    exit_button = ImageButton(
        WIDTH/2-(120/2), 350, 200, 90,
        '', 'images/exit.png', 'images/exit_light.png'
    )

    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(main_backround, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.USEREVENT and event.button == start_button:
                level_choose()

            if event.type == pygame.USEREVENT and event.button == exit_button:
                running = False
                pygame.quit()
                sys.exit()

            for btn in [start_button, exit_button]:
                btn.handle_event(event)

        for btn in [start_button, exit_button]:
            btn.check_hoover(pygame.mouse.get_pos())
            btn.draw(screen)

        pygame.display.flip()


def level_choose():
    """Экран выбора уровней игры"""
    levels = [
        ImageButton(WIDTH/2-130/2, 100, 200, 100, '',
                    'images/level_1.png', 'images/level_1_light.png'),
        ImageButton(WIDTH/2-130/2, 200, 200, 100, '',
                    'images/level_2.png', 'images/level_2_light.png'),
        ImageButton(WIDTH/2-130/2, 300, 200, 100, '',
                    'images/level_3.png', 'images/level_3_light.png')
    ]
    back = ImageButton(WIDTH/2-(100/2), 400, 200, 100,
                       '', 'images/back.png', 'images/back_light.png')

    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(main_backround, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            if event.type == pygame.USEREVENT and event.button == back:
                running = False

            for i, button in enumerate(levels):
                if event.type == pygame.USEREVENT and event.button == button:
                    in_play(i + 1)

            for btn in [*levels, back]:
                btn.handle_event(event)

        for btn in [*levels, back]:
            btn.check_hoover(pygame.mouse.get_pos())
            btn.draw(screen)

        pygame.display.flip()


def in_play(inlevel):
    """основная функция игры"""

    gameWindow = pygame.display.set_mode((WIDTH, HEIGHT))

    GREEN = (1, 50, 32)
    GRAVITY = 2

    score = 0

    def redrawGameWindow(gameWindow):
        background1.draw(gameWindow)
        background2.draw(gameWindow)

        # Отрисовка платформ
        for tile in tiles[chosenTile]:
            tile.draw(gameWindow)
        for tile in tiles[nextChosenTile]:
            tile.draw(gameWindow)

        # Отрисовка игрока и счета
        player1.draw(gameWindow)
        txt(str(score), WIDTH - 90, 50, 50, GREEN)
        txt("SCORE:", WIDTH - 310, 50, 50, GREEN)

        pygame.display.update()

    def text_objects(text, font, colour):
        textSurface = font.render(text, True, colour)
        return textSurface, textSurface.get_rect()

    def txt(text, x, y, size, colour):
        largeText = pygame.font.Font("Banty Bold.ttf", size)
        TextSurf, TextRect = text_objects(text, largeText, colour)
        TextRect.center = (x, y)
        gameWindow.blit(TextSurf, TextRect)

    class Player():
        def __init__(self, x, y):
            self.h = 60
            self.w = 86
            self.x = x
            self.y = y
            self.vy = 10
            self.spritePicNum = 1
            self.spriteDir = "right"
            self.spritePic = []

            # Загрузка спрайтов игрока
            for i in range(12):
                try:
                    img = pygame.image.load(f"images/sprite{i}.png")
                    self.spritePic.append(img)
                except:
                    # Если спрайт не найден
                    self.spritePic.append(pygame.Surface((self.w, self.h)))

            # Анимация движения
            self.nextLeftPic = [1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1]
            self.nextRightPic = [4, 4, 4, 4, 5, 6, 7, 5, 4, 4, 4, 4]

        # Отрисовка игрока
        def draw(self, gameWindow):
            gameWindow.blit(
                self.spritePic[self.spritePicNum], (self.x, self.y))

        # Проверка столкновения с другим объектом
        def collide(self, other):
            if pygame.Rect(self.x, self.y, self.w, self.h).colliderect(other.x, other.y, other.w, other.h):
                return True

        # Переворот спрайта игрока
        def flip(self):
            for i in range(len(self.spritePic)):
                if isinstance(self.spritePic[i], pygame.Surface):
                    self.spritePic[i] = pygame.transform.flip(
                        self.spritePic[i], False, True)

    class Tile():
        # Препятствия
        def __init__(self, x, y, w, h):
            self.x = x
            self.y = y
            self.w = w
            self.h = h
            self.img = pygame.image.load("images/line.jpg")
            self.img = pygame.transform.scale(self.img, (self.w, self.h))
            self.img = self.img.convert_alpha()
            self.img2 = pygame.image.load("images/line2.jpg")
            self.img2 = pygame.transform.scale(self.img2, (self.w, self.h))
            self.img2 = self.img2.convert_alpha()
            self.img3 = pygame.image.load("images/line3.jpg")
            self.img3 = pygame.transform.scale(self.img3, (self.w, self.h))
            self.img3 = self.img3.convert_alpha()

        # Отрисовка платформы
        def draw(self, gameWindow):
            if self.w == self.h:
                gameWindow.blit(self.img, (self.x, self.y))
            elif self.h > self.w:
                gameWindow.blit(self.img3, (self.x, self.y))
            else:
                gameWindow.blit(self.img2, (self.x, self.y))

        # Движение платформы
        def move(self, speed):
            self.x -= speed

    class Sprite(pygame.sprite.Sprite):
        def __init__(self, picture=None, x=0, y=0, speed=0):
            pygame.sprite.Sprite.__init__(self)
            self.x = x
            self.y = y
            self.speed = speed
            self.visible = False
            image1 = pygame.image.load(picture)
            self.image = pygame.transform.scale(image1, (800, 600))
            self.rect = self.image.get_rect()
            self.update()

        # Появление игрока
        def spawn(self, x, y):
            self.x = x - self.rect.width / 2
            self.y = y - self.rect.height / 2
            self.rect = pygame.Rect(
                self.x, self.y, self.rect.width, self.rect.height)
            self.visible = True
            self.update()

        # Отрисовка игрока
        def draw(self, surface):
            surface.blit(self.image, self.rect)

        def update(self):  # Обновление после спрайта
            self.rect = pygame.Rect(
                self.x, self.y, self.rect.width, self.rect.height)

        # Движение игрока
        def moveLeft(self, shift):
            self.x -= shift
            self.update()

    ####################### Наборы препятсвий #############################
    tiles1 = [Tile(0, 100, 300, 50), Tile(400, 100, 300, 50), 
              Tile(0, 450, 200, 50), Tile(200, 450, 200, 50),
              Tile(500, 450, 300, 50), Tile(600, 225, 50, 150),
              Tile(200, 225, 50, 150)
              ]

    tiles2 = [Tile(0, 400, 200, 50), Tile(200, 400, 200, 50), 
              Tile(400, 400, 200, 50), Tile(600, 400, 200, 50), 
              Tile(0, 200, 200, 50), Tile(200, 350, 50, 50),
              Tile(350, 250, 50, 50), Tile(500, 350, 50, 50), 
              Tile(650, 250, 50, 50), Tile(200, 200, 200, 50),
              Tile(400, 200, 200, 50), Tile(600, 200, 200, 50),
              ]

    tiles3 = [Tile(0, 100, 200, 50), Tile(200, 100, 200, 50),
              Tile(400, 100, 200, 50), Tile(600, 100, 200, 50),
              Tile(200, 150, 200, 50), Tile(400, 150, 200, 50),
              Tile(300, 200, 200, 50),Tile(0, 450, 200, 50), 
              Tile(200, 450, 200, 50), Tile(400, 450, 200, 50), 
              Tile(600, 450, 200, 50), Tile(200, 400, 200, 50), 
              Tile(400, 400, 200, 50), Tile(300, 350, 200, 50)
              ]

    tiles4 = [Tile(0, 150, 200, 50), Tile(200, 100, 100, 50), 
              Tile(300, 50, 200, 50), Tile(500, 100, 100, 50),
              Tile(600, 150, 200, 50), Tile(0, 400, 200, 50),
              Tile(200, 450, 100, 50), Tile(300, 500, 200, 50),
              Tile(500, 450, 100, 50),Tile(600, 400, 200, 50)
              ]

    tiles5 = [Tile(0, 100, 200, 50), Tile(200, 100, 200, 50),
              Tile(400, 100, 200, 50), Tile(600, 100, 200, 50),
              Tile(150, 225, 50, 150), Tile(450, 225, 50, 150),
              Tile(300, 350, 50, 100), Tile(300, 150, 50, 100),
              Tile(600, 350, 50, 100), Tile(600, 150, 50, 100),
              Tile(0, 450, 200, 50), Tile(200, 450, 200, 50),
              Tile(400, 450, 200, 50), Tile(600, 450, 200, 50)
              ]

    # случайная последовательность препятствий
    tiles = [tiles1, tiles2, tiles3, tiles4, tiles5]
    chosenTile = random.randint(0, len(tiles) - 1)
    nextChosenTile = random.randint(0, len(tiles) - 1)
    while (nextChosenTile == chosenTile):
        nextChosenTile = random.randint(0, len(tiles) - 1)
    for tile in tiles[nextChosenTile]:
        tile.x += WIDTH

    BACKGROUND_SPEED = 5
    background1 = Sprite("images/backround1.jpg")
    background1.spawn(WIDTH/2, HEIGHT/2)
    background2 = Sprite("images/backround2.jpg")
    background2.spawn(WIDTH/2+background1.rect.width, HEIGHT/2)

    player1 = Player(WIDTH // 3, 300)
    clock = pygame.time.Clock()
    FPS = 30
    isOnGround = False

    running = True
    while running:
        # условия победы, ускорение ед отс/ откр рас закр
        if inlevel == 1:
            if score == 100:
                level_succsess(score, 1)
            elif score >= 200 and score < 500:
                BACKGROUND_SPEED = 5
            elif score >= 500 and score < 600:
                BACKGROUND_SPEED = 6
            elif score >= 600:
                BACKGROUND_SPEED = 7

        elif inlevel == 2:
            if score == 200:
                level_succsess(score, 2)
            elif score >= 200 and score < 500:
                BACKGROUND_SPEED = 8
            elif score >= 500 and score < 600:
                BACKGROUND_SPEED = 8
            elif score >= 600:
                BACKGROUND_SPEED = 10

        else:
            if score == 300:
                level_succsess(score, 3)
            elif score >= 200 and score < 500:
                BACKGROUND_SPEED = 10
            elif score >= 500 and score < 600:
                BACKGROUND_SPEED = 12
            elif score >= 600:
                BACKGROUND_SPEED = 13

        redrawGameWindow(gameWindow)
        clock.tick(FPS)
        pygame.event.clear()
        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            running = False
        player1.spriteDir = "right"

        if player1.y:
            player1.spritePicNum = player1.nextRightPic[player1.spritePicNum]

        # перемещение
        if isOnGround:
            if GRAVITY > 0 and keys[pygame.K_UP]:
                player1.flip()
                GRAVITY *= -1
                player1.y += GRAVITY

            elif GRAVITY < 0 and keys[pygame.K_DOWN]:
                player1.flip()
                GRAVITY *= -1
                player1.y += GRAVITY

        for tile in tiles[chosenTile]:
            isOnGround = player1.collide(tile)
            if isOnGround == True:
                if (GRAVITY > 0):
                    player1.y = tile.y - player1.h + 1
                elif (GRAVITY < 0):
                    player1.y = tile.y + tile.h - 1
                break

        if (not isOnGround):
            for tile in tiles[nextChosenTile]:
                isOnGround = player1.collide(tile)
                if isOnGround == True:
                    if (GRAVITY > 0):
                        player1.y = tile.y - player1.h + 1
                    elif (GRAVITY < 0):
                        player1.y = tile.y + tile.h - 1
                    break

        if (isOnGround == None):
            isOnGround = False

        for tile in tiles[chosenTile]:
            tile.move(BACKGROUND_SPEED)
            if pygame.Rect(player1.x, player1.y, player1.w, player1.h).colliderect(tile.x, tile.y + 7, tile.w + 10, tile.h - 14):
                player1.x -= BACKGROUND_SPEED

        for tile in tiles[nextChosenTile]:
            tile.move(BACKGROUND_SPEED)

            if pygame.Rect(player1.x, player1.y, player1.w, player1.h).colliderect(tile.x, tile.y + 7, tile.w + 10, tile.h - 14):
                player1.x -= BACKGROUND_SPEED

        if (tiles[chosenTile][0].x == -WIDTH):
            score += 50

            for tile in tiles[chosenTile]:
                tile.x += WIDTH

            chosenTile = random.randint(0, len(tiles) - 1)
            while (nextChosenTile == chosenTile):
                chosenTile = random.randint(0, len(tiles) - 1)

            for tile in tiles[chosenTile]:
                tile.x += WIDTH

        if (tiles[nextChosenTile][0].x == -WIDTH):
            score += 50
            for tile in tiles[nextChosenTile]:  # начисление очков
                tile.x += WIDTH
            nextChosenTile = random.randint(0, len(tiles) - 1)

            while (nextChosenTile == chosenTile):
                nextChosenTile = random.randint(0, len(tiles) - 1)
            for tile in tiles[nextChosenTile]:
                tile.x += WIDTH

        if isOnGround:
            player1.vy = 0
        else:
            player1.vy = player1.vy + GRAVITY
            player1.y = player1.y + player1.vy
        background1.moveLeft(BACKGROUND_SPEED)  # фон1 влево

        if background1.x < -background1.rect.width:
            background1.x = background2.rect.width - BACKGROUND_SPEED
        background2.moveLeft(BACKGROUND_SPEED)  # фон2 влево

        if background2.x < -background2.rect.width:
            background2.x = background1.rect.width - BACKGROUND_SPEED

        if player1.x < 0-player1.w or player1.y > HEIGHT or player1.y < 0:  # проверка выхода за границы игрока
            game_end(score, inlevel)

# Уровень пройден


def level_succsess(score, inlevel):

    GREEN = (1, 50, 32)

    gameWindow = pygame.display.set_mode((WIDTH, HEIGHT))

    def text_objects(text, font, colour):
        textSurface = font.render(text, True, colour)
        return textSurface, textSurface.get_rect()

    def txt(text, x, y, size, colour):
        largeText = pygame.font.Font("Banty Bold.ttf", size)
        TextSurf, TextRect = text_objects(text, largeText, colour)
        TextRect.center = (x, y)
        gameWindow.blit(TextSurf, TextRect)

    main_backround = pygame.image.load('images/level_passed.png')
    main_backround = main_backround.convert_alpha()

    next_level = ImageButton(WIDTH/2-(190/2), 200, 200,
                             80, '', 'images/next_level.png', 'images/next_level_light.png')
    menu = ImageButton(WIDTH/2-(100/2), 300, 100, 50,
                       '', 'images/menu.png', 'images/menu_light.png')
    running = True

    while running:
        screen.fill((0, 0, 0))
        screen.blit(main_backround, (0, 0))

        txt("score:", WIDTH//2, 400, 40, GREEN)          # счет
        txt(str(score), WIDTH // 2 + 120, 400, 40, GREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.USEREVENT and event.button == next_level:
                if inlevel == 1:
                    in_play(2)
                elif inlevel == 2:
                    in_play(3)
            if event.type == pygame.USEREVENT and event.button == menu:
                main_menu()

            for btn in [next_level, menu]:
                btn.handle_event(event)

        for btn in [next_level, menu]:
            btn.check_hoover(pygame.mouse.get_pos())
            btn.draw(screen)

        pygame.display.flip()

# проигрыш


def game_end(score, inlevel):
    GREEN = (1, 50, 32)
    gameWindow = pygame.display.set_mode((WIDTH, HEIGHT))

    def text_objects(text, font, colour):
        textSurface = font.render(text, True, colour)
        return textSurface, textSurface.get_rect()

    def txt(text, x, y, size, colour):
        largeText = pygame.font.Font("Banty Bold.ttf", size)
        TextSurf, TextRect = text_objects(text, largeText, colour)
        TextRect.center = (x, y)
        gameWindow.blit(TextSurf, TextRect)

    main_backround = pygame.image.load('images/game_over.png')
    main_backround = main_backround.convert_alpha()

    restart = ImageButton(WIDTH/2-(190/2), 200, 200, 50,
                          '', 'images/restart.png', 'images/restart_light.png')
    menu = ImageButton(WIDTH/2-(100/2), 300, 100, 50,
                       '', 'images/menu.png', 'images/menu_light.png')
    running = True

    while running:
        screen.fill((0, 0, 0))
        screen.blit(main_backround, (0, 0))

        txt("score:", WIDTH//2, 400, 40, GREEN)
        txt(str(score), WIDTH // 2 + 120, 400, 40, GREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.USEREVENT and event.button == restart:
                if inlevel == 1:
                    in_play(1)
                elif inlevel == 2:
                    in_play(2)
                elif inlevel == 3:
                    in_play(3)
            if event.type == pygame.USEREVENT and event.button == menu:
                main_menu()

            for btn in [restart, menu]:
                btn.handle_event(event)

        for btn in [restart, menu]:
            btn.check_hoover(pygame.mouse.get_pos())
            btn.draw(screen)

        pygame.display.flip()


if __name__ == '__main__':
    main_menu()
