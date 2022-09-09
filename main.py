import re
import numpy as np
from PIL import Image

class player:
    '''
    clase que permite guardar y encapsular los datos del jugador para realizar recursión sin afectar la ejecución
    '''
    def __init__(self, directionIndex, playerPos, directionList = ('West','South','East','North')):
        '''
        inicializa los datos del jugador, permitiendo posteriormente almacenar sus datos para rescatarlos y/o actualizarlos 
        al realizar recursión
        
            parametros:
                directionIndex (int): indice de direccion inicial para determinar la direccion por defecto del jugador segun su lista de direcciones, varia entre 0 y 3
                playerPos (lista de dos enteros): posicion inicial del jugador en formato [x,y]
        '''

        self.directionList = directionList
        self.directionIndex = directionIndex
        self.playerPos = playerPos
        self.playerDirection = directionList[directionIndex]

    def setPlayerPos(self, newPlayerPos):
        '''
        guarda en el objeto la posición del jugador con respecto a la matriz

            parametros:
                newPlayerPos (lista de dos enteros): posicion del jugador respecto a la matriz en formato [x,y]
            
            retorno:
                no retorna, solo actualiza datos del objeto
        '''
        self.playerPos = newPlayerPos
        #print(self.playerPos)

    def setPlayerDirection(self, newDirectionIndex):
        '''
        actualiza la direccion del jugador a partir de su nuevo indice de dirección, reasignando la dirección
        segun las posiciones de la lista de direcciones disponibles del jugador

            parametros:
                newDirectionIndex(int): nuevo indice de direccion con el que se desea acceder a la lista de direcciones y actualizar la direccion del jugador, varia entre 0-3
        
            retorno:
                no retorna, solo actualiza los datos de la direccion del jugador
        '''
        self.directionIndex = newDirectionIndex
        self.playerDirection = self.directionList[self.directionIndex]
        #print(self.playerDirection)

class matrix:
    '''
    clase que permite guardar y encapsular los datos de la matriz para utilizarse en recursión sin afectar la ejecución
    '''
    def __init__(self, matriz=[]):
        '''
        inicializa el objeto como una lista vacía, permitiendo actualizar posteriormente la matriz
        
            parametros:
                no recibe parametros como tal

            retorno:
                no retorna, solo genera el objeto
        '''
        self.matriz = matriz

    def updateMatrix(self, matriz):
        '''
        actualiza la matriz del objeto, guardando los nuevos datos actualizados de la matriz

            parametros:
                matriz (lista de listas de tuplas de enteros): matriz correspondiente a la imagen que se desea guardar y encapsular, contiene los datos de los colores de cada casilla de la matriz
            
            retorno:
                no retorna, solo actualiza la matriz del objeto
        '''
        self.matriz = matriz
        #for i in range(len(self.matriz)):
        #    print(self.matriz[i])

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


def tokenizer(code):
    '''
    basado en el ejemplo de Tokenizer del modulo RE de python, identifica los tokens de cierto string
    correspondiente al codigo y realiza análisis sintactico, permite iterar el string, retornando tuplas
    en formato (<instruccion>,<expresion>), las cuales se pueden guardar posteriormente en una lista para ejecutar
    código secuencialmente, dado que se utiliza yield en lugar de return, transformando la funcion en generador
    permitiendo suspender la función sin eliminar variables locales, 

        parametros:
            code(string): string del archivo de código al cual se desea analizar sintaxis e identificar tokens
        
        retorno:
            tup (tupla): tupla correspondiente al token identificado, en formato (<nombre_instruccion>,<expresión_reconocida>)
    '''
    tokenSpecs = [
        #('numero', r' \d+'),
        ('ancho',r'Ancho \d+'),
        ('backColor',r'Color de fondo (Rojo|Verde|Azul|Negro|Blanco|RGB[(]([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])[,]([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])[,]([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])[)])'),
        #('color', r'Rojo|Verde|Azul|Negro|Blanco|RGB[(]\d+[,]\d+[,]\d+[)]'),
        ('repetir', r'Repetir \d+ veces {'),
        ('pintar', r'Pintar (Rojo|Verde|Azul|Negro|Blanco|RGB[(]([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])[,]([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])[,]([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])[)])'),
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
        tup = (tipo, valor)
        yield tup

def initMatrix(ancho):
    '''
    funcion que inicializa la matriz, formando las filas y columnas según el ancho dado, rellenando 
    y formando cada casilla con un color predeterminado, retorna la matriz inicializada, la cual se puede
    guardar en el objeto Matriz

        parametros:
            ancho (int): tamano que se le desea dar a la matriz, inicializandola como matriz cuadrada de tamano ancho x ancho

        retorno:
            matrix (lista de listas de tuplas de enteros): matriz cuadrada ancho x ancho, correspondiente a la imagen que se desea crear, donde cada posicion de la matriz es una tupla correspondiente a cierto color

    '''
    matrix = []
    for i in range(ancho):
        filasMatriz = []
        for j in range(ancho):
            filasMatriz.append((0,0,0))
        matrix.append(filasMatriz)
    
    return matrix

def background(color, matrix, ancho):
    '''
    pinta el fondo de la matriz de cierto color según su color ya sea por nombre o en código RGB,
    retornando la matriz para su actualización en el objeto Matrix

        parametros:
            color (string): nombre de cierto color o su código RGB correspondiente, con el que se desea pintar el fondo de la imagen
            matrix (lista de listas de tuplas): matriz correspondiente a la imagen, donde cada tupla corresponde al color de casilla
            ancho (int): tamano de la matriz, con el que se permite iterar y actualizar los datos
        
        retorno:
            matrix (lista de listas de tuplas de enteros): matriz correspondiente a la imagen con el fondo pintado segun el color
    '''
    
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
        for j in range(ancho):
            for i in range(ancho):
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
    '''
    pinta la casilla de la posicion del jugador en la matriz segun cierto codigo de color
    identificado y retorna la matriz para su actualización

        Parametros:
            color (string): string con el nombre del color o el codigo RGB de cierto color con el que se desea pintar la casilla
            matrix (lista de listas de tuplas): matriz correspondiente a la imagen recuperada del objeto 'Matriz', donde cada tupla es una casilla correspondiente a un color
            player (objeto/clase): objeto que almacena la posición y dirección del jugador

        Retorno:
            matrix (lista de listas de tuplas de enteros): matriz actualizada que se utiliza para actualizar los datos del objeto matriz
    '''
    
    playerPos = player.playerPos
    xPos = playerPos[0]
    yPos = playerPos[1]
    #print(xPos,yPos)
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
    '''
    actualiza la direccion del jugador segun su indice de direccion (el cual varía entre 0 y 3, donde
    0 corresponde a oeste, 1 a sur, 2 a este y 3 a norte) y la orden (izquierda o derecha), actualizando 
    la dirección de movimiento del jugador según se necesite al invocar la función con respecto al token reconocido

        Parametros:
            directionIndex (int): indice de direccion actual del jugador
            order (string): direccion a la que se desea girar al jugador (R para derecha, L para izquierda)
        
        Retorno:
            directionIndex(int): indice de direccion actualizado del jugador, permite actualizar la direccion posteriormente
    '''
    #print('preCambio:'+str(directionIndex))
    if order == 'R':
        directionIndex+=1
    elif order == 'L':
        directionIndex+=3 
    #print('postCambio:'+str(directionIndex))
    directionIndex = directionIndex % 4
    #print ('postMod:'+str(directionIndex))
    return directionIndex

def commandExecution(matriz, ancho, lines, player):
    '''
    Funcion que toma los objetos de la matriz y el jugador, rescata sus datos y los actualiza segun los tokens reconocidos previamente en el
    analisis lexico, ejecutando secuencialmente las ordenes reconocidas

        Parametros:
            matriz (objeto): lista de listas de tuplas de enteros correspondientes a los colores, formando una matriz de cierto ancho que se reconoce según tokens
            ancho (int): tamano de la matriz n x n correspondiente a los colores, con el cual se inicializa e itera la matriz
            lines (lista): lista de listas de tuplas, cada sublista interior (correspondiente a una linea) contiene los tokens identificados de la linea, los cuales se encuentran en una tupla, cada cual en formato ('<instrucción>','<expresión identificada>')
            player (objeto): datos del jugador, su posicion y dirección

        Retorno:
            No retorna, solo actúa como proceso, actualizando la matriz y el jugador segun los tokens identificados
    '''
    tempPlayerPos = player.playerPos
    #tempDirectionIndex = player.directionIndex
    playerDirection = player.playerDirection
    matrix = matriz.matriz
    errorLineFlag = False
    numErrores = 0
    cycleTabs = 0

    for i in range(len(lines)):
        largoLinea = len(lines[i])
        #print(lines[i])
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
                tempDirectionIndex = player.directionIndex
                if lines[i][j][1] == 'Derecha':
                    #print('DER')
                    tempDirectionIndex = changeDirection(tempDirectionIndex,'R')
                elif lines[i][j][1] == 'Izquierda':
                    #print('IZQ')
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
                if player.playerPos[0] > (ancho-1):
                    #raise ValueError('Player out of boundaries')
                    print('player out of matrix')
                    exit()
                elif player.playerPos[1] > (ancho-1):
                    print('player out of matrix')
                    exit()
                elif player.playerPos[0] < 0:
                    print('player out of matrix')
                    exit()
                elif player.playerPos[1] < 0:
                    print('player out of matrix')
                    exit()

                #print(player.playerPos)
        
            elif lines[i][j][0] == 'pintar':
                colorPintura = re.findall(colorPattern,lines[i][j][1])
              
                matrix = paintCell(colorPintura[0],matrix,player)
                #for kl in range(len(matrix)):
                #    print(matrix[kl])
                matriz.updateMatrix(matrix) #new

            elif lines[i][j][0] == 'repetir':
                cantidadRep = re.findall(digPattern, lines[i][j][1])
                repEsperadas= int(cantidadRep[0])
                firstLinePointer = i+1
                lastLinePointer = i+1
                neededTabs = 1
                tempLines = []
                while lastLinePointer<len(lines):
                    #print(lines[lastLinePointer])
                    tempLines.append(lines[lastLinePointer])
                    if lines[lastLinePointer][j][0] == 'cierraCiclo':
                        break
                    #print("FLAG")
                    #print(lastLinePointer)
                    #print(len(lines))
                    lastLinePointer+=1   

                #print("POSTRECOVERY")
                repLinesqty = lastLinePointer-firstLinePointer
                
                #for l in range(repLinesqty):
                #    print(tempLines[l])
                
                #print("LINESFORREP")
                for l in range(repLinesqty):
                    if tempLines[l][0][0] == 'tab':
                        tempLines[l].pop(0)
                    #print(tempLines[l])
                #print("ENDLINESFORREP")

                repRealizadas = 1
                #print("START CYCLE:")
                while repRealizadas<repEsperadas:
                    commandExecution(matriz,ancho,tempLines,player)
                    #print("POSTRECURSION")
                    repRealizadas+=1
                #print("END CYCLE")

################################################
# CODIGO MAIN
################################################

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
playerPos = [0,0]

for line in file:
    completeCode.append(line)
file.close()

lines = []
errorLines = []
errorFile = open("errores.txt","w+")
for line in completeCode:
    
    errorLineFlag = False
    lineTokenList = []
    for token in tokenizer(line):
        if token[0] == 'NOMATCH':
            #print("FOUND")
            execute = False
            errorLines.append((iteration,line))
        lineTokenList.append(token)
        if token[0] == 'ancho':
            #print("FOUND")
            if iteration != 1:
                execute = False
                errorLines.append((iteration,line))
        if token[0] == 'backColor':
            if iteration != 2:
                execute = False
                errorLines.append((iteration,line))
    
    lines.append(lineTokenList)
    iteration+=1

for errorIndex in range(len(errorLines)):
    errorFile.write(str(errorLines[errorIndex][0])+" "+errorLines[errorIndex][1])

file.close()

if execute:
    errorFile.write("No hay errores!")
    J1 = player(directionIndex,playerPos)
    matrizPNG = matrix()
    commandExecution(matrizPNG,ancho,lines,J1)
    MatrizAImagen(matrizPNG.matriz)
    for l in range(len(matrizPNG.matriz)):
        print(matrizPNG.matriz[l])

errorFile.close()