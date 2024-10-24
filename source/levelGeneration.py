import random, numpy
size = 8
cordinates = [round((size-1)/2),round((size-1)/2)] #current cordinates, starting at middle
middlecords = [round((size-1)/2),round((size-1)/2)] #middle of map

def GenerateMap(size):
    global map
    #generates matrix SIZE X SIZE filled with 0
    map = numpy.zeros((size, size), dtype=object, order='C')
    #dtype should be changed to bool after finishing


def PrintMap():
    print(map)
    print()


def MakeRoom(MakeRoomCords, roomType):
    map[MakeRoomCords[0],MakeRoomCords[1]] = roomType
    #Makes room (turns 0 into 1) at cords


def GenerateLevel(LevelLength):
    global cordinates
    MakeRoom(middlecords, 1)
    #generates starting room in the middle

    for i in range(LevelLength): #Makes room for every LevelLenght
        direction = random.randint(1,4)  #Choose random direction (cardinal) in which to generate the next room

        match direction: #matches the direction to logical operation
            case 1:
                cordinates[0] -= 1 #moves the coords 1 room NORTH /\
                CheckIfCordinateIsInBound(cordinates)
                MakeRoom(cordinates, 1)

            case 2:
                cordinates[1] += 1 #moves the coords 1 room EAST >
                CheckIfCordinateIsInBound(cordinates)
                MakeRoom(cordinates, 1)

            case 3:
                cordinates[0] += 1 #moves the coords 1 room SOUTH \/
                CheckIfCordinateIsInBound(cordinates)
                MakeRoom(cordinates, 1)

            case 4:
                cordinates[1] -= 1 #moves the coords 1 room WEST <
                CheckIfCordinateIsInBound(cordinates)
                MakeRoom(cordinates, 1)

def CheckIfCordinateIsInBound(checkedCord):
    global cordinates
    if checkedCord[0] > (size - 1) or checkedCord[0] < 1 or checkedCord[1] < 1 or checkedCord[1] > (size - 1):
        cordinates = [round((size-1)/2),round((size-1)/2)] 
        #if room isnt in map switches the coordinates to middle
        #NOTE: DONT USE MIDDLECORDS, use middlecords expresion to prevent change of middlecord


numberOfRooms = numpy.count_nonzero(map)
GenerateMap(size)
GenerateLevel(30)




