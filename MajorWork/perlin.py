import random
import numpy

def generateWhiteNoise(width,height):

    # Create an empty NumPy array with zeros
    height_map = numpy.zeros((height, width))

    # Fill the height map with random values between 0 and 1
    for i in range(0,height):
        for j in range(0,width):
            number = random.randint(0,2)
            if number == 2:
                number = 0
            height_map[i][j] = number
    
    material_map = numpy.zeros((height, width), dtype='int')

    # Smooth the map using averaging
    smoothed_map = numpy.zeros_like(height_map)
    kernel = numpy.array([[1, 2, 1], [2, 3, 2], [1, 2, 1]])  # Averaging kernel

    for y in range(1, height - 1):  # Skip borders to avoid out-of-bounds access
        for x in range(1, width - 1):
            # Apply kernel to get neighbor average
            neighborhood = height_map[y-1:y+2, x-1:x+2]
            smoothed_map[y, x] = numpy.average(neighborhood, weights=kernel)

    for x in range(height):
        for y in range(width):
            if smoothed_map[x][y] > 0.60:
                material_map[x][y] = 1
                
    return material_map

# generates 3 white noise maps and makes each one into an ore then combines them
def generate_ore_map(width, height):
    coal = generateWhiteNoise(width, height)
    diamond = generateWhiteNoise(width, height)
    iron = generateWhiteNoise(width, height)
    
    ore_map = numpy.zeros((height, width))
    for x in range(height):
        for y in range(width):
            if coal[x][y] == 1:
                ore_map[x][y] = 1
            if diamond[x][y] == 1:
                ore_map[x][y] = 2
            if iron[x][y] == 1:
                ore_map[x][y] = 3

    return ore_map