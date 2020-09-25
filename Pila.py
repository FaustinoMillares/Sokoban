class _Nodo:
    def __init__(self, dato, prox=None):
        self.dato = dato
        self.prox = prox

class Pila:
    def __init__(self):
        """
        INVARIANTE: el tope siempre es un nodo, o en caso de que la pila este vacia es None
        """
        self.tope = None
    
    def apilar(self, dato):
        nuevo = _Nodo(dato, self.tope)
        self.tope = nuevo
    
    def desapilar(self):
        """
        Desapila el elemento que está en el tope de la pila
        y lo devuelve.
        Pre: la pila NO está vacía.
        Pos: el nuevo tope es el que estaba abajo del tope anterior
        """
        if self.esta_vacia():
            raise Exception("La  pila esta vacia")
        dato = self.tope.dato
        self.tope = self.tope.prox
        return dato
        
    def ver_tope(self):
        """
        Devuelve el elemento que está en el tope de la pila.
        Pre: la pila NO está vacía.
        """
        if self.esta_vacia():
            raise Exception("La  pila esta vacia")
        return self.tope.dato
        
    def esta_vacia(self):
        return self.tope is None