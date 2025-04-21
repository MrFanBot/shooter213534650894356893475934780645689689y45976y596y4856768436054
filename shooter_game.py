from pygame import *
from random import *
lost = 0
x1 = 100
y1 = 100
destroyed_count = 0
missed_count = 0
score_hit = 0
font.init()
font = font.SysFont('Arial', 36)

win_width = 700
win_height = 500
BLACK = (0, 0, 0)
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite): 

    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed

class Enemy(GameSprite):
    def __init__(self, sprite_image, sprite_x, sprite_y, sprite_speed):
        super().__init__(sprite_image, sprite_x, sprite_y, sprite_speed)

    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= 10
        if self.rect.y < 0:
            self.kill()


window = display.set_mode((win_width, win_height))
display.set_caption("Шутер")
background = transform.scale(image.load("galaxy.jpg"), (700, 500))
rocket = Player("rocket.png", x1, y1, 10)

enemy1 = Enemy('ufo.png', randint(20, 615), -75, 2)
enemy2 = Enemy('ufo.png', randint(20, 615), -100, 2)
enemy3 = Enemy('ufo.png', randint(20, 615), -75, 2)
enemy4 = Enemy('ufo.png', randint(20, 615), -65, 2)
enemy5 = Enemy('ufo.png', randint(20, 615), -125, 2)


enemy_group = sprite.Group()
enemy_group.add(enemy1)
enemy_group.add(enemy2)
enemy_group.add(enemy3)
enemy_group.add(enemy4)
enemy_group.add(enemy5)


bullet_group = sprite.Group()

clock = time.Clock()
FPS = 60

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()


game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                bullet = Bullet('bullet.png', rocket.rect.x, rocket.rect.y, 20)
                bullet_group.add(bullet)

    
    window.blit(background,(0, 0))

    for enemy in enemy_group:
        if enemy.rect.y > 500:
            missed_count += 1
            enemy.rect.y = random.randint(-100, -40)
            enemy.rect.x = random.randint(0, 700 - enemy.rect.width)

    hits = sprite.groupcollide(bullet_group, enemy_group, True, True)
    #for hit in hits:
        #rocket.score_hit += 1
        #enemy = Enemy(random.randint(0, 700 - 50), random.randint(-100, -40))
        #enemy_group.add(enemy)
    
    for enemy in enemy_group:
        if enemy.rect.top > 500:
            player.score_missed += 1
            enemy.rect.y = random.randint(-100, -40)
            enemy.rect.x = random.randint(0, 700 - enemy.rect.width)

    enemy_group.draw(window)
    bullet_group.draw(window)

    enemy_group.update()
    bullet_group.update()
    rocket.update()
    rocket.reset()


    destroyed_text = font.render(f"Сбито: {destroyed_count}", True, (255, 255, 255))
    missed_text = font.render(f"Пропущено: {missed_count}", True, (255, 255, 255))
    window.blit(destroyed_text, (10, 10))
    window.blit(missed_text, (10, 40))

    display.update()
    clock.tick(FPS)