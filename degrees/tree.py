class ColaClass():
    def __init__(self):        
        self.movietree = []
        self.startree = []
        self.coleccion = {}
    
    def add_startree(self,value):
        self.startree.append(value)
    def del_startree(self,value):
        if value in self.startree:
            self.startree.remove(value)
    def get_startree(self):
        return self.startree
    
    def add_movietree(self,value):
        self.movietree.append(value)
    
    def del_movietree(self,value):
        if value in self.movietree:
            self.movietree.remove(value)
    
    def get_movietree(self):
        return self.movietree
    def add_colection(self, star, largo):
        self.coleccion.update({star:largo})
    
    def del_colection(self, star):
        if star in self.coleccion:
            del self.coleccion[star]
    
    def update_coleccion(self,start):
        if self.coleccion[start] > 1:
            self.coleccion[start] = self.coleccion[start] -1
        self.del_colection(self, start)
        
class NodesClass:
    def __init__(self):
        self.__Ptree = {}  

    def get_nodo(self)->dict:
        return self.__Ptree
    
    def add_node(self, pelicula:int, start:int):
        self.__Ptree.update({ pelicula : start})
    
    def del_node(self, pelicula:int):
        if pelicula in self.__Ptree:
            del self.__Ptree[pelicula]