from brush import Coordinate
from create_texture import *
import re

class Mel:

    #Prends une ligne, extrait les coordonnées et regardes si des coordonnées correspondant dans les brushs du .map
    def find_correspondance_with_brush(self, linetext, brushs):
        linetext = linetext[:-2]
        resultats = re.findall(r'-p (\S+ \S+ \S+)', linetext)
        
        #Parcours des couples de coordonnées
        for result in resultats:
            mel_coordinates = Coordinate(result)

            #Parcours des brushs
            for map_brush in brushs:
                if map_brush.coord1 == mel_coordinates or map_brush.coord2 == mel_coordinates or map_brush.coord3 == mel_coordinates :
                    return map_brush.texturename
                
        return None

    #Parcours du mel et ajoute les textures en fonction du map
    def parse_mel_add_brush_texture_and_return_new_mel(self, map):
        find = False
        added_texture = False
        textures = {}

        for i in range(0, len(self.lines)-2):
            #Récupération du texte
            linetext = self.lines[i].strip()

            if(linetext.startswith("$strPolyInfo") and not find):
                find = True
                texture_name = self.find_correspondance_with_brush(linetext, map.brushs)
                if(texture_name != None):
                    added_texture = True
                    
                    if texture_name not in textures:
                        textures[texture_name] = len(textures)
                        self.lines = create_texture(self.lines, i, "texture"+str(textures[texture_name]), texture_name)

            if(linetext.startswith("parent $strBrush[0]") and added_texture):
                self.lines = add_force_texture(self.lines, i, textures[texture_name])
                    
            #Nouveau brush
            if(linetext.startswith("progressWindow")):
                find = False
                added_texture = False

    def __init__(self, mel_path, map):
        f = open(mel_path, "r")
        self.lines = f.readlines()
        self.parse_mel_add_brush_texture_and_return_new_mel(map)