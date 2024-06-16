class Coordinate:
    def __init__(self, coordinateArray):
        coordinateArray = coordinateArray.split()
        self.x = int(float(coordinateArray[0]))
        self.y = int(float(coordinateArray[1]))
        self.z = int(float(coordinateArray[2]))

    def __eq__(self, other_coordinates):
        if isinstance(other_coordinates, Coordinate):
            return self.x == other_coordinates.x and self.y == other_coordinates.y and self.z == other_coordinates.z
        return False

class Brush:
    def __init__(self, point1, point2, point3, texturename):
        self.point1 = point1
        self.point2 = point2
        self.point3 = point3
        self.texturename = texturename