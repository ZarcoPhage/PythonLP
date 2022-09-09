...............................
interprete de lenguaje PixelArt
...............................
-----------------------------------------------
REQUERIMENTOS
-----------------------------------------------

> Python 3.9.2
> Instalar paquete Pillow 9.1.0 
> Instalar paquete numpy 1.19.5

-----------------------------------------------
DESCRIPCIÓN
-----------------------------------------------
Este programa se encarga de interpretar y ejecutar el lenguaje PixelArt (LPA), realizando
análisis sintactico al código que se le entrega en el archivo "código.txt" presente en la
carpeta del programa, si la sintaxis del código es correcta, el programa se ejecuta
secuencialmente, generando una imagen según las instrucciones otorgadas, en otro caso, genera
un archivo de errores del código

-----------------------------------------------
COMO USAR
-----------------------------------------------
> asegurarse de cumplir con los requerimentos
> para utilizar este programa de forma óptima, ingrese su código en el archivo "codigo.txt"
  de la presente carpeta
> las primeras dos lineas de su codigo deben ir en el siguiente formato:
    1 Ancho <numero>
    2 Color de fondo <Color>

    > los numeros pueden variar mientras sean numeros positivos
    > el color por otra parte puede ser un color predeterminado (Rojo, Verde, Blanco, Negro
      o Azul), o un color en su código RGB, el cual debe ser ingresado en formato RGB(0-255,0-255,0-255)
    > si los códigos RGB salen del rango de numeros 0-255, se considerará error de sintaxis
    > si hace uso de los colores predeterminados, estos deben llevar la primera letra en mayuscula, de otra
      forma se considerará error de sintaxis
    > la instruccion de Ancho asigna el tamano de su imagen, debe estar únicamente en la primera
      línea de su código, de otra forma, se considerará error y será agregado al archivo de errores de sintaxis
    > la instruccion de Color de fondo debe ubicarse en la segunda línea de su código y solo podrá
      ser ocupada una vez, de otra forma, se considerará error y será agregado como error de sintaxis

> las instrucciones SIEMPRE se ejecutan de izquierda a derecha, factor a tener en cuenta al escribir su código
> una vez escritas estas lineas, debe tener en cuenta que su imagen se iniciará con el ancho y
  color otorgados, su jugador/Pincel inicia en la posición 0,0 de su matriz, siendo esta la esquina
  superior izquierda, y en direccion hacia el Oeste haciendo uso del plano cartesiano y 4 direcciones,
  Norte, Sur, Este, Oeste
> a partir de la tercera línea puede hacer uso de las siguientes instrucciones para generar su imagen:
    > Izquierda: para girar su jugador/pincel/puntero a la izquierda en 90 grados (sentido antihorario)
    
    > Derecha: para girar su jugador/pincel/puntero a la derecha en 90 grados (sentido horario)
    
    > Avanzar <numero>: para avanzar a su jugador en una posicion en la direccion que se encuentra
        > si su jugador sale de la matriz en alguna direccion, se considerará error de ejecución 
          y la imagen no será generada
        > el numero debe ser positivo

    > Pintar <color>: para pintar la casilla actual de su jugador del color seleccionado
        > esta orden sigue las mismas instrucciones que los colores para el color de fondo, es decir,
          los colores predeterminados deben llevar su primera letra mayuscula, y los códigos RGB deben responder
          al formato RGB(<numero>,<numero>,<numero>), los numeros de estos códigos no pueden bajar de cero ni sobrepasar
          255, de otra forma, se considerará error de sintaxis
    
    > Repetir <numero> veces { <instrucciones> }: para generar ciclos en su código
        > esta instruccion en específico tiene sintaxis fuerte, SIEMPRE debe invocarse sola en una linea, donde las 
          instrucciones de las lineas siguientes deben estar indentadas, para cerrar el ciclo, debe incluirse
          la llave cerrada ( } ) sin indentar, tal como el siguiente ejemplo:

            Repetir 4 veces {
                Pintar Rojo Avanzar
                Avanzar
                <instrucciones>
                <instrucciones>
                ...    
            } 

        > esta sintaxis debe respetarse en todo momento, de otra manera puede considerarse error de sintaxis o, en su 
          defecto, llevar a comportamiento inesperado del programa (generar otra imagen inesperada, crash del programa,
          entre otros).
        > si se desea anidar instrucciones de Repetir, debe respetarse de igual forma esta sintaxis, para evitar comportamiento
          inesperado, tal como el siguiente ejemplo:

            Repetir 4 veces {
                Pintar Rojo Avanzar
                Avanzar
                Repetir 3 veces {
                    Avanzar Pintar RGB(1,5,2)
                    <instrucciones>
                    ...
                }
                <instrucciones>
                <instrucciones>
                ...    
            }

        > el programa no acepta ordenes de repetir de una sola linea, ya que lleva a comportamiento indebido del programa

> cualquiera de las instrucciones mencionadas que se invoquen deben escribirse tal cual se presentan, de otra forma,
  se considerarán error de sintaxis

> para ejecutar el programa luego de escribir su código, dirijase en terminal a la carpeta del programa y use el siguiente comando:

    $ python main.py

> en el caso de una ejecución exitosa, se imprimirá por pantalla la matriz resultante final y se generará una imagen
  con nombre "pixelart.png" a partir de la matriz

> en caso de errores de sintaxis, se generará un archivo "errores.txt" en la carpeta del programa con las lineas de error
     
-------------------------------------------------
CONSIDERACIONES
-------------------------------------------------
> el programa no ha sido exhaustivamente testeado, por lo que pueden existir ciertos bugs en la ejecución que no hayan sido probados
> este programa fue desarrollado en Linux:
    Parrot OS 5.0 (Electro Ara)
> se incluye un codigo de prueba para entender la sintaxis que debe ser utilizada, si desea cambiar la imagen y usar otro código,
  sobreescriba el archivo "codigo.txt" presente en la carpeta
