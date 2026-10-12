import pygame, sys, random, math, os
# mergie back to main test
def resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and for PyInstaller onefile.
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

pygame.init()
pygame.font.init()
pygame.mixer.init()

info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w // 3, info.current_h // 2
screen = pygame.display.set_mode((WIDTH, HEIGHT))




class Player:
    def __init__(self,pos,color):
        self.pos = pygame.math.Vector2(pos)
        self.w = 50
        self.h = 50
        self.color = color
        self.radius = 25

        self.dragging = False
        self.drag_start = pygame.Vector2()
        self.power = 0.03
        self.friction = 0.98
        self.velocity = pygame.Vector2(0,0)\
        
        self.image = pygame.image.load(resource_path("player.png")).convert_alpha()


    def Handle_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.dragging = True
            self.drag_start = pygame.Vector2(event.pos)

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False
            drag_end = pygame.Vector2(event.pos)
            delta = drag_end - self.drag_start

            # store velo
            self.velocity +=  -delta * self.power


    def update(self):
        self.pos += self.velocity
        self.velocity *= self.friction

        if self.pos.x < 0:
            self.pos.x = self.radius
            self.velocity.x = -.7 * self.velocity.x
        elif self.pos.x > WIDTH:
            self.pos.x = WIDTH - self.radius
            self.velocity.x = -.7 * self.velocity.x
        if self.pos.y < 0:
            self.pos.y = self.radius
            self.velocity.y = -self.velocity.y
        elif self.pos.y > HEIGHT:
            self.pos.y = HEIGHT -.7 *  self.radius
            self.velocity.y = -.7 * self.velocity.y

       # print(self.velocity)

    def draw(self,surface):
        scaled_image = pygame.transform.scale(self.image, (self.radius*2, self.radius*2))
        rect = scaled_image.get_rect(center=self.pos)
        surface.blit(scaled_image, rect)


        if self.dragging:
            mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
            pygame.draw.line(surface, (255,0,0), self.drag_start, mouse_pos, 3)
            pygame.draw.line(surface, (255,0,0), self.pos, self.pos, 3)



class Basic_Enemy:
    def __init__(self,pos,speed):
        self.pos = pygame.Vector2(pos)
        self.w = 50
        self.h = 50
        self.color = (0,255,0)
        self.velocity = pygame.Vector2(0,0)
        self.target = player.pos
        self.friction = 0.98
        self.speed = speed

        self.image = pygame.image.load(resource_path("enemy.png")).convert_alpha()

    def update(self, dt):
        self.pos += self.velocity

        # Boundary collision
        if self.pos.x < 0:
            self.velocity.x = -.5 * self.velocity.x

        elif self.pos.x > WIDTH:
            self.velocity.x = -.5 * self.velocity.x

        if self.pos.y < 0:
            self.velocity.y = -.5 * self.velocity.y
        elif self.pos.y > HEIGHT:
            self.velocity.y = -.5 * self.velocity.y

        # Movement towards player foundation
        
        if self.pos.x < self.target.x:
            self.velocity.x += self.speed * dt
        elif self.pos.x > self.target.x:
            self.velocity.x -= self.speed * dt
        if self.pos.y < self.target.y:
            self.velocity.y += self.speed * dt
        elif self.pos.y > self.target.y:
            self.velocity.y -= self.speed * dt
        
        self.velocity *= self.friction

    def draw(self,surface):
        scaled_image = pygame.transform.scale(self.image, (self.w, self.h))

        rect = scaled_image.get_rect(center=self.pos)
        surface.blit(scaled_image, rect)



class static_Enemy():
    def __init__(self,pos,w = 15,h = 15):
        self.pos = pygame.Vector2(pos)
        self.radius = 5
        self.w = 15
        self.h = 15
        self.color = (255,100,0)

    def draw(self,surface):
        pygame.draw.rect(surface, self.color,(self.pos.x,self.pos.y, self.w, self.h))

class Coin():
    def __init__(self,pos,color, speed= 10):
        self.pos = pygame.math.Vector2(pos)
        self.w = 25
        self.h = 25
        self.color = color
        self.radius = 5
        self.friction = 0.97
        self.velocity = pygame.math.Vector2()
        self.speed = speed
        self.target = player.pos
        self.following = False

        self.image = pygame.image.load(resource_path("catnip.png")).convert_alpha()
    def draw(self,surface):
        scaled_image = pygame.transform.scale(self.image, (self.w, self.h))

        rect = scaled_image.get_rect(center=self.pos)
        surface.blit(scaled_image, rect)

    def update(self, dt):
        
        
        distance = math.sqrt(((self.target.x - self.pos.x) ** 2) + ((self.target.y - self.pos.y) ** 2))
        print(f"{distance:0.0f}")

        if distance <= 150 or self.following:
            self.following = True
            self.pos += self.velocity

            if self.pos.x < self.target.x:
                self.velocity.x += self.speed * dt
            elif self.pos.x > self.target.x:
                self.velocity.x -= self.speed * dt
            if self.pos.y < self.target.y:
                self.velocity.y += self.speed * dt
            elif self.pos.y > self.target.y:
                self.velocity.y -= self.speed * dt
            
            self.velocity *= self.friction
        else:
            #self.velocity = self.velocity * 0
            self.pos += pygame.math.Vector2(
                random.uniform(-1,1),
                random.uniform(-1,1)
            )
        
Main_menu_BG = pygame.image.load(resource_path("space.png")).convert_alpha()
Shop_BG = pygame.image.load(resource_path("kissingcat.png")).convert_alpha()
background_image = pygame.image.load(resource_path("space.png"))

player = Player((WIDTH // 2,HEIGHT // 2),(255,255,255))
enimes = [
    Basic_Enemy((random.randint(0, WIDTH-50), random.randint(0, HEIGHT-50)), random.uniform(5, 7)),
]

coins_onscreen = [
    Coin((59,50),(255,255,0), random.randint(25,30))
]



def Spawn_amount(enenmy_list, Name_of_class, Spawn_count):
    for _ in range(Spawn_count):
        enenmy_list.append(Name_of_class((random.randint(0, WIDTH-50), random.randint(0, HEIGHT-50)), random.uniform(5, 10)))
def Spawn_coins(Spawn_count):
    for _ in range(Spawn_count):
        coins_onscreen.append(Coin((player.pos.x + random.randint(-50,50),player.pos.y + random.randint(-50,50)),(255,255,0), random.randint(25,30)))

def circle_rect_collision(circle_pos, circle_radius, rect):
    closest_x = max(rect.left, min(circle_pos.x, rect.right))
    closest_y = max(rect.top, min(circle_pos.y, rect.bottom))

    distance_x = circle_pos.x - closest_x
    distance_y = circle_pos.y - closest_y

    return (distance_x ** 2 + distance_y ** 2) < (circle_radius ** 2)


    
collison_sound = pygame.mixer.Sound(resource_path("collision.mp3"))
Spawn_amount(enimes, Basic_Enemy,random.randint(5,10))

font = pygame.font.Font(None, 32)
menu_font = pygame.font.Font(None, 64)

pygame.display.set_caption("SPACE KITTY")
def game():
    wave = 1
    money = 0
    clock = pygame.time.Clock()
    dt = clock.tick(60) / 1000  # Delta time in seconds.
    dragging = False

    global game_running
    game_running = True
    while game_running:
        screen.blit(background_image, (0,0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_running = False
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_s:
                    game_running = False
                    shop()
                if event.key == pygame.K_g:
                    enimes.remove(enimes[len(enimes)-1])
            player.Handle_event(event)
        
        keys = pygame.key.get_pressed()

        player.draw(screen)
        player.update()

        for enemy in enimes[:]:
            enemy_rect = pygame.Rect(enemy.pos.x,enemy.pos.y,enemy.w,enemy.h)
            if circle_rect_collision(player.pos,player.radius, enemy_rect):

                if abs(player.velocity.x) > 5 or abs(player.velocity.y) > 5:
                    enimes.remove(enemy)
                    Spawn_coins(10)
                    player.velocity = player.velocity * 0.8
                    player.color = (255,0,0)
                    collison_sound.play()
                else:
                    running = False
                    death_screen()

                    enimes.clear()

                break
        for coins in coins_onscreen[:]:
            coin_rect = pygame.Rect(coins.pos.x,coins.pos.y,coins.w,coins.h)
            if circle_rect_collision(player.pos,player.radius, coin_rect) or circle_rect_collision(player.pos,player.radius, coin_rect) :
                print("hit coin")
                coins_onscreen.remove(coins)
                money += int(1 * (wave / 15 + 1))


            
        for enemy in enimes:
            enemy.draw(screen)

        for enemy in enimes:
            enemy.update(dt)

        for coins in coins_onscreen:
            coins.update(dt)
            
        for coins in coins_onscreen:
            coins.draw(screen)

        if enimes == []:
            wave = wave + 1
            Spawn_amount(enimes, Basic_Enemy,random.randint(5 * wave,10 * wave))



        current_velo = player.velocity.x + player.velocity.y / 2

        speed_text = font.render(f"speed {abs(current_velo):0.0f}", True,(255,255,255))
        screen.blit(speed_text,(0,0))

        score_text = font.render(f"Score: {money}", True, (255,0,255))
        screen.blit(score_text , (WIDTH - score_text.get_width() - 10, 0))

        wave_text = font.render(f"Wave: {wave}", True, (255,0,255))
        screen.blit(wave_text , ((WIDTH - wave_text.get_width()) // 2, 30))

        tick = clock.tick(60)
        pygame.display.flip()

def shop():
    global score
    global game_running
    game_running = True
    while game_running:
        clock = pygame.time.Clock()
        dt = clock.tick(60) / 1000  # Delta time in seconds.
        
        screen.blit(Shop_BG, (0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                running = False
                game()
        pygame.display.flip()
        tick = clock.tick(60)

def main_menu():
    running = True
    while running:
        screen.blit(Main_menu_BG, (0,0))

        title_text = menu_font.render("SPACE KITTY", True, (255,0,255))
        instruction_text = font.render("Press the Space bar to Start", True, (255,0,255))
        screen.blit(title_text, ((WIDTH - title_text.get_width()) // 2, HEIGHT // 3))
        screen.blit(instruction_text, ((WIDTH - instruction_text.get_width()) // 2, HEIGHT // 2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                running = False
                game()

        pygame.display.flip()
def death_screen():
    running = True
    dead_BG = pygame.image.load(resource_path("deadcat.png")).convert_alpha()
    scaled_dead_BG = pygame.transform.scale(dead_BG, (WIDTH, HEIGHT))
    while running:
        screen.blit(scaled_dead_BG, (0,0))
        title_text = menu_font.render("You Died", True, (255,0,255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                collison_sound.play()
                sys.exit()

        pygame.display.flip()


if __name__ == "__main__":  
    main_menu()



#
#
#
#
#           _______________
#          /        |######|
#         /         |######|
# _______/          |######|___________
#     ______                 ______  {}|
#    /      \               /      \   |
#   /        \             /        \  |
# --------------------------------------
#
#
#
#

