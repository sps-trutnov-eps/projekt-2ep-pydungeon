import random, numpy
size = 6

def GenerateMap(size):
    global map
    map = numpy.zeros((size, size), dtype=numpy.int8, order='C')

def PrintMap():
    print(map)
    print()

def MakeRoom(cords):
    map[cords[0],cords[1]] = 1

def GenerateLevel(LevelLength):
    middlecords = [round((size-1)/2),round((size-1)/2)]

    for lenght in range(LevelLength):
        direction = random.randint(1,4)
        MakeRoom(((middlecords[0] + direction),
                 (middlecords[1] + direction)))


GenerateMap(5)
GenerateLevel(3)
PrintMap()
'''
    1N
  4W  2E
    3S
'''

