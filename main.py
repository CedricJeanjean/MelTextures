
from map import Map
from mel import Mel
import sys

def create_mel(lines):
    with open('new_mel.mel', 'w') as fichier:
        for line in lines:
            fichier.write(line)
    
if __name__ == '__main__':
    map = Map(sys.argv[1])
    mel = Mel(sys.argv[2], map)

    create_mel(mel.lines)

    print("Created")