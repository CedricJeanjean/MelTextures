from brush import Brush, Coordinate
import re

class Map:

    def get_curve_brush(self, i):
        pass

    def parse_cube_text(self, texte):
        last_close_parenthesis = texte.rfind(')')

        result = texte[:last_close_parenthesis + 1]
        #Texture
        rest = texte[last_close_parenthesis + 1:]
        texturename = rest.split(" ")[1]

        coordinates = re.findall(r'\((.*?)\)', result)
        return Brush(coord1=Coordinate(coordinates[0]),coord2=Coordinate(coordinates[1]),coord3=Coordinate(coordinates[2]), texturename=texturename)

    def get_brush(self, line, ind):
        while(line.startswith("(")):
            #Parse du cube
            cube_brush = self.parse_cube_text(line)
            if(cube_brush.texturename != "caulk"):
                return cube_brush
            
            #Si la texture est caulk, on continue
            ind += 1
            line = self.lines[ind].strip()
        
        #Si toutes les textures du brush sont caulk, on l'ignore, il ne doit pas être affiché
        return None

    #Parcours du map et récupére les coordonnées avec la texture
    def parse_map_file(self):
        for i in range(0, len(self.lines)-2):
            #Récupération du texte
            linetext = self.lines[i].strip()

            #Récupération du texte du début des informations
            ind_start_content = i+2
            linetext_start_content = self.lines[ind_start_content].strip()

            if(linetext_start_content.startswith("contents")):
                ind_start_content += 1
                linetext_start_content = self.lines[ind_start_content].strip()
            elif(linetext_start_content.startswith("curve")):
                ind_start_content += 2

            #Récupération des brushs
            if(linetext.startswith("// brush") and linetext_start_content.startswith("(")):
                self.brushs.append(self.get_brush(linetext_start_content, ind_start_content))
            elif(linetext_start_content.startswith("curve")):
                self.brushscurve.append(self.get_curve_brush(ind_start_content))

    def __init__(self, map_path):
        f = open(map_path, "r")
        self.lines = f.readlines()

        self.brushs = []
        self.brushscurve = []
        
        self.parse_map_file()