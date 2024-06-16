from brush import Coordinate
from create_texture import *
import re

class Mel:

    def find_correspondance_between_coords_and_brush(self, brushs, mel_coordinates):
        #Parcours des brushs
        for map_brush in brushs:
            if map_brush.point1 == mel_coordinates or map_brush.point2 == mel_coordinates or map_brush.point3 == mel_coordinates :
                return map_brush.texturename
        return None
    
    def find_texture_brush(self, brushs, mel_coordinates_array):
        max_nb_coord_found = 0
        texturename = None
        #Parcours des brushs
        for brusharray in brushs:
            nb_coord_found = 0
            current_texture = None

            #Parcours de chaque coordonnées de la ligne du .mel
            for mel_coordinates_array_line in mel_coordinates_array:
                for mel_coordinates in mel_coordinates_array_line:
                    #Parcours de chaque ligne d'un brush du .map
                    for single_brush in brusharray:
                        #Si la texture n'est pas caulk, on la sauvegarde comme texture du matériau global
                        if(single_brush.texturename != "caulk"):
                            current_texture = single_brush.texturename

                        #Si les coordonnées d'un point correspondent entre un mel et un map
                        if single_brush.point1 == mel_coordinates or single_brush.point2 == mel_coordinates or single_brush.point3 == mel_coordinates :
                            nb_coord_found += 1

            #Comparaison avec le max
            if(nb_coord_found > max_nb_coord_found and current_texture != None):
                max_nb_coord_found = nb_coord_found
                texturename = current_texture
            
        return texturename

    #Prends une ligne, extrait les coordonnées et regardes si des coordonnées correspondant dans les brushs du .map
    def find_coordinates_in_mel_brush_line(self, linetext):
        linetext = linetext[:-2]
        resultats = re.findall(r'-p (\S+ \S+ \S+)', linetext)
        return_array = []

        for result in resultats:
            return_array.append(Coordinate(result))
        
        return return_array

    #Prends une ligne, extrait les coordonnées et regarde si des coordonnées correspondant dans les brushs du .map
    def find_correspondance_with_brush_curve(self, linetext):
        linetext = linetext.split(" (")[0] #Enleve les informations après les coordonnées
        linetext = linetext.split("ws ")[1] #Enleve les informations avant les coordonnées

        return Coordinate(linetext)
    
    #Recherche la texture en fonction du type brush ou curve
    def find_coordinates_in_line(self, linetext, i):
        #If brush
        if(linetext.startswith("$strPolyInfo = `polyCreateFacet")):
            return self.find_coordinates_in_mel_brush_line(linetext)
        #Curve
        linetext = self.lines[i+2].strip() #La ligne qui nous intéresse est en i+2
        return self.find_correspondance_with_brush_curve(linetext)
    
    #Ajoute la texture au mel si elle n'existe pas et retourne la texture
    def add_texture(self, i, texture_name):
        if(texture_name != None and texture_name not in self.textures):  
            #Création de la texture dans le mel
            self.textures[texture_name] = len(self.textures)
            self.lines = create_texture(self.lines, i, "texture"+str(self.textures[texture_name]), texture_name)

    #Parcours du mel et ajoute les textures en fonction du map
    def parse_mel_add_brush_texture_and_return_new_mel(self, map):
        self.textures = {}
        current_mel_coords = []
        #Variable qui contient la ligne ou créer la texture quand elle sera trouvé
        line_to_create_texture = 0

        type_brush = "curve"

        for i in range(0, len(self.lines)-2):
            #Récupération du texte
            linetext = self.lines[i].strip()

            if(linetext.startswith("$strPolyInfo")):
                if(linetext.startswith("$strPolyInfo = `polyCreateFacet")):
                    type_brush = "brush"
                current_mel_coords.append(self.find_coordinates_in_line(linetext, i))
                if line_to_create_texture == 0:
                    line_to_create_texture = i

            #Ajout de la texture
            if(linetext.startswith("parent")):
                if(type_brush == "brush"):
                    texture_name = self.find_texture_brush(map.brushs, current_mel_coords)
                else:
                    texture_name = self.find_correspondance_between_coords_and_brush(map.brushscurve, current_mel_coords[0])
                self.add_texture(line_to_create_texture, texture_name)
                if texture_name != None:
                    self.lines = add_force_texture(self.lines, i, self.textures[texture_name])
                    
            #Nouveau brush
            if(linetext.startswith("progressWindow")):
                line_to_create_texture = 0
                current_mel_coords = []
                type_brush = "curve"

    def __init__(self, mel_path, map):
        f = open(mel_path, "r")
        self.lines = f.readlines()
        self.parse_mel_add_brush_texture_and_return_new_mel(map)