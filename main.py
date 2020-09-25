import soko
import gamelib
from time import sleep
from Pila import Pila

VACIO=" "
PARED="#"
CAJA="$"
JUGADOR="@"
OBJETIVO="."
OBJETIVO_CAJA="*"
OBJETIVO_JUGADOR="+"
NORTE=(0,-1)
SUR=(0,1)
ESTE=(1,0)
OESTE=(-1,0)

def cargar_memoria(archivo):
    """
    Lee el archivo con los niveles recibido por parametro y los guarda en una lista de listas
    donde cada lista contiene 2 elementos, el primero el numero del nivel mas el titulo si es que tiene,
    y el segundo la descripcion del nivel
    """
    niveles=[]
    desc=[]
    try:
        with open(archivo) as n:
            for linea in n:
                if "\n"==linea:
                    niveles.append([nivel,desc])
                    desc=[]
                linea=linea.strip("\n")
                if "Level" in linea:
                    nivel=linea
                if "'" in linea:
                    nivel+=" - "+linea
                if PARED in linea:
                    desc.append(linea)
    except IOError:
        print(f"El archivo {archivo} no existe")
    
    return niveles

def cargar_configuracion_teclas(archivo):
    """
    Recibe un archivo con la asignacion de las teclas a sus respectivas acciones,
    el formato del archivo debe ser <tecla>=<accion>, donde <tecla> puede ser cualquier
    tecla del teclado y <accion> debe ser una de las acciones posibles en el juego,
    que son NORTE, SUR, ESTE, OESTE, REINICIAR y SALIR.

    Nota: una accion puede esta asociada a mas de una tecla.

    Devuelve un diccionario con la configuracion de las teclas, donde las claves son
    las acciones posibles y los valores son una lista con las teclas asignadas a esa
    accion.
    """
    configuracion_de_teclas={"NORTE":[], "SUR":[], "ESTE":[], "OESTE":[], "REINICIAR":[], "SALIR":[], "DESHACER":[], "PISTA":[]}
    try:
        with open(archivo) as configuracion:
            for linea in configuracion:
                linea=linea.rstrip("\n")
                if "=" not in linea:
                    continue
                linea=linea.split("=")# linea queda de esta forma:[<tecla>,<accion>]
                for accion in configuracion_de_teclas:
                    if accion==linea[1].lstrip():
                        configuracion_de_teclas[accion].append(linea[0].rstrip())
    except IOError:
        print(f"El archivo {archivo} no existe")

    return configuracion_de_teclas
    
def pedir_accion(configuracion, tecla):
    """
    Recibe la configuracion de teclas y una tecla,
    y devuelve la accion asociada a esa tecla
    """
    movimientos={"NORTE":NORTE, "SUR":SUR, "ESTE":ESTE, "OESTE":OESTE}
    for accion in configuracion:
        if tecla in configuracion[accion]:
            if accion in movimientos:
                return movimientos.get(accion)
            return accion
    return None

def juego_mostrar(grilla, titulo):
    """
    Dibuja la grilla recibida en la pantalla
    """
    imagenes={PARED:'img/wall.gif' ,CAJA:'img/box.gif' ,JUGADOR:'img/player.gif' ,OBJETIVO:'img/goal.gif', VACIO:'img/ground.gif'}
    gamelib.title(titulo)
    
    for fila in range(len(grilla)):
        for celda in range(len(grilla[0])):
            gamelib.draw_image('img/ground.gif', 64*celda, 64*fila)
            if grilla[fila][celda]==OBJETIVO_CAJA:
                gamelib.draw_image(imagenes[CAJA], 64*celda, 64*fila)
                gamelib.draw_image(imagenes[OBJETIVO], 64*celda, 64*fila)
                continue
            if grilla[fila][celda]==OBJETIVO_JUGADOR:
                gamelib.draw_image(imagenes[JUGADOR], 64*celda, 64*fila)
                gamelib.draw_image(imagenes[OBJETIVO], 64*celda, 64*fila)
                continue
            gamelib.draw_image(imagenes[grilla[fila][celda]], 64*celda, 64*fila)

def h(grilla):
    """
    Recibe la grilla como lista de listas y devuelve una representacion inmutable de esta,
    que sera una cadena con la representación del nivel en el formato de niveles.txt
    """
    nuevo = ""
    for fila in grilla:
        nuevo += "\n"
        for celda in fila:
            nuevo += celda
    return nuevo
                
def buscar_solucion(grilla):
    return _backtrack(grilla, {}, (NORTE, ESTE, OESTE, SUR), Pila())
    
def _backtrack(grilla, visitados, acciones_posibles, movimientos):
    visitados[h(grilla)] = True
    if soko.juego_ganado(grilla):
        return True, movimientos
    for accion in acciones_posibles:
        nuevo_estado = soko.mover(grilla, accion)
        if h(nuevo_estado) in visitados:
            continue
        solucion_encontrada, movimientos = _backtrack(nuevo_estado, visitados, acciones_posibles, movimientos)
        if solucion_encontrada:
            movimientos.apilar(accion)
            return True, movimientos
    return False, Pila()

def main():
    niveles=cargar_memoria("niveles.txt")
    configuracion=cargar_configuracion_teclas("teclas.txt")
    for nivel in niveles:
        # Inicializar el estado del juego
        grilla=soko.crear_grilla(nivel[1])
        gamelib.resize(len(grilla[0])*64, len(grilla)*64)
        movimientos = Pila()
        
        while gamelib.is_alive():
            # Dibujar la pantalla
            gamelib.draw_begin()
            juego_mostrar(grilla, nivel[0])
            gamelib.draw_end()

            ev = gamelib.wait(gamelib.EventType.KeyPress)
            if not ev:
                break

            tecla = ev.key
            accion = pedir_accion(configuracion, tecla)

            # Actualizar el estado del juego, según la `tecla` presionada
            
            if accion == "PISTA":
                gamelib.draw_begin()
                juego_mostrar(grilla, nivel[0])
                gamelib.draw_text("Pensando...", 40, 10, size=10, fill="white")
                gamelib.draw_end()
                solucion = buscar_solucion(grilla)
                gamelib.get_events()
                
                if not solucion[0]:
                    gamelib.draw_begin()
                    juego_mostrar(grilla, nivel[0])
                    gamelib.draw_text("No hay pistas disponibles :(", 85, 10, size=10, fill="white")
                    gamelib.draw_end()
                    ev = gamelib.wait(gamelib.EventType.KeyPress)
                    continue
                    
                if solucion[0]:
                    gamelib.draw_begin()
                    juego_mostrar(grilla, nivel[0])
                    gamelib.draw_text("Pista Disponible", 50, 10, size=10, fill="white")
                    gamelib.draw_end()
                    while not solucion[1].esta_vacia():
                        ev = gamelib.wait(gamelib.EventType.KeyPress)
                        if not ev:
                            break
                        tecla = ev.key
                        accion = pedir_accion(configuracion, tecla)
                        if accion != None and accion != "PISTA":
                            break
                        if accion == "PISTA":
                            movimientos.apilar(grilla)
                            grilla = soko.mover(grilla, solucion[1].desapilar())
                            gamelib.draw_begin()
                            juego_mostrar(grilla, nivel[0])
                            gamelib.draw_text("Pista Disponible", 50, 10, size=10, fill="white")
                            gamelib.draw_end()
            
            if soko.juego_ganado(grilla):
                sleep(0.1)
                break
            
            if accion=="SALIR":
                return
            
            if accion=="REINICIAR":
                grilla=soko.crear_grilla(nivel[1])
                movimientos = Pila()
                continue
            
            if accion == "DESHACER":
                if movimientos.esta_vacia():
                    continue
                grilla = movimientos.desapilar()
                continue        
            
            if not accion:
                continue
            
            movimientos.apilar(grilla)
            grilla=soko.mover(grilla, accion)
            
            if soko.juego_ganado(grilla):
                gamelib.draw_begin()
                juego_mostrar(grilla, nivel[0])
                gamelib.draw_end()
                sleep(0.1)
                break
            
gamelib.init(main)