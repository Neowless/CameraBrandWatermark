
import math
def coordinate_transform(coordinate):
    if coordinate[1] == "N":
        latitude = coordinate[2][0] + coordinate[2][1] / 60 + coordinate[2][2] / 3600
    else:
        latitude = -coordinate[2][0] - coordinate[2][1] / 60 - coordinate[2][2] / 3600

    if coordinate[3] == "E":
        longitude = coordinate[4][0] + coordinate[4][1] / 60 + coordinate[4][2] / 3600
    else:
        longitude = -coordinate[4][0] - coordinate[4][1] / 60 - coordinate[4][2] / 3600

    if coordinate[2][1] > math.floor(coordinate[2][1]):
        coordinate22 = (coordinate[2][1]-math.floor(coordinate[2][1]))*60
        coordinate21 = math.floor(coordinate[2][1])
    else:
        coordinate22 = 0
        coordinate21 = coordinate[2][1]
    if coordinate[4][1] > math.floor(coordinate[4][1]):
        coordinate42 = (coordinate[4][1]-math.floor(coordinate[4][1]))*60
        coordinate41 = math.floor(coordinate[4][1])
    else:
        coordinate42 = 0
        coordinate41 = coordinate[4][1]

    Str = (str(int(coordinate[2][0]))+"°"+str(int(float(coordinate21)))+"'"+str(int(float(coordinate22)))+"''"
           +coordinate[1]+" "+str(int(coordinate[4][0]))+"°"+str(int(float(coordinate41)))+"'"+
           str(int(float(coordinate42)))+"''"+coordinate[3])

    return(float(latitude),float(longitude),Str)


