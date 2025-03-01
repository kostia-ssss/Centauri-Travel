import pygame
pygame.init()
from random import randint
import time

# settings
FPS = 60
jump = 0
lvl = 1
a = 1
music = 1
CanJump = True
Open = False

clock = pygame.time.Clock()

wind_w, wind_h = 700, 500
window = pygame.display.set_mode((wind_w , wind_h))
pygame.display.set_caption("Centauri Travels")

bg = pygame.image.load("bg.jfif")
bg = pygame.transform.scale(bg, (wind_w, wind_h))

pygame.mixer.music.load("music.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

class Sprite:
    def __init__(self , x , y , w , h, img):
        self.img = img
        self.rect = pygame.Rect(x, y, w, h)
        self.img = pygame.transform.scale(self.img , (w, h))
    
    def draw(self):
        window.blit(self.img , (self.rect.x, self.rect.y))
        
class Player(Sprite):
    def __init__(self , x , y , w , h , img1, img2 , speed, jumpforce):
        super().__init__(x, y, w, h, img1)
        self.img_r = self.img
        self.img_l = pygame.transform.scale(img2, (w, h))
        self.speed = speed
        self.speed = speed
        self.jumpforce = jumpforce
    
    def move(self):
        global jump, CanJump
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.img = self.img_l
            if self.rect.x > 0:
                self.rect.x -= self.speed
                # if any(self.rect.colliderect(p.rect) for p in plats_lvl2) or self.rect.colliderect(door.rect):
                #     self.rect.x += self.speed
        if keys[pygame.K_d]:
            self.img = self.img_r
            if self.rect.right < wind_w:
                self.rect.x += self.speed
                # if any(self.rect.colliderect(p.rect) for p in plats_lvl2) or self.rect.colliderect(door.rect):
                #     self.rect.x -= self.speed
        
        if keys[pygame.K_SPACE] and CanJump == True:
            jump = self.jumpforce
            CanJump = False
        elif self.rect.colliderect(ground.rect):
            jump = 0
            CanJump = True
            while self.rect.colliderect(ground.rect):
                self.rect.y -= 1
        else:
            jump -= 1

class Enemy(Sprite):
    def __init__(self , x , y , w , h , img1 , speed):
        super().__init__(x, y, w, h, img1)
        self.speed = speed
    
    def move(self):
        self.rect.x += self.speed
        if self.rect.x > 500 or self.rect.x < 300:
            self.speed *= -1

class Laser(Enemy):
    def __init__(self , x , y , w , h , img1 , delay):
        super().__init__(x, y, w, h, img1, 0)
        self.delay = delay
    
    def anim(self):
        global a
        a = randint(1, 7)
        if cur_time%self.delay != 0:
            self.img = pygame.image.load(f"Laser{a}.png")
            self.img = pygame.transform.scale(self.img, (self.rect.w, self.rect.h))
        else:
            self.img = pygame.image.load("Laser_off.png")
            self.img = pygame.transform.scale(self.img, (self.rect.w, self.rect.h))

class Lift(Sprite):
    def __init__(self, w, h, img, speed, x1, x2, y1, y2, type):
        super().__init__(x1, y1, w, h, img)
        self.speed = speed
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.type = type
    
    def move(self):
        if self.type == "horisontal":
            self.rect.x += self.speed
            if self.rect.x >= self.x2 or self.rect.x <= self.x1:
                self.speed *= -1
        elif self.type == "vertical":
            self.rect.y += self.speed
            if self.rect.y >= self.y2 or self.rect.y <= self.y1:
                self.speed *= -1
        
p_img1 = pygame.image.load("Player_idle.png")
p_img2 = pygame.transform.flip(p_img1, True, False)
plat_img = pygame.image.load("platform.png")
enemy_img = pygame.image.load("enemy.png")
door_img = pygame.image.load("door.png")
key_img = pygame.image.load("key.png")
laser_off_img = pygame.image.load("Laser_off.png")

player = Player(50, 400, 30, 50, p_img1, p_img2, 5, 20)
ground = Sprite(0, wind_h-50, wind_w, 50, plat_img)
start = Sprite(50, 400, 20, 50, pygame.image.load("Portal.png"))
finish = Sprite(150, 90, 20, 50, pygame.image.load("Portal.png"))
key = Sprite(500, 150, 100, 30, pygame.image.load("key.png"))
door = Sprite(150, 120, 25, 100, pygame.image.load("door.png"))
enemy_lvl2 = Enemy(300, 10000, 70, 30, enemy_img, 2)
play_btn = Sprite(wind_w/2-70, wind_h/2-50, 140, 100, pygame.image.load("Play_btn.png"))
menu_btn = Sprite(wind_w-60, 0, 60, 30, pygame.image.load("Menu_btn.png"))
lift = Lift(100, 30, plat_img, 3, 0, 500, 0, 0, "horisontal")

plats_lvl1 = [Sprite(480, 298, 100, 30, plat_img),
              Sprite(290, 206, 100, 30, plat_img),
              Sprite(125, 134, 100, 30, plat_img)]
plats_lvl2 = [Sprite(292, 296, 100, 30, plat_img),
              Sprite(483, 206, 100, 30, plat_img),
              Sprite(0, 202, 227, 30, plat_img),
              Sprite(0, 0, 227, 132, plat_img)]
plats_lvl3 = [Sprite(0, 0, wind_w, wind_h-150, plat_img)]

lasers_lvl3 = [Laser(133, 350, 20, 100, pygame.image.load("Laser1.png"), 2),
               Laser(224, 350, 20, 100, pygame.image.load("Laser1.png"), 2),
               Laser(367, 350, 20, 100, pygame.image.load("Laser1.png"), 2),
               Laser(513, 350, 20, 100, pygame.image.load("Laser1.png"), 2)]

def reset():
    global Open
    player.rect.x = start.rect.x
    player.rect.y = start.rect.y
    Open = False

start_time = time.time()
cur_time = start_time

game = True
menu = True
while game:
    mus = Sprite(21, 17, 100, 60, pygame.image.load(f"music{music}.png"))
    window.blit(bg, (0, 0))
    if not menu:
        new_time = time.time()
        cur_time = int(new_time - start_time)
        
        lift.draw()
        lift.move()
        player.draw()
        player.move()
        menu_btn.draw()
        ground.draw()
        start.draw()
        finish.draw()
        player.rect.y -= jump
        
        if player.rect.colliderect(finish.rect):
            lvl += 1
            print(lvl)
            reset()
        
        if player.rect.colliderect(enemy_lvl2.rect):
            reset()
            
        if lvl == 1:
            for plat in plats_lvl1:
                plat.draw()
                if plat.rect.colliderect(player.rect):
                    if jump >= 0:
                        jump = 1
                        player.rect.y += 15
                    elif jump < 0:
                        CanJump = False
                        while plat.rect.colliderect(player.rect):
                            player.rect.y -= 1
                        CanJump = True
        elif lvl == 2:
            if Open == False:
                door.draw()
                key.draw()
            finish.rect.x = 110
            finish.rect.y = 120
            for plat in plats_lvl2:
                plat.draw()
                if plat.rect.colliderect(player.rect):
                    if jump >= 0:
                        jump = 1
                        player.rect.y += 15
                    elif jump < 0:
                        CanJump = False
                        while plat.rect.colliderect(player.rect):
                            player.rect.y -= 1
                        CanJump = True
            
            enemy_lvl2.rect.y = 420
            enemy_lvl2.draw()
            enemy_lvl2.move()
            if player.rect.colliderect(key.rect):
                Open = True
        elif lvl == 3:
            for plat in plats_lvl3:
                plat.draw()
                if plat.rect.colliderect(player.rect):
                    if jump >= 0:
                        jump = 1
                        player.rect.y += 15
                    elif jump < 0:
                        CanJump = False
                        while plat.rect.colliderect(player.rect):
                            player.rect.y -= 1
                        CanJump = True
            for l in lasers_lvl3:
                l.draw()
                l.anim()
                if player.rect.colliderect(l.rect):
                    if l.img == laser_off_img:
                        print("hhhh")
                    else:
                        reset()
    
    if music == 0:
        pygame.mixer.music.pause()
    else:
        pygame.mixer.music.unpause()
    
    if menu:
        play_btn.draw()
        mus.draw()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            print(x)
            print(y)
            if play_btn.rect.collidepoint(x, y):
                menu = False
            if menu_btn.rect.collidepoint(x, y):
                menu = True
            if mus.rect.collidepoint(x, y):
                if music == 0:
                    music = 1
                else:
                    music = 0
    pygame.display.update()
    clock.tick(FPS)
pygame.quit()