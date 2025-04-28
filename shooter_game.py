from pygame import *
from time import time as timer
mixer.init()
font.init()
from random import randint


mw_height = 500
mw_width = 700

mw = display.set_mode((mw_width, mw_height))
display.set_caption('Space Force: Arcade Edition')

clock = time.Clock()

game = True
finish = False

background = transform.scale(image.load('galaxy.jpg'), (mw_width, mw_height))

fire_sound = mixer.Sound('fire.ogg')

mixer.music.load('space.ogg')
mixer.music.play()

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, size_x, size_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5: 
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < mw_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 15, 20)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > mw_height:
            self.rect.x = randint(80, mw_width - 80)
            self.rect.y = 0
            lost += 1


class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > mw_height:
            self.rect.x = randint(80, mw_width - 80)
            self.rect.y = 0

class Bullet(GameSprite):
    def update(self):
       self.rect.y -= self.speed
       if self.rect.y < 0:
           self.kill()

ship = Player('rocket.png', 5, 400, 10, 80, 100)

monsters = sprite.Group()
bullets = sprite.Group()
asteroids = sprite.Group()

for i in range(5):
    monster = Enemy('ufo.png', randint(80, 620), -40, randint(1, 4), 80, 50)
    monsters.add(monster)
    
for i in range(1, 3):
    asteroid = Asteroid('asteroid.png', randint(30, 670), -40, randint(1, 7), 80, 50)
    asteroids.add(asteroid)


font1 = font.SysFont('Arial', 80)
font2 = font.SysFont('Arial', 36)


lost = 0
score = 0


rel_time = False
life = 3 
num_fire = 0


win = font1.render('YOU WIN', True, (255, 255, 255)) 
lose = font1.render('YOU LOSE', True, (255, 255, 255))











while game:
    for e in event.get():
        if e.type == QUIT:
           game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    ship.fire()
                    fire_sound.play()
                if num_fire >= 5 and rel_time == False:
                    end_time = timer()
                    rel_time = True

    # if life == 0 or lost >= 4:
    #     finish = True
         
    # if life == 3:
    #     life_color = (0, 200, 0)
    # if life == 2:
    #     life_color = (255, 255, 0)
    # if life == 1:
    #     life_color = (200, 0 , 0)
    #text_life = font1.render(str(life), True, life_color)
    #mw.blit(text_life, (650, 10))

    


    if finish != True:
        mw.blit(background, (0, 0))
        txt = font2.render('Счет: ' + str(score), True, (255, 255, 255))
        mw.blit(txt, (10, 20))
        txt_lost = font2.render('Пропущено: ' + str(lost), True, (255, 255, 255))
        mw.blit(txt_lost, (10, 50))




        if rel_time == True:
            now_time = timer()
            if now_time - end_time < 3:
                rel = font2.render('Wait, reload...', True, (255, 255, 255))
                mw.blit(rel, (260, 460))
        else:
            num_fire = 0
            rel_time = False


        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            finish = True
            mw.blit(lose, (200, 200))
        
        
        bullets.draw(mw)
        collides = sprite.groupcollide(monsters, bullets, True, True) 
        for i in collides:
            score += 1
            monster = Enemy('ufo.png', randint(80, 620), -40, randint(1, 4), 80, 50)
            monsters.add(monster)
        
        if score >= 10:
            finish = True
            mw.blit(win, (200, 200))
       #-----------------#
        ship.update()
        ship.reset()
        bullets.update()
        bullets.draw(mw)
        monsters.update()
        monsters.draw(mw)
        asteroids.draw(mw)
        asteroids.update()
        display.update()
        #clock.tick() не обязательно
    display.update()
    time.delay(50)
