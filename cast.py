import pygame
from math import atan2, cos, sin, pi, sqrt

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SKY = (50, 100, 200)
GROUND = (200, 200, 100)
TRASPARENT = (152 , 0,136, 255)
GERUDO_SKY = (255, 165, 0)

colors = [
    (0, 20, 10),
    (4, 40, 63),
    (0, 91, 82),
    (219, 242, 38),
    (21, 42, 138)
]


wall1 = pygame.image.load('./wall.png')

sprite1 = pygame.image.load('./down.png')
sprite2 = pygame.image.load('./space_sprite.jpg')

starts = pygame.image.load('./introscreen.jpg')
ends = pygame.image.load('./end.jpg')


walls = {
    "1" : wall1,
}

enemies = [
    {
        "number": 0,
        "x" : 300,
        "y" : 300,
        "sprite":  sprite1,
        "position" : "x: " + str(300) + "y: " +str(300) 
    }, 
    {
        "number": 1,
        "x" : 400,
        "y" : 225,
        "sprite":  sprite1,
        "position" : "x: " + str(300) + "y: " +str(110) 
    },
    {
        "number": 2,
        "x" : 150,
        "y" : 420,
        "sprite":  sprite1,
        "position" : "x: " + str(300) + "y: " +str(110) 
    }
]

class Raycaster(object):
    def __init__(self, screen):
        self.screen = screen
        x, y, self.width, self.height = screen.get_rect()
        self.block_size = 50
        self.score = 0
        self.map = []
        self.last_angle = 0
        self.player = {
            "x": int(self.block_size + (self.block_size / 2)),
            "y": int(self.block_size + (self.block_size / 2)),
            "fov": int(pi / 3),
            "a": 0
        }
        self.scale = 10
        self.zbuffer = [9999999999 for z in range(0, int(self.width/2))]
    
    def clearZ(self):
        self.zbuffer = [9999999999 for z in range(0, int(self.width/2))]

    def point(self, x, y, c = WHITE):
        # No usa aceleracion grafica. Usar pixel o point usado en juego de la vida
        self.screen.set_at((x, y), c)

    def block(self, x, y, wall):
        for i in range(x, x + self.block_size):
            for j in range(y, y + self.block_size):
                tx = int((i - x) * 128 / self.block_size)
                ty = int((j - y) * 128 / self.block_size)
                c = wall.get_at((tx, ty))
                self.point(i, j, c)

    def load_map(self, filename):
        with open(filename) as f:
            for line in f.readlines():
                self.map.append(list(line))

    def draw_stake(self, x, h, c,tx):
        start_y = int(self.height / 2 - h / 2)
        end_y = int(self.height / 2 + h / 2)
        height = end_y - start_y
        for y in range(start_y, end_y):
            ty = int((y - start_y) * 128 / height)
            color = walls[c].get_at((tx, ty))
            self.point(x, y, color)
    
    def display_fps(self, clock):
        font = pygame.font.SysFont('Arial', 16)
        fps = str(round(clock.get_fps(), 3))
        fps_text = font.render(fps, 1, pygame.Color("black"))
        return self.screen.blit(fps_text, (self.width - 40, self.height - 40))

    def cast_ray(self, a):
        d = 0
        origin_x = self.player["x"]
        origin_y = self.player["y"]


        while True:
            x = int(origin_x + d * cos(a))
            y = int(origin_y + d * sin(a))

            i = int(x / self.block_size)
            j = int(y / self.block_size)

            if self.map[j][i] != ' ':
                hitx = x - i * self.block_size
                hity = y - j * self.block_size

                if 1 < hitx and hitx < self.block_size - 1:
                    maxhit = hitx
                else:
                    maxhit = hity

                tx = int(maxhit * 128 / self.block_size)
                return d, self.map[j][i], tx

            self.point(x, y)
            d += 1

    def draw_map(self):
        for x in range(0, 500, self.block_size):
            for y in range(0, 500, self.block_size):
                i = int(x / self.block_size)
                j = int(y / self.block_size)

                if self.map[j][i] !=  ' ':
                    self.block(x, y, walls["1"])

    def draw_player(self):
        self.point(self.player["x"], self.player["y"])
    
    def draw_sprite(self, sprite):
        sprite_a = atan2(
            sprite["y"] - self.player["y"], 
            sprite["x"] - self.player["x"]
        )

        d = (
            (self.player["x"] - sprite["x"])**2 + 
            (self.player["y"] - sprite["y"])**2
            )** 0.5

        sprite_size = int(((self.width/2)/d) * self.height/self.scale)

        sprite_x = int(
            (self.width/2) + 
            (sprite_a - self.player["a"]) * 
            (self.width/2) / self.player["fov"] 
            + sprite_size/2)

        sprite_y = int(self.height/2 - sprite_size/2)

        for x in range(sprite_x, sprite_x + sprite_size):
            for y in range(sprite_y, sprite_y + sprite_size):
                tx = int((x - sprite_x) * 128 / sprite_size)
                ty = int((y - sprite_y) * 128 / sprite_size)
                
                c = sprite["sprite"].get_at((tx, ty))

                if c != WHITE:
                    if(x > int(self.width/2) and x < int(self.width)):
                        if self.zbuffer[x - int(self.width/2)] >= d:
                            self.point(x, y, c)
                            self.zbuffer[x - int(self.width/2)] = d

    def render(self):
        self.draw_map()
        self.draw_player()

        density = 100

        # minimap

        for i in range(0, density):
            a = self.player["a"] - self.player["fov"] / 2 + self.player["fov"] * i / density
            d, c, t = self.cast_ray(a)


        # separador

        for i in range(0, 500): 
            self.point(499, i)
            self.point(500, i)
            self.point(501, i)

        # draw in 3d

        for i in range(0, int(self.width/2)):
            a = self.player["a"] - self.player["fov"] / 2 + self.player["fov"] * i / (self.width / 2)
            d, c, tx = self.cast_ray(a)
            
            x = int(self.width / 2) + i
            try:
                h = (self.height / (d * cos(a - self.player["a"]))) * self.height / 5
                if self.zbuffer[i] >= d:
                    self.draw_stake(x, h, c, tx)
                    self.zbuffer[i] = d
            except:
                self.inverse()
        
        for enemy in enemies:
            if enemy:
                self.point(int(enemy["x"]), int(enemy["y"]), (255, 0, 0))
        
        for enemy in enemies:
            if enemy:
                self.draw_sprite(enemy)
        
    def inverse(self):
        if abs(self.player["a"]) == 0:
            if self.last_move == "left":
                self.player["y"] += 10
            elif self.last_move == "right":
                self.player["y"] -= 10
            elif self.last_move == "up":
                self.player["x"] -= 10
            elif self.last_move == "down":
                self.player["x"] += 10
        elif abs(self.player["a"]) == pi/4:
            if self.last_move == "left":
                self.player["x"] -= 10
                self.player["y"] += 10
            elif self.last_move == "right":
                self.player["x"] += 10
                self.player["y"] -=10
            elif self.last_move == "up":
                self.player["x"] -= 10
                self.player["y"] -= 10
            elif self.last_move == "down":
                self.player["x"] += 10
                self.player["y"] += 10
        elif abs(self.player["a"]) == pi/2:
            if self.last_move == "left":
                self.player["x"] -= 10
            elif self.last_move == "right":
                self.player["x"] += 10
            elif self.last_move == "up":
                self.player["y"] -= 10
            elif self.last_move == "down":
                self.player["y"] += 10
        elif abs(self.player["a"]) == 3*pi/4:
            if self.last_move == "left":
                self.player["x"] -= 10
                self.player["y"] -= 10
            elif self.last_move == "right":
                self.player["x"] += 10
                self.player["y"] += 10
            elif self.last_move == "up":
                self.player["x"] += 10
                self.player["y"] -= 10
            elif self.last_move == "down":
                self.player["x"] -= 10
                self.player["y"] += 10
        elif abs(self.player["a"]) == pi:
            if self.last_move == "left":
                self.player["y"] -= 10
            elif self.last_move == "right":
                self.player["y"] += 10
            elif self.last_move == "up":
                self.player["x"] += 10
            elif self.last_move == "down":
                self.player["x"] -= 10
        elif abs(self.player["a"]) == 5*pi/4:
            if self.last_move == "left":
                self.player["x"] += 10
                self.player["y"] -= 10
            elif self.last_move == "right":
                self.player["x"] -= 10
                self.player["y"] += 10
            elif self.last_move == "up":
                self.player["x"] += 10
                self.player["y"] += 10
            elif self.last_move == "down":
                self.player["x"] -= 10
                self.player["y"] -= 10
        elif abs(self.player["a"]) == 3*pi/2:
            if self.last_move == "left":
                self.player["x"] += 10
            elif self.last_move == "right":
                self.player["x"] -= 10
            elif self.last_move == "up":
                self.player["y"] += 10
            elif self.last_move == "down":
                self.player["y"] -= 10
        elif abs(self.player["a"]) == 7*pi/4:
            if self.last_move == "left":
                self.player["x"] += 10
                self.player["y"] += 10
            elif self.last_move == "right":
                self.player["x"] -= 10
                self.player["y"] -= 10
            elif self.last_move == "up":
                self.player["x"] -= 10
                self.player["y"] += 10
            elif self.last_move == "down":
                self.player["x"] += 10
                self.player["y"] -= 10
    
    def collect(self, sprite):
        player_x = self.player["x"]
        player_y = self.player["y"]
        sprite_x = sprite["x"]
        sprite_y = sprite["y"]

        d = sqrt((player_x - sprite_x)**2 + (player_y - sprite_y)**2)
        sprite_a = atan2(sprite_y - player_y, sprite_x - player_x)
        sprite_size = int(((self.width/2)/d) * self.height/self.scale)
        sprite_y = int(self.height/2 - sprite_size/2)
        sprite_x = int(
            (self.width/2) + 
            (sprite_a - self.player["a"]) * 
            (self.width/2) / self.player["fov"] 
            + sprite_size/2)
        
        for x in range(750, 751):
            for y in range(250, 251):
                tx = int((x - sprite_x) * 128 / sprite_size)
                ty = int((y - sprite_y) * 128 / sprite_size)

                try:
                    c = sprite["sprite"].get_at((tx, ty))
                except:
                    c = 0
                if c != WHITE and c !=0 and self.zbuffer[250] >= d: 
                    c = 0
                    enemy_number = sprite["number"]
                    enemies.pop(enemy_number)
                    enemies.insert(enemy_number, None)
                    pygame.mixer.Sound.play(get_sound)
                    self.score += 1
                    break


        


pygame.init()
screen = pygame.display.set_mode((1000, 500))
r = Raycaster(screen)
pygame.mixer.init()
pygame.mixer.music.load("./Lost_Woods.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)
get_sound = pygame.mixer.Sound('./Collect_sound.mp3')
end = False
running = False
running2 = False

start = True
while start:
    for x  in range(r.width):
        for y in range(r.height):
            c = starts.get_at((x, y))
            r.point(x, y, c)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                start = False
                r.load_map('map.txt')
                running = True
            elif event.key == pygame.K_2:
                start = False
                r.load_map('map2.txt')
                running2 = True
clock = pygame.time.Clock()


while running:
    if r.score == 3:
        running = False
        end = True
    
    screen.fill(BLACK)
    screen.fill(SKY, (r.width / 2, 0, r.width, r.height / 2))
    screen.fill(GROUND, (r.width / 2, r.height / 2, r.width, r.height))
    r.clearZ()
    r.display_fps(clock)
    r.render()

    pygame.display.flip()
    
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            running = False
        
        if (event.type == pygame.MOUSEMOTION):
            r.player["a"] += event.rel[0] * 5 / (r.width / 2) 

        if (event.type == pygame.KEYDOWN):

            if event.key == pygame.K_a:
                r.player["a"] = (r.player["a"] - pi / 4)% (2 * pi)
                r.last_angle = r.player["a"]
            if event.key == pygame.K_d:
                r.player["a"] = (r.player["a"] + pi / 4)% (2 * pi)
                r.last_angle = r.player["a"]
            if event.key == pygame.K_SPACE:
                for i in enemies:
                    if i != None:
                        r.collect(i)
            if event.key == pygame.K_f:
                print("no funciono tu idea")
                r.player["a"] = r.last_angle


            if event.key == pygame.K_RIGHT:
                r.last_move = "right"
                if r.player["a"] == 0:
                    r.player["y"] += 10
                if abs(r.player["a"]) == pi/4:
                    r.player["x"] -= 10
                    r.player["y"] += 10
                if abs(r.player["a"]) == pi/2:
                    r.player["x"] -= 10
                if abs(r.player["a"]) == 3*pi/4:
                    r.player["x"] -= 10
                    r.player["y"] -= 10
                if abs(r.player["a"]) == pi:
                    r.player["y"] -= 10
                if abs(r.player["a"]) == 5*pi/4:
                    r.player["x"] += 10
                    r.player["y"] -= 10
                if abs(r.player["a"]) == 3*pi/2:
                    r.player["x"] += 10
                if abs(r.player["a"]) == 7*pi/4:
                    r.player["x"] += 10
                    r.player["y"] += 10
            if event.key == pygame.K_LEFT:
                r.last_move = "left"
                if r.player["a"] == 0:
                    r.player["y"] -= 10
                if abs(r.player["a"]) == pi/4:
                    r.player["x"] += 10
                    r.player["y"] -= 10
                if abs(r.player["a"]) == pi/2:
                    r.player["x"] += 10
                if abs(r.player["a"]) == 3*pi/4:
                    r.player["x"] += 10
                    r.player["y"] += 10
                if abs(r.player["a"]) == pi:
                    r.player["y"] += 10
                if abs(r.player["a"]) == 5*pi/4:
                    r.player["x"] -= 10
                    r.player["y"] += 10
                if abs(r.player["a"]) == 3*pi/2:
                    r.player["x"] -= 10
                if abs(r.player["a"]) == 7*pi/4:
                    r.player["x"] -= 10
                    r.player["y"] -= 10
            if event.key == pygame.K_UP:
                r.last_move = "up"
                if r.player["a"] == 0:
                    r.player["x"] += 10
                if abs(r.player["a"]) == pi/4:
                    r.player["x"] += 10
                    r.player["y"] += 10
                if abs(r.player["a"]) == pi/2:
                    r.player["y"] += 10
                if abs(r.player["a"]) == 3*pi/4:
                    r.player["x"] -= 10
                    r.player["y"] += 10
                if abs(r.player["a"]) == pi:
                    r.player["x"] -= 10
                if abs(r.player["a"]) == 5*pi/4:
                    r.player["x"] -= 10
                    r.player["y"] -= 10
                if abs(r.player["a"]) == 3*pi/2:
                    r.player["y"] -= 10
                if abs(r.player["a"]) == 7*pi/4:
                    r.player["x"] += 10
                    r.player["y"] -= 10
            if event.key == pygame.K_DOWN:
                r.last_move = "down"
                if r.player["a"] == 0:
                    r.player["x"] -= 10
                if abs(r.player["a"]) == pi/4:
                    r.player["x"] -= 10
                    r.player["y"] -= 10
                if abs(r.player["a"]) == pi/2:
                    r.player["y"] -= 10
                if abs(r.player["a"]) == 3*pi/4:
                    r.player["x"] += 10
                    r.player["y"] -= 10
                if abs(r.player["a"]) == pi:
                    r.player["x"] += 10
                if abs(r.player["a"]) == 5*pi/4:
                    r.player["x"] += 10
                    r.player["y"] += 10
                if abs(r.player["a"]) == 3*pi/2:
                    r.player["y"] += 10
                if abs(r.player["a"]) == 7*pi/4:
                    r.player["x"] -= 10
                    r.player["y"] += 10
    clock.tick()

while running2:
    if r.score == 3:
        running2 = False
        end = True
    
    screen.fill(BLACK)
    screen.fill(GERUDO_SKY, (r.width / 2, 0, r.width, r.height / 2))
    screen.fill(GROUND, (r.width / 2, r.height / 2, r.width, r.height))
    r.clearZ()
    r.display_fps(clock)
    r.render()

    pygame.display.flip()
    
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            running2 = False
        
        if (event.type == pygame.MOUSEMOTION):
            r.player["a"] -= event.rel[0] * 5 / (r.width / 2)

        if (event.type == pygame.KEYDOWN):

            if event.key == pygame.K_a:
                r.player["a"] = (r.player["a"] - pi / 4)% (2 * pi)
            if event.key == pygame.K_d:
                r.player["a"] = (r.player["a"] + pi / 4)% (2 * pi)
            if event.key == pygame.K_SPACE:
                for i in enemies:
                    if i != None:
                        r.collect(i)
            if event.key == pygame.K_f:
                print("no funciono tu idea")
                r.player["a"] = r.last_angle


            if event.key == pygame.K_RIGHT:
                r.last_move = "right"
                if r.player["a"] == 0:
                    r.player["y"] += 10
                if abs(r.player["a"]) == pi/4:
                    r.player["x"] -= 10
                    r.player["y"] += 10
                if abs(r.player["a"]) == pi/2:
                    r.player["x"] -= 10
                if abs(r.player["a"]) == 3*pi/4:
                    r.player["x"] -= 10
                    r.player["y"] -= 10
                if abs(r.player["a"]) == pi:
                    r.player["y"] -= 10
                if abs(r.player["a"]) == 5*pi/4:
                    r.player["x"] += 10
                    r.player["y"] -= 10
                if abs(r.player["a"]) == 3*pi/2:
                    r.player["x"] += 10
                if abs(r.player["a"]) == 7*pi/4:
                    r.player["x"] += 10
                    r.player["y"] += 10
            if event.key == pygame.K_LEFT:
                r.last_move = "left"
                if r.player["a"] == 0:
                    r.player["y"] -= 10
                if abs(r.player["a"]) == pi/4:
                    r.player["x"] += 10
                    r.player["y"] -= 10
                if abs(r.player["a"]) == pi/2:
                    r.player["x"] += 10
                if abs(r.player["a"]) == 3*pi/4:
                    r.player["x"] += 10
                    r.player["y"] += 10
                if abs(r.player["a"]) == pi:
                    r.player["y"] += 10
                if abs(r.player["a"]) == 5*pi/4:
                    r.player["x"] -= 10
                    r.player["y"] += 10
                if abs(r.player["a"]) == 3*pi/2:
                    r.player["x"] -= 10
                if abs(r.player["a"]) == 7*pi/4:
                    r.player["x"] -= 10
                    r.player["y"] -= 10
            if event.key == pygame.K_UP:
                r.last_move = "up"
                if r.player["a"] == 0:
                    r.player["x"] += 10
                if abs(r.player["a"]) == pi/4:
                    r.player["x"] += 10
                    r.player["y"] += 10
                if abs(r.player["a"]) == pi/2:
                    r.player["y"] += 10
                if abs(r.player["a"]) == 3*pi/4:
                    r.player["x"] -= 10
                    r.player["y"] += 10
                if abs(r.player["a"]) == pi:
                    r.player["x"] -= 10
                if abs(r.player["a"]) == 5*pi/4:
                    r.player["x"] -= 10
                    r.player["y"] -= 10
                if abs(r.player["a"]) == 3*pi/2:
                    r.player["y"] -= 10
                if abs(r.player["a"]) == 7*pi/4:
                    r.player["x"] += 10
                    r.player["y"] -= 10
            if event.key == pygame.K_DOWN:
                r.last_move = "down"
                if r.player["a"] == 0:
                    r.player["x"] -= 10
                if abs(r.player["a"]) == pi/4:
                    r.player["x"] -= 10
                    r.player["y"] -= 10
                if abs(r.player["a"]) == pi/2:
                    r.player["y"] -= 10
                if abs(r.player["a"]) == 3*pi/4:
                    r.player["x"] += 10
                    r.player["y"] -= 10
                if abs(r.player["a"]) == pi:
                    r.player["x"] += 10
                if abs(r.player["a"]) == 5*pi/4:
                    r.player["x"] += 10
                    r.player["y"] += 10
                if abs(r.player["a"]) == 3*pi/2:
                    r.player["y"] += 10
                if abs(r.player["a"]) == 7*pi/4:
                    r.player["x"] -= 10
                    r.player["y"] += 10
    clock.tick()

while end:
    for x  in range(r.width):
        for y in range(r.height):
            c = ends.get_at((x, y))
            r.point(x, y, c)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end = False