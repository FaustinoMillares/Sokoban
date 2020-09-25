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

def crear_grilla(desc):
    '''Crea una grilla a partir de la descripción del estado inicial.

    La descripción es una lista de cadenas, cada cadena representa una
    fila y cada caracter una celda. Los caracteres pueden ser los siguientes:

    Caracter  Contenido de la celda
    --------  ---------------------
           #  Pared
           $  Caja
           @  Jugador
           .  Objetivo
           *  Objetivo + Caja
           +  Objetivo + Jugador

    Ejemplo:

    >>> crear_grilla([
        '#####',
        '#.$ #',
        '#@  #',
        '#####',
    ])
    '''
    grilla=[]
    for filas in range(len(desc)):
        grilla.append([])
        for columnas in range(len(desc[filas])):#Me alcanza con utilizar la primer fila ya que como la grilla es rectangular las columnas son iguales en todas las filas
            grilla[filas].append(desc[filas][columnas])
    
    maximo=0
    for i in grilla:
        if len(i)>maximo:
            maximo=len(i)
    for f in grilla:
        while len(f)<maximo:
            f.append(" ")
            
    return grilla

def posicion_jugador(grilla):
    '''Devuelve una tupla con la columna y fila donde se encuentra el jugador'''
    for filas in range(len(grilla)):
        for columnas in range (len(grilla[0])):
            if grilla[filas][columnas]==JUGADOR or grilla[filas][columnas]==OBJETIVO_JUGADOR:
                posicion=(columnas, filas)
                return posicion

def dimensiones(grilla):
    '''Devuelve una tupla con la cantidad de columnas y filas de la grilla.'''
    f=len(grilla)
    c=len(grilla[0])#Como la grilla sera rectangular las columnas son iguales en todas las filas, asi que alcanza con ver cuantas hay en la primera fila
    dimensiones=(c, f)
    return dimensiones


def hay_pared(grilla, c, f):
    '''Devuelve True si hay una pared en la columna y fila (c, f).'''
    if PARED in grilla[f][c]:
        return True
    return False

def hay_objetivo(grilla, c, f):
    '''Devuelve True si hay un objetivo en la columna y fila (c, f).'''
    if grilla[f][c]==OBJETIVO or grilla[f][c]==OBJETIVO_JUGADOR or grilla[f][c]==OBJETIVO_CAJA:
        return True
    return False

def hay_caja(grilla, c, f):
    '''Devuelve True si hay una caja en la columna y fila (c, f).'''
    if grilla[f][c]==CAJA or grilla[f][c]==OBJETIVO_CAJA:
        return True
    return False

def hay_jugador(grilla, c, f):
    '''Devuelve True si el jugador está en la columna y fila (c, f).'''
    if grilla[f][c]==JUGADOR or grilla[f][c]==OBJETIVO_JUGADOR:
        return True
    return False

def hay_vacio(grilla, c, f):
    '''Devuelve True si la columna y fila (c, f) esta vacia'''
    if VACIO in grilla[f][c]:
        return True
    return False

def juego_ganado(grilla):
    '''Devuelve True si el juego está ganado.'''
    for f in range(len(grilla)):
        for c in range(len(grilla[0])):
            if grilla[f][c]==OBJETIVO or grilla[f][c]==OBJETIVO_JUGADOR:# Ya que la consigna nos dice que: "la grilla contiene al menos tantas cajas como objetivos", entonces para que el juego este ganado no deberia haber ni objetivos vacios ni objetivos con jugador en toda la grilla
                return False
    return True

def mover(grilla, direccion):
    '''Mueve el jugador en la dirección indicada.

    La dirección es una tupla con el movimiento horizontal y vertical. Dado que
    no se permite el movimiento diagonal, la dirección puede ser una de cuatro
    posibilidades:

    direccion  significado
    ---------  -----------
    (-1, 0)    Oeste
    (1, 0)     Este
    (0, -1)    Norte
    (0, 1)     Sur

    La función debe devolver una grilla representando el estado siguiente al
    movimiento efectuado. La grilla recibida NO se modifica; es decir, en caso
    de que el movimiento sea válido, la función devuelve una nueva grilla.
    '''
    nueva_grilla=grilla[:]#Creo una nueva_grilla copiando la grilla que viene por parametro
    posicion = posicion_jugador(grilla)#Utilizo esta funcion para saber donde esta mi jugador y a partir de esa posicion efectuar los movimientos
    c_jugador = posicion[0]
    f_jugador = posicion[1]
    c_nueva = c_jugador + direccion[0]
    f_nueva = f_jugador + direccion[1]
    if hay_pared(grilla, c_nueva, f_nueva):
        return nueva_grilla
    if hay_vacio(grilla, c_nueva, f_nueva):
        if hay_objetivo(grilla, c_jugador, f_jugador):
            nueva_f_jugador=nueva_grilla[f_jugador][:]      #------------------------------------------------------
            nueva_f_jugador[c_jugador]=OBJETIVO             # Esto es en caso de que se mueva direccion Norte o Sur
            nueva_grilla.pop(f_jugador)                     # y haya que cambiar 2 filas distintas 
            nueva_grilla.insert(f_jugador, nueva_f_jugador) #------------------------------------------------------
            
            nueva_fila=nueva_grilla[f_nueva][:]
            nueva_fila[c_jugador]=OBJETIVO
            nueva_fila[c_nueva]=JUGADOR
            nueva_grilla.pop(f_nueva)
            nueva_grilla.insert(f_nueva, nueva_fila)
            
            return nueva_grilla
        else:
            nueva_f_jugador=nueva_grilla[f_jugador][:]      #------------------------------------------------------
            nueva_f_jugador[c_jugador]=VACIO                # Esto es en caso de que se mueva direccion Norte o Sur
            nueva_grilla.pop(f_jugador)                     # y haya que cambiar 2 filas distintas 
            nueva_grilla.insert(f_jugador, nueva_f_jugador) #------------------------------------------------------
            
            nueva_fila=nueva_grilla[f_nueva][:]
            nueva_fila[c_jugador]=VACIO
            nueva_fila[c_nueva]=JUGADOR
            nueva_grilla.pop(f_nueva)
            nueva_grilla.insert(f_nueva, nueva_fila)
            
            return nueva_grilla
    if hay_objetivo(grilla, c_nueva, f_nueva) and not hay_caja(grilla, c_nueva, f_nueva):
        if hay_objetivo(grilla, c_jugador, f_jugador):
            nueva_f_jugador=nueva_grilla[f_jugador][:]      #------------------------------------------------------
            nueva_f_jugador[c_jugador]=OBJETIVO             # Esto es en caso de que se mueva direccion Norte o Sur
            nueva_grilla.pop(f_jugador)                     # y haya que cambiar 2 filas distintas 
            nueva_grilla.insert(f_jugador, nueva_f_jugador) #------------------------------------------------------
            
            nueva_fila=nueva_grilla[f_nueva][:]
            nueva_fila[c_jugador]=OBJETIVO
            nueva_fila[c_nueva]=OBJETIVO_JUGADOR
            nueva_grilla.pop(f_nueva)
            nueva_grilla.insert(f_nueva, nueva_fila)
            
            return nueva_grilla
        else:
            nueva_f_jugador=nueva_grilla[f_jugador][:]      #------------------------------------------------------
            nueva_f_jugador[c_jugador]=VACIO                # Esto es en caso de que se mueva direccion Norte o Sur
            nueva_grilla.pop(f_jugador)                     # y haya que cambiar 2 filas distintas 
            nueva_grilla.insert(f_jugador, nueva_f_jugador) #------------------------------------------------------
            
            nueva_fila=nueva_grilla[f_nueva][:]
            nueva_fila[c_jugador]=VACIO
            nueva_fila[c_nueva]=OBJETIVO_JUGADOR
            nueva_grilla.pop(f_nueva)
            nueva_grilla.insert(f_nueva, nueva_fila)
            
            return nueva_grilla
    if hay_caja(grilla, c_nueva, f_nueva) and not hay_objetivo(grilla, c_nueva, f_nueva):
        if hay_pared(grilla, c_nueva+direccion[0], f_nueva+direccion[1]) or hay_caja(grilla, c_nueva+direccion[0], f_nueva+direccion[1]):
            return nueva_grilla
        if hay_vacio(grilla, c_nueva+direccion[0], f_nueva+direccion[1]):
            if hay_objetivo(grilla, c_jugador, f_jugador):
                nueva_f_jugador=nueva_grilla[f_jugador][:]                  #------------------------------------------------------
                nueva_f_jugador[c_jugador]=OBJETIVO                         #------------------------------------------------------
                nueva_grilla.pop(f_jugador)                                 #------------------------------------------------------
                nueva_grilla.insert(f_jugador, nueva_f_jugador)             #------------------------------------------------------
                                                                            #------------------------------------------------------
                nueva_f_caja=nueva_grilla[f_nueva][:]                       #------------------------------------------------------
                nueva_f_caja[c_jugador]=JUGADOR                             # Esto es en caso de que se mueva direccion Norte o Sur
                nueva_grilla.pop(f_nueva)                                   # y haya que cambiar 3 filas distintas
                nueva_grilla.insert(f_nueva, nueva_f_caja)                  #------------------------------------------------------
                                                                            #------------------------------------------------------
                nueva_f_vacio=nueva_grilla[f_nueva+direccion[1]][:]         #------------------------------------------------------
                nueva_f_vacio[c_jugador]=CAJA                               #------------------------------------------------------
                nueva_grilla.pop(f_nueva+direccion[1])                      #------------------------------------------------------
                nueva_grilla.insert(f_nueva+direccion[1], nueva_f_vacio)    #------------------------------------------------------
                
                nueva_fila=nueva_grilla[f_nueva][:]
                nueva_fila[c_jugador]=OBJETIVO
                nueva_fila[c_nueva+direccion[0]]=CAJA
                nueva_fila[c_nueva]=JUGADOR
                nueva_grilla.pop(f_nueva)
                nueva_grilla.insert(f_nueva, nueva_fila)
                
                return nueva_grilla
            else:
                nueva_f_jugador=nueva_grilla[f_jugador][:]                  #------------------------------------------------------
                nueva_f_jugador[c_jugador]=VACIO                            #------------------------------------------------------
                nueva_grilla.pop(f_jugador)                                 #------------------------------------------------------
                nueva_grilla.insert(f_jugador, nueva_f_jugador)             #------------------------------------------------------
                                                                            #------------------------------------------------------
                nueva_f_caja=nueva_grilla[f_nueva][:]                       #------------------------------------------------------
                nueva_f_caja[c_jugador]=JUGADOR                             # Esto es en caso de que se mueva direccion Norte o Sur
                nueva_grilla.pop(f_nueva)                                   # y haya que cambiar 3 filas distintas
                nueva_grilla.insert(f_nueva, nueva_f_caja)                  #------------------------------------------------------
                                                                            #------------------------------------------------------
                nueva_f_vacio=nueva_grilla[f_nueva+direccion[1]][:]         #------------------------------------------------------
                nueva_f_vacio[c_jugador]=CAJA                               #------------------------------------------------------
                nueva_grilla.pop(f_nueva+direccion[1])                      #------------------------------------------------------
                nueva_grilla.insert(f_nueva+direccion[1], nueva_f_vacio)    #------------------------------------------------------
                
                nueva_fila=nueva_grilla[f_nueva][:]
                nueva_fila[c_jugador]=VACIO
                nueva_fila[c_nueva+direccion[0]]=CAJA
                nueva_fila[c_nueva]=JUGADOR
                nueva_grilla.pop(f_nueva)
                nueva_grilla.insert(f_nueva, nueva_fila)
                
                return nueva_grilla
        if hay_objetivo(grilla, c_nueva+direccion[0], f_nueva+direccion[1]):
            if hay_objetivo(grilla, c_jugador, f_jugador):
                nueva_f_jugador=nueva_grilla[f_jugador][:]                  #------------------------------------------------------
                nueva_f_jugador[c_jugador]=OBJETIVO                         #------------------------------------------------------
                nueva_grilla.pop(f_jugador)                                 #------------------------------------------------------
                nueva_grilla.insert(f_jugador, nueva_f_jugador)             #------------------------------------------------------
                                                                            #------------------------------------------------------
                nueva_f_caja=nueva_grilla[f_nueva][:]                       #------------------------------------------------------
                nueva_f_caja[c_jugador]=JUGADOR                             # Esto es en caso de que se mueva direccion Norte o Sur
                nueva_grilla.pop(f_nueva)                                   # y haya que cambiar 3 filas distintas
                nueva_grilla.insert(f_nueva, nueva_f_caja)                  #------------------------------------------------------
                                                                            #------------------------------------------------------
                nueva_f_objetivo=nueva_grilla[f_nueva+direccion[1]][:]      #------------------------------------------------------
                nueva_f_objetivo[c_jugador]=OBJETIVO_CAJA                   #------------------------------------------------------
                nueva_grilla.pop(f_nueva+direccion[1])                      #------------------------------------------------------
                nueva_grilla.insert(f_nueva+direccion[1], nueva_f_objetivo) #------------------------------------------------------
                
                nueva_fila=nueva_grilla[f_nueva][:]
                nueva_fila[c_jugador]=OBJETIVO
                nueva_fila[c_nueva+direccion[0]]=OBJETIVO_CAJA
                nueva_fila[c_nueva]=JUGADOR
                nueva_grilla.pop(f_nueva)
                nueva_grilla.insert(f_nueva, nueva_fila)
                
                return nueva_grilla
            else:
                nueva_f_jugador=nueva_grilla[f_jugador][:]                  #------------------------------------------------------
                nueva_f_jugador[c_jugador]=VACIO                            #------------------------------------------------------
                nueva_grilla.pop(f_jugador)                                 #------------------------------------------------------
                nueva_grilla.insert(f_jugador, nueva_f_jugador)             #------------------------------------------------------
                                                                            #------------------------------------------------------
                nueva_f_caja=nueva_grilla[f_nueva][:]                       #------------------------------------------------------
                nueva_f_caja[c_jugador]=JUGADOR                             # Esto es en caso de que se mueva direccion Norte o Sur
                nueva_grilla.pop(f_nueva)                                   # y haya que cambiar 3 filas distintas
                nueva_grilla.insert(f_nueva, nueva_f_caja)                  #------------------------------------------------------
                                                                            #------------------------------------------------------
                nueva_f_objetivo=nueva_grilla[f_nueva+direccion[1]][:]      #------------------------------------------------------
                nueva_f_objetivo[c_jugador]=OBJETIVO_CAJA                   #------------------------------------------------------
                nueva_grilla.pop(f_nueva+direccion[1])                      #------------------------------------------------------
                nueva_grilla.insert(f_nueva+direccion[1], nueva_f_objetivo) #------------------------------------------------------
                
                nueva_fila=nueva_grilla[f_nueva][:]
                nueva_fila[c_jugador]=VACIO
                nueva_fila[c_nueva+direccion[0]]=OBJETIVO_CAJA
                nueva_fila[c_nueva]=JUGADOR
                nueva_grilla.pop(f_nueva)
                nueva_grilla.insert(f_nueva, nueva_fila)
                
                return nueva_grilla
            
    if hay_caja(grilla, c_nueva, f_nueva) and hay_objetivo(grilla, c_nueva, f_nueva):
        if hay_pared(grilla, c_nueva+direccion[0], f_nueva+direccion[1]) or hay_caja(grilla, c_nueva+direccion[0], f_nueva+direccion[1]):
            return nueva_grilla
        if hay_vacio(grilla, c_nueva+direccion[0], f_nueva+direccion[1]):
            if hay_objetivo(grilla, c_jugador, f_jugador):
                nueva_f_jugador=nueva_grilla[f_jugador][:]                  #------------------------------------------------------
                nueva_f_jugador[c_jugador]=OBJETIVO                         #------------------------------------------------------
                nueva_grilla.pop(f_jugador)                                 #------------------------------------------------------
                nueva_grilla.insert(f_jugador, nueva_f_jugador)             #------------------------------------------------------
                                                                            #------------------------------------------------------
                nueva_f_cajayobjetivo=nueva_grilla[f_nueva][:]              #------------------------------------------------------
                nueva_f_cajayobjetivo[c_jugador]=OBJETIVO_JUGADOR           # Esto es en caso de que se mueva direccion Norte o Sur
                nueva_grilla.pop(f_nueva)                                   # y haya que cambiar 3 filas distintas
                nueva_grilla.insert(f_nueva, nueva_f_cajayobjetivo)         #------------------------------------------------------
                                                                            #------------------------------------------------------
                nueva_f_vacio=nueva_grilla[f_nueva+direccion[1]][:]         #------------------------------------------------------
                nueva_f_vacio[c_jugador]=CAJA                               #------------------------------------------------------
                nueva_grilla.pop(f_nueva+direccion[1])                      #------------------------------------------------------
                nueva_grilla.insert(f_nueva+direccion[1], nueva_f_vacio)    #------------------------------------------------------
                
                nueva_fila=nueva_grilla[f_nueva][:]
                nueva_fila[c_jugador]=OBJETIVO
                nueva_fila[c_nueva+direccion[0]]=CAJA
                nueva_fila[c_nueva]=OBJETIVO_JUGADOR
                nueva_grilla.pop(f_nueva)
                nueva_grilla.insert(f_nueva, nueva_fila)
                
                return nueva_grilla
            else:
                nueva_f_jugador=nueva_grilla[f_jugador][:]                  #------------------------------------------------------
                nueva_f_jugador[c_jugador]=VACIO                            #------------------------------------------------------
                nueva_grilla.pop(f_jugador)                                 #------------------------------------------------------
                nueva_grilla.insert(f_jugador, nueva_f_jugador)             #------------------------------------------------------
                                                                            #------------------------------------------------------
                nueva_f_cajayobjetivo=nueva_grilla[f_nueva][:]              #------------------------------------------------------
                nueva_f_cajayobjetivo[c_jugador]=OBJETIVO_JUGADOR           # Esto es en caso de que se mueva direccion Norte o Sur
                nueva_grilla.pop(f_nueva)                                   # y haya que cambiar 3 filas distintas
                nueva_grilla.insert(f_nueva, nueva_f_cajayobjetivo)         #------------------------------------------------------
                                                                            #------------------------------------------------------
                nueva_f_vacio=nueva_grilla[f_nueva+direccion[1]][:]         #------------------------------------------------------
                nueva_f_vacio[c_jugador]=CAJA                               #------------------------------------------------------
                nueva_grilla.pop(f_nueva+direccion[1])                      #------------------------------------------------------
                nueva_grilla.insert(f_nueva+direccion[1], nueva_f_vacio)    #------------------------------------------------------
                
                nueva_fila=nueva_grilla[f_nueva][:]
                nueva_fila[c_jugador]=VACIO
                nueva_fila[c_nueva+direccion[0]]=CAJA
                nueva_fila[c_nueva]=OBJETIVO_JUGADOR
                nueva_grilla.pop(f_nueva)
                nueva_grilla.insert(f_nueva, nueva_fila)
                
                return nueva_grilla
            
        if hay_objetivo(grilla, c_nueva+direccion[0], f_nueva+direccion[1]):
            if hay_objetivo(grilla, c_jugador, f_jugador):
                nueva_f_jugador=nueva_grilla[f_jugador][:]                  #------------------------------------------------------
                nueva_f_jugador[c_jugador]=OBJETIVO                         #------------------------------------------------------
                nueva_grilla.pop(f_jugador)                                 #------------------------------------------------------
                nueva_grilla.insert(f_jugador, nueva_f_jugador)             #------------------------------------------------------
                                                                            #------------------------------------------------------
                nueva_f_cajayobjetivo=nueva_grilla[f_nueva][:]              #------------------------------------------------------
                nueva_f_cajayobjetivo[c_jugador]=OBJETIVO_JUGADOR           # Esto es en caso de que se mueva direccion Norte o Sur
                nueva_grilla.pop(f_nueva)                                   # y haya que cambiar 3 filas distintas
                nueva_grilla.insert(f_nueva, nueva_f_cajayobjetivo)         #------------------------------------------------------
                                                                            #------------------------------------------------------
                nueva_f_objetivo=nueva_grilla[f_nueva+direccion[1]][:]      #------------------------------------------------------
                nueva_f_objetivo[c_jugador]=OBJETIVO_CAJA                   #------------------------------------------------------
                nueva_grilla.pop(f_nueva+direccion[1])                      #------------------------------------------------------
                nueva_grilla.insert(f_nueva+direccion[1], nueva_f_objetivo) #------------------------------------------------------
                
                nueva_fila=nueva_grilla[f_nueva][:]
                nueva_fila[c_jugador]=OBJETIVO
                nueva_fila[c_nueva+direccion[0]]=OBJETIVO_CAJA
                nueva_fila[c_nueva]=OBJETIVO_JUGADOR
                nueva_grilla.pop(f_nueva)
                nueva_grilla.insert(f_nueva, nueva_fila)
                
                return nueva_grilla
            else:
                nueva_f_jugador=nueva_grilla[f_jugador][:]                  #------------------------------------------------------
                nueva_f_jugador[c_jugador]=VACIO                            #------------------------------------------------------
                nueva_grilla.pop(f_jugador)                                 #------------------------------------------------------
                nueva_grilla.insert(f_jugador, nueva_f_jugador)             #------------------------------------------------------
                                                                            #------------------------------------------------------
                nueva_f_cajayobjetivo=nueva_grilla[f_nueva][:]              #------------------------------------------------------
                nueva_f_cajayobjetivo[c_jugador]=OBJETIVO_JUGADOR           # Esto es en caso de que se mueva direccion Norte o Sur
                nueva_grilla.pop(f_nueva)                                   # y haya que cambiar 3 filas distintas
                nueva_grilla.insert(f_nueva, nueva_f_cajayobjetivo)         #------------------------------------------------------
                                                                            #------------------------------------------------------
                nueva_f_objetivo=nueva_grilla[f_nueva+direccion[1]][:]      #------------------------------------------------------
                nueva_f_objetivo[c_jugador]=OBJETIVO_CAJA                   #------------------------------------------------------
                nueva_grilla.pop(f_nueva+direccion[1])                      #------------------------------------------------------
                nueva_grilla.insert(f_nueva+direccion[1], nueva_f_objetivo) #------------------------------------------------------
                
                nueva_fila=nueva_grilla[f_nueva][:]
                nueva_fila[c_jugador]=VACIO
                nueva_fila[c_nueva+direccion[0]]=OBJETIVO_CAJA
                nueva_fila[c_nueva]=OBJETIVO_JUGADOR
                nueva_grilla.pop(f_nueva)
                nueva_grilla.insert(f_nueva, nueva_fila)
                
                return nueva_grilla