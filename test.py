import numpy

array = [1, [2, 3, 4], [5, [6, 7]]]

print(array[0])
print(array[1][2])
print(array[2][1][1])


grid = numpy.zeros((5,5))
print(grid)

for i in numpy.nditer(grid, flags=['multi_index', 'refs_ok'],op_flags=['readwrite']):
    i += 1
    grid[3] = i

print(grid)