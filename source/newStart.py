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
    numberOfRooms = levelGeneration.numberOfRooms

    rychlostHrace = 5
    velikostHrace = 120
    barvaHrace = (128, 159, 255)
    hracRect = pygame.Rect(rozliseniObrazovky[0]/2 - velikostHrace/2, rozliseniObrazovky[1]/2 - velikostHrace/2, velikostHrace, velikostHrace)

    cooldown = 200 # (60/cooldown)krat za sekundu muzes vystrelit
    global last_shot_time
    last_shot_time = 0
    
    #iterates over whole grid  --------- Allows to store list in elements       
    for element in numpy.nditer(grid, flags=['multi_index', 'refs_ok'],op_flags=['readwrite']): 
        if element <= 1: #iterates over every room (isn't 0 in grid)
            # [type, layout, [listOfEnemies], [listOfProjectiles]]

            #Temporar var
            roomType = int(element) #if room is normal (#1), spawn (2#), etc
            roomLayout = random.randint(1,1) #currently only one layout (shape of walls)
            listOfEnemies = [] #apeend class times number of enemies supposed to be in room (random * difficulty)
            listOfProjectiles = [] #empty till bullets are shot from player

            # [...] edits the original array instead of creating temporary array (from numpy)       
            element[...] = [
                roomType,
                roomLayout, 
                listOfEnemies, 
                listOfProjectiles
            ] 
    grid[middlecord[0],middlecord[1]][0] = 2

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
           

    def pohybHrace(hrac_rect, key_press):
        if key_press[pygame.K_s]:
            hracRect[1] += rychlostHrace
        if key_press[pygame.K_w]:
            hracRect[1] -= rychlostHrace
        if key_press[pygame.K_d]:
            hracRect[0] += rychlostHrace
        if key_press[pygame.K_a]:
            hracRect[0] -= rychlostHrace

    def KontrolaOutOfBounds(rozliseni): 
        velikostHrace = hracRect[2]
        if hracRect[0] < 0 - velikostHrace: #vlevo
            current_room[0] -= 1
            hracRect[0] = (rozliseni[0] - velikostHrace) #sets player at oposite side of screen
            hracRect[1] = rozliseni[1]/2 - velikostHrace/2

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


    def update():
        okno.fill(backgroundColor)

        #Vystřelí když uběhl cooldown od posledního výstřelu
        if pygame.mouse.get_pressed()[0] and current_time - last_shot_time >= cooldown:
            vystreleniProjectilu(listProjectilu, hracRect, current_time)
        
        listProjectiluIndex = grid[current_room[0],current_room[1]][3]
        for projectily in listProjectiluIndex[:]:
            projectily.movement()
            projectily.draw(okno)

            if projectily.despawn(rozliseniObrazovky):
                listProjectiluIndex.remove(projectily)
            
            # pygame.Rect.collidelist() returns zero if no collision, otherwise returns index of collision
            if pygame.Rect.collidelist(projectily.projectileRect, [topLeftWall, leftTopWall, topRightWall, rightTopWall, rightDownWall, downRightWall, LefDowntWall, DownLeftWall]) >= 0:
                listProjectiluIndex.remove(projectily)
                #deletes when colided with wall

        pohybHrace(hracRect, key_press)
        KontrolaOutOfBounds(rozliseniObrazovky)
        pygame.draw.rect(okno, barvaHrace, hracRect)
        draw(current_room)

        pygame.display.flip() 

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
        print(grid[current_room[0]][current_room[1]])

        DrawRoom()

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

        update()

################################################################################################################################################################################################################################
if __name__ == '__main__':
    Main()