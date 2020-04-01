import os

class baseBacias(object):

    def __init__(self, path):

        self.bacias = os.listdir(path)
        self.path = path
    
    def Dicionario_de_bases(self):

        aux = {} # Instanciando um Dicionario

        for i in self.bacias:

            aux[i] = []

            for j in os.listdir(self.path + '/' + i):

                aux[i].append(j)
        
        return aux


class construtorDeCaminhos(object):

    def __init__(self, caminho):

        self.caminho = caminho
        self.Dicionario = baseBacias(caminho).Dicionario_de_bases() # Chamando a classe baseBacias dentro do construtor devolvendo o dicionario ja pronto!!!
    
    def construct(self):

        aux = {}

        for bacia in self.Dicionario:
        
            aux[bacia] = []
            aux[bacia] = [self.caminho + '/' +  bacia + '/' + posto for posto in self.Dicionario[bacia]]
        
        return aux
