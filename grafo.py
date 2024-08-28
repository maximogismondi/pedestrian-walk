import random


class Grafo:
    def __init__(self, es_dirigido=False, lista_vertices=[]):
        self.es_dirigido = es_dirigido
        self.adyacencias = {}
        self.data = {}
        for v in lista_vertices:
            self.adyacencias[v] = {}
            self.data[v] = None

    def __contains__(self, v):
        return v in self.adyacencias

    def __setitem__(self, v, data):
        vecinos = self.adyacencias[v] if v in self else {}
        self.adyacencias[v] = vecinos
        self.data[v] = data

    def _validar_vertice(self, v):
        if v not in self:
            raise IndexError("Vertice " + v + " no esta en el grafo")

    def __getitem__(self, v):
        self._validar_vertice(v)
        return self.data[v]

    def arista(self, v, w, peso=1):
        self._validar_vertice(v)
        self._validar_vertice(w)
        self.adyacencias[v][w] = peso
        if not self.es_dirigido:
            self.adyacencias[w][v] = peso

    def eliminar_arista(self, v, w):
        self._validar_vertice(v)
        self._validar_vertice(w)
        del self.adyacencias[v][w]
        if not self.es_dirigido:
            del self.adyacencias[w][v]

    def hay_arista(self, v, w):
        self._validar_vertice(v)
        self._validar_vertice(w)
        return w in self.adyacencias[v]

    def peso_arista(self, v, w):
        if not self.hay_arista(v, w):
            raise ValueError("Los vertices " + v + " y " + w + " no estan unidos")
        return self.adyacencias[v][w]

    def keys(self):
        return list(self.adyacencias.keys())

    def random(self):
        return random.choice(self.keys())

    def adyacentes(self, v):
        return list(self.adyacencias[v].keys())

    def __iter__(self):
        return iter(self.adyacencias)

    def __repr__(self):
        cadena = "{\n"
        for v in self:
            cadena += "\t" + str(v) + ": ["
            adyacentes = self.adyacentes(v)
            i = 1
            for w in adyacentes:
                cadena += str(w) + ("" if i == len(adyacentes) else ", ")
                i += 1
            cadena += "]\n"
        cadena += "}"
        return cadena

    def __str__(self):
        return repr(self)

    def __len__(self):
        return len(self.adyacencias)
