import pygame
import sys
import math
import copy
import levelGeneration 
import random

print(levelGeneration.map)


#####################################

def Main():
    pygame.init()

    def DrawRoom():
        global topLeftWall, leftTopWall, topRightWall, rightTopWall, rightDownWall, downRightWall, LefDowntWall, DownLeftWall

        #draw walls
        leftTopWall = pygame.draw.rect(window, wallColour, (0,0, wallWidth, resolutionY/2 - holeSize/2))
        topLeftWall = pygame.draw.rect(window, wallColour, (0,0, resolutionX/2 - holeSize/2, wallWidth))

        topRightWall = pygame.draw.rect(window, wallColour, (resolutionX/2 + holeSize/2, 0, resolutionX/2 - holeSize/2, wallWidth))
        rightTopWall = pygame.draw.rect(window, wallColour, (resolutionX - wallWidth, 0, wallWidth, resolutionY/2 - holeSize/2))

        rightDownWall = pygame.draw.rect(window, wallColour, (resolutionX - wallWidth, resolutionY/2 + holeSize/2, wallWidth, resolutionY/2 - holeSize/2))
        downRightWall = pygame.draw.rect(window, wallColour, (resolutionX/2 + holeSize/2, resolutionY - wallWidth, resolutionX/2 - wallWidth/2, wallWidth))

        LefDowntWall = pygame.draw.rect(window, wallColour, (0, resolutionY/2 + holeSize/2, wallWidth, resolutionY/2 - holeSize/2))
        DownLeftWall = pygame.draw.rect(window, wallColour, (0, resolutionY - wallWidth, resolutionX/2 - holeSize/2, wallWidth))

    listProjectilu = []
    class Projectile:
        def __init__(self, x, y, angle, radius, penetrace = 1):
            self.x = x
            self.y = y
            self.angle = angle
            self.radius = radius # velikost kulky
            self.vel = 15  # rychlost kulky
            self.penetrace = penetrace #how many times it can strike smt

            self.rect = pygame.Rect(self.x, self.y, self.radius, self.radius)

        def movement(self):
            self.x += math.cos(self.angle) * self.vel
            self.y += math.sin(self.angle) * self.vel

        def draw(self, window):
            if self.penetrace > 0:
                self.projectileHitbox = pygame.Rect(int(self.x), int(self.y), self.radius, self.radius) #creates rectangle hitbox around projectile
                pygame.draw.circle(window, (255, 0, 0), (int(self.x), int(self.y)), self.radius)

        def despawn(self, resolutionX, resolutionY): # despawn kulky m
            return self.x < 0 or self.x > resolutionX or self.y < 0 or self.y > resolutionY
        
        def updateRect(self):
            self.rect = pygame.Rect(self.x, self.y, self.radius, self.radius)

    listRammers = []
    class Rammer:
        def __init__(self, x, y, hp, rychlost, velikost = 60,):
            self.x = x
            self.y = y
            self.hp = hp
            self.velikost = velikost
            self.rychlost = rychlost


        def movement(self, poziceHraceX, poziceHraceY, velikostHrace):
            if self.x > poziceHraceX + velikostHrace - 10:
                self.x -= self.rychlost
            elif self.x < poziceHraceX - velikostHrace + 10:
                self.x += self.rychlost
            
            if self.y > poziceHraceY + velikostHrace - 10:
                self.y -= self.rychlost
            elif self.y < poziceHraceY - velikostHrace + 10:
                self.y += self.rychlost      
        
        def draw(self, window):
            if self.hp > 0:
                pygame.draw.rect(window, (0, 100, 255), (self.x, self.y, self.velikost, self.velikost))

        def detekceKulky(self, listProjectily):
            for i in listProjectily:
                if pygame.Rect.colliderect(pygame.Rect(self.x, self.y, self.velikost, self.velikost), i.rect):  
                    if i.penetrace > 0:
                        self.hp -= 20
                    i.penetrace -= 1

        def utok(self, hracRect, hracZivoty):
            while pygame.Rect.colliderect(pygame.Rect(self.x, self.y, self.velikost, self.velikost), hracRect):
                hracZivoty -= 10  #damage 
                print(hracZivoty)
            return hracZivoty






    currentRoom = copy.copy(levelGeneration.middlecords)
    listRoomek = []
    class Room:
        def __init__(self, cordX, cordY):
            self.cordX = cordX
            self.cordY = cordY


        def drawRoom(self, listRammer, listProjectilu, hracRect, hracZivoty):
            window.fill(black)
            
            DrawRoom() #draws walls
            #Player-Wall collision
            #kdyz se hrac a zed overlapne tak vrati hrace do posledni ulozeny pozice
            if pygame.Rect.collidelist(hracRect, [topLeftWall, leftTopWall, topRightWall, rightTopWall, rightDownWall, downRightWall, LefDowntWall, DownLeftWall]) >= 0:
                hracRect = ulozenaPoziceHrace

            pygame.draw.rect(window, (255, 125, 255), hracRect) #draw player

            #draw rammers
            for rammer in listRammers:
                if rammer.hp > 0:
                    rammer.draw(window)
                    rammer.movement(hracRect.x, hracRect.y, velikostHrace)
                    rammer.detekceKulky(listProjectilu)
                    hracZivoty = rammer.utok(hracRect, hracZivoty)

            #draw projectiles
            #check for projectile collisions
            for projektil in listProjectilu[:]:
                projektil.movement()
                projektil.draw(window)
                projektil.updateRect()

                #out of bound check
                if projektil.despawn(resolutionX, resolutionY):
                    listProjectilu.remove(projektil)

                #wall colisions
                # pygame.Rect.collidelist() returns zero if no collision, otherwise returns index of collision
                if pygame.Rect.collidelist(projektil.projectileHitbox, [topLeftWall, leftTopWall, topRightWall, rightTopWall, rightDownWall, downRightWall, LefDowntWall, DownLeftWall]) >= 0:
                    listProjectilu.remove(projektil)
        
            
    listRoomek.append(Room(currentRoom[0], currentRoom[1]))



    resolutionX = 1920
    resolutionY = 1080
    window = pygame.display.set_mode((resolutionX, resolutionY))
    pygame.display.set_caption("Top Down Shooter")
    clock = pygame.time.Clock()

    poziceHraceX = resolutionX/2
    poziceHraceY = 320
    rychlostHrace = 5
    velikostHrace = 60
    hracRect = pygame.Rect(poziceHraceX, poziceHraceY, velikostHrace, velikostHrace)
    hracZivoty = 100


    ulozenaPoziceHrace = pygame.Rect(0, 0, 0, 0) 


    cooldown = 200  # cooldown zbraně
    last_shot_time = 0 

    wallColour = (255, 255, 255)
    wallWidth = 100

    black = (0, 0, 0)
    holeSize = 250


    #Rammer Spawn
    numberOfSpawnedRammers = 3
    for i in range(numberOfSpawnedRammers):
            listRammers.append(Rammer(
            random.randint(wallWidth, resolutionX - wallWidth), #spawn cord X
            random.randint(wallWidth, resolutionY - wallWidth), #spawn cord Y (both inside the room)
            50 #hp
            ,3 #rychlost
            ))


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
            listProjectilu.append(Projectile(hracRect[0] + 30, hracRect[1] + 30, angle, 5))
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

        for room in listRoomek:
            room.drawRoom(listRammers, listProjectilu, hracRect, hracZivoty)
        



        pygame.display.flip()

Main()
