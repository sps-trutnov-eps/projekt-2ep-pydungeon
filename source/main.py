import pygame, sys, copy, numpy, random, math
import levelGeneration

def Main():
    pygame.init()

    holeSize = 250
    wallWidth = 100
    wallColour = (51, 46, 37)
    #plugColor = (45, 40, 29)
    plugColor = (51, 46, 37)
    rozliseniObrazovky = (1920, 1080)

    okno = pygame.display.set_mode((rozliseniObrazovky))
    clock = pygame.time.Clock()

    grid = levelGeneration.map #recieves random map from levelGeneration.py    Type -> numpy.array
    middlecord = copy.copy(levelGeneration.middlecords) #middle of grid
    current_room = copy.copy(middlecord) #sets current room at middle (spawn room)
    print(grid)

    rychlostHrace = 20
    velikostHrace = 60
    global hracRect, hracAnimace
    hracRect = pygame.Rect(rozliseniObrazovky[0]/2 - velikostHrace/2, rozliseniObrazovky[1]/2 - velikostHrace/2, velikostHrace, velikostHrace)
    hracAnimace = 0 #0 idle, 1 left, 2, top, 3 right, 4 down
    

    cooldown = 200 # (60/cooldown)krat za sekundu muzes vystrelit
    global last_shot_time
    last_shot_time = 0

    global topLeftWall, leftTopWall, topRightWall, rightTopWall, rightDownWall, downRightWall, LefDowntWall, DownLeftWall, leftPlug, rightPlug, horniPlug, dolniPlug
    global poziceHracePredPohybem
    poziceHracePredPohybem = pygame.Rect(0, 0, 0, 0)

    background = pygame.image.load("source/textures/background.png")
    rammerTexture = pygame.image.load('source/textures/rammerTexture.png')
    playerTextureDown = pygame.image.load("source/textures/player_down.png")
    playerTextureLeft = pygame.image.load("source/textures/player_left.png")
    playerTextureRight = pygame.image.load("source/textures/player_right.png")
    playerTextureUp = pygame.image.load("source/textures/player_up.png")
    playerTextureIdle = pygame.image.load("source/textures/player_idle.png")

    sentryCannon = pygame.image.load("source/textures/sentry_canon.png").convert_alpha()
    sentryCannon = pygame.transform.scale(sentryCannon, (108, 40))

    sentryBase = pygame.image.load("source/textures/sentry_base.png")
    sentryBase = pygame.transform.scale(sentryBase, (112, 112))

    listProjectilu = []
    class Projectile:
        def __init__(self, projectileRect, angle, penetration=1):
            self.projectileRect = projectileRect
            self.angle = angle
            self.rychlost = 15 #rychlost kulky
            self.penetration = penetration #kolikrát může hitnou kulka aka kolik ma zivotu

        def movement(self):
            self.projectileRect[0] += math.cos(self.angle) * self.rychlost
            self.projectileRect[1] += math.sin(self.angle) * self.rychlost

        def draw(self, okno):
            pygame.draw.circle(okno, (255, 255, 255), (self.projectileRect[0], self.projectileRect[1]), self.projectileRect[2])

        def despawn(self, resolution): # vrati true kdyz je venku z mapy nebo kulka nema "hp"
            return self.projectileRect[0] < 0 or self.projectileRect[0] > resolution[0] or self.projectileRect[1] < 0 or self.projectileRect[1] > resolution[1] or self.penetration < 1
           
    def updateProjectileClass(listProjectiluIndex, rozliseniObrazovky):
        for projectily in listProjectiluIndex[:]:
            projectily.movement()
            projectily.draw(okno)

            if projectily.despawn(rozliseniObrazovky):
                listProjectiluIndex.remove(projectily)
            
            #pygame.Rect.collidelist() returns zero if no collision, otherwise returns index of collided rect
            if pygame.Rect.collidelist(projectily.projectileRect, [topLeftWall, leftTopWall, topRightWall, rightTopWall, rightDownWall, downRightWall, LefDowntWall, DownLeftWall]) >= 0:
                listProjectiluIndex.remove(projectily)
            
    listRammer = []
    class Rammer:
        def __init__(self, rammerRect, hp):
            # Convert tuple to pygame.Rect if necessary
            if isinstance(rammerRect, tuple):
                self.rammerRect = pygame.Rect(rammerRect)  # Converts tuple (x, y, width, height) to pygame.Rect
            elif isinstance(rammerRect, pygame.Rect):
                self.rammerRect = rammerRect
            else:
                raise ValueError("rammerRect must be a tuple or pygame.Rect")

            self.velikost = self.rammerRect.width  # The size is now the width of the rectangle
            self.hp = hp

            self.currentAcceleration = 0
            self.INCchangeInAccelaration = 0.5
            self.DECchangeInAccelaration = 0.5
            self.maxSpeed = 6


        def draw(self, okno):
            # pygame.draw.rect(okno, (255, 0, 0), self.rammerRect)
            okno.blit(rammerTexture, self.rammerRect)

        def detekceKulek(self, listProjectilu):
            for projectil in listProjectilu:
                if pygame.Rect.colliderect(projectil.projectileRect, self.rammerRect):
                    #když projectil a rammer střetne
                    listProjectilu.remove(projectil)
                    self.hp -= 10


        def attack(self, hracRect):
            # Calculate the center of the player and the rammer
            centerOfPlayer = pygame.Vector2(hracRect[0] + velikostHrace / 2, hracRect[1] + velikostHrace / 2)
            centerRammer = pygame.Vector2(self.rammerRect.center)  # Use the center of the pygame.Rect

            # Calculate the direction from the rammer to the player
            direction = centerOfPlayer - centerRammer

            # Ensure direction is normalized and non-zero
            if direction.length() > 0:
                direction = direction.normalize()

            # Handle acceleration and deceleration based on movement
            if HracSeHybe: 
                self.currentAcceleration += self.INCchangeInAccelaration
                if self.currentAcceleration > self.maxSpeed:
                    self.currentAcceleration = self.maxSpeed
            else:
                self.currentAcceleration -= self.DECchangeInAccelaration/2 #/2 so they glide longer
                if self.currentAcceleration < 0:
                    self.currentAcceleration = 0

            # Update the rammer's position based on the current acceleration and direction
            self.rammerRect.x += int(self.currentAcceleration * direction.x)
            self.rammerRect.y += int(self.currentAcceleration * direction.y)


    def rammerClassUpdate(listRammer):
        for rammer in listRammer[:]:
            rammer.draw(okno)
            rammer.attack(hracRect)
            rammer.detekceKulek(grid[current_room[0],current_room[1]][3])

            if rammer.hp <= 0:
                listRammer.remove(rammer)


    def spawnNumberOfRammers(numberOfRammers, list, rozliseniObrazovky, wallWidth):
        for number in range(numberOfRammers):
            rammerRect = (random.randint(wallWidth, rozliseniObrazovky[0] - wallWidth - 60),#X
                          random.randint(wallWidth, rozliseniObrazovky[1] - wallWidth - 60),
                          60, 60) #velikost
            list.append(Rammer(rammerRect, 50))

    class Sentry:
        def __init__(self, cordX, cordY):
            self.cordX = cordX
            self.cordY = cordY
            self.velikost = 90
            self.sentryRect = pygame.Rect(self.cordX, self.cordY, self.velikost, self.velikost)
            self.textureCannon = sentryCannon
            self.textureBase = sentryBase
            self.angleOfCannon = 0
            self.cannon_rect = pygame.Rect(0, 0, 0, 0)

        def draw(self):
            okno.blit(self.textureBase, self.sentryRect)
            okno.blit(self.textureCannon, self.cannon_rect)

        def rotateCannon(self):
            mousePos = pygame.mouse.get_pos()

            x_dist = mousePos[0] - self.cordX
            y_dist = -(mousePos[1] - self.cordY)
            angle = math.degrees(math.atan2(y_dist, x_dist))

            self.textureCannon = pygame.transform.rotate(sentryCannon, angle - 180)
            self.cannon_rect = self.textureCannon.get_rect(center = (self.cordX + 54, self.cordY + 54))

    def sentryClassUpdate(listSentry):
        for sentry in listSentry:
            sentry.draw()
            sentry.rotateCannon()

    def SpawnNumberOfSentry(numberOfSentry, list, rozliseniObrazovky, wallWidth):
        for number in range(numberOfSentry):
            list.append(Sentry((random.randint(wallWidth + 60, rozliseniObrazovky[0] - wallWidth - 120)), #cordX
                               (random.randint(wallWidth + 60, rozliseniObrazovky[1] - wallWidth - 120)) #cordY
                                ))

    grid[middlecord[0],middlecord[1]] = 2
    #sets the middle of map (spawn room) room types
    #iterates over whole grid  --------- Allows to store list in elements       
    for element in numpy.nditer(grid, flags=['multi_index', 'refs_ok'],op_flags=['readwrite']): 
        if element >= 1 : #iterates over every room (isn't 0 in grid)
            # [0type, 1layout, 2[listOfRammers], 3[listOfProjectiles], 4[listOfSentries]]

            #Temporar var
            roomType = int(element) #if room is normal (#1), spawn (2#), etc
            roomLayout = random.randint(1,1) #currently only one layout (shape of walls)
            listOfRammers = [] #apeend class times number of enemies supposed to be in room (random * difficulty)
            listOfProjectiles = [] #empty till bullets are shot from player
            listOfSentry = [] #list of sentryes in room


            spawnNumberOfRammers(random.randint(1, 3), listOfRammers, rozliseniObrazovky, wallWidth)
            SpawnNumberOfSentry(random.randint(0, 2), listOfSentry, rozliseniObrazovky, wallWidth)

            # [...] edits the original array instead of creating temporary array (from numpy)       
            element[...] = [
                roomType,
                roomLayout, 
                listOfRammers, 
                listOfProjectiles,
                listOfSentry
            ] 

    #Empties the spawn room list of rammer, aka removes all rammer from spawn room
    grid[middlecord[0], middlecord[1]][2] = []
    grid[middlecord[0], middlecord[1]][4] = []


    def KontrolaOutOfBounds(rozliseni, Grid):
        velikostHrace = hracRect[2]
        try: 
            if hracRect[0] < 0 - velikostHrace and Grid[current_room[0], current_room[1] - 1] != 0: #VLEVO, kontrola jestli roomka do ktery chce vejít existuje
                current_room[1] -= 1
                hracRect[0] = (rozliseni[0] - velikostHrace) #sets player at oposite side of screen
                hracRect[1] = rozliseni[1]/2 - velikostHrace/2 #middle of opposite 
        
            elif hracRect[0] >= rozliseni[0] and Grid[current_room[0], current_room[1] + 1] != 0: #pravo
                current_room[1] += 1
                hracRect[0] = 0 - velikostHrace
                hracRect[1] = rozliseni[1]/2 - velikostHrace/2
        
            elif hracRect[1] < 0 - velikostHrace and Grid[current_room[0] - 1, current_room[1]] != 0: #horni
                current_room[0] -= 1
                hracRect[1] = rozliseni[1]
                hracRect[0] = rozliseni[0]/2 - velikostHrace/2
                
            elif hracRect[1] >= rozliseni[1] and Grid[current_room[0] + 1, current_room[1]] != 0: #dole
                current_room[0] += 1
                hracRect[1] = 0 - velikostHrace
                hracRect[0] = rozliseni[0]/2 - velikostHrace/2
        except IndexError:
            print("ERROR")

        

    #NOTE need to make local function
    def vystreleniProjectilu(listProjectilu, hracRect, current_time):
        global last_shot_time
        # Střelba projektilů při kliknutí myší
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Vypočítání úhlu střelby
        rel_x, rel_y = mouse_x - (hracRect[0] + velikostHrace/2), mouse_y - (hracRect[1] + velikostHrace/2)
        angle = math.atan2(rel_y, rel_x)
        listProjectilu.append(Projectile(pygame.Rect(hracRect[0] + velikostHrace/2, hracRect[1] + velikostHrace/2, 5, 5), angle, 1))
        #append to 3th index of a list in grid(2d array)
        grid[current_room[0],current_room[1]][3].append(Projectile(pygame.Rect(hracRect[0] + velikostHrace/2, hracRect[1] + velikostHrace/2, 5, 5), angle, 1))
        last_shot_time = current_time  # čas posledního výstřelu

    def DrawRoom(): #Draws walls
        global topLeftWall, leftTopWall, topRightWall, rightTopWall, rightDownWall, downRightWall, LefDowntWall, DownLeftWall, leftPlug, rightPlug, horniPlug, dolniPlug
        leftTopWall = pygame.draw.rect(okno, wallColour, (0,0, wallWidth, rozliseniObrazovky[1]/2 - holeSize/2))
        topLeftWall = pygame.draw.rect(okno, wallColour, (0,0, rozliseniObrazovky[0]/2 - holeSize/2, wallWidth))

        topRightWall = pygame.draw.rect(okno, wallColour, (rozliseniObrazovky[0]/2 + holeSize/2, 0, rozliseniObrazovky[0]/2 - holeSize/2, wallWidth))
        rightTopWall = pygame.draw.rect(okno, wallColour, (rozliseniObrazovky[0] - wallWidth, 0, wallWidth, rozliseniObrazovky[1]/2 - holeSize/2))

        rightDownWall = pygame.draw.rect(okno, wallColour, (rozliseniObrazovky[0] - wallWidth, rozliseniObrazovky[1]/2 + holeSize/2, wallWidth, rozliseniObrazovky[1]/2 - holeSize/2))
        downRightWall = pygame.draw.rect(okno, wallColour, (rozliseniObrazovky[0]/2 + holeSize/2, rozliseniObrazovky[1] - wallWidth, rozliseniObrazovky[0]/2 - wallWidth/2, wallWidth))

        LefDowntWall = pygame.draw.rect(okno, wallColour, (0, rozliseniObrazovky[1]/2 + holeSize/2, wallWidth, rozliseniObrazovky[1]/2 - holeSize/2))
        DownLeftWall = pygame.draw.rect(okno, wallColour, (0, rozliseniObrazovky[1] - wallWidth, rozliseniObrazovky[0]/2 - holeSize/2, wallWidth))

        #draw plug 'door' if the room that it leads to doesnt exist
        #Error handling because it threw error when it tried to check a room that was outside of array
        leftPlugRect = (0, 0, 0, 0)
        try: 
            if grid[current_room[0], current_room[1] - 1] == 0: #VLEVO
                leftPlugRect = (0, rozliseniObrazovky[1]/2 - holeSize/2, wallWidth, holeSize)
                leftPlug = pygame.draw.rect(okno, plugColor, leftPlugRect)
        except IndexError:
            leftPlugRect = (0, rozliseniObrazovky[1]/2 - holeSize/2, wallWidth, holeSize)
            leftPlug = pygame.draw.rect(okno, plugColor, leftPlugRect)
            
        rightPlugRect = (0, 0, 0, 0)
        try: 
            if grid[current_room[0], current_room[1] + 1] == 0: #pravo
                rightPlugRect = (rozliseniObrazovky[0] - wallWidth, rozliseniObrazovky[1]/2 - holeSize/2, wallWidth, holeSize)
                rightPlug = pygame.draw.rect(okno, plugColor, rightPlugRect)
        except IndexError:
            rightPlugRect = (rozliseniObrazovky[0] - wallWidth, rozliseniObrazovky[1]/2 - holeSize/2, wallWidth, holeSize)
            rightPlug = pygame.draw.rect(okno, plugColor, rightPlugRect)
            
        horniPlugRect = (0, 0, 0, 0)
        try: 
            if grid[current_room[0] - 1, current_room[1]] == 0: #horni
                horniPlugRect = (rozliseniObrazovky[0]/2 - holeSize/2, 0, holeSize, wallWidth)
                horniPlug = pygame.draw.rect(okno, plugColor, horniPlugRect)
        except IndexError:
            horniPlugRect = (rozliseniObrazovky[0]/2 - holeSize/2, 0, holeSize, wallWidth)
            horniPlug = pygame.draw.rect(okno, plugColor, horniPlugRect)
            
        dolniPlugRect = (0, 0, 0, 0)
        try: 
            if grid[current_room[0] + 1, current_room[1]] == 0: #dole
                dolniPlugRect = (rozliseniObrazovky[0]/2 - holeSize/2, rozliseniObrazovky[1] - wallWidth, holeSize, wallWidth)
                dolniPlug = pygame.draw.rect(okno, plugColor, dolniPlugRect)
        except IndexError:
            dolniPlugRect = (rozliseniObrazovky[0]/2 - holeSize/2, rozliseniObrazovky[1] - wallWidth, holeSize, wallWidth)
            dolniPlug = pygame.draw.rect(okno, plugColor, dolniPlugRect)
            
        global hracRect
        if pygame.Rect.collidelist(hracRect, [topLeftWall, leftTopWall, topRightWall, rightTopWall, rightDownWall, downRightWall, LefDowntWall, DownLeftWall, leftPlugRect, rightPlugRect, horniPlugRect, dolniPlugRect]) >= 0:
            hracRect = copy.copy(playerPosBefore)

    def pohybHrace(hrac_rect, key_press):
        global HracSeHybe, playerPosBefore, hracAnimace
        playerPosBefore = copy.copy(hrac_rect)

        if key_press[pygame.K_s]:
            hrac_rect[1] += rychlostHrace
            hracAnimace = 4

        if key_press[pygame.K_w]:
            hrac_rect[1] -= rychlostHrace
            hracAnimace = 2

        if key_press[pygame.K_d]:
            hrac_rect[0] += rychlostHrace
            hracAnimace = 3

        if key_press[pygame.K_a]:
            hrac_rect[0] -= rychlostHrace
            hracAnimace = 1

        if not any(key_press):
            hracAnimace = 0

        #Rammer's player movement detection
        if hrac_rect != playerPosBefore:
            HracSeHybe = True
        else: 
            HracSeHybe = False

    def DrawPlayer():
        match hracAnimace:
            case 1: #left
                okno.blit(playerTextureLeft, hracRect)
            case 2: #up
                okno.blit(playerTextureUp, hracRect)
            case 3: #left
                okno.blit(playerTextureRight, hracRect)
            case 4: #down
                okno.blit(playerTextureDown, hracRect)
            case 0: #idle
                okno.blit(playerTextureIdle, hracRect)
            

    def update():
        global poziceHracePredPohybem
        okno.blit(background, [0, 0])

        #STŘELBA  ----  Vystřelí když uběhl cooldown od posledního výstřelu
        if pygame.mouse.get_pressed()[0] and current_time - last_shot_time >= cooldown:
            vystreleniProjectilu(listProjectilu, hracRect, current_time)
        updateProjectileClass(grid[current_room[0],current_room[1]][3], rozliseniObrazovky)

        #RAMMERS  ----
        rammerClassUpdate(grid[current_room[0],current_room[1]][2])

        #Sentry
        sentryClassUpdate(grid[current_room[0],current_room[1]][4])

        #POHYB    ----  
        DrawRoom() #zdi
        pohybHrace(hracRect, key_press)
        KontrolaOutOfBounds(rozliseniObrazovky, grid)

        DrawPlayer()
        pygame.display.update() 


    runOneTime = 0
    while True:
        clock.tick(60) #FPS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        current_time = pygame.time.get_ticks()
        key_press = pygame.key.get_pressed()


        
        if runOneTime == 0:
            #stabilazes the rammer's player movement detection
            pohybHrace(hracRect, key_press)
            runOneTime = 1

        if key_press[pygame.K_ESCAPE]:
            sys.exit()


        update()

################################################################################################################################################################################################################################
if __name__ == '__main__':
    Main()