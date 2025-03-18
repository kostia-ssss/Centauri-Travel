# importing
import pygame
pygame.init()
from random import randint
import time
import json

# settings
FPS = 60
a = 1
i = 1
music = 1
patrons = 70
Open = False
On = False
EnemyAlive = True
BossAlive = True
Dangerous = True
CanBuyYellow = False
CanBuyWhite = False
CanBuyGreen = False
CanBuyPurple = False
CanBuyTurquoise = False
PlayHistory = False
CPBS = True

# loading
try:
    with open("data.json", "r", encoding="utf-8") as file:
        data = json.load(file)
except:
    with open("data.json", "w", encoding="utf-8") as file:
        data = {"coins": 8, "lvl": 6, "costume": "Player", "costumes": {"Player": "Yes", "Yellow": "No", "White": "No", "Green": "No", "Purple": "No", "Turquoise": "No"}, "music": "No"}
        json.dump(data, file)

lvl = data["lvl"]
score = data["coins"]
costume = data["costume"]
if data["music"] == "Yes":
    music = 1
else:
    music = 0

# creating window and background
clock = pygame.time.Clock()

wind_w, wind_h = 700, 500
window = pygame.display.set_mode((wind_w , wind_h))
pygame.display.set_caption("Centauri Travels")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

bg = pygame.image.load("bg.jfif")
bg = pygame.transform.scale(bg, (wind_w, wind_h))

# music
pygame.mixer.music.load("music.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)
coin_sound = pygame.mixer.Sound("coin_sound.mp3")
boss_sound = pygame.mixer.Sound("boss_sound.mp3")

# classes
class Sprite:
    def __init__(self , x , y , w , h, img):
        self.img = img
        self.rect = pygame.Rect(x, y, w, h)
        self.img = pygame.transform.scale(self.img , (w, h))
    
    def draw(self):
        window.blit(self.img , (self.rect.x, self.rect.y))
        
class Player(Sprite):
    def __init__(self , x , y , w , h , img1, img2 , speed, jumpforce, imgs, yel_imgs, wht_imgs, turq_imgs, purp_imgs, grn_imgs):
        super().__init__(x, y, w, h, img1)
        global costume
        self.img_r = self.img
        self.img_l = pygame.transform.scale(img2, (w, h))
        self.speed = speed
        self.jumpforce = jumpforce
        self.images = []
        self.imgs = imgs
        self.yel_imgs = yel_imgs
        self.wht_imgs = wht_imgs
        self.turq_imgs = turq_imgs
        self.purp_imgs = purp_imgs
        self.grn_imgs = grn_imgs
        self.jump_count = 10
        self.CanJump = True
        self.isJump = False
        self.isLift = False
        self.max_wait = 15
        self.wait = self.max_wait
        for im in imgs:
            im = pygame.transform.scale(im, (w, h))
            self.images.append(im)
        
        self.state = "stand"
        self.im_num = 0
        self.anim_timer = 10
    
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            # self.img = self.img_l
            if self.rect.x > 0:
                self.rect.x -= self.speed
                if self.check_collisions(plats):
                    self.rect.x += self.speed
        if keys[pygame.K_d]:
            # self.img = self.img_r
            if self.rect.right < wind_w:
                x, y = self.rect.x, self.rect.y
                self.rect.x += self.speed
                if self.check_collisions(plats):
                    self.rect.x, self.rect.y = x, y

        if keys[pygame.K_a] or keys[pygame.K_d]:
            self.state = "walk"
        else:
            self.state = "idle"
    
    def jumping(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.CanJump:
            self.isJump = True
            self.jump_count = self.jumpforce
            self.CanJump = False
        if self.isJump:
            x, y = self.rect.x, self.rect.y
            self.rect.y -= self.jump_count
            self.jump_count -= 1
            if self.jump_count <= 0:
                self.isJump = False
            if self.check_collisions(plats):
                self.rect.x, self.rect.y = x, y
        else:
            x, y = self.rect.x, self.rect.y
            self.rect.y += 10
            if self.check_collisions(plats) or self.rect.colliderect(lift.rect):
                self.CanJump = True
                self.rect.x, self.rect.y = x, y
            if self.rect.colliderect(lift.rect):
                self.isLift = True
            if self.isLift:
                if not self.isJump:
                    self.rect.bottom = lift.rect.y
                self.isLift = False
            
    
    def check_collisions(self, plats):
        if any(self.rect.colliderect(plat.rect) for plat in plats):
            return True
        else:
            return False

    def change_costume(self):
        if costume == "Player":
            imgs = self.imgs
        if costume == "Yellow":
            imgs = self.yel_imgs
        if costume == "White":
            imgs = self.wht_imgs
        if costume == "Turquoise":
            imgs = self.turq_imgs
        if costume == "Green":
            imgs = self.grn_imgs
        if costume == "Purple":
            imgs = self.purp_imgs
        
        for im in imgs:
            im = pygame.transform.scale(im, (self.rect.w, self.rect.h))
            imgs.append(im)
            imgs.pop(0)

        return imgs
    
    def animate(self, imgs):
        if self.anim_timer == 0:
            if self.state == "walk":
                if self.im_num > 2 or self.im_num < 1:
                    self.im_num = 1
            elif self.state == "idle":
                if self.im_num > 0:
                    self.im_num = 0
            self.img = imgs[self.im_num]
            self.im_num += 1
            self.anim_timer = 10
        else:
            self.anim_timer -= 1
    
    def fire(self, pos):
        global patrons
        if self.wait == 0:
            bullets.append(Bullet(self.rect.centerx - 13,self.rect.y, 10, 10, pygame.image.load("bullet.png"), 15, pos, "player"))
            self.wait = self.max_wait
            patrons -= 1
        else:
            self.wait -= 1
    
    def take_damage(self):
        global losing, hp
        if hp > 1:
            HP.pop(hp-1)
            hp -= 1
        else:
            losing = True

class Enemy(Sprite):
    def __init__(self , x , y , w , h , img1 , speed):
        super().__init__(x, y, w, h, img1)
        self.speed = speed
    
    def move(self):
        self.rect.x += self.speed
        if self.rect.x > 500 or self.rect.x < 300:
            self.speed *= -1

class UltraEnemy(Sprite):
    def __init__(self , x , y , w , h , img1 , hor_speed, vert_speed, len1, len2):
        super().__init__(x, y, w, h, img1)
        self.speed = hor_speed
        self.hor_speed = hor_speed
        self.vert_speed = vert_speed
        self.len1 = len1
        self.len2 = len2
        self.dx = 0
        self.dy = 0
        self.hor = True
        self.vert = False
    
    def move(self):
        if self.hor:
            self.rect.x += self.hor_speed
            self.dx += abs(self.hor_speed)
            if self.dx > self.len1:
                self.vert = True
                self.hor = False
                self.hor_speed *= -1
                self.dx = 0
        if self.vert:
            self.rect.y += self.vert_speed
            self.dy += abs(self.vert_speed)
            if self.dy > self.len2:
                self.vert = False
                self.hor = True
                self.vert_speed *= -1
                self.dy = 0

class Laser(Sprite):
    def __init__(self , x , y , w , h , img1 , delay):
        super().__init__(x, y, w, h, img1)
        self.delay = delay
    
    def anim(self):
        global a, Dangerous
        a = randint(1, 7)
        if cur_time%self.delay != 0:
            self.img = pygame.image.load(f"Lasers/Laser{a}.png")
            Dangerous = True
            self.img = pygame.transform.scale(self.img, (self.rect.w, self.rect.h))
        else:
            self.img = pygame.image.load("Lasers/Laser_off.png")
            Dangerous = False
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
    def __init__(self, x, y, w, h, image, speed, pos, type):
        super().__init__(x, y, w, h, image)
        self.speed = speed
        self.type = type
        v1 = pygame.Vector2(x, y)
        v2 = pygame.Vector2(pos[0], pos[1])
        v3 = v2 - v1
        self.vect = v3.normalize()

    def move(self):
        global hp, losing
        self.rect.x += self.vect[0] * self.speed
        self.rect.y += self.vect[1] * self.speed
        if self.type == "player":
            if self.rect.bottom <= 0 or self.rect.y > wind_h or self.rect.right <= 0 or self.rect.x > wind_w:
                bullets.remove(self)   
        elif self.type == "boss":
            if self.rect.colliderect(player.rect):
                player.take_damage()
            
            if self.rect.colliderect(player.rect) or any(self.rect.colliderect(plat.rect) for plat in plats):
                Bbullets.remove(self)

class Boss(Sprite):
    def __init__(self, x, y, w, h, img, speed):
        super().__init__(x, y, w, h, img)
        self.CanFire = False
        self.max_wait = 50
        self.wait = self.max_wait
        self.speed = speed
        self.hp = 10
    
    def move(self):
        self.rect.x += self.speed
            
        if self.rect.right >= wind_w or self.rect.left <= 0:
            self.speed *= -1
    
    def check_player_pos(self):
        if self.wait == 0:
            self.CanFire = True
            self.wait = self.max_wait
        else:
            self.CanFire = False
            self.wait -= 1
        
        if self.CanFire:
            self.player_x, self.player_y = player.rect.centerx, player.rect.centery
            pl_pos = [self.player_x, self.player_y]
            return pl_pos
    
    def shooting_player(self, pos):
        if pos != None:
            Bbullets.append(Bullet(self.rect.centerx, self.rect.centery, 25, 25, pygame.image.load("Bbullet.png"), 5, pos, "boss"))
    
    def take_damage(self):
        global BossAlive
        if hp > 1:
            self.hp -= 1
        else:
            BossAlive = False

# loading images
p_img1 = pygame.image.load("pl_anim/Player_idle1.png")
p_img2 = pygame.transform.flip(p_img1, True, False)
plat_img = pygame.image.load("platform.png")
enemy_img = pygame.image.load("enemy.png")
door_img = pygame.image.load("door.png")
key_img = pygame.image.load("key.png")
laser_off_img = pygame.image.load("Lasers/Laser_off.png")
coin_img = pygame.image.load("coin.png")

# lists of costumes
images = [pygame.image.load("pl_anim/Player_idle1.png"),
          pygame.image.load("pl_anim/Player_walk2.png"),
          pygame.image.load("pl_anim/Player_walk3.png")]

Wimages = [pygame.image.load("pl_anim/White_idle1.png"),
          pygame.image.load("pl_anim/White_walk2.png"),
          pygame.image.load("pl_anim/White_walk3.png")]

Yimages = [pygame.image.load("pl_anim/Yellow_idle1.png"),
          pygame.image.load("pl_anim/Yellow_walk2.png"),
          pygame.image.load("pl_anim/Yellow_walk3.png")]

Gimages = [pygame.image.load("pl_anim/Green_idle1.png"),
          pygame.image.load("pl_anim/Green_walk2.png"),
          pygame.image.load("pl_anim/Green_walk3.png")]

Timages = [pygame.image.load("pl_anim/Turquoise_idle1.png"),
          pygame.image.load("pl_anim/Turquoise_walk2.png"),
          pygame.image.load("pl_anim/Turquoise_walk3.png")]

Pimages = [pygame.image.load("pl_anim/Purple_idle1.png"),
          pygame.image.load("pl_anim/Purple_walk2.png"),
          pygame.image.load("pl_anim/Purple_walk3.png")]

# creating objects
player = Player(50, 400, 30, 50, p_img1, p_img2, 5, 20, images, Yimages, Wimages, Timages, Pimages, Gimages)
start = Sprite(50, 400, 20, 50, pygame.image.load("Portal.png"))
finish = Sprite(150, 90, 20, 50, pygame.image.load("Portal.png"))
key = Sprite(500, 150, 100, 30, pygame.image.load("key.png"))
door = Sprite(150, 120, 25, 100, pygame.image.load("door.png"))
enemy_lvl2 = Enemy(300, 10000, 70, 30, enemy_img, 2)
play_btn = Sprite(wind_w/2-70, wind_h/2-50, 140, 100, pygame.image.load("Play_btn.png"))
shop_btn = Sprite(wind_w/2-70, wind_h/2+100, 140, 100, pygame.image.load("Shop_btn.png"))
history_btn = Sprite(27, 280, 140, 100, pygame.image.load("History_btn.png"))
QTM_btn = Sprite(0, 0, 70, 50, pygame.image.load("Quit_to_menu_btn.png"))
menu_btn = Sprite(wind_w-60, 0, 60, 30, pygame.image.load("Menu_btn.png"))
lift1 = Lift(100, 30, plat_img, 3, 570, 570, 70, 410, "vertical")
lift2 = Lift(100, 30, plat_img, 1, 570, 570, 100, 304, "vertical")
btn = Sprite(391, 333, 30, 30, pygame.image.load("button.png"))
logo = Sprite(156, 67, 400, 70, pygame.image.load("logo.png"))
shop_shablon = Sprite(0, 0, wind_w, wind_h, pygame.image.load("shop.png"))
new_enemy = UltraEnemy(307, 260, 50, 50, pygame.image.load("New_enemy.png"), 10, 10, 150, 100)
close_btn = Sprite(wind_w-60, 30, 60, 30, pygame.image.load("Close_btn.png"))
boss = Boss(0, 0, 150, 100, pygame.image.load("boss.png"), 3)

hist1 = Sprite(0, 0, wind_w, wind_h, pygame.image.load("kat_scena/1.png"))
hist2 = Sprite(0, 0, wind_w, wind_h, pygame.image.load("kat_scena/2.png"))
hist3 = Sprite(0, 0, wind_w, wind_h, pygame.image.load("kat_scena/3.png"))
hist4 = Sprite(0, 0, wind_w, wind_h, pygame.image.load("kat_scena/4.png"))
hist5 = Sprite(0, 0, wind_w, wind_h, pygame.image.load("kat_scena/5.png"))

lift = lift1

buy_btn1 = Sprite(68, 209, 35, 25, pygame.image.load("buy_btn.png"))
buy_btn2 = Sprite(242, 207, 35, 25, pygame.image.load("buy_btn.png"))
buy_btn3 = Sprite(396, 214, 35, 25, pygame.image.load("buy_btn.png"))
buy_btn4 = Sprite(556, 197, 35, 25, pygame.image.load("buy_btn.png"))
buy_btn5 = Sprite(68, 436, 35, 25, pygame.image.load("buy_btn.png"))

buybtns = [buy_btn1, buy_btn2, buy_btn3, buy_btn4, buy_btn5]

plats = [Sprite(480, 298, 100, 30, plat_img),
        Sprite(290, 206, 100, 30, plat_img),
        Sprite(125, 134, 100, 30, plat_img),
        Sprite(0, wind_h-50, wind_w, 50, plat_img)]

bullets = []
Bbullets = []

HP = [Sprite(100, 0, 25, 25, pygame.image.load("heart.png")),
      Sprite(135, 0, 25, 25, pygame.image.load("heart.png")),
      Sprite(170, 0, 25, 25, pygame.image.load("heart.png"))]

coins = [Sprite(142, 400, 25, 25, coin_img),
         Sprite(245, 400, 25, 25, coin_img),
         Sprite(344, 400, 25, 25, coin_img),
         Sprite(451, 400, 25, 25, coin_img),
         Sprite(545, 400, 25, 25, coin_img)]

font = pygame.font.SysFont("Century Gothic", 20)
big_font = pygame.font.SysFont("Century Gothic", 40)
bold_font = pygame.font.SysFont("Century Gothic", 40, True)
small_font = pygame.font.SysFont("Century Gothic", 15)

tutorial_txt1 = small_font.render("Press A & D to move", True, (255, 255, 255))
tutorial_txt2 = small_font.render("Press SPACE to jump", True, (255, 255, 255))
tutorial_txt3 = small_font.render("Don't touch the enemy!", True, (255, 255, 255))
lose = bold_font.render("You lose(", True, (255, 0, 0))
reset_txt = bold_font.render("Press R to reset", True, (255, 255, 255))
tutorial_txt = tutorial_txt1

portal2 = Portal(283, 256, 20, 50, pygame.image.load("Portal.png"), None)
portal1 = Portal(105, 256, 20, 50, pygame.image.load("Portal.png"), None)

portal2.pair = portal1
portal1.pair = portal2

lasers_lvl3 = [Laser(133, 350, 20, 100, pygame.image.load("Lasers/Laser1.png"), 2),
               Laser(224, 350, 20, 100, pygame.image.load("Lasers/Laser1.png"), 2),
               Laser(367, 350, 20, 100, pygame.image.load("Lasers/Laser1.png"), 2),
               Laser(513, 350, 20, 100, pygame.image.load("Lasers/Laser1.png"), 2)]

def reset():
    global Open, On, EnemyAlive
    player.rect.x = start.rect.x
    player.rect.y = start.rect.y
    Open = False
    On = False
    EnemyAlive = True

def save_costume(costume):
    with open("data.json", "w", encoding="utf-8") as file:
        data["costume"] = costume
        json.dump(data, file)

def save():
    with open("data.json", "w", encoding="utf-8") as file:
        json.dump(data, file)

def draw_plats(list_of_plats):
    for plat in list_of_plats:
        plat.draw()

start_time = time.time()
cur_time = start_time

hp = len(HP)

# main loop
game = True
menu = True
shop = False
losing = False
while game:
    i += 1
    mus = Sprite(21, 17, 100, 60, pygame.image.load(f"music{music}.png"))
    window.blit(bg, (0, 0))
    if not menu and not losing:
        # player.img = pygame.image.load(f"pl_anim/{costume}_idle1.png")
        # player.img = pygame.transform.scale(player.img, (player.rect.w, player.rect.h))
        if patrons < 70:
            patrons += 0.01
        mouse_x, mouse_y = pygame.mouse.get_pos()
        score_txt = font.render(f"Coins: {score}", True, (200, 255, 200))
        window.blit(score_txt, (0, 0))
        p_txt = font.render(f"Patrons: {int(patrons)}", True, (170, 255, 200))
        window.blit(p_txt, (wind_w-180, 0))
        lvl_txt = big_font.render(f"Level {lvl}", True, (200, 255, 200))
        window.blit(lvl_txt, (263, 214))
        
        new_time = time.time()
        cur_time = new_time - start_time
        for coin in coins:
            coin.draw()
            if player.rect.colliderect(coin.rect):
                coin_sound.play(1)
                coins.remove(coin)
                score += 1
                
        window.blit(tutorial_txt, (122, 349))
        player.draw()
        player.move()
        player.jumping()
        imgs = player.change_costume()
        player.animate(imgs)
        menu_btn.draw()
        start.draw()
        finish.draw()
        if lvl > 3 and lvl < 6:
            btn.draw()
        
        for p in plats:
            p.draw()
        
        for b in bullets:
            b.draw()
            b.move()
            if b.rect.colliderect(new_enemy.rect) and EnemyAlive:
                EnemyAlive = False
                bullets.remove(b)
        
        if player.rect.colliderect(finish.rect):
            lvl += 1
            with open("data.json", "w", encoding="utf-8") as file:
                data["lvl"] = int(data["lvl"]) + 1
                json.dump(data, file)
            reset()
        
        if player.rect.colliderect(enemy_lvl2.rect):
            player.take_damage()
            reset()
        
        if player.rect.colliderect(btn.rect):
            On = True
            
        if lvl == 1:
            plats = [Sprite(480, 298, 100, 30, plat_img),
                    Sprite(290, 206, 100, 30, plat_img),
                    Sprite(125, 134, 100, 30, plat_img),
                    Sprite(0, wind_h-50, wind_w, 50, plat_img)]
            tutorial_txt = tutorial_txt1
            window.blit(tutorial_txt2, (357, 330))
        elif lvl == 2:
            plats = [Sprite(292, 296, 100, 30, plat_img),
                    Sprite(483, 206, 100, 30, plat_img),
                    Sprite(0, 202, 227, 30, plat_img),
                    Sprite(0, 0, 227, 132, plat_img),
                    Sprite(0, wind_h-50, wind_w, 50, plat_img)]
            tutorial_txt = tutorial_txt3
            if Open == False:
                door.draw()
                key.draw()
            finish.rect.x = 110
            finish.rect.y = 125
            
            enemy_lvl2.rect.y = 420
            enemy_lvl2.draw()
            enemy_lvl2.move()
            if player.rect.colliderect(key.rect):
                Open = True
            if player.rect.colliderect(door.rect) and not Open:
                player.rect.x += player.speed
        elif lvl == 3:
            plats = [Sprite(0, 0, wind_w, wind_h-150, plat_img),
                    Sprite(0, wind_h-50, wind_w, 50, plat_img)]
            finish.rect.x = wind_w - 100
            finish.rect.y = 400
            enemy_lvl2.rect.y = 10000
            for l in lasers_lvl3:
                l.draw()
                l.anim()
                if player.rect.colliderect(l.rect):
                    if Dangerous == False:
                        pass
                    else:
                        if hp > 1:
                            HP.pop(hp-1)
                            hp -= 1
                        else:
                            losing = True
                        reset()
        
        elif lvl == 4:
            plats = [Sprite(362, 366, 100, 20, plat_img),
                    Sprite(0, 96, 486, 25, plat_img),
                    Sprite(0, wind_h-50, wind_w, 50, plat_img)]
            finish.rect.x = 44
            finish.rect.y = 21
            lift = lift1
            lift.draw()
            lift.move()
        
        elif lvl == 5:
            plats = [Sprite(190, 379, 100, 20, plat_img),
                    Sprite(549, 346, 200, 25, plat_img),
                    Sprite(0, 150, 150, 20, plat_img),
                    Sprite(150, 0, 20, 170, plat_img),
                    Sprite(0, wind_h-50, wind_w, 50, plat_img)]
            finish.rect.x = 630
            finish.rect.y = 400
            portal2.rect.x = 26
            portal2.rect.y = 95
            key.rect.x = 570
            key.rect.y = 70
            door.rect.x = 594
            door.rect.y = 370
            btn.rect.x = 86
            btn.rect.y = 95
            lift = lift2
            
            lift.draw()
            lift.move()
            if Open == False:
                door.draw()
                key.draw()
            
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
                
            if player.rect.colliderect(key.rect):
                Open = True
        
        elif lvl == 6:
            plats = [Sprite(0, wind_h-50, wind_w, 50, plat_img),
                     Sprite(362, 266, 100, 20, plat_img),
                     Sprite(549, 346, 200, 25, plat_img)]
            door.rect.x = 594
            door.rect.y = 370
            finish.rect.x = 630
            finish.rect.y = 400
            if player.rect.colliderect(key.rect):
                Open = True
            
            if player.rect.colliderect(door.rect) and Open == False:
                player.rect.x -= player.speed
                
            if Open == False:
                door.draw()
                key.draw()
                
            if EnemyAlive:
                new_enemy.draw()
                new_enemy.move()
            
            if player.rect.colliderect(new_enemy.rect):
                if EnemyAlive:
                    player.take_damage()
                    reset()
                else:
                    pass
        
        elif lvl == 7:
            plats = [Sprite(0, wind_h-50, wind_w, 50, plat_img)]
            lvl_txt = bold_font.render("BOSS", True, (255, 0, 0))
            if CPBS:
                boss_sound.play()
                CPBS = False
            
            if BossAlive:
                finish.rect.x = 100000
            else:
                finish.rect.x = wind_w - 150
            
            if BossAlive:
                boss.draw()
                boss.move()
                pos_pl =  boss.check_player_pos()
                boss.shooting_player(pos_pl)
                for Bb in Bbullets:
                    Bb.draw()
                    Bb.move()
                if pos_pl != None:
                    print(pos_pl)
                for bul in bullets:
                    if boss.rect.colliderect(bul.rect):
                        boss.take_damage()
                        bullets.remove(bul)
                    

    
    if music == 0:
        pygame.mixer.music.pause()
        data["music"] = "No"
        save()
    else:
        pygame.mixer.music.unpause()
        data["music"] = "Yes"
        save()
    
    if score >= 5:
        CanBuyYellow = True
        save()
    if score >= 10:
        CanBuyWhite = True
        save()
    if score >= 15:
        CanBuyGreen = True
        save()
    if score >= 20:
        CanBuyPurple = True
        save()
    if score >= 25:
        CanBuyTurquoise = True
        save()
    
    for h in HP:
        if losing == False:
            h.draw()
    
    if menu:
        play_btn.draw()
        shop_btn.draw()
        history_btn.draw()
        mus.draw()
        logo.draw()
        close_btn.draw()
        score_txt = font.render(f"Coins: {score}", True, (200, 255, 200))
        window.blit(score_txt, (0, 0))
    
    if shop:
        shop_shablon.draw()
        QTM_btn.draw()
        for btn in buybtns:
            btn.draw()
    
    if losing:
        window.blit(lose, (200, 200))
        window.blit(reset_txt, (200, 300))
    
    if PlayHistory:
        print(i)
        if i < 100:
            hist1.draw()
        elif i >= 100 and i < 150:
            hist2.draw()
        elif i >= 150 and i < 200:
            hist3.draw()
        elif i >= 200 and i < 250:
            hist4.draw()
        elif i >= 250 and i < 300:
            hist5.draw()
        else:
            PlayHistory = False
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            costume = "Player"
            save_costume(costume)
        elif keys[pygame.K_2] and data["costumes"]["Yellow"] == "Yes":
            costume = "Yellow"
            save_costume(costume)
        elif keys[pygame.K_3] and data["costumes"]["White"] == "Yes":
            costume = "White"
            save_costume(costume)
        elif keys[pygame.K_4] and data["costumes"]["Green"] == "Yes":
            costume = "Green"
            save_costume(costume)
        elif keys[pygame.K_5] and data["costumes"]["Purple"] == "Yes":
            costume = "Purple"
            save_costume(costume)
        elif keys[pygame.K_6] and data["costumes"]["Turquoise"] == "Yes":
            costume = "Turquoise"
            save_costume(costume)
        elif keys[pygame.K_r] and losing == True:
            HP = [Sprite(100, 0, 25, 25, pygame.image.load("heart.png")),
                Sprite(135, 0, 25, 25, pygame.image.load("heart.png")),
                Sprite(170, 0, 25, 25, pygame.image.load("heart.png"))]
            losing = False
            hp = 3
        elif keys[pygame.K_s]:
            pos = pygame.mouse.get_pos()
            if patrons > 0 and not menu:
                player.fire(pos)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            print(x)
            print(y)
            if play_btn.rect.collidepoint(x, y):
                menu = False
            if QTM_btn.rect.collidepoint(x, y):
                shop = False
            if menu_btn.rect.collidepoint(x, y):
                menu = True
                with open("data.json", "w", encoding="utf-8") as file:
                    data["coins"] = int(data["coins"]) + (score-int(data["coins"]))
                    json.dump(data, file)
            if shop_btn.rect.collidepoint(x, y):
                shop = True
            if close_btn.rect.collidepoint(x, y):
                game = False
            
            if buy_btn1.rect.collidepoint(x, y) and CanBuyGreen == True:
                data["costumes"]["Green"] = "Yes"
            if buy_btn2.rect.collidepoint(x, y) and CanBuyPurple:
                data["costumes"]["Purple"] = "Yes"
            if buy_btn3.rect.collidepoint(x, y) and CanBuyYellow:
                data["costumes"]["Yellow"] = "Yes"
            if buy_btn4.rect.collidepoint(x, y) and CanBuyWhite:
                data["costumes"]["White"] = "Yes"
            if buy_btn5.rect.collidepoint(x, y) and CanBuyTurquoise:
                data["costumes"]["Turquoise"] = "Yes"
            
            if history_btn.rect.collidepoint(x, y):
                i = 0
                PlayHistory = True
            
            if mus.rect.collidepoint(x, y):
                if music == 0:
                    music = 1
                else:
                    music = 0
    pygame.display.update()
    clock.tick(FPS)
pygame.quit()