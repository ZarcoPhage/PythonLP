import re
import numpy as np
from PIL import Image

class player:
    def __init__(self, directionIndex, playerPos, directionList = ('West','South','East','North')):
        self.directionList = directionList
        self.directionIndex = directionIndex
        self.playerPos = playerPos
        self.playerDirection = directionList[directionIndex]

    def setPlayerPos(self, newPlayerPos):
        self.playerPos = newPlayerPos

    def setPlayerDirection(self, newDirectionIndex):
        self.directionIndex = newDirectionIndex
        self.playerDirection = self.directionList[self.directionIndex]

class matrix:
    def __init__(self, matriz=[]):
        self.matriz = matriz

    def updateMatrix(self, matriz):
        self.matriz = matriz

def MatrizAImagen(matriz, filename='pixelart.png', factor=10):
    '''
    Convierte una matriz de valores RGB en una imagen y la guarda como un archivo png.
    Las imagenes son escaladas por un factor ya que con los ejemplos se producirian imagenes muy pequeñas.
        Parametros:
                matriz (lista de lista de tuplas de enteros): Matriz que representa la imagen en rgb.
                filename (str): Nombre del archivo en que se guardara la imagen.
                factor (int): Factor por el cual se escala el tamaño de las imagenes.
    '''
    matriz = np.array(matriz, dtype=np.uint8)
    np.swapaxes(matriz, 0, -1)

    N = np.shape(matriz)[0]

    img = Image.fromarray(matriz, 'RGB')
    img = img.resize((N*10, N*10), Image.Resampling.BOX)
    img.save(filename)


def tokenizer(code): #basado en ejemplo de tokenizer en documentación modulo RE
    tokenSpecs = [
        #('numero', r' \d+'),
        ('ancho',r'Ancho \d+'),
        ('backColor',r'Color de fondo (Rojo|Verde|Azul|Negro|Blanco|RGB[(]\d+[,]\d+[,]\d+[)])'),
        #('color', r'Rojo|Verde|Azul|Negro|Blanco|RGB[(]\d+[,]\d+[,]\d+[)]'),
        ('repetir', r'Repetir \d+ veces {'),
        ('pintar', r'Pintar (Rojo|Verde|Azul|Negro|Blanco|RGB[(]\d+[,]\d+[,]\d+[)])'),
        ('avanzar', r'Avanzar \d+|Avanzar'),
        ('direccion', r'Derecha|Izquierda'),
        ('tab',r'   '),
        ('cierraCiclo', r'[}]'),
        ('NOMATCH',r'\w+')
    ]
    tokenRegex = '|'.join('(?P<%s>%s)' % par for par in tokenSpecs)
    for matchObject in re.finditer(tokenRegex, code, flags=re.DOTALL):
        tipo = matchObject.lastgroup
        valor = matchObject.group()
        #numLinea = 1
        #linIni = 0
        yield (tipo, valor)

def initMatrix(ancho):
    matrix = []
    for i in range(ancho):
        filasMatriz = []
        for j in range(ancho):
            filasMatriz.append((0,0,0))
        matrix.append(filasMatriz)
    
    return matrix

def background(color, matrix, ancho):
    if color == 'Rojo':
        newColor = (255,0,0)
        for i in range(ancho):
            for j in range(ancho):
                matrix[i][j] = newColor
        return matrix
    elif color == 'Verde':
        newColor = (0,255,0)
        for i in range(ancho):
            for j in range(ancho):
                matrix[i][j] = newColor
        return matrix
    elif color == 'Azul':
        newColor = (0,0,255)
        for i in range(ancho):
            for j in range(ancho):
                matrix[i][j] = newColor
        return matrix
    elif color == 'Negro':
        newColor = (0,0,0)
        for i in range(ancho):
            for j in range(ancho):
                matrix[i][j] = newColor
        return matrix
    elif color == 'Blanco':
        newColor = (255,255,255)
        for i in range(ancho):
            for j in range(ancho):
                matrix[i][j] = newColor
        return matrix
    else:
        match = re.findall(r'\d+',color)
        #print(match)
        rVal = int(match[0])
        gVal = int(match[1])
        bVal = int(match[2])
        newColor = (rVal, gVal, bVal)
        for i in range(ancho):
            for j in range(ancho):
                matrix[i][j] = newColor
        return matrix

def paintCell(color, matrix, player):
    playerPos = player.playerPos
    xPos = playerPos[0]
    yPos = playerPos[1]
    print(xPos,yPos)
    if color == 'Rojo':
        newColor = (255,0,0)
        matrix[xPos][yPos] = newColor
        return matrix
    elif color == 'Verde':
        newColor = (0,255,0)
        matrix[xPos][yPos] = newColor
        return matrix
    elif color == 'Azul':
        newColor = (0,0,255)
        matrix[xPos][yPos] = newColor
        return matrix
    elif color == 'Negro':
        newColor = (0,0,0)
        matrix[xPos][yPos] = newColor
        return matrix
    elif color == 'Blanco':
        newColor = (255,255,255)
        matrix[xPos][yPos] = newColor
        return matrix
    else:
        match = re.findall(r'\d+',color)
        #print(match)
        rVal = int(match[0])
        gVal = int(match[1])
        bVal = int(match[2])
        newColor = (rVal, gVal, bVal)
        matrix[xPos][yPos] = newColor
        return matrix

def changeDirection(directionIndex, order):
    if order == 'R':
        directionIndex+=1
    elif order == 'L':
        directionIndex+=3 
    directionIndex = directionIndex % 4
    return directionIndex

def commandExecution(matriz, ancho, lines, player):
    tempPlayerPos = player.playerPos
    tempDirectionIndex = player.directionIndex
    playerDirection = player.playerDirection
    matrix = matriz.matriz
    errorLineFlag = False
    numErrores = 0
    cycleTabs = 0

    for i in range(len(lines)):
        largoLinea = len(lines[i])
        print(lines[i])
        for j in range(largoLinea):
            if lines[i][j][0] == 'ancho':
                numAncho = re.findall(digPattern,lines[i][j][1])
                ancho = int(numAncho[0])
                matrix = initMatrix(ancho)
                matriz.updateMatrix(matrix) #new

            elif lines[i][j][0] == 'backColor':
                colorFondo = re.findall(colorPattern,lines[i][j][1])
                matrix = background(colorFondo[0],matrix,ancho)
                matriz.updateMatrix(matrix) #new

            elif lines[i][j][0] == 'direccion':
                if lines[i][j][1] == 'Derecha':
                    tempDirectionIndex = changeDirection(tempDirectionIndex,'R')
                elif lines[i][j][1] == 'Izquierda':
                    tempDirectionIndex = changeDirection(tempDirectionIndex,'L')
                player.setPlayerDirection(tempDirectionIndex)
                #print(player.playerDirection)

            elif lines[i][j][0] == 'avanzar':
                indAvances = 0
                avancesEsperados = 1
                cantidadAv = re.findall(digPattern,lines[i][j][1])
                if(len(cantidadAv))>0:
                    avancesEsperados = int(cantidadAv[0])
                
                while indAvances<avancesEsperados:        
                    if player.playerDirection == 'North':
                        tempPlayerPos[0]-=1
                    elif player.playerDirection == 'South':
                        tempPlayerPos[0]+=1
                    elif player.playerDirection == 'West':
                        tempPlayerPos[1]+=1
                    elif player.playerDirection == 'East':
                        tempPlayerPos[1]-=1
                    indAvances+=1
                player.setPlayerPos(tempPlayerPos)
                print(player.playerPos)
        
            elif lines[i][j][0] == 'pintar':
                colorPintura = re.findall(colorPattern,lines[i][j][1])
              
                matrix = paintCell(colorPintura[0],matrix,player)
                for kl in range(len(matrix)):
                    print(matrix[kl])
                matriz.updateMatrix(matrix) #new

            elif lines[i][j][0] == 'repetir':
                cantidadRep = re.findall(digPattern, lines[i][j][1])
                repEsperadas= int(cantidadRep[0])
                firstLinePointer = i+1
                lastLinePointer = i+1
                neededTabs = 1
                tempLines = []
                while lastLinePointer<len(lines):
                    tempLines.append(lines[lastLinePointer])
                    if lines[lastLinePointer][j][0] == 'cierraCiclo':
                        break
                    lastLinePointer+=1   

                repLinesqty = lastLinePointer-firstLinePointer
                print("LINESFORREP")
                for l in range(repLinesqty):
                    tempLines[l].pop(0)
                    print(tempLines[l])
                print("ENDLINESFORREP")

                repRealizadas = 0
                while repRealizadas<repEsperadas:
                    commandExecution(matriz,ancho,tempLines,player)
                    print("POSTRECURSION")
                    repRealizadas+=1


    if numErrores == 0:
        errorFile.write("No hay errores!")

    tempMatrix = matriz.matriz
    for i in range(ancho):
        print(tempMatrix[i])
    MatrizAImagen(matriz.matriz)


################################################
# CODIGO MAIN
################################################

#inicializacion
completeCode = []

digPattern = re.compile(r'\d+')
colorPattern =re.compile('(Rojo|Verde|Azul|Negro|Blanco|RGB[(]\d+[,]\d+[,]\d+[)])')
file = open("codigo.txt","r")
errorFile = open("errores.txt","w+")
iteration = 1
cycleTabs = 0
numErrores = 0
errorLineFlag = False
execute = True


ancho = 0

directionIndex = 0
#directions = ('West','South','East','North')
playerPos = [0,0]
#playerDirection = directions[directionIndex]

#matrix = []

#lectura, tokenizacion y parseo

for line in file:
    completeCode.append(line)
file.close()

#print(completeCode)

lines = []
errorLines = []
errorFile = open("errores.txt","w+")
for line in completeCode:
    
    errorLineFlag = False
    lineTokenList = []
    
    print("line "+str(iteration)+": "+line)
    
    for token in tokenizer(line):
        if token[0] == 'NOMATCH':
            #print("FOUND")
            execute = False
            errorLines.append((iteration,line))
        lineTokenList.append(token)
    
    
    lines.append(lineTokenList)
    iteration+=1

for errorIndex in range(len(errorLines)):
    errorFile.write(str(errorLines[errorIndex][0])+" "+errorLines[errorIndex][1])


for line in range(len(lines)):

    print("linea"+str(line+1)+":")
    print(lines[line])

file.close()

if execute:
    J1 = player(directionIndex,playerPos)
    matrizPNG = matrix()
    commandExecution(matrizPNG,ancho,lines,J1)

errorFile.close()


#print(completeCode)

#print(code)
#commandExecution(code)

#print(re.findall(scanPattern, code))



'''
TO DO: 
- Reconocimiento de tokens DONE
- ejecucion de instrucciones: FALTA INSTRUCCION REPETIR
- detección de errores: DONE
- creacion de imagen luego de la ejecucion: DONE
- creacion de archivo errores: DONE
- mostrar por consola los valores de la matriz RGB en caso de ejecución exitosa: DONE
'''


