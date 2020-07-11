import pygame
import random

# game made using the pygame.sprite
# which is a pygame module with basic game object classes

WIDTH = 480
HEIGHT = 600
FPS = 30  # HOW FAST SCREEN IS UPDATED FRAMES/SEC
PINK = (250, 222, 212)

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Title and icon
pygame.display.set_caption("Mochi Jump")
icon = pygame.image.load('mochi.png')
pygame.display.set_icon(icon)

game_ended = False

height = 10
JUMP_SPEED = 20  # Y speed
MOVE_SPEED = 10  # X speed
MAX_COUNT = 30

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
over_font = pygame.font.Font('freesansbold.ttf', 64)
agn_font = pygame.font.Font('freesansbold.ttf', 32)


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (0, 0, 0))
    agn_text = agn_font.render("press enter to play again", True, (0, 0, 0))
    score_text = agn_font.render("score: " + str(player.score), True, (0, 0, 0))
    screen.blit(over_text, (40, 250))
    screen.blit(agn_text, (45, 310))
    screen.blit(score_text, (45, 340))


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.img = ['fork.png', 'knife.png', 'spoon.png']
        i = random.randint(0, 2)
        self.image = pygame.image.load(self.img[i])
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-2000, -10)
        self.speedy = random.randrange(1, 9)

    def update(self):
        # self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + random.randrange(1000):  # or self.rect.left < -25 or self.rect.right >  WIDTH + 20:
            self.image = pygame.image.load(self.img[random.randint(0, 2)])
            self.rect = self.image.get_rect()
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-40, 0)


class Platform(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('board.png')
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.speedy = 0.5
        self.lst = platforms.sprites()
        y_pos = player.rect.top

        max = HEIGHT

        for p in self.lst:  # only enter after first one
            if p.rect.top < max:
                max = p.rect.top

        if max != HEIGHT:
            y_pos = max - 120
        self.rect.y = y_pos

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10:  # or self.rect.left < -25 or self.rect.right >  WIDTH + 20:
            self.lst = platforms.sprites()
            max = HEIGHT
            for p in self.lst:
                if p.rect.top < max:
                    max = p.rect.top

            y_pos = max - 120  # make platform higher than highest one already existing
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = y_pos


# player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('clear_mochi.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 50
        self.speedx = 0
        self.speedy = JUMP_SPEED  # jumping
        # global height
        self.jump_count = 10
        self.vel = [-15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                    11, 12, 13, 14, 15]
        self.count = 0
        self.done = False
        self.again = False
        self.score = 0
        self.game_ended = False

    def collide(self):
        hits = pygame.sprite.spritecollide(player, platforms, False)

        if hits and self.vel[self.count] >= 0:
            self.rect.bottom = hits[0].rect.top
            self.score += 1
            return True
        return False

    def mob_collide(self):
        hits = pygame.sprite.spritecollide(player, mobs, False)
        # avoid out of bounds
        if hits:
            return True
        return False

    def game_over(self):
        # if enter pressed, reset game. if not, stay still
        keystate = pygame.key.get_pressed()
        while not keystate[pygame.K_RETURN]:
            game_over_text()

        # if exit while loop, return pressed

    def update(self):

        if self.game_ended:
            game_over_text()
            keystate = pygame.key.get_pressed()
            if keystate[pygame.K_RETURN]:
                self.rect.centerx = WIDTH / 2
                self.rect.bottom = HEIGHT - 50
                self.count = 0
                self.score = 0
                self.game_ended = False

        else:

            score = font.render("Score: " + str(self.score), True, (0, 0, 0))
            screen.blit(score, (2, 2))

            self.speedx = 0
            keystate = pygame.key.get_pressed()
            if keystate[pygame.K_LEFT]:
                self.speedx = -MOVE_SPEED
            if keystate[pygame.K_RIGHT]:
                self.speedx = MOVE_SPEED
            self.rect.x += self.speedx
            if self.rect.right > WIDTH:
                self.rect.left = 0
            if self.rect.left < 0:
                self.rect.right = WIDTH

            if player.collide():
                self.count = 0

            self.rect.y += self.vel[self.count]
            if self.count >= len(self.vel) - 1:
                self.count = len(self.vel) - 1
            else:
                self.count += 1

            if (player.rect.top >= HEIGHT + 10) or player.mob_collide():
                self.game_ended = True


all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
mobs = pygame.sprite.Group()
player = Player()

for i in range(7):
    m = Platform()
    all_sprites.add(m)
    platforms.add(m)

for i in range(4):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

all_sprites.add(player)

running = True

while running:

    clock.tick(FPS)

    screen.fill(PINK)

    # process input/events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()

    for sprite in all_sprites:
        sprite.rect.y += 1

    # draw/render
    all_sprites.draw(screen)

    # after drawing, flip display

    pygame.display.flip()

pygame.quit()
