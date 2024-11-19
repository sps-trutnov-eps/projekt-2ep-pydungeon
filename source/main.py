import pygame, sys, copy, numpy, random, math
import levelGeneration

def Menu():
    okno = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption('Game Menu')
    background = pygame.image.load("source/textures/menu_background.png")
    

    while True:
        for event in pygame.event.get():
         if event.type == pygame.QUIT:
            sys.exit()
        mouse_x, mouse_y = pygame.mouse.get_pos()


        if (764 <= mouse_x <= 1156) and (328 <= mouse_y <= 442) and event.type == pygame.MOUSEBUTTONDOWN: # souřadnice tlačítka(764, 328) (1156, 442)
            Main()

        okno.blit(background, [0,0])
        pygame.display.flip()



def Main():
    pygame.init()

    holeSize = 250
    wallWidth = 100
    wallColour = (51, 46, 37)
    #plugColor = (45, 40, 29)
    plugColor = (51, 46, 37)
    rozliseniObrazovky = (1920, 1080)
    bossWallWidth = 50
    global barvyPresPlate
    barvyPresPlate = [(255, 0, 0), (255, 0, 0), (255, 0, 0), (255, 0, 0)]

    okno = pygame.display.set_mode((rozliseniObrazovky))
    clock = pygame.time.Clock()

    numberOfRooms = levelGeneration.numberOfRooms
    grid = levelGeneration.map #recieves random map from levelGeneration.py    Type -> numpy.array
    middlecord = copy.copy(levelGeneration.middlecords) #middle of grid
    current_room = copy.copy(middlecord) #sets current room at middle (spawn room)
    print(grid)

    rychlostHrace = 10
    velikostHrace = 60
    global hracRect, hracAnimace, hracHP
    hracRect = pygame.Rect(rozliseniObrazovky[0]/2 - velikostHrace/2 + 250, rozliseniObrazovky[1]/2 - velikostHrace/2 + 250, velikostHrace, velikostHrace)
    hracAnimace = 0 #0 idle, 1 left, 2, top, 3 right, 4 down
    hracHP = 100
    hracMaximumHp = copy.copy(hracHP)

    global currentXP, maxXP
    currentXP = 0
    maxXP = 100
    
    cooldown = 200 # (60/cooldown)krat za sekundu muzes vystrelit
    global last_shot_time
    last_shot_time = 0

    pocetNepratel = 0

    global topLeftWall, leftTopWall, topRightWall, rightTopWall, rightDownWall, downRightWall, LefDowntWall, DownLeftWall, leftPlug, rightPlug, horniPlug, dolniPlug
    global bossTopWall, bossLeftWall, bossDownWall, bossRightWall

    leftTopWall = pygame.draw.rect(okno, wallColour, (0,0, wallWidth, rozliseniObrazovky[1]/2 - holeSize/2))
    topLeftWall = pygame.draw.rect(okno, wallColour, (0,0, rozliseniObrazovky[0]/2 - holeSize/2, wallWidth))

    topRightWall = pygame.draw.rect(okno, wallColour, (rozliseniObrazovky[0]/2 + holeSize/2, 0, rozliseniObrazovky[0]/2 - holeSize/2, wallWidth))
    rightTopWall = pygame.draw.rect(okno, wallColour, (rozliseniObrazovky[0] - wallWidth, 0, wallWidth, rozliseniObrazovky[1]/2 - holeSize/2))

    rightDownWall = pygame.draw.rect(okno, wallColour, (rozliseniObrazovky[0] - wallWidth, rozliseniObrazovky[1]/2 + holeSize/2, wallWidth, rozliseniObrazovky[1]/2 - holeSize/2))
    downRightWall = pygame.draw.rect(okno, wallColour, (rozliseniObrazovky[0]/2 + holeSize/2, rozliseniObrazovky[1] - wallWidth, rozliseniObrazovky[0]/2 - wallWidth/2, wallWidth))

    LefDowntWall = pygame.draw.rect(okno, wallColour, (0, rozliseniObrazovky[1]/2 + holeSize/2, wallWidth, rozliseniObrazovky[1]/2 - holeSize/2))
    DownLeftWall = pygame.draw.rect(okno, wallColour, (0, rozliseniObrazovky[1] - wallWidth, rozliseniObrazovky[0]/2 - holeSize/2, wallWidth))

    bossTopWall = pygame.draw.rect(okno, wallColour, (0, 0, rozliseniObrazovky[0], bossWallWidth))
    bossLeftWall = pygame.draw.rect(okno, wallColour, (0, 0, bossWallWidth, rozliseniObrazovky[0]))
    bossDownWall = pygame.draw.rect(okno, wallColour, (0, rozliseniObrazovky[1] - bossWallWidth, rozliseniObrazovky[0], bossWallWidth))
    bossRightWall = pygame.draw.rect(okno, wallColour, (rozliseniObrazovky[0] - bossWallWidth, 0, bossWallWidth, rozliseniObrazovky[1]))

    global poziceHracePredPohybem
    poziceHracePredPohybem = pygame.Rect(0, 0, 0, 0)

    scalingFactorGOB = 4
    gameOverBanner = pygame.image.load("source/textures/gameOverBanner.png")
    gameOverBanner = pygame.transform.scale_by(gameOverBanner, 4)

    bossBackground = pygame.image.load("source/textures/boss_background.png")
    activatedPortalBackground = pygame.image.load("source/textures/activated_background.png")
    initialBackground = pygame.image.load("source/textures/initial_background.png")
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

    myFont = pygame.font.SysFont('Consolas', 30)

    runOneTime = 0
    global runGame, runBossFight
    runGame = 1
    runBossFight = 0
    global spawnBossSequnce
    spawnBossSequnce = 0
    
    global upgradeScreenOn
    upgradeScreenOn = True
    global bossSpawnSequenceFinished
    bossSpawnSequenceFinished = False
    global bossDefeated
    bossDefeated = False

    class Boss:
        def __init__(self):
            self.hp = 1500
            self.maxHP = 1500

            self.velikost = 250
            self.bossRect = pygame.Rect(rozliseniObrazovky[0]/2 - self.velikost/2, rozliseniObrazovky[1]/2 - self.velikost/2, self.velikost, self.velikost)

            self.bossHpRatio = self.hp/self.maxHP

        def draw(self):
            outlineThickness = 25
            pygame.draw.rect(okno, (200, 15, 45), (self.bossRect[0] - outlineThickness, self.bossRect[1] - outlineThickness, self.velikost + outlineThickness*2, self.velikost + outlineThickness*2), outlineThickness)
            pygame.draw.rect(okno, (220, 20, 60), self.bossRect)

        def drawHPbar(self):
            pygame.draw.rect(okno, (35, 25, 50), (59, 1041, 1803, 31)) #gray
            pygame.draw.rect(okno, (200, 15, 45), (59, 1041, 1803*self.bossHpRatio, 31)) #red
            pygame.draw.rect(okno, (15, 15, 15), (51, 1033, 1819, 47), 8) #outline

        def detekceKulek(self, listProjectilu):
            for projectil in listProjectilu:
                if pygame.Rect.colliderect(projectil.projectileRect, self.bossRect):
                    #když projectil a rammer střetne
                    listProjectilu.remove(projectil)
                    self.hp -= projectil.damage

        def updateRatio(self):
            self.bossHpRatio = self.hp / self.maxHP
            
        def kolizeHraceBoss(self):
            global hracHP
            if pygame.Rect.colliderect(hracRect, self.bossRect):
                hracHP -= 10
                self.hp -= 10

    class Projectile:
        def __init__(self, projectileRect, angle, penetration=1):
            self.projectileRect = projectileRect
            self.angle = angle
            self.rychlost = 15 #rychlost kulky
            self.penetration = penetration #kolikrát může hitnou kulka aka kolik ma zivotu
            self.damage = 25

        def movement(self):
            self.projectileRect[0] += math.cos(self.angle) * self.rychlost
            self.projectileRect[1] += math.sin(self.angle) * self.rychlost

        def draw(self, okno):
            pygame.draw.circle(okno, (255, 255, 255), (self.projectileRect[0], self.projectileRect[1]), self.projectileRect[2])

        def despawn(self, resolution): # vrati true kdyz je venku z mapy nebo kulka nema "hp"
            return self.projectileRect[0] < 0 or self.projectileRect[0] > resolution[0] or self.projectileRect[1] < 0 or self.projectileRect[1] > resolution[1] or self.penetration < 1
           
    def updateProjectileClass(listProjectiluIndex, rozliseniObrazovky):
        global bossTopWall, bossLeftWall, bossDownWall, bossRightWall
        for projectily in listProjectiluIndex[:]:
            projectily.movement()
            projectily.draw(okno)

            if projectily.despawn(rozliseniObrazovky):
                listProjectiluIndex.remove(projectily)
                
            
            if runBossFight == 1:
                #pygame.Rect.collidelist() returns zero if no collision, otherwise returns index of collided rect
                if pygame.Rect.collidelist(projectily.projectileRect, [bossTopWall, bossLeftWall, bossDownWall, bossRightWall]) >= 0:
                    listProjectiluIndex.remove(projectily)
            else:
                if pygame.Rect.collidelist(projectily.projectileRect, [topLeftWall, leftTopWall, topRightWall, rightTopWall, rightDownWall, downRightWall, LefDowntWall, DownLeftWall]) >= 0:
                    listProjectiluIndex.remove(projectily)
                    
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
            self.lastShotTime = random.randint(0, 1)/10
            self.cooldown = 100

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
                    self.hp -= projectil.damage

        def ubyraniHP(self):
            global hracHP
            if pygame.Rect.colliderect(hracRect, self.rammerRect):
                if current_time - self.lastShotTime >= self.cooldown:
                    hracHP -= 10
                    self.hp -= 10
                    self.last_shot_time = current_time


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
        global currentXP
        for rammer in listRammer[:]:
            rammer.draw(okno)
            rammer.attack(hracRect)
            rammer.detekceKulek(grid[current_room[0],current_room[1]][3])
            rammer.ubyraniHP()

            if rammer.hp <= 0:
                listRammer.remove(rammer)
                currentXP += 100


    def spawnNumberOfRammers(numberOfRammers, list, rozliseniObrazovky, wallWidth):
        for number in range(numberOfRammers):
            rammerRect = (random.randint(wallWidth, rozliseniObrazovky[0] - wallWidth - 60),#X
                          random.randint(wallWidth, rozliseniObrazovky[1] - wallWidth - 60),
                          60, 60) #velikost
            list.append(Rammer(rammerRect, 50))

    class SentryBullet:
        def __init__(self, cordX, cordY):
            self.cordX = cordX
            self.cordY = cordY
            self.rychlost = 5
            self.sentryBulletRect = pygame.Rect(self.cordX, self.cordY, 15, 15)
            self.penetration = 1 #how many times bullet can hit
            
            dx = hracRect.centerx - self.sentryBulletRect.centerx
            dy = hracRect.centery - self.sentryBulletRect.centery
            distance = math.sqrt(dx**2 + dy**2)

            self.vel_x = (dx / distance) * self.rychlost
            self.vel_y = (dy / distance) * self.rychlost

        def draw(self):
            pygame.draw.circle(okno, (255, 0, 0), (self.sentryBulletRect[0], self.sentryBulletRect[1]), self.sentryBulletRect[2])

        def movement(self):
            self.sentryBulletRect.centerx += self.vel_x
            self.sentryBulletRect.centery += self.vel_y

        def despawn(self, resolution): # vrati true kdyz je venku z mapy nebo kulka nema "hp"
            return self.sentryBulletRect[0] < 0 or self.sentryBulletRect[0] > resolution[0] or self.sentryBulletRect[1] < 0 or self.sentryBulletRect[1] > resolution[1] or self.penetration < 1
           
        def detekceHrace(self):
            global hracHP
            if pygame.Rect.colliderect(hracRect, self.sentryBulletRect):
                self.penetration -= 1
                hracHP -= 10



    def SentryBulletClassUpdate(list):
        for bullet in list:
            bullet.draw()
            bullet.movement()
            bullet.detekceHrace()

            if bullet.despawn(rozliseniObrazovky):
                list.remove(bullet)

            if pygame.Rect.collidelist(bullet.sentryBulletRect, [topLeftWall, leftTopWall, topRightWall, rightTopWall, rightDownWall, downRightWall, LefDowntWall, DownLeftWall]) >= 0:
                try: list.remove(bullet)
                except Exception as e: print(f"error: {e}")

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
            self.lastShotTime = random.randint(0, 1)/10
            self.cooldown = 600
            self.hp = 70

        def draw(self):
            okno.blit(self.textureBase, self.sentryRect)
            okno.blit(self.textureCannon, self.cannon_rect)

        def rotateCannon(self):
            x_dist = hracRect.centerx - self.cordX
            y_dist = -(hracRect.centery - self.cordY)
            self.angleOfCannon = math.degrees(math.atan2(y_dist, x_dist))

            self.textureCannon = pygame.transform.rotate(sentryCannon, self.angleOfCannon - 180)
            self.cannon_rect = self.textureCannon.get_rect(center = (self.cordX + 54, self.cordY + 54))

        def attack(self, list):
            if current_time - self.lastShotTime >= self.cooldown:
                
                list.append(SentryBullet(self.sentryRect.centerx, self.sentryRect.centery))
                self.lastShotTime = current_time
        
        def detekceKulek(self, listProjectilu):
            for projectil in listProjectilu:
                if pygame.Rect.colliderect(projectil.projectileRect, self.sentryRect):
                    listProjectilu.remove(projectil)
                    self.hp -= projectil.damage

        def detekceKolizeHrace(self):
            global hracHP

            if pygame.Rect.colliderect(self.sentryRect, hracRect):
                hracHP -= 10
                self.hp -= 10

    def sentryClassUpdate(listSentry):
        global currentXP
        for sentry in listSentry:
            sentry.draw()
            sentry.rotateCannon()
            sentry.attack(grid[current_room[0],current_room[1]][5])
            sentry.detekceKulek(grid[current_room[0], current_room[1]][3])
            sentry.detekceKolizeHrace()

            if sentry.hp <= 0:
                listSentry.remove(sentry)
                currentXP += 10

    def SpawnNumberOfSentry(numberOfSentry, list, rozliseniObrazovky, wallWidth):
        for number in range(numberOfSentry):
            list.append(Sentry((random.randint(wallWidth + 60, rozliseniObrazovky[0] - wallWidth - 120)), #cordX
                               (random.randint(wallWidth + 60, rozliseniObrazovky[1] - wallWidth - 120)) #cordY
                                ))

    #sets the middle of map (spawn room) room types
    grid[middlecord[0],middlecord[1]] = 2
    #iterates over whole grid  --------- Allows to store list in elements       
    for element in numpy.nditer(grid, flags=['multi_index', 'refs_ok'],op_flags=['readwrite']): 
        if element >= 1 : #iterates over every room (isn't 0 in grid)
            # [0type, 1layout, 2[listOfRammers], 3[listOfProjectiles], 4[listOfSentries], 5[listOfSentryProjectile], 6[listBoss]]

            #Temporar var
            roomType = int(element) #if room is normal (#1), spawn (2#), etc
            roomLayout = random.randint(1,1) #currently only one layout (shape of walls)
            listOfRammers = [] #apeend class times number of enemies supposed to be in room (random * difficulty)
            listOfProjectiles = [] #empty till bullets are shot from player
            listOfSentry = [] #list of sentryes in room
            listOfSentryProjectile = [] #sentries projectile
            listBoss = []

            if roomType == 1:
                pocetSpawnutychRammeru = random.randint(0, 0)
                pocetSpawnutychSentry = random.randint(0, 0)
                spawnNumberOfRammers(pocetSpawnutychRammeru, listOfRammers, rozliseniObrazovky, wallWidth)
                SpawnNumberOfSentry(pocetSpawnutychSentry, listOfSentry, rozliseniObrazovky, wallWidth)
                pocetNepratel += (pocetSpawnutychSentry + pocetSpawnutychRammeru)

            # [...] edits the original array instead of creating temporary array (from numpy)       
            element[...] = [
                roomType,
                roomLayout, 
                listOfRammers, 
                listOfProjectiles,
                listOfSentry,
                listOfSentryProjectile,
                listBoss
            ]

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
        global topLeftWall, leftTopWall, topRightWall, rightTopWall, rightDownWall, downRightWall, LefDowntWall, DownLeftWall, leftPlug, rightPlug, horniPlug, dolniPlug, bossTopWall, bossLeftWall, bossDownWall, bossRightWall
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
        if runBossFight == 0:
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

    def KontrolaTeleportuAHrace(rectHrace):
        global runBossFight, runGame
        teleportRect = pygame.Rect(860, 445, 210, 210)
        if pygame.Rect.colliderect(teleportRect, rectHrace):
            runGame = 0
            runBossFight = 1

    def drawHPbar():
        hracHpRatio = hracHP / hracMaximumHp
        pygame.draw.rect(okno, (35, 25, 50), (50, 10, 500, 20)) #gray
        pygame.draw.rect(okno, (255, 0, 0), (50, 10, 500 * hracHpRatio, 20)) #red
        pygame.draw.rect(okno, (15, 15, 15), (45, 5, 510, 30), 5) #outline

    def drawXpBar():
        xpRatio = currentXP / maxXP
        pygame.draw.rect(okno, (35, 25, 50), (1360, 10, 500, 20)) #gray
        pygame.draw.rect(okno, (96, 245, 22), (1360, 10, 500 * xpRatio, 20)) #green
        pygame.draw.rect(okno, (15, 15, 15), (1360, 5, 505, 30), 5) #outline

    def kontrolaXP():
        global currentXP, maxXP, upgradeScreenOn
        if currentXP >= maxXP:
            currentXP = 0
            maxXP = maxXP*1.5

            upgradeScreenOn = True
            UpgradeScreen()
            print("choose upgrade")

    def UpgradeScreen():
        global upgradeScreenOn
        upgradeScreen = pygame.image.load("source/textures/Upgrade_screen.png")

        upgrade1 = pygame.image.load("source/textures/upgrady/upgrade1.png")
        upgrade2 = pygame.image.load("source/textures/upgrady/upgrade2.png")
        upgrade3 = pygame.image.load("source/textures/upgrady/upgrade3.png")
        listVsechnUpgradu = {"DescriptionOfUpgrade1": upgrade1, "DescriptionOfUpgrade2": upgrade2, "Lonnnnnnnnnnnnnng descriiiiiption of UPPPGRAde numero 3333 a": upgrade3}

        upgradeSelectionNumber = 3
        velikostUpgradu = 360

        listUpgraduNaVybirani = copy.copy(listVsechnUpgradu)

        vybraneUpgrady = []
        vybraneDesc = []
        for i in range(upgradeSelectionNumber):
            upg = random.choice(list(listUpgraduNaVybirani.items()))
            vybraneUpgrady.append(upg[1])
            vybraneDesc.append(upg[0])

            listUpgraduNaVybirani.pop(upg[0])

        while upgradeScreenOn:
            for updateEvent in pygame.event.get():
                if updateEvent.type == pygame.QUIT:
                    sys.exit()

            mouse_x, mouse_y = pygame.mouse.get_pos()
            mouseRect = pygame.Rect(mouse_x, mouse_y, 1, 1)

            okno.blit(upgradeScreen, (0, 0))

            upgradeRect = [pygame.Rect(120, 540, velikostUpgradu, velikostUpgradu), pygame.Rect(760, 540, velikostUpgradu, velikostUpgradu), pygame.Rect(1400, 540, velikostUpgradu, velikostUpgradu)]
            for i in range(upgradeSelectionNumber):
                pygame.draw.rect(okno, (0, 0, 0), ((rozliseniObrazovky[0]/upgradeSelectionNumber*i) + 120, rozliseniObrazovky[1]/2 - velikostUpgradu/2 + 180, velikostUpgradu, velikostUpgradu), 15)
                okno.blit(vybraneUpgrady[i], ((rozliseniObrazovky[0]/upgradeSelectionNumber*i) + 120, rozliseniObrazovky[1]/2 - velikostUpgradu/2 + 180, velikostUpgradu, velikostUpgradu))

                try:
                    if pygame.Rect.colliderect(mouseRect, upgradeRect[i]) and updateEvent.type == pygame.MOUSEBUTTONUP:
                        print(f"Pressed upgrade {vybraneUpgrady[i]}  desc: {vybraneDesc[i]}")
                        upgradeScreenOn = False
                except UnboundLocalError:
                    print("eroorrr") 

            pygame.display.flip()

    def update():
        global poziceHracePredPohybem
        if [current_room[0], current_room[1]] == [middlecord[0], middlecord[1]]:
            if pocetNepratel == 0:
                okno.blit(activatedPortalBackground, [0, 0])
                KontrolaTeleportuAHrace(hracRect)

            else:
                okno.blit(initialBackground, [0, 0])
        else:
            okno.blit(background, [0, 0])

        if hracHP > 0:
            #STŘELBA  ----  Vystřelí když uběhl cooldown od posledního výstřelu
            if pygame.mouse.get_pressed()[0] and current_time - last_shot_time >= cooldown:
                vystreleniProjectilu(grid[current_room[0], current_room[1]][3], hracRect, current_time)
            updateProjectileClass(grid[current_room[0],current_room[1]][3], rozliseniObrazovky)

            #RAMMERS  ----
            rammerClassUpdate(grid[current_room[0],current_room[1]][2])

            #Sentry   ----
            SentryBulletClassUpdate(grid[current_room[0],current_room[1]][5])
            sentryClassUpdate(grid[current_room[0],current_room[1]][4])
            
            #POHYB    ----  
            pohybHrace(hracRect, key_press)
            KontrolaOutOfBounds(rozliseniObrazovky, grid)
            DrawPlayer()

        else:
            okno.fill(wallColour)
            okno.blit(gameOverBanner, (rozliseniObrazovky[0]/2 - gameOverBanner.get_width()/2, rozliseniObrazovky[1]/2 - gameOverBanner.get_height()/2))

        DrawRoom() #zdi

        #Display HP
        HpTextSurface = myFont.render(f"HP: {hracHP}", 1, (255, 255, 255))
        okno.blit(HpTextSurface, (10, 5))

        #display XP text
        XPtextSurface = myFont.render("XP", 1, (255, 255, 255))
        okno.blit(XPtextSurface, (rozliseniObrazovky[0] - 48, 5))

        drawHPbar()
        drawXpBar()
        kontrolaXP()

        pygame.display.update() 

    def DrawBossRoom():
        global bossTopWall, bossLeftWall, bossDownWall, bossRightWall, hracRect
        bossTopWall = pygame.draw.rect(okno, wallColour, (0, 0, rozliseniObrazovky[0], bossWallWidth))
        bossLeftWall = pygame.draw.rect(okno, wallColour, (0, 0, bossWallWidth, rozliseniObrazovky[0]))
        bossDownWall = pygame.draw.rect(okno, wallColour, (0, rozliseniObrazovky[1] - bossWallWidth, rozliseniObrazovky[0], bossWallWidth))
        bossRightWall = pygame.draw.rect(okno, wallColour, (rozliseniObrazovky[0] - bossWallWidth, 0, bossWallWidth, rozliseniObrazovky[1]))

        if pygame.Rect.collidelist(hracRect, [bossTopWall, bossLeftWall, bossDownWall, bossRightWall]) >= 0:
            hracRect = copy.copy(playerPosBefore)


    def drawPresurePlates():
        global spawnBossSequnce
        #Presures plates
        ofsetX, ofsetY = 220, 170
        presPlate1 = pygame.draw.rect(okno, barvyPresPlate[0], (ofsetX + bossWallWidth, ofsetY + bossWallWidth, 60, 60)) #vlevo nahoře [0]
        presPlate2 = pygame.draw.rect(okno, barvyPresPlate[1], (rozliseniObrazovky[0] - (ofsetX + bossWallWidth), ofsetY + bossWallWidth, 60, 60)) #pravo nahoře [1]

        presPlate3 = pygame.draw.rect(okno, barvyPresPlate[2], (ofsetX + bossWallWidth, rozliseniObrazovky[1] - (ofsetY + bossWallWidth), 60, 60)) #vlevo dole [2]
        presPlate4 = pygame.draw.rect(okno, barvyPresPlate[3], (rozliseniObrazovky[0] - (ofsetX + bossWallWidth), rozliseniObrazovky[1] - (ofsetY + bossWallWidth), 60, 60)) #pravo dole [3]
        
        if pygame.Rect.collidelist(hracRect, [presPlate1, presPlate2, presPlate3, presPlate4]) >= 0:
            pressedPresPlate = pygame.Rect.collidelist(hracRect, [presPlate1, presPlate2, presPlate3, presPlate4])
            match pressedPresPlate:
                case 0:
                    barvyPresPlate [0] = (0, 255, 0)
                case 1:
                    barvyPresPlate [1] = (0, 255, 0)
                case 2:
                    barvyPresPlate [2] = (0, 255, 0)
                case 3:
                    barvyPresPlate [3] = (0, 255, 0)

        # if barvyPresPlate == [(0, 255, 0), (0, 255, 0), (0, 255, 0), (0, 255, 0),]:
        #     spawnBossSequnce = 1

        if barvyPresPlate == [(0, 255, 0), (255, 0, 0), (255, 0, 0), (255, 0, 0),]:
            spawnBossSequnce = 1

    def spawnBoss():
        global bossSpawnSequenceFinished

        if bossSpawnSequenceFinished == False:
            #spawn sequnce
            grid[current_room[0],current_room[1]][6].append(Boss())
            bossSpawnSequenceFinished = True

    #boss room
    def updateBoss():
        global bossDefeated
        okno.blit(bossBackground, [0,0])

        if hracHP > 0:
            if spawnBossSequnce == 0:
                drawPresurePlates() #Presure plates

            #STŘELBA  ----  Vystřelí když uběhl cooldown od posledního výstřelu
            if pygame.mouse.get_pressed()[0] and current_time - last_shot_time >= cooldown:
                vystreleniProjectilu(grid[current_room[0], current_room[1]][3], hracRect, current_time)
            updateProjectileClass(grid[current_room[0],current_room[1]][3], rozliseniObrazovky)

            if spawnBossSequnce == 1:
                spawnBoss()

            #POHYB    ----  
            pohybHrace(hracRect, key_press)
            KontrolaOutOfBounds(rozliseniObrazovky, grid)
            DrawPlayer()

            if bossSpawnSequenceFinished:
                for boss in grid[current_room[0],current_room[1]][6]:
                    boss.draw()
                    boss.detekceKulek(grid[current_room[0], current_room[1]][3])
                    boss.updateRatio()
                    boss.kolizeHraceBoss()

                    if boss.hp <= 0:
                        grid[current_room[0],current_room[1]][6].remove(boss)
                        bossDefeated = True
                        

        else:
            okno.fill(wallColour)
            okno.blit(gameOverBanner, (rozliseniObrazovky[0]/2 - gameOverBanner.get_width()/2, rozliseniObrazovky[1]/2 - gameOverBanner.get_height()/2))


        DrawBossRoom() #zdi

        if bossSpawnSequenceFinished:
            for boss in grid[current_room[0],current_room[1]][6]:
                boss.drawHPbar()

        if bossDefeated:
            okno.fill((0, 0, 0))

        #Display HP
        HpTextSurface = myFont.render(f"HP: {hracHP}", 1, (255, 255, 255))
        okno.blit(HpTextSurface, (8, 5))

        #display XP text
        XPtextSurface = myFont.render("XP", 1, (255, 255, 255))
        okno.blit(XPtextSurface, (rozliseniObrazovky[0] - 48, 5))

        drawHPbar()
        drawXpBar()
        kontrolaXP()

        pygame.display.update() 

    while True:
        clock.tick(60) #FPS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        current_time = pygame.time.get_ticks()
        key_press = pygame.key.get_pressed()
        mousePosX, mousePoxY = pygame.mouse.get_pos()
        

        if runOneTime == 0:
            #stabilazes the rammer's player movement detection
            pohybHrace(hracRect, key_press)
            runOneTime = 1

        if key_press[pygame.K_ESCAPE]:
            sys.exit()

        if runBossFight == 0:
            update()
        else:
            updateBoss()

        print(f"X: {mousePosX}, Y: {mousePoxY}")

        


################################################################################################################################################################################################################################

if __name__ == '__main__':
    Menu()
