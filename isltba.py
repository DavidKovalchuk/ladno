from pygame import *
window = display.set_mode((700,500))
display.set_caption('game')
run = True
class GameSprite(sprite.Sprite):
    def __init__(self,picture,w,h,x,y):
        super().__init__()
        self.image = transform.scale(image.load(picture),(w,h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))
class Player(GameSprite):
    def __init__(self,picture,w,h,x,y,x_speed,y_speed):
        GameSprite.__init__(self,picture,w,h,x,y)
        self.x_speed = x_speed
        self.y_speed = y_speed
    def update(self):
        self.rect.x += self.x_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0:
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.x_speed < 0:
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right)
        self.rect.y += self.y_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0:
            for p in platforms_touched:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
        elif self.y_speed < 0:
            for p in platforms_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom)
    def fire(self):
        bullet = Bullet('bullet.png',self.rect.right,self.rect.centery,30,20,10)
        bullets.add(bullet)
class Enemy(GameSprite):
    def __init__(self, picture, w, h, x, y, speed,x1,x2):
        GameSprite.__init__(self, picture, w, h, x, y)
        self.speed = speed
        self.direction = 'left'
        self.x1 = x1
        self.x2 = x2
    def update(self):
        if self.rect.x <=self.x1:
            self.direction = 'right'
        if self.rect.x >=self.x2:
            self.direction = 'left'
        if self.direction == 'left':
            self.rect.x -= self.speed
        if self.direction == 'right':
            self.rect.x += self.speed
class Bullet(GameSprite):
    def __init__(self, picture, x, y, w, h, speed):
        GameSprite.__init__(self, picture, w, h, x, y)
        self.speed = speed
    def update(self):
        self.rect.x += self.speed
        if self.rect.x > 710:
            self.kill()
        sprite.groupcollide(bullets, barriers, True, False)
        sprite.groupcollide(bullets, vorogs, True, True)
wall1 = GameSprite('dfdfdf.jpg',60,200,200,300)
wall2 = GameSprite('dfdfdf.jpg',60,200,350,0)
wall3 = GameSprite('dfdfdf.jpg',60,200,500,300)
wall4 = GameSprite('dfdfdf.jpg',60,200,0,50)
wall5 = GameSprite('dfdfdf.jpg',300,50,50,100)
final = GameSprite('final.png', 40, 40, 400, 100)
pacman = Player('121212.png',80,80,100,250,0,0)
vorog = Enemy('ufo.png', 40,40,200,200,10,200,300)
vorog2 = Enemy('ufo.png', 40,40,100,100,10,400,600)
win = transform.scale(image.load('win.jpg'), (700,500))
loose = transform.scale(image.load('game_over.jpg'), (700,500)) 
background = transform.scale(image.load('background.jpg'), (700,500))
bullets = sprite.Group()
barriers = sprite.Group()
barriers.add(wall1)
barriers.add(wall2)
barriers.add(wall3)
barriers.add(wall4)
barriers.add(wall5)
vorogs = sprite.Group()
vorogs.add(vorog)
vorogs.add(vorog2)
finsish = False
while run:
    window.fill((255,255,255))
    time.delay(50)
    window.blit(background, (0,0))
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                pacman.fire()
            if e.key == K_UP:
                pacman.y_speed = -5
            if e.key == K_DOWN:
                pacman.y_speed = 5
            if e.key == K_LEFT:
                pacman.x_speed = -5
            if e.key == K_RIGHT:
                pacman.x_speed = 5
        elif e.type == KEYUP:
            if e.key == K_UP:
                pacman.y_speed = 0
            if e.key == K_DOWN:
                pacman.y_speed = 0
            if e.key == K_LEFT:
                pacman.x_speed = 0
            if e.key == K_RIGHT:
                pacman.x_speed = 0
    if finsish != True:
        barriers.draw(window)
        final.reset()
        pacman.update()
        pacman.reset()
        vorogs.update()
        vorogs.draw(window)
        bullets.update()
        bullets.draw(window)
        if sprite.collide_rect(pacman, final):
            finish = True
            window.blit(win, (0,0))
        if sprite.spritecollide(pacman, vorogs, False): 
            finish = True
            window.blit(loose, (0,0))
    display.update()