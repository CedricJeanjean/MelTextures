def create_texture(lines, ind, texture_id, texture_name):
    lines[ind-1] = "shadingNode -asShader lambert -name \""+texture_id+"\";\n"+"shadingNode -asTexture file -name \""+texture_id+"_file\";\n"+"setAttr \""+texture_id+"_file.fileTextureName\" -type \"string\" \"D:/steam/SteamApps/common/Call of duty 4 Multiplayer/texture_assests/"+texture_name+".jpg\";\n"+"connectAttr \""+texture_id+"_file.outColor\" \""+texture_id+".color\";\n"+"sets -renderable true -noSurfaceShader true -empty -name \""+texture_id+"SG\";\n"+"connectAttr \""+texture_id+".outColor\" \""+texture_id+"SG.surfaceShader\";\n"
    return lines

def add_force_texture(lines, ind, texture_id):
    lines[ind+1] = "sets -edit -forceElement \"texture"+str(texture_id)+"SG\";\n"
    return lines