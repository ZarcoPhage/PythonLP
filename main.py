import re
import numpy as np
from PIL import Image

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
        numLinea = 1
        linIni = 0
        if tipo == 'numero':
            valor = int(valor)
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

def paintCell(color, matrix, playerPos):
    #print(playerPos)
    xPos = playerPos[0]
    yPos = playerPos[1]
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

################################################
# CODIGO MAIN
################################################

#inicializacion
completeCode = ""

digPattern = re.compile(r'\d+')
colorPattern =re.compile('(Rojo|Verde|Azul|Negro|Blanco|RGB[(]\d+[,]\d+[,]\d+[)])')
file = open("codigo.txt","r")
errorFile = open("errores.txt","w+")
iteration = 1
cycleTabs = 0
numErrores = 0
errorLineFlag = False

directionIndex = 0
directions = ('West','South','East','North')
playerPos = [0,0]
playerDirection = directions[directionIndex]

matrix = []

#lectura, tokenizacion y parseo
for line in file:
    
    errorLineFlag = False
    lineTokenList = []
    
    #print("line "+str(iteration)+": "+line)
    
    for token in tokenizer(line):
        lineTokenList.append(token)

    for i in range(len(lineTokenList)):
        if lineTokenList[i][0] == 'NOMATCH':
            if errorLineFlag == False:
                errorFile.write(str(iteration)+" "+line)
                numErrores += 1
                errorLineFlag = True
            #print('ERROR EN LINEA: '+str(iteration))         
        
        elif lineTokenList[i][0] == 'ancho':
            numAncho = re.findall(digPattern,lineTokenList[i][1])
            ancho = int(numAncho[0])
            matrix = initMatrix(ancho)
        
        elif lineTokenList[i][0] == 'backColor':
            colorFondo = re.findall(colorPattern,lineTokenList[i][1])
            matrix = background(colorFondo[0],matrix,ancho)

        elif lineTokenList[i][0] == 'direccion':

            if lineTokenList[i][1] == 'Derecha':
                directionIndex = changeDirection(directionIndex,'R')
            elif lineTokenList[i][1] == 'Izquierda':
                directionIndex = changeDirection(directionIndex,'L')
            playerDirection = directions[directionIndex]
            #print(playerDirection)

        elif lineTokenList[i][0] == 'avanzar':
            indAvances = 0
            avancesEsperados = 1
            cantidadAv = re.findall(digPattern,lineTokenList[i][1])
            if(len(cantidadAv))>0:
                avancesEsperados = int(cantidadAv[0])
                
            while indAvances<avancesEsperados:        
                if playerDirection == 'North':
                    playerPos[0]-=1
                elif playerDirection == 'South':
                    playerPos[0]+=1
                elif playerDirection == 'West':
                    playerPos[1]+=1
                elif playerDirection == 'East':
                    playerPos[1]-=1
                indAvances+=1
            
            #print(playerPos)
        
        elif lineTokenList[i][0] == 'pintar':
            #print(lineTokenList[i][1])
            colorPintura = re.findall(colorPattern,lineTokenList[i][1]) 
            matrix = paintCell(colorPintura[0],matrix,playerPos)

        #print(lineTokenList[i])
        
    
    completeCode += line
    iteration+=1

file.close()

if numErrores == 0:
    errorFile.write("No hay errores!")
    for i in range(ancho):
        print(matrix[i])
    MatrizAImagen(matrix)

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


