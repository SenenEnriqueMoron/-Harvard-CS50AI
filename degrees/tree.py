class arbol():
    def __init__(self):
        self._indextree = []
        self._movietree = []
        self._startree = []
    
    @property
    def indextree(self):
        return self._indextree
    
    @indextree.setter
    def indextree(self, value):
        self._indextree.append(value)

    @property
    def movietree(self):
        return self._movietree
    
    @movietree.setter
    def movietree(self, value):
        self._movietree.append(value)

    @property
    def startree(self):
        return self._startree
    
    @startree.setter
    def startree(self, value):
        self._startree.append(value)