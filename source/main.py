import pygame
import sys
import math


class Projectile:
    def __init__(self, x, y, angle, radius):
        self.x = x
        self.y = y
        self.angle = angle
        self.radius = radius # velikost kulky
        self.vel = 10  # rychlost kulky

    def movement(self):
        self.x += math.cos(self.angle) * self.vel
        self.y += math.sin(self.angle) * self.vel

    def draw(self, window):
        self.projectileHitbox = pygame.Rect(int(self.x), int(self.y), self.radius, self.radius) #creates rectangle hitbox around projectile
        pygame.draw.circle(window, (255, 0, 0), (int(self.x), int(self.y)), self.radius)

    def despawn(self, res_x, res_y): # despawn kulky m
        return self.x < 0 or self.x > res_x or self.y < 0 or self.y > res_y
    


#####################################

def Main():
    pygame.init()
    res_x = 1600
    res_y = 1200
    window = pygame.display.set_mode((res_x, res_y))
    pygame.display.set_caption("Top Down Shooter")
    clock = pygame.time.Clock()


    x_player = 320
    y_player = 320
    rychlostHrace = 5

    projektily = []


    cooldown = 200  # cooldown zbraně
    last_shot_time = 0 

    wallColour = (255, 255, 255)
    wallWidth = 100

    black = (0, 0, 0)
    holeSize = 250

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Získání aktuálního času
        current_time = pygame.time.get_ticks()

        # Střelba projektilů při kliknutí myší
        if pygame.mouse.get_pressed()[0] and current_time - last_shot_time >= cooldown:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Vypočítání úhlu střelby
            rel_x, rel_y = mouse_x - (x_player + 30), mouse_y - (y_player + 30)
            angle = math.atan2(rel_y, rel_x)
            projektily.append(Projectile(x_player + 30, y_player + 30, angle, 5))
            last_shot_time = current_time  # čas posledního výstřelu

        # Pohyb hráče
        key_press = pygame.key.get_pressed()
        if key_press[pygame.K_ESCAPE]:
            sys.exit()

        if key_press[pygame.K_w]:
            y_player -= rychlostHrace
        if key_press[pygame.K_s]:
            y_player += rychlostHrace
        if key_press[pygame.K_a]:
            x_player -= rychlostHrace
        if key_press[pygame.K_d]:
            x_player += rychlostHrace


        window.fill(black)

        #draw walls
        leftTopWall = pygame.draw.rect(window, wallColour, (0,0, wallWidth, res_y/2 - holeSize/2))
        topLeftWall = pygame.draw.rect(window, wallColour, (0,0, res_x/2 - holeSize/2, wallWidth))

        topRightWall = pygame.draw.rect(window, wallColour, (res_x/2 + holeSize/2, 0, res_x/2 - holeSize/2, wallWidth))
        rightTopWall = pygame.draw.rect(window, wallColour, (res_x - wallWidth, 0, wallWidth, res_y/2 - holeSize/2))

        rightDownWall = pygame.draw.rect(window, wallColour, (res_x - wallWidth, res_y/2 + holeSize/2, wallWidth, res_y/2 - holeSize/2))
        downRightWall = pygame.draw.rect(window, wallColour, (res_x/2 + holeSize/2, res_y - wallWidth, res_x/2 - wallWidth/2, wallWidth))

        LefDowntWall = pygame.draw.rect(window, wallColour, (0, res_y/2 + holeSize/2, wallWidth, res_y/2 - holeSize/2))
        DownLeftWall = pygame.draw.rect(window, wallColour, (0, res_y - wallWidth, res_x/2 - holeSize/2, wallWidth))


        #check for projectile collisions
        for projektil in projektily[:]:
            projektil.movement()
            projektil.draw(window)

            #wall colisions
            # pygame.Rect.collidelist() returns zero if no collision, otherwise returns index of collision
            if pygame.Rect.collidelist(projektil.projectileHitbox, [topLeftWall, leftTopWall, topRightWall, rightTopWall, rightDownWall, downRightWall, LefDowntWall, DownLeftWall]) >= 0:
                projektily.remove(projektil)

            #out of bound check
            if projektil.despawn(res_x, res_y):
                projektily.remove(projektil)

        pygame.draw.rect(window, (255, 125, 255), (x_player, y_player, 60, 60))
        pygame.display.flip()

Main()
