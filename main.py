import pygame
pygame.init()
from random import randint
import time
import math

# settings
FPS = 60
jump = 0
lvl = 4
score = 0
a = 1
music = 1
CanJump = True
Open = False
On = False

clock = pygame.time.Clock()

wind_w, wind_h = 700, 500
window = pygame.display.set_mode((wind_w , wind_h))
pygame.display.set_caption("Centauri Travels")

bg = pygame.image.load("bg.jfif")
bg = pygame.transform.scale(bg, (wind_w, wind_h))

pygame.mixer.music.load("music.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)
coin_sound =  pygame.mixer.Sound("coin_sound.mp3")

class Sprite:
    def __init__(self , x , y , w , h, img):
        self.img = img
        self.rect = pygame.Rect(x, y, w, h)
        self.img = pygame.transform.scale(self.img , (w, h))
    
    def draw(self):
        window.blit(self.img , (self.rect.x, self.rect.y))
        
class Player(Sprite):
    def __init__(self , x , y , w , h , img1, img2 , speed, jumpforce, images):
        super().__init__(x, y, w, h, img1)
        self.img_r = self.img
        self.img_l = pygame.transform.scale(img2, (w, h))
        self.speed = speed
        self.jumpforce = jumpforce
        self.images = []
        for im in images:
            im = pygame.transform.scale(im, (w, h))
            self.images.append(im)
        self.state = "idle"
        self.im_num = 0
        self.anim_timer = 10
        #print(self.images)
    
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

        if keys[pygame.K_a] or keys[pygame.K_d]:
            self.state = "walk"
        else:
            self.state = "idle"
        
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
    
    def animate(self):
        if self.anim_timer == 0:
            if self.state == "walk":
                if self.im_num > 4 or self.im_num < 2:
                    self.im_num = 2
            elif self.state == "idle":
                if self.im_num > 1:
                    self.im_num = 0
            self.image = self.images[self.im_num]
            self.im_num += 1
            self.anim_timer = 10
        else:
            self.anim_timer -= 1
            # print(self.state)
    
    def fire(self, pos):
        bullets.append(Bullet(self.rect.centerx - 13,self.rect.y, 10, 10, pygame.image.load("bullet.png"), 15, pos))

class Enemy(Sprite):
    def __init__(self , x , y , w , h , img1 , speed):
        super().__init__(x, y, w, h, img1)
        self.speed = speed
    
    def move(self):
        self.rect.x += self.speed
        if self.rect.x > 500 or self.rect.x < 300:
            self.speed *= -1

class Laser(Sprite):
    def __init__(self , x , y , w , h , img1 , delay):
        super().__init__(x, y, w, h, img1)
        self.delay = delay
    
    def anim(self):
        global a
        a = randint(1, 7)
        if cur_time%self.delay != 0:
            self.img = pygame.image.load(f"Lasers/Laser{a}.png")
            self.img = pygame.transform.scale(self.img, (self.rect.w, self.rect.h))
        else:
            self.img = pygame.image.load("Lasers/Laser_off.png")
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
        global On
        if On == True:
            if self.type == "horisontal":
                self.rect.x += self.speed
                if self.rect.x >= self.x2 or self.rect.x <= self.x1:
                    self.speed *= -1
            elif self.type == "vertical":
                self.rect.y += self.speed
                if self.rect.y >= self.y2 or self.rect.y <= self.y1:
                    self.speed *= -1

class Portal(Sprite):
    def __init__(self, x, y, w, h, img, pair):
        super().__init__(x, y, w, h, img)
        self.pair = pair
    
    def teleport(self):
        player.rect.x = self.pair.rect.x
        player.rect.y = self.pair.rect.y

class Bullet(Sprite):
    def __init__(self, x, y, w, h, image, speed, pos):
        super().__init__(x, y, w, h, image)
        self.speed = speed
        v1 = pygame.Vector2(x, y)
        v2 = pygame.Vector2(pos[0], pos[1])
        v3 = v2 - v1
        self.vect = v3.normalize()

    def move(self):
        self.rect.x += self.vect[0] * self.speed
        self.rect.y += self.vect[1] * self.speed
        if self.rect.bottom <= 0 or self.rect.y > wind_h or self.rect.right <= 0 or self.rect.x > wind_w:
            bullets.remove(self)
        
images = [pygame.image.load("pl_anim/Player_idle1.png"), pygame.image.load("pl_anim/Player_idle2.png"), pygame.image.load("pl_anim/Player_walk1.png"), pygame.image.load("pl_anim/Player_walk2.png"), pygame.image.load("pl_anim/Player_walk3.png")]        

p_img1 = pygame.image.load("pl_anim/Player_idle1.png")
p_img2 = pygame.transform.flip(p_img1, True, False)
plat_img = pygame.image.load("platform.png")
enemy_img = pygame.image.load("enemy.png")
door_img = pygame.image.load("door.png")
key_img = pygame.image.load("key.png")
laser_off_img = pygame.image.load("Lasers/Laser_off.png")
coin_img = pygame.image.load("coin.png")

player = Player(50, 400, 30, 50, p_img1, p_img2, 5, 20, images)
ground = Sprite(0, wind_h-50, wind_w, 50, plat_img)
start = Sprite(50, 400, 20, 50, pygame.image.load("Portal.png"))
finish = Sprite(150, 90, 20, 50, pygame.image.load("Portal.png"))
key = Sprite(500, 150, 100, 30, pygame.image.load("key.png"))
door = Sprite(150, 120, 25, 100, pygame.image.load("door.png"))
enemy_lvl2 = Enemy(300, 10000, 70, 30, enemy_img, 2)
play_btn = Sprite(wind_w/2-70, wind_h/2-50, 140, 100, pygame.image.load("Play_btn.png"))
menu_btn = Sprite(wind_w-60, 0, 60, 30, pygame.image.load("Menu_btn.png"))
lift = Lift(100, 30, plat_img, 3, 570, 570, 70, 410, "vertical")
lift2 = Lift(100, 30, plat_img, 3, 570, 570, 70, 304, "vertical")
btn = Sprite(391, 333, 30, 30, pygame.image.load("button.png"))
logo = Sprite(156, 67, 400, 70, pygame.image.load("logo.png"))

plats_lvl1 = [Sprite(480, 298, 100, 30, plat_img),
              Sprite(290, 206, 100, 30, plat_img),
              Sprite(125, 134, 100, 30, plat_img)]

plats_lvl2 = [Sprite(292, 296, 100, 30, plat_img),
              Sprite(483, 206, 100, 30, plat_img),
              Sprite(0, 202, 227, 30, plat_img),
              Sprite(0, 0, 227, 132, plat_img)]

plats_lvl3 = [Sprite(0, 0, wind_w, wind_h-150, plat_img)]

plats_lvl4 = [Sprite(362, 366, 100, 20, plat_img),
              Sprite(0, 96, 486, 25, plat_img)]

plats_lvl5 = [Sprite(190, 379, 100, 20, plat_img),
              Sprite(549, 346, 200, 25, plat_img)]

bullets = []

coins = [Sprite(142, 400, 25, 25, coin_img),
         Sprite(245, 400, 25, 25, coin_img),
         Sprite(344, 400, 25, 25, coin_img),
         Sprite(451, 400, 25, 25, coin_img),
         Sprite(545, 400, 25, 25, coin_img)]

font = pygame.font.SysFont("Century Gothic", 20)
big_font = pygame.font.SysFont("Century Gothic", 40)



portal2 = Portal(283, 256, 20, 50, pygame.image.load("Portal.png"), None)
portal1 = Portal(105, 256, 20, 50, pygame.image.load("Portal.png"), None)

portal2.pair = portal1
portal1.pair = portal2

# lasers_lvl3 = [Laser(133, 350, 20, 100, pygame.image.load("Laser1.png"), 2),
#                Laser(224, 350, 20, 100, pygame.image.load("Laser1.png"), 2),
#                Laser(367, 350, 20, 100, pygame.image.load("Laser1.png"), 2),
#                Laser(513, 350, 20, 100, pygame.image.load("Laser1.png"), 2)]

def reset():
    global Open, On
    player.rect.x = start.rect.x
    player.rect.y = start.rect.y
    Open = False
    On = False

start_time = time.time()
cur_time = start_time

game = True
menu = True
while game:
    mus = Sprite(21, 17, 100, 60, pygame.image.load(f"music{music}.png"))
    window.blit(bg, (0, 0))
    if not menu:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        score_txt = font.render(f"Coins: {score}", True, (200, 255, 200))
        window.blit(score_txt, (0, 0))
        lvl_txt = big_font.render(f"Level {lvl}", True, (200, 255, 200))
        window.blit(lvl_txt, (263, 214))
        
        new_time = time.time()
        cur_time = int(new_time - start_time)
        for coin in coins:
            coin.draw()
            if player.rect.colliderect(coin.rect):
                coin_sound.play(1)
                coins.remove(coin)
                score += 1
        lift.draw()
        lift.move()
        player.draw()
        player.move()
        player.animate()
        menu_btn.draw()
        ground.draw()
        start.draw()
        finish.draw()
        btn.draw()
        player.rect.y -= jump
        
        for b in bullets:
            b.draw()
            b.move()
        
        if player.rect.colliderect(finish.rect):
            lvl += 1
            print(lvl)
            reset()
        
        if player.rect.colliderect(enemy_lvl2.rect):
            reset()
        
        if player.rect.colliderect(btn.rect):
            On = True
            
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
            finish.rect.y = 125
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
            finish.rect.x = wind_w - 100
            finish.rect.y = 400
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
            # for l in lasers_lvl3:
            #     l.draw()
            #     l.anim()
            #     if player.rect.colliderect(l.rect):
            #         if l.img == laser_off_img:
            #             print("hhhh")
            #         else:
            #             reset()
        
        elif lvl == 4:
            finish.rect.x = 44
            finish.rect.y = 21
            for plat in plats_lvl4:
                plat.draw()
                if plat.rect.colliderect(player.rect) or player.rect.colliderect(lift.rect):
                    if jump >= 0:
                        jump = 1
                        player.rect.y += 15
                    elif jump < 0:
                        CanJump = False
                        while plat.rect.colliderect(player.rect):
                            player.rect.y -= 1
                        CanJump = True
        
        elif lvl == 5:
            finish.rect.x = 44
            finish.rect.y = 21
            for plat in plats_lvl5:
                plat.draw()
                if plat.rect.colliderect(player.rect) or player.rect.colliderect(lift.rect):
                    if jump >= 0:
                        jump = 1
                        player.rect.y += 15
                    elif jump < 0:
                        CanJump = False
                        while plat.rect.colliderect(player.rect):
                            player.rect.y -= 1
                        CanJump = True

                portal1.draw()
                portal2.draw()
                if player.rect.colliderect(portal1.rect):
                    #portal1.teleport()
                    jump = 0
                    player.rect.x = portal2.rect.x - 30
                    player.rect.y = portal2.rect.y
                elif player.rect.colliderect(portal2.rect):
                    #portal2.teleport()
                    jump = 0
                    player.rect.x = portal1.rect.x - 30
                    player.rect.y = portal1.rect.y
    if music == 0:
        pygame.mixer.music.pause()
    else:
        pygame.mixer.music.unpause()
    
    if menu:
        play_btn.draw()
        mus.draw()
        logo.draw()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if event.button == 1:
                pos = event.pos
                player.fire(pos)
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