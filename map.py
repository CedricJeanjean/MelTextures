from brush import Brush, Coordinate
import re

class Map:
    
    def split_curve_coord(self, coords):
        coords = coords.split("v ")[1]
        return coords.split(" t")[0]

    def get_curve_brush(self, i):
        texture_indice = i
        coord_indice = i+4

        #Test la présence de la ligne contents
        value_line = self.lines[texture_indice].strip()
        if(value_line.startswith("contents")):
            texture_indice = texture_indice+1
            coord_indice = coord_indice+1

        #Test la présence de la ligne toolFlags
        value_line = self.lines[texture_indice].strip()
        if(value_line.startswith("toolFlags")):
            texture_indice = texture_indice+1
            coord_indice = coord_indice+1
        
        #Récupération des textures et des coordonnées
        texturename = self.lines[texture_indice].strip()

        try: #Certains meshs n'ont pas 3 coordonnées, on les ignores
            coords1 = self.lines[coord_indice].strip()
            coords1 = Coordinate(self.split_curve_coord(coords1))
            coords2 = self.lines[coord_indice+1].strip()
            coords2 = Coordinate(self.split_curve_coord(coords2))
            coords3 = self.lines[coord_indice+2].strip()
            coords3 = Coordinate(self.split_curve_coord(coords3))

            return Brush(point1=coords1,point2=coords2,point3=coords3, texturename=texturename)
        except:
            return None

    def parse_cube_text(self, texte):
        last_close_parenthesis = texte.rfind(')')

        result = texte[:last_close_parenthesis + 1]
        #Texture
        rest = texte[last_close_parenthesis + 1:]
        texturename = rest.split(" ")[1]

        coordinates = re.findall(r'\((.*?)\)', result)
        return Brush(point1=Coordinate(coordinates[0]),point2=Coordinate(coordinates[1]),point3=Coordinate(coordinates[2]), texturename=texturename)

    #Retourne un tableau avec tous les brushs de l'élément
    def get_brush(self, line, ind):
        brushs = []
        while(line.startswith("(")):
            #Parse du cube
            #cube_brush = self.parse_cube_text(line)
            #if(cube_brush.texturename != "caulk"):
            #    return cube_brush
            brushs.append(self.parse_cube_text(line))
            
            #Si la texture est caulk, on continue
            ind += 1
            line = self.lines[ind].strip()
        
        #Si toutes les textures du brush sont caulk, on l'ignore, il ne doit pas être affiché
        return brushs

    #Parcours du map et récupére les coordonnées avec la texture
    def parse_map_file(self):
        for i in range(0, len(self.lines)-2):
            #Récupération du texte
            linetext = self.lines[i].strip()

            #Récupération du texte du début des informations
            ind_start_content = i+2
            linetext_start_content = self.lines[ind_start_content].strip()

            #Dans certains cas, une ligne contents est présente, elle doit être ignorée
            if(linetext_start_content.startswith("contents")):
                ind_start_content += 1
                linetext_start_content = self.lines[ind_start_content].strip()

            #Récupération des brushs
            if(linetext.startswith("// brush") and linetext_start_content.startswith("(")):
                brushs = self.get_brush(linetext_start_content, ind_start_content)
                if len(brushs) != 0:
                    self.brushs.append(brushs)
            elif(linetext_start_content.startswith("curve") or linetext_start_content.startswith("mesh")):
                #Les curves et meshs commencent 2 lignes plus tard
                ind_start_content += 2

                curvebrush = self.get_curve_brush(ind_start_content)
                if curvebrush != None:
                    self.brushscurve.append(curvebrush)
                    #Dans certains cas complexes, les curves sont traitées comme des brushs normaux dans mel
                    self.brushs.append([curvebrush])

    def __init__(self, map_path):
        f = open(map_path, "r")
        self.lines = f.readlines()

        self.brushs = []
        self.brushscurve = []
        
        self.parse_map_file()