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

    #Prends une ligne, extrait les coordonnées et regardes si des coordonnées correspondant dans les brushs du .map
    def find_correspondance_with_brush(self, linetext, brushs):
        linetext = linetext[:-2]
        resultats = re.findall(r'-p (\S+ \S+ \S+)', linetext)
        
        #Parcours des couples de coordonnées
        for result in resultats:
            texturename = self.find_correspondance_between_coords_and_brush(brushs, Coordinate(result))
            if(texturename != None):
                return texturename
                
        return None

    #Prends une ligne, extrait les coordonnées et regarde si des coordonnées correspondant dans les brushs du .map
    def find_correspondance_with_brush_curve(self, linetext, brushs):
        linetext = linetext.split(" (")[0] #Enleve les informations après les coordonnées
        linetext = linetext.split("ws ")[1] #Enleve les informations avant les coordonnées

        return self.find_correspondance_between_coords_and_brush(brushs, Coordinate(linetext))
    
    #Recherche la texture en fonction du type brush ou curve
    def find_texture(self, map, linetext, i):
        #Test si le poly mel est un cube ou une curve
        if(linetext.startswith("$strPolyInfo = `polyCreateFacet")):
            return self.find_correspondance_with_brush(linetext, map.brushs)
        linetext = self.lines[i+2].strip() #La ligne qui nous intéresse est en i+2
        return self.find_correspondance_with_brush_curve(linetext, map.brushscurve)
    
    #Ajoute la texture au mel si elle n'existe pas et retourne la texture
    def add_texture(self, map, linetext, i):
        texture_name = self.find_texture(map, linetext,i)

        if(texture_name != None and texture_name not in self.textures):  
            #Création de la texture dans le mel
            self.textures[texture_name] = len(self.textures)
            self.lines = create_texture(self.lines, i, "texture"+str(self.textures[texture_name]), texture_name)
        
        return texture_name

    #Parcours du mel et ajoute les textures en fonction du map
    def parse_mel_add_brush_texture_and_return_new_mel(self, map):
        find = False
        self.textures = {}

        for i in range(0, len(self.lines)-2):
            #Récupération du texte
            linetext = self.lines[i].strip()

            if(linetext.startswith("$strPolyInfo") and not find):
                find = True
                texture_name = self.add_texture(map, linetext, i)

            if(linetext.startswith("parent") and texture_name != None):
                self.lines = add_force_texture(self.lines, i, self.textures[texture_name])
                    
            #Nouveau brush
            if(linetext.startswith("progressWindow")):
                find = False

    def __init__(self, mel_path, map):
        f = open(mel_path, "r")
        self.lines = f.readlines()
        self.parse_mel_add_brush_texture_and_return_new_mel(map)