# імпортовані модулі та бібліотеки
import pygame
import os

# загальні налаштування
os.environ['SDL_VIDEO_WINDOW_POS'] = "20,0"
pygame.init()


# клас Налаштувань
class Settings():
    def __init__(self, display_w, display_h, texture_w, texture_h, display_color, ticks):
        self.directory = os.path.dirname(__file__)
        self.clock = pygame.time.Clock()
        self.ticks = ticks

        self.display_w = display_w
        self.display_h = display_h
        self.texture_w = texture_w
        self.texture_h = texture_h

        self.texture_start_x = 0
        self.texture_start_y = 0
        
        self.display = pygame.display.set_mode((self.display_w, self.display_h), pygame.NOFRAME)
        self.display_color = display_color
        
        self.game = True
        self.good_game = False
        self.end_game = False

        self.bullet_list = []

        self.alpha_color = 0
        self.end_background = pygame.Surface((display_w, display_h), pygame.SRCALPHA)

        self.back_music = pygame.mixer.music.load(self.directory + "/sounds/" + "back_music.mp3")
        self.shoot_sound = pygame.mixer.Sound(self.directory + "/sounds/" + "shoot.mp3")
        self.shoot_sound.set_volume(0.1)
        self.win_sound = pygame.mixer.Sound(self.directory + "/sounds/" + "win.mp3")
        self.death_sound = pygame.mixer.Sound(self.directory + "/sounds/" + "death_2.mp3")

        #self.start_music()
    
    def start_music(self):
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)

    def show_end(self):
        if self.alpha_color == 0:
            if self.good_game:
                self.win_sound.play()
            else:
                self.death_sound.play()
        if self.alpha_color < 255:
            self.alpha_color += 1
        self.end_background.fill((0,0,0, self.alpha_color))
        self.display.blit(self.end_background, (0,0))
        if self.good_game == True and self.alpha_color >= 30:
            good_text = Text("YOU WIN", (0, 255, 0), "Comic Sans MS", 100, self.display_w/2 - 240, self.display_h/2 - 50)
            good_text.draw()
        elif self.good_game == False and self.alpha_color >= 30:
            bad_text = Text("YOU LOSE", (255, 0, 0), "Comic Sans MS", 100, self.display_w/2 - 240, self.display_h/2 - 50)
            bad_text.draw()


# клас Тексту
class Text():
    def __init__(self, text, color, font_name, font_size, x, y):
        self.x = x
        self.y = y
        self.font = pygame.font.SysFont(font_name, font_size)
        self.text_render = self.font.render(text, True, color)

    def draw(self):
        settings.display.blit(self.text_render, (self.x, self.y))


# клас Гравця
class Player(): 
    def __init__(self, x, y, width, height, color, image, health_image, run_animation_name, run_animation_amount, health, speed=5):
        self.hitbox = pygame.Rect(x, y, width, height)
        self.color = color
        self.image = pygame.image.load(settings.directory + "/textures/" + image)
        
        self.health = health
        self.health_image_big = pygame.image.load(settings.directory + "/textures/" + health_image)
        self.health_image = pygame.transform.scale(self.health_image_big, (35, 35))
        
        self.go_left = False
        self.go_right = False
        self.go_up = False
        self.go_down = False
        self.speed = speed
        
        self.keys = 0

        self.direction = "R"
        self.run_animation_name = run_animation_name
        self.run_animation_amount = run_animation_amount
        self.run_animation_r_images = [] 
        self.run_animation_l_images = []
        
        self.animation_tick = 0 
        self.animation_limit = settings.ticks
        self.animation_number = 0
        self.create_run_animation()

        self.run_animation_now = self.run_animation_r_images

    def create_run_animation(self):
        for i in range(0, self.run_animation_amount): 
            temp_image = pygame.image.load(settings.directory + "/textures/" + self.run_animation_name + str(i) + ".png")  
            self.run_animation_r_images.append(temp_image)
            temp_l_image = pygame.transform.flip(temp_image, True, False)
            self.run_animation_l_images.append(temp_l_image)
         
    def draw_color(self):
        pygame.draw.rect(settings.display, self.color, self.hitbox)
        self.draw_health()

    def draw_image(self):
        settings.display.blit(self.run_animation_now[self.animation_number], self.hitbox)
        self.draw_health()

    def draw_health(self):
        x = 1445
        y = 25
        for hp in range(self.health):
            settings.display.blit(self.health_image, (x, y))
            y += 40

    def get_damage(self, death_type):
        self.health -= 1
        if self.health <= 0:
            self.die(death_type)

    def die(self, death_type):
        settings.end_game = True
        if death_type == "B":
            settings.death_sound = pygame.mixer.Sound(settings.directory + "/sounds/" + "death_2.mp3")
        else:
            settings.death_sound = pygame.mixer.Sound(settings.directory + "/sounds/" + "death_1.mp3")

    def exit(self):
        if self.keys >= 3:
            if self.hitbox.colliderect(level.door):
                settings.good_game = True
                settings.end_game = True

    def move(self):
        
        self.exit()

        if self.go_left == True:
           self.hitbox.x -= self.speed
        if self.go_right == True:
           self.hitbox.x += self.speed
        if self.go_up == True:
           self.hitbox.y -= self.speed
        if self.go_down == True:
           self.hitbox.y += self.speed

        for wall in level.wall_list:
            if self.hitbox.colliderect(wall.hitbox): 
                if self.hitbox.right >= wall.hitbox.left and self.hitbox.right <= wall.hitbox.left + self.speed:
                    self.hitbox.right = wall.hitbox.left
                if self.hitbox.left <= wall.hitbox.right and self.hitbox.left >= wall.hitbox.right - self.speed:
                    self.hitbox.left = wall.hitbox.right
                if self.hitbox.top <= wall.hitbox.bottom and self.hitbox.top >= wall.hitbox.bottom - self.speed:
                    self.hitbox.top = wall.hitbox.bottom
                if self.hitbox.bottom >= wall.hitbox.top and self.hitbox.bottom <= wall.hitbox.top + self.speed:
                    self.hitbox.bottom = wall.hitbox.top


# клас Ключа
class Key():
    def __init__(self, x, y, width, height, color, image):
        self.hitbox = pygame.Rect(x, y, width, height)
        self.color = color
        self.image = pygame.image.load(settings.directory + '/textures/' + image)

    def draw_color(self):
        pygame.draw.rect(settings.display, self.color, self.hitbox)

    def draw_image(self):
        settings.display.blit(self.image, self.hitbox)

    def take_key(self):
        if self.hitbox.colliderect(player.hitbox):
            self.hitbox.x = settings.display_w - 58
            if player.keys == 0: 
                self.hitbox.y = 205
            elif player.keys == 1:
                self.hitbox.y = 225
            elif player.keys == 2:
                self.hitbox.y = 245
            player.keys += 1


# клас Стіна
class Wall():
    def __init__(self, x, y, width, height, color, image):
        self.hitbox = pygame.Rect(x, y, width, height)
        self.color = color
        self.image = pygame.image.load(settings.directory + "/textures/" + image)

    def draw_color(self):
        pygame.draw.rect(settings.display, self.color, self.hitbox)

    def draw_image(self):
        settings.display.blit(self.image, self.hitbox)


# клас Куля
class Bullet():
    def __init__(self, x, y, width, height, color, image, speed, damage, bul_type, bul_direction):
        self.hitbox = pygame.Rect(x, y, width, height)
        self.color = color 
        self.image = pygame.image.load(settings.directory + "/textures/" + image)
        self.damage = damage 
        self.speed = speed 
        self.flied_distance = 0
        self.total_distance = speed * settings.ticks
        self.bul_type = bul_type
        self.bul_direction = bul_direction

    def draw_color(self):
        pygame.draw.rect(settings.display, self.color, self.hitbox)
    
    def draw_image(self):
        settings.display.blit(self.image, self.hitbox)

    def fly(self):
        if self.flied_distance < self.total_distance:
            if self.bul_direction == "L":
                self.hitbox.x -= self.speed
            if self.bul_direction == "R":
                self.hitbox.x += self.speed
            if self.bul_direction == "U":
                self.hitbox.y -= self.speed
            if self.bul_direction == "D":
                self.hitbox.y += self.speed

            self.flied_distance += self.speed
        else:
            settings.bullet_list.remove(self)

    def check_hit(self):
        for w in level.wall_list:
            if self.hitbox.colliderect(w.hitbox):
                settings.bullet_list.remove(self)
                break

        if self.hitbox.colliderect(player.hitbox) and self.bul_type == "bad":
            settings.bullet_list.remove(self)
            player.get_damage("B")           

        for enemy in level.enemy_list:
            if self.hitbox.colliderect(enemy.hitbox) and self.bul_type == "good":
                settings.bullet_list.remove(self)
                enemy.get_damage()
                break


# клас Рівень
class Level():
    def __init__(self, textures, start_x, start_y):
        self.wall_list = []
        self.texture_list = []
        self.kill_list = []
        self.enemy_list = []
        self.key_list = []
        self.door = None
        self.textures = textures
        self.start_x = start_x
        self.start_y = start_y

    def build_level(self):
        for row in self.textures:
            for element in row:
                if element == 1:
                    wall = Wall(settings.texture_start_x, settings.texture_start_y, settings.texture_w, settings.texture_h, (255,0,0), "wall_h_t.png")
                    level.wall_list.append(wall)
                elif element == 2:
                    wall = Wall(settings.texture_start_x, settings.texture_start_y, settings.texture_w, settings.texture_h, (255,0,0), "wall_h_b.png")
                    level.wall_list.append(wall)
                elif element == 3:
                    wall = Wall(settings.texture_start_x, settings.texture_start_y, settings.texture_w, settings.texture_h, (255,0,0), "wall_v.png")
                    level.wall_list.append(wall)
                elif element == 4:
                    wall = Wall(settings.texture_start_x, settings.texture_start_y, settings.texture_w, settings.texture_h, (255,0,0), "wall_t.png")
                    level.wall_list.append(wall)
                elif element == 5:
                    wall = Wall(settings.texture_start_x, settings.texture_start_y, settings.texture_w, settings.texture_h, (255,0,0), "wall_b_l.png")
                    level.wall_list.append(wall)
                elif element == 6:
                    wall = Wall(settings.texture_start_x, settings.texture_start_y, settings.texture_w, settings.texture_h, (255,0,0), "wall_b_r.png")
                    level.wall_list.append(wall)
                elif element == 7:
                    wall = Wall(settings.texture_start_x, settings.texture_start_y, settings.texture_w, settings.texture_h, (255,0,0), "wall_door.png")
                    level.wall_list.append(wall)
                    self.door = pygame.Rect(settings.texture_start_x, settings.texture_start_y, settings.texture_w, settings.texture_h + 20)
                elif element == 9:
                    spike = Wall(settings.texture_start_x, settings.texture_start_y, settings.texture_w, settings.texture_h, (0,0,255), "thorns.png")
                    level.kill_list.append(spike)
                elif element == 0:
                    floor = Wall(settings.texture_start_x, settings.texture_start_y, settings.texture_w, settings.texture_h, (0,255,0), "floor.png")
                    level.texture_list.append(floor)

                settings.texture_start_x += settings.texture_w
            settings.texture_start_y += settings.texture_h
            settings.texture_start_x = 0


# клас Ворог
class Enemy():  
    def __init__(self, x, y, wight, height, color, direction, image, health=3, attack_speed=5):
        self.hitbox = pygame.Rect(x, y, wight, height)
        self.color = color
        self.image = pygame.image.load(settings.directory + "/textures/" + image)

        self.direction = direction

        self.health = health
        self.list_health = []

        self.attack_timer = 0
        self.attack_limit = 2 * settings.ticks
        self.attack_speed = attack_speed

        self.create_health() 

    def create_health(self):
        health_x = self.hitbox.x
        health_y = self.hitbox.y-20

        for hp in range(self.health):
            serdechko = pygame.Rect(health_x, health_y, 13, 13)
            self.list_health.append(serdechko)
            health_x += 15
            
    def draw_health(self):
        for hp in self.list_health:
            pygame.draw.rect(settings.display, (255, 255, 0), hp)
    
    def draw_color(self):
        pygame.draw.rect(settings.display, self.color, self.hitbox)
        self.draw_health()
 
    def draw_image(self):
        settings.display.blit(self.image, self.hitbox)
        self.draw_health()

    def attack(self):
        self.attack_timer += 1
        if self.attack_timer == self.attack_limit:
            bullet = Bullet(self.hitbox.centerx - 5, self.hitbox.centery - 5, 10, 10, (255, 0, 0), "bullet_bad.png", self.attack_speed, 1, "bad", self.direction)
            settings.bullet_list.append(bullet)
            self.attack_timer = 0

    def get_damage(self):
        del self.list_health[-1]
        if len(self.list_health) <= 0:
            level.enemy_list.remove(self)

# Мапа: 20 x 12 = 240
textures = [
    [4,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,7,4],
    [3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
    [3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
    [3,1,1,1,0,1,4,0,0,0,1,1,4,0,9,0,0,9,0,3],
    [3,0,0,0,0,0,3,0,4,0,0,0,3,9,0,0,9,9,0,3],
    [3,0,1,4,0,0,3,0,3,0,0,0,3,0,0,0,9,9,9,3],
    [3,0,0,3,0,0,3,0,3,0,0,0,3,0,9,0,0,0,0,3],
    [3,0,0,3,0,0,3,0,3,0,0,0,3,9,0,0,9,0,0,3],
    [3,0,0,3,0,0,3,0,3,0,0,0,3,0,9,9,0,9,0,3],
    [3,1,1,1,0,1,1,0,3,0,0,0,3,0,0,0,0,9,0,3],
    [3,0,0,0,0,0,0,0,3,0,0,0,3,9,0,9,0,0,0,3],
    [5,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,6]
]

# Налаштування
settings = Settings(1500, 900, 75, 75, (0, 200, 0), 60)

# Рівень
level = Level(textures, 90, 760)
level.build_level()

# Вороги
enemy1 = Enemy(80, 170, 50, 50, (0, 0, 250), "R", "enemy_r.png", 3, 25) # вправо
enemy2 = Enemy(685, 575, 50, 50, (0, 0, 250), "R", "enemy_r.png", 3) # вправо
enemy3 = Enemy(845, 475, 50, 50, (0, 0, 250), "L", "enemy_l.png", 3) # вліво
enemy4 = Enemy(845, 675, 50, 50, (0, 0, 250), "L", "enemy_l.png", 3) # вліво
enemy5 = Enemy(165, 485, 50, 50, (0, 0, 250), "L", "enemy_l.png", 3) # вліво
enemy6 = Enemy(315, 100, 50, 50, (0, 0, 250), "D", "enemy_d.png", 3, 15) # вниз
enemy7 = Enemy(765, 330, 50, 50, (0, 0, 250), "D", "enemy_d.png", 3, 15) # вниз
enemy8 = Enemy(1360, 325, 50, 50, (0, 0, 250), "U", "enemy_u.png", 3) # вверх

level.enemy_list = [
    enemy1,
    enemy2,
    enemy3,
    enemy4,
    enemy5,
    enemy6,
    enemy7,
    enemy8
]

# Гравець
player = Player(level.start_x, level.start_y, 40, 50, (20,130,75), "knight_run_0.png", "heart.png", "knight_run_", 10, 3, 5)

# Ключі
key_red = Key(175, 640, 39, 21, (250, 15, 0), 'red_key.png')
key_green = Key(685, 790, 39, 21, (60, 255, 0), 'green_key.png')
key_blue = Key(990, 630, 39, 21, (25, 15, 250), 'blue_key.png')

level.key_list.append(key_red)
level.key_list.append(key_green)
level.key_list.append(key_blue)


while settings.game:

    if settings.end_game == False:
        # фон
        settings.display.fill(settings.display_color)

        # стіни
        for wall in level.wall_list:
            wall.draw_image()

        # текстури
        for texture in level.texture_list:
            texture.draw_image()

        # шипи
        for kill_item in level.kill_list:
            kill_item.draw_image()
            if player.hitbox.colliderect(kill_item.hitbox):
                player.die("T")
                
        # ключі
        for key in level.key_list:
            key.take_key()
            key.draw_image()        
    
        # гравець
        player.draw_image()

        player.animation_tick += 1
        
        if player.animation_tick % 6 == 0:
            player.animation_number += 1

        if player.animation_tick == player.animation_limit:
            player.animation_number = 0
            player.animation_tick = 0

        # вороги
        for e in level.enemy_list:
            e.draw_image()
            e.attack()

        # кулі
        for bul in settings.bullet_list:
            bul.draw_image()
            bul.fly()
            bul.check_hit()

        for event in pygame.event.get():
            # вихід 1
            if event.type == pygame.QUIT:
                settings.game = False

            # клавіша натиснута
            if event.type == pygame.KEYDOWN:
                
                # вихід 2
                if event.key == pygame.K_ESCAPE:
                    settings.game = False

                # постріл
                if event.key == pygame.K_SPACE:
                    bullet = Bullet(player.hitbox.centerx, player.hitbox.centery, 10, 10, (255, 255, 0), "bullet_good.png", 7, 1, "good", player.direction)
                    settings.bullet_list.append(bullet)
                    settings.shoot_sound.play()

                # переміщення - старт
                if event.key == pygame.K_w:
                    player.go_up = True
                if event.key == pygame.K_a:
                    player.go_left = True
                    player.direction = "L"
                    player.run_animation_now = player.run_animation_l_images
                if event.key == pygame.K_d:
                    player.go_right = True
                    player.direction = "R"
                    player.run_animation_now = player.run_animation_r_images
                if event.key == pygame.K_s:
                    player.go_down = True
                
            # клавіша відтиснута
            if event.type == pygame.KEYUP:

                # переміщення - стоп
                if event.key == pygame.K_w:
                    player.go_up = False
                if event.key == pygame.K_a:
                    player.go_left = False
                if event.key == pygame.K_d:
                    player.go_right = False
                if event.key == pygame.K_s:
                    player.go_down = False

        player.move()

    else:
        settings.show_end()
        
        for event in pygame.event.get():
            # вихід 3
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    settings.game = False

    pygame.display.flip()
    settings.clock.tick(settings.ticks)