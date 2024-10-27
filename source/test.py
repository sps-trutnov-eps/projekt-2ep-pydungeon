import pygame, sys, copy, numpy, random, math
import levelGeneration

def Main():
    pygame.init()

    # Global variables that were implicitly referenced
    global HracSeHybe, current_time, key_press
    HracSeHybe = False
    
    holeSize = 250
    wallWidth = 100
    wallColour = (0, 255, 115)
    plugColor = (25, 200, 115)
    backgroundColor = (179, 0, 179)
    rozliseniObrazovky = (1920, 1080)

    okno = pygame.display.set_mode((rozliseniObrazovky))
    clock = pygame.time.Clock()

    grid = levelGeneration.map #recieves random map from levelGeneration.py    Type -> numpy.array
    middlecord = copy.copy(levelGeneration.middlecords) #middle of grid
    global current_room
    current_room = copy.copy(middlecord) #sets current room at middle (spawn room)
    print(grid)

    rychlostHrace = 5
    velikostHrace = 60
    barvaHrace = (128, 159, 255)
    hracRect = pygame.Rect(rozliseniObrazovky[0]/2 - velikostHrace/2, rozliseniObrazovky[1]/2 - velikostHrace/2, velikostHrace, velikostHrace)

    cooldown = 200 # (60/cooldown)krat za sekundu muzes vystrelit
    global last_shot_time
    last_shot_time = 0
    rammerMoving = False
    last_time_pressed = 0
    pauseCooldown = 500

    playerPosBefore = (0,0)
    
    # Wall rectangles made global for access in other functions
    global topLeftWall, leftTopWall, topRightWall, rightTopWall, rightDownWall, downRightWall, LefDowntWall, DownLeftWall
    
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
            
            if pygame.Rect.collidelist(projectily.projectileRect, [topLeftWall, leftTopWall, topRightWall, rightTopWall, rightDownWall, downRightWall, LefDowntWall, DownLeftWall]) >= 0:
                listProjectiluIndex.remove(projectily)
            
    listRammer = []
    class Rammer:
        def __init__(self, rammerRect, hp):
            if isinstance(rammerRect, tuple):
                self.rammerRect = pygame.Rect(*rammerRect)  # Unpack tuple for Rect constructor
            elif isinstance(rammerRect, pygame.Rect):
                self.rammerRect = rammerRect
            else:
                raise ValueError("rammerRect must be a tuple or pygame.Rect")

            self.velikost = self.rammerRect.width
            self.hp = hp

            self.currentAcceleration = 0
            self.INCchangeInAccelaration = 0.5
            self.DECchangeInAccelaration = 0.5
            self.maxSpeed = 6

        def draw(self, okno):
            pygame.draw.rect(okno, (255, 0, 0), self.rammerRect)

        def detekceKulek(self, listProjectilu):
            for projectil in listProjectilu[:]:  # Use slice to avoid modification during iteration
                if pygame.Rect.colliderect(projectil.projectileRect, self.rammerRect):
                    listProjectilu.remove(projectil)
                    self.hp -= 10

        def attack(self, hracRect):
            centerOfPlayer = pygame.Vector2(hracRect[0] + velikostHrace / 2, hracRect[1] + velikostHrace / 2)
            centerRammer = pygame.Vector2(self.rammerRect.center)

            direction = centerOfPlayer - centerRammer

            if direction.length() > 0:
                direction = direction.normalize()

            if HracSeHybe: 
                self.currentAcceleration += self.INCchangeInAccelaration
                if self.currentAcceleration > self.maxSpeed:
                    self.currentAcceleration = self.maxSpeed
            else:
                self.currentAcceleration -= self.DECchangeInAccelaration/2
                if self.currentAcceleration < 0:
                    self.currentAcceleration = 0

            self.rammerRect.x += int(self.currentAcceleration * direction.x)
            self.rammerRect.y += int(self.currentAcceleration * direction.y)

    def rammerClassUpdate(listRammer):
        for rammer in listRammer[:]:  # Use slice to avoid modification during iteration
            rammer.draw(okno)
            rammer.attack(hracRect)
            rammer.detekceKulek(grid[current_room[0],current_room[1]][3])

            if rammer.hp <= 0:
                listRammer.remove(rammer)

    def spawnNumberOfRammers(numberOfRammers, list, rozliseniObrazovky, wallWidth):
        for number in range(numberOfRammers):
            rammerRect = (random.randint(wallWidth, rozliseniObrazovky[0] - wallWidth - 60),
                          random.randint(wallWidth, rozliseniObrazovky[1] - wallWidth - 60),
                          60, 60)
            list.append(Rammer(rammerRect, 50))


    grid[middlecord[0],middlecord[1]] = 2
    #sets the middle of map (spawn room) room types
    #iterates over whole grid  --------- Allows to store list in elements       
    for element in numpy.nditer(grid, flags=['multi_index', 'refs_ok'],op_flags=['readwrite']): 
        if element >= 1 : #iterates over every room (isn't 0 in grid)
            # [0type, 1layout, 2[listOfRammers], 3[listOfProjectiles]]

            #Temporar var
            roomType = int(element) #if room is normal (#1), spawn (2#), etc
            roomLayout = random.randint(1,1) #currently only one layout (shape of walls)
            listOfRammers = [] #apeend class times number of enemies supposed to be in room (random * difficulty)
            listOfProjectiles = [] #empty till bullets are shot from player


            spawnNumberOfRammers(random.randint(1, 3), listOfRammers, rozliseniObrazovky, wallWidth)

            # [...] edits the original array instead of creating temporary array (from numpy)       
            element[...] = [
                roomType,
                roomLayout, 
                listOfRammers, 
                listOfProjectiles
            ] 
    #Empties the spawn room list of rammer, aka removes all rammer from spawn room
    grid[middlecord[0], middlecord[1]][2] = []


    def pohybHrace(hrac_rect, key_press):
        global HracSeHybe
        playerPosBefore = copy.copy(hrac_rect)

        if key_press[pygame.K_s]:
            hrac_rect[1] += rychlostHrace
        if key_press[pygame.K_w]:
            hrac_rect[1] -= rychlostHrace
        if key_press[pygame.K_d]:
            hrac_rect[0] += rychlostHrace
        if key_press[pygame.K_a]:
            hrac_rect[0] -= rychlostHrace

        if list(hrac_rect) != list(playerPosBefore):  # Convert to list for comparison
            HracSeHybe = True
        else: 
            HracSeHybe = False

    def KontrolaOutOfBounds(rozliseni): 
        velikostHrace = hracRect[2]
        
        # Return coordinates for center of room
        center_x = rozliseni[0]/2 - velikostHrace/2
        center_y = rozliseni[1]/2 - velikostHrace/2
        
        def isValidRoom(room_element):
            """Check if the room exists and is accessible"""
            # If room_element is a list (initialized room), check first element
            if isinstance(room_element, (list, numpy.ndarray)):
                return room_element[0] != 0
            # If room_element is a number (uninitialized room), check its value
            return room_element != 0
        
        try:
            if hracRect[0] < 0 - velikostHrace: #vlevo
                next_room = grid[current_room[0] - 1, current_room[1]]
                if isValidRoom(next_room):
                    current_room[1] -= 1
                    hracRect[0] = (rozliseni[0] - velikostHrace)
                    hracRect[1] = rozliseni[1]/2 - velikostHrace/2
                else:
                    hracRect[0] = center_x
                    hracRect[1] = center_y

            elif hracRect[0] >= rozliseni[0]: #pravo
                next_room = grid[current_room[0] + 1, current_room[1]]
                if isValidRoom(next_room):
                    current_room[1] += 1
                    hracRect[0] = 0 - velikostHrace
                    hracRect[1] = rozliseni[1]/2 - velikostHrace/2
                else:
                    hracRect[0] = center_x
                    hracRect[1] = center_y

            elif hracRect[1] < 0 - velikostHrace: #horni
                next_room = grid[current_room[0], current_room[1] - 1]
                if isValidRoom(next_room):
                    current_room[0] -= 1
                    hracRect[1] = rozliseni[1]
                    hracRect[0] = rozliseni[0]/2 - velikostHrace/2
                else:
                    hracRect[0] = center_x
                    hracRect[1] = center_y

            elif hracRect[1] >= rozliseni[1]: #dole
                next_room = grid[current_room[0], current_room[1] + 1]
                if isValidRoom(next_room):
                    current_room[0] += 1
                    hracRect[1] = 0 - velikostHrace
                    hracRect[0] = rozliseni[0]/2 - velikostHrace/2
                else:
                    hracRect[0] = center_x
                    hracRect[1] = center_y
                    
        except IndexError:
            # If we try to access a room outside the grid boundaries
            hracRect[0] = center_x
            hracRect[1] = center_y
            
    def vystreleniProjectilu(listProjectilu, hracRect, current_time):
        global last_shot_time
        mouse_x, mouse_y = pygame.mouse.get_pos()

        rel_x, rel_y = mouse_x - (hracRect[0] + velikostHrace/2), mouse_y - (hracRect[1] + velikostHrace/2)
        angle = math.atan2(rel_y, rel_x)
        listProjectilu.append(Projectile(pygame.Rect(hracRect[0] + velikostHrace/2, hracRect[1] + velikostHrace/2, 5, 5), angle, 1))
        grid[current_room[0],current_room[1]][3].append(Projectile(pygame.Rect(hracRect[0] + velikostHrace/2, hracRect[1] + velikostHrace/2, 5, 5), angle, 1))
        last_shot_time = current_time

    def DrawRoom():
        global topLeftWall, leftTopWall, topRightWall, rightTopWall, rightDownWall, downRightWall, LefDowntWall, DownLeftWall
        
        leftTopWall = pygame.draw.rect(okno, wallColour, (0,0, wallWidth, rozliseniObrazovky[1]/2 - holeSize/2))
        topLeftWall = pygame.draw.rect(okno, wallColour, (0,0, rozliseniObrazovky[0]/2 - holeSize/2, wallWidth))
        
        topRightWall = pygame.draw.rect(okno, wallColour, (rozliseniObrazovky[0]/2 + holeSize/2, 0, rozliseniObrazovky[0]/2 - holeSize/2, wallWidth))
        rightTopWall = pygame.draw.rect(okno, wallColour, (rozliseniObrazovky[0] - wallWidth, 0, wallWidth, rozliseniObrazovky[1]/2 - holeSize/2))
        
        rightDownWall = pygame.draw.rect(okno, wallColour, (rozliseniObrazovky[0] - wallWidth, rozliseniObrazovky[1]/2 + holeSize/2, wallWidth, rozliseniObrazovky[1]/2 - holeSize/2))
        downRightWall = pygame.draw.rect(okno, wallColour, (rozliseniObrazovky[0]/2 + holeSize/2, rozliseniObrazovky[1] - wallWidth, rozliseniObrazovky[0]/2 - wallWidth/2, wallWidth))
        
        LefDowntWall = pygame.draw.rect(okno, wallColour, (0, rozliseniObrazovky[1]/2 + holeSize/2, wallWidth, rozliseniObrazovky[1]/2 - holeSize/2))
        DownLeftWall = pygame.draw.rect(okno, wallColour, (0, rozliseniObrazovky[1] - wallWidth, rozliseniObrazovky[0]/2 - holeSize/2, wallWidth))
        
    def draw(current_room):
        DrawRoom()

    def update():
        okno.fill(backgroundColor)

        if pygame.mouse.get_pressed()[0] and current_time - last_shot_time >= cooldown:
            vystreleniProjectilu(listProjectilu, hracRect, current_time)

        updateProjectileClass(grid[current_room[0],current_room[1]][3], rozliseniObrazovky)
        rammerClassUpdate(grid[current_room[0],current_room[1]][2])

        pohybHrace(hracRect, key_press)
        KontrolaOutOfBounds(rozliseniObrazovky)

        pygame.draw.rect(okno, barvaHrace, hracRect)
        draw(current_room)
        pygame.display.update() 

    runOneTime = 0
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        current_time = pygame.time.get_ticks()
        key_press = pygame.key.get_pressed()
        
        if runOneTime == 0:
            current_room = [0, 0]
            pohybHrace(hracRect, key_press)
            runOneTime = 1

        if key_press[pygame.K_ESCAPE]:
            sys.exit()


        update()

if __name__ == '__main__':
    Main()