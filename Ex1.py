import pygame
import math
import random


def load_image(name):
    fullname = f"{'data'}/{name}"
    image = pygame.image.load(fullname).convert_alpha()
    return image


pygame.init()

clock = pygame.time.Clock()

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 102, 0)
YELLOW = (255, 255, 0)

fps = 60
wscene = 48*15
hscene = 64*10

# scene = pygame.display.set_mode((wscene, hscene), pygame.FULLSCREEN)
scene = pygame.display.set_mode((wscene, hscene))
pygame.display.set_caption("Ходим и прыгаем!")


class Ground(pygame.sprite.Sprite):
    def __init__(self, posx, posy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((64, 64))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        # self.rect.center = (wscene / 2, hscene / 2)
        self.rect.x = posx
        self.rect.y = posy

        self.deltax = 0
        self.deltay = 0


class Hero(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Hero, self).__init__()

        #self.list = []
        #for i in range(1, 3):
        #    self.list.append(load_image("hero/hero" + str(i) + ".png"))
        # self.list_idle = [self.convert(f) for f in glob("cat/Idle*.png")]

        #self.counter = 0
        #self.image = self.list[0]
        #self.image = self.list[0]
        # self.w, self.h = self.image.get_size()
        #self.rect = self.image.get_rect()

        self.image = pygame.Surface((48, 64))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

        w = self.rect.width
        h = self.rect.height

        

        self.hdir = ""
        self.prov = ""
        
        self.vdir = ""
        

        self.xVelocity = 0
        self.yVelocity = 0
        self.speed = 1
        
        self.jumpCount = 12
        self.gravity = 2
        self.isJump = False
        self.mask = pygame.mask.from_surface(self.image)

    # def convert(self, f):
    #    return pygame.image.load(f).convert_alpha()
    def getKeys(self):
        self.hdir = ""
        
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.xVelocity -= self.speed
            self.hdir = "left"
        if key[pygame.K_RIGHT]:
            self.xVelocity += self.speed
            self.hdir = "right"
        if key[pygame.K_SPACE]:

            resDictY = self.checkY()
            if resDictY["isGround"]:
                self.yVelocity -= 20


    def checkY(self):
        # круглое отрицательное число ;)
        resDict = {'isGround': False, 'deltaY': 15}
        ybottom = self.y + self.rect.height

        deltaY = 65

        lstcollide = pygame.sprite.spritecollide(self, grounds, False)
        for elemcolground in lstcollide:
            
            # из всех колиженов берем только "горизонтальные"
            if elemcolground.rect.y <= ybottom and (self.rect.centery < elemcolground.rect.top):
                elemcolground.image.fill(BLUE)
                resDict['isGround'] = True
                #print("       delta", ybottom, "   ", elemcolground.rect.y)
                if (ybottom - elemcolground.rect.y) <= resDict['deltaY']:
                    deltaY = ybottom - elemcolground.rect.y
                    resDict['deltaY'] = elemcolground.rect.y + 1
                    
        #print("       ", resDict)
        return resDict

    def checkX(self):
        resDict = {'isBlock': False, 'deltaX': 0}

        ybottom = self.y + self.rect.height
        lstcollide = pygame.sprite.spritecollide(self, grounds, False)
        for elemcolground in lstcollide:
           

            # из всех колиженов берем только "вертикальные"
            if ( self.rect.bottom - elemcolground.rect.top) >= 2:
                print("coltop=", elemcolground.rect.top, "    sprbottm=", self.rect.bottom)
                elemcolground.image.fill(YELLOW)
                resDict['isBlock'] = True
                #print("       delta", ybottom, "   ", elemcolground.rect.y)
                # помеха слева
                if (elemcolground.rect.right - self.rect.left) > 0:
                    elemcolground.image.fill(YELLOW)
                    #resDict['deltaX']
                    #deltaY = ybottom - elemcolground.rect.y
                    #resDict['deltaX'] = elemcolground.rect.y + 1
                
                # помеха справа
                if (self.rect.right - elemcolground.rect.right) > 0:
                    elemcolground.image.fill(ORANGE)

                    
        #print(resDict)
        return resDict

            
    def move(self, dt):
        #print("Начало  MOVE")
        #print("     velos=", self.yVelocity, "   self.y=", self.y)

        oldx = self.x
        oldy = self.y
        #print("     oldy=", oldy)

        self.x += self.xVelocity
        self.y += self.yVelocity

        #print("     self.y=", self.y)

        self.rect.x = self.x
        self.rect.y = self.y

        for elemground in grounds:
            elemground.image.fill(GREEN)

        resDictY = self.checkY()
        if resDictY["isGround"]:
            
            self.y = resDictY["deltaY"] - self.rect.height
            self.rect.y = self.y
            self.yVelocity = 0

        if self.yVelocity < self.jumpCount and not resDictY["isGround"]: 
            self.yVelocity += self.gravity
    
        #print("     velos=", self.yVelocity, "   self.y=", self.y)
        
        resDictX = self.checkX()
        if resDictX["isBlock"]:
            self.x = resDictX["deltaX"] - self.rect.width
            self.rect.x = self.x
            self.xVelocity = 0

        # рабочий фрагмент
        if self.xVelocity != 0 and not resDictX["isBlock"]:
            self.xVelocity /= 70*dt

        #print("Конец MOVE\n\n")
        
    def update(self):
        self.rect = pygame.Rect(self.x, self.y, 48, 64)

# Цикл игры

all_sprites = pygame.sprite.Group()
grounds = pygame.sprite.Group()

MyHero = Hero(200, 200)
all_sprites.add(MyHero)


for i in range(0, 20):
    ground = Ground(i * 64, hscene - 64)
    grounds.add(ground)

gr1 = Ground(0, hscene - 128)
gr3 = Ground(0, hscene - 192)
gr4 = Ground(0, hscene - 256)
gr2 = Ground(wscene // 2, hscene - 128)
grounds.add(gr1)
grounds.add(gr2)
grounds.add(gr3)
grounds.add(gr4)



lpause = False
running = True
while running:
    # Ввод процесса (события)
    clock.tick(fps)
    dt = clock.tick(60)/1000

    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
            
            if event.key == pygame.K_p:
                lpause = True
           
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_p:
                lpause = False


    # Рендеринг
    
    scene.fill(BLUE)
    grounds.draw(scene)

    
    
    MyHero.getKeys()
    if not lpause:
        MyHero.move(dt)
    
    all_sprites.update()
    all_sprites.draw(scene)
    
    # После отрисовки всего, переворачиваем экран
    pygame.display.update()


pygame.quit()
