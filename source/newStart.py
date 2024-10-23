import pygame, sys, copy, numpy, random, math
import levelGeneration

def Main():
    pygame.init()

    holeSize = 250
    wallWidth = 100
    wallColour = (0, 255, 115)
    backgroundColor = (179, 0, 179)
    rozliseniObrazovky = (1920, 1080)

    okno = pygame.display.set_mode((rozliseniObrazovky))
    clock = pygame.time.Clock()

    grid = levelGeneration.map #recieves random map from levelGeneration.py    Type -> numpy.array
    middlecord = copy.copy(levelGeneration.middlecords) #middle of grid
    current_room = copy.copy(middlecord) #sets current room at middle (spawn room)

    rychlostHrace = 5
    velikostHrace = 60
    barvaHrace = (128, 159, 255)
    hracRect = pygame.Rect(rozliseniObrazovky[0]/2 - velikostHrace/2, rozliseniObrazovky[1]/2 - velikostHrace/2, velikostHrace, velikostHrace)

    cooldown = 200 # (60/cooldown)krat za sekundu muzes vystrelit
    global last_shot_time
    last_shot_time = 0
    rammerMoving = False

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
        def __init__(self, rammerRect, hp, rychlost):
            # Convert tuple to pygame.Rect if necessary
            if isinstance(rammerRect, tuple):
                self.rammerRect = pygame.Rect(rammerRect)  # Converts tuple (x, y, width, height) to pygame.Rect
            elif isinstance(rammerRect, pygame.Rect):
                self.rammerRect = rammerRect
            else:
                raise ValueError("rammerRect must be a tuple or pygame.Rect")

            self.velikost = self.rammerRect.width  # The size is now the width of the rectangle
            self.hp = hp
            self.rychlost = rychlost

            self.currentAcceleration = 0
            self.changeInAccelaration = 0.5
            self.maxSpeed = 10

        def draw(self, okno):
            # Draw the rammer using pygame.Rect
            pygame.draw.rect(okno, (255, 255, 0), self.rammerRect)

        def attack(self, hracRect, rammerMoving):
            # Calculate the center of the player and the rammer
            centerOfPlayer = pygame.Vector2(hracRect[0] + velikostHrace / 2, hracRect[1] + velikostHrace / 2)
            centerRammer = pygame.Vector2(self.rammerRect.center)  # Use the center of the pygame.Rect

            # Calculate the direction from the rammer to the player
            direction = centerOfPlayer - centerRammer

            # Ensure direction is normalized and non-zero
            if direction.length() > 0:
                direction = direction.normalize()

            # Calculate the ending position (scaled direction for attack)
            lineLength = centerRammer.distance_to(centerOfPlayer)  # Get the distance between the rammer and player
            scaledDirection = direction * lineLength * 1.2  # Scale the direction to move beyond the player

            # Calculate the ending and starting positions
            endingPos = centerRammer + scaledDirection
            startPos = centerRammer - (direction * lineLength * 0.3)  # Wind-up runway before attack

            # Draw the attack line
            pygame.draw.line(okno, (0, 0, 255), startPos, endingPos, 5)

            # Handle acceleration and deceleration based on movement
            if rammerMoving:
                self.currentAcceleration += self.changeInAccelaration
                if self.currentAcceleration > self.maxSpeed:
                    self.currentAcceleration = self.maxSpeed
            else:
                self.currentAcceleration -= self.changeInAccelaration
                if self.currentAcceleration < 0:
                    self.currentAcceleration = 0

            # Update the rammer's position based on the current acceleration and direction
            self.rammerRect.x += int(self.currentAcceleration * direction.x)
            self.rammerRect.y += int(self.currentAcceleration * direction.y)


    listRammer.append(Rammer(pygame.Rect(520,520, 60, 60), 60, 2))

    def rammerClassUpdate(listRammer):
        for rammer in listRammer:
            rammer.draw(okno)
            rammer.attack(hracRect, rammerMoving)


    def spawnNumberOfRammers(numberOfRammers, list, rozliseniObrazovky, wallWidth):
        for number in range(numberOfRammers):
            rammerRect = (random.randint(wallWidth, rozliseniObrazovky[0] - wallWidth - 60),#X
                          random.randint(wallWidth, rozliseniObrazovky[1] - wallWidth - 60),
                          60, 60) #velikost
            list.append(Rammer(rammerRect, 50, 5))


    #iterates over whole grid  --------- Allows to store list in elements       
    for element in numpy.nditer(grid, flags=['multi_index', 'refs_ok'],op_flags=['readwrite']): 
        if element <= 1: #iterates over every room (isn't 0 in grid)
            # [0type, 1layout, 2[listOfRammers], 3[listOfProjectiles]]

            #Temporar var
            roomType = int(element) #if room is normal (#1), spawn (2#), etc
            roomLayout = random.randint(1,1) #currently only one layout (shape of walls)
            listOfRammers = [] #apeend class times number of enemies supposed to be in room (random * difficulty)
            listOfProjectiles = [] #empty till bullets are shot from player

            spawnNumberOfRammers(random.randint(1, 1), listOfRammers, rozliseniObrazovky, wallWidth)

            # [...] edits the original array instead of creating temporary array (from numpy)       
            element[...] = [
                roomType,
                roomLayout, 
                listOfRammers, 
                listOfProjectiles
            ] 
    grid[middlecord[0],middlecord[1]][0] = 2
    #sets the middle of map (spawn room) room types



    def pohybHrace(hrac_rect, key_press):
        if key_press[pygame.K_s]:
            hrac_rect[1] += rychlostHrace
        if key_press[pygame.K_w]:
            hrac_rect[1] -= rychlostHrace
        if key_press[pygame.K_d]:
            hrac_rect[0] += rychlostHrace
        if key_press[pygame.K_a]:
            hrac_rect[0] -= rychlostHrace

    def KontrolaOutOfBounds(rozliseni): 
        velikostHrace = hracRect[2]
        if hracRect[0] < 0 - velikostHrace: #vlevo
            current_room[0] -= 1
            hracRect[0] = (rozliseni[0] - velikostHrace) #sets player at oposite side of screen
            hracRect[1] = rozliseni[1]/2 - velikostHrace/2 #middle of opposite 

        elif hracRect[0] >= rozliseni[0]: #pravo
            current_room[0] += 1
            hracRect[0] = 0 - velikostHrace
            hracRect[1] = rozliseni[1]/2 - velikostHrace/2

        elif hracRect[1] < 0 - velikostHrace: #horni
            current_room[1] -= 1
            hracRect[1] = rozliseni[1]
            hracRect[0] = rozliseni[0]/2 - velikostHrace/2

        elif hracRect[1] >= rozliseni[1]: #dole
            current_room[1] += 1
            hracRect[1] = 0 - velikostHrace
            hracRect[0] = rozliseni[0]/2 - velikostHrace/2


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
        global topLeftWall, leftTopWall, topRightWall, rightTopWall, rightDownWall, downRightWall, LefDowntWall, DownLeftWall
        leftTopWall = pygame.draw.rect(okno, wallColour, (0,0, wallWidth, rozliseniObrazovky[1]/2 - holeSize/2))
        topLeftWall = pygame.draw.rect(okno, wallColour, (0,0, rozliseniObrazovky[0]/2 - holeSize/2, wallWidth))

        topRightWall = pygame.draw.rect(okno, wallColour, (rozliseniObrazovky[0]/2 + holeSize/2, 0, rozliseniObrazovky[0]/2 - holeSize/2, wallWidth))
        rightTopWall = pygame.draw.rect(okno, wallColour, (rozliseniObrazovky[0] - wallWidth, 0, wallWidth, rozliseniObrazovky[1]/2 - holeSize/2))

        rightDownWall = pygame.draw.rect(okno, wallColour, (rozliseniObrazovky[0] - wallWidth, rozliseniObrazovky[1]/2 + holeSize/2, wallWidth, rozliseniObrazovky[1]/2 - holeSize/2))
        downRightWall = pygame.draw.rect(okno, wallColour, (rozliseniObrazovky[0]/2 + holeSize/2, rozliseniObrazovky[1] - wallWidth, rozliseniObrazovky[0]/2 - wallWidth/2, wallWidth))

        LefDowntWall = pygame.draw.rect(okno, wallColour, (0, rozliseniObrazovky[1]/2 + holeSize/2, wallWidth, rozliseniObrazovky[1]/2 - holeSize/2))
        DownLeftWall = pygame.draw.rect(okno, wallColour, (0, rozliseniObrazovky[1] - wallWidth, rozliseniObrazovky[0]/2 - holeSize/2, wallWidth))

    def draw(current_room): #draw the room (enemies, bullet, walls)
        #print(grid[current_room[0]][current_room[1]])

        DrawRoom() #zdi

    def update():
        okno.fill(backgroundColor)

        #STŘELBA  ----  Vystřelí když uběhl cooldown od posledního výstřelu
        if pygame.mouse.get_pressed()[0] and current_time - last_shot_time >= cooldown:
            vystreleniProjectilu(listProjectilu, hracRect, current_time)
        updateProjectileClass(grid[current_room[0],current_room[1]][3], rozliseniObrazovky)

        #RAMMERS  ----
        rammerClassUpdate(grid[current_room[0],current_room[1]][2])

        #POHYB    ----  
        pohybHrace(hracRect, key_press)
        KontrolaOutOfBounds(rozliseniObrazovky)
        pygame.draw.rect(okno, barvaHrace, hracRect)
        draw(current_room)

        pygame.display.update() 

    while True:
        clock.tick(60) #FPS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        current_time = pygame.time.get_ticks()
        key_press = pygame.key.get_pressed()

        if key_press[pygame.K_ESCAPE]:
            sys.exit()

        if key_press[pygame.K_h]:
            rammerMoving = not rammerMoving
            print(f"Changed       rammerMoving: {rammerMoving}")

        update()

################################################################################################################################################################################################################################
if __name__ == '__main__':
    Main()