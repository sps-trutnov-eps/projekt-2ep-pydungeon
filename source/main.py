import pygame
import sys
import math
import copy
import levelGeneration 

print(levelGeneration.map)

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

    def despawn(self, resolutionX, resolutionY): # despawn kulky m
        return self.x < 0 or self.x > resolutionX or self.y < 0 or self.y > resolutionY
    

class Roomka:
    def __init__(self, cordX, cordY, type):
        self.cordX = cordX
        self.cordY = cordY
        self.type = type

    def moveToDifferentRoom(self):
        pass
    
    def DrawRoom(self, cordX, cordY):
        drawRoom()
#####################################

def Main():
    pygame.init()
    resolutionX = 1600
    resolutionY = 1200
    window = pygame.display.set_mode((resolutionX, resolutionY))
    pygame.display.set_caption("Top Down Shooter")
    clock = pygame.time.Clock()


    poziceHraceX = resolutionX/2
    poziceHraceY = 320
    rychlostHrace = 5
    velikostHrace = 60
    hracRect = pygame.Rect(poziceHraceX, poziceHraceY, velikostHrace, velikostHrace)
    ulozenaPoziceHrace = pygame.Rect(0, 0, 0, 0) 

    projektily = []
    cooldown = 200  # cooldown zbraně
    last_shot_time = 0 

    wallColour = (255, 255, 255)
    wallWidth = 100

    black = (0, 0, 0)
    holeSize = 250

    currentRoom = copy.copy(levelGeneration.middlecords)


    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Získání aktuálního času a keypressed
        current_time = pygame.time.get_ticks()
        key_press = pygame.key.get_pressed()

        #update hracovych pozici
        ulozenaPoziceHrace = copy.copy(hracRect)
        prostredekHrace = (hracRect[0] + velikostHrace/2, hracRect[1] + velikostHrace/2)

        # Střelba projektilů při kliknutí myší
        if pygame.mouse.get_pressed()[0] and current_time - last_shot_time >= cooldown:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Vypočítání úhlu střelby
            rel_x, rel_y = mouse_x - (hracRect[0] + 30), mouse_y - (hracRect[1] + 30)
            angle = math.atan2(rel_y, rel_x)
            projektily.append(Projectile(hracRect[0] + 30, hracRect[1] + 30, angle, 5))
            last_shot_time = current_time  # čas posledního výstřelu

        # Pohyb hráče
        if key_press[pygame.K_ESCAPE]:
            sys.exit()

        if key_press[pygame.K_w]:
            hracRect[1] -= rychlostHrace
        if key_press[pygame.K_s]:
            hracRect[1] += rychlostHrace
        if key_press[pygame.K_a]:
            hracRect[0] -= rychlostHrace
        if key_press[pygame.K_d]:
            hracRect[0] += rychlostHrace

        #kontrola out of bounds hrace
        if 0 > prostredekHrace[0]:
            currentRoom[0] -= 1 #levy vychod
        elif prostredekHrace[0] > resolutionX:
            currentRoom[0] += 1 #pravy vychod
        elif 0 > prostredekHrace[1]:
            currentRoom[1] += 1 #horni vychod
        elif prostredekHrace[1] > resolutionY:
            currentRoom[1] -= 1 #dolni vychod


        def DrawRoom():
            global topLeftWall, leftTopWall, topRightWall, rightTopWall, rightDownWall, downRightWall, LefDowntWall, DownLeftWall
            window.fill(black)

            #draw walls
            leftTopWall = pygame.draw.rect(window, wallColour, (0,0, wallWidth, resolutionY/2 - holeSize/2))
            topLeftWall = pygame.draw.rect(window, wallColour, (0,0, resolutionX/2 - holeSize/2, wallWidth))

            topRightWall = pygame.draw.rect(window, wallColour, (resolutionX/2 + holeSize/2, 0, resolutionX/2 - holeSize/2, wallWidth))
            rightTopWall = pygame.draw.rect(window, wallColour, (resolutionX - wallWidth, 0, wallWidth, resolutionY/2 - holeSize/2))

            rightDownWall = pygame.draw.rect(window, wallColour, (resolutionX - wallWidth, resolutionY/2 + holeSize/2, wallWidth, resolutionY/2 - holeSize/2))
            downRightWall = pygame.draw.rect(window, wallColour, (resolutionX/2 + holeSize/2, resolutionY - wallWidth, resolutionX/2 - wallWidth/2, wallWidth))

            LefDowntWall = pygame.draw.rect(window, wallColour, (0, resolutionY/2 + holeSize/2, wallWidth, resolutionY/2 - holeSize/2))
            DownLeftWall = pygame.draw.rect(window, wallColour, (0, resolutionY - wallWidth, resolutionX/2 - holeSize/2, wallWidth))
        DrawRoom()

        #Player-Wall collision
        #kdyz se hrac a zed overlapne tak vrati hrace do posledni ulozeny pozice
        if pygame.Rect.collidelist(hracRect, [topLeftWall, leftTopWall, topRightWall, rightTopWall, rightDownWall, downRightWall, LefDowntWall, DownLeftWall]) >= 0:
            hracRect = ulozenaPoziceHrace
            
        #check for projectile collisions
        for projektil in projektily[:]:
            projektil.movement()
            projektil.draw(window)

            #wall colisions
            # pygame.Rect.collidelist() returns zero if no collision, otherwise returns index of collision
            if pygame.Rect.collidelist(projektil.projectileHitbox, [topLeftWall, leftTopWall, topRightWall, rightTopWall, rightDownWall, downRightWall, LefDowntWall, DownLeftWall]) >= 0:
                projektily.remove(projektil)

            #out of bound check
            if projektil.despawn(resolutionX, resolutionY):
                projektily.remove(projektil)

        pygame.draw.rect(window, (255, 125, 255), hracRect)
        

        pygame.display.flip()

Main()
