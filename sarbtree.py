import os


class Tree(object):
    def __init__(self, name='root', archives=None, children=None):
        self.name = name
        self.archives = []
        self.children = []
        if archives is not None: 
            for archive in archives:
                self.archives.append(archive)
        if children is not None:
            for child in children:
                self.add_child(child)
    def __repr__(self):
        return self.name
    def add_child(self, node):
        assert isinstance(node, Tree)
        self.children.append(node)
    def add_archive(self, archive):
        self.archives.append(archive)
    def dump(self):
        print self.name
        print self.archives
        if self.children is not None: 
            for child in self.children: 
                child.dump()

def create (path): #funcao que cria o arquivo .sar
    dir = open(path+'.sar', 'w')

    directory = Tree(path)
    isRoot = True
    for dirname, dirnames, filenames in os.walk('.', topdown = True): # dirname: pasta atual, dirnames: subpastas, filenames: nomes de arquivo
        if '.git' in dirnames:
            # isso aqui eh soh pra ele nao entrar na pasta .git e imprimir um monte de coisa chata
            dirnames.remove('.git')
        for subdirname in dirnames:
            subdir = Tree(subdirname)
            directory.add_child(subdir)
            #print("subdirname "+ subdirname)

        for filename in filenames:
            if isRoot: #quer dizer que ta na pasta raiz
                directory.add_archive(filename)
            
            else: #senao ta em subpasta
                cont = 0 
                index = 0
                for pasta in directory.children: #navego por todos os filhos
                    if (dirname != pasta.name): #se nao for o que eu to procurando, continuo procurando
                        cont = cont + 1
                    else:
                        index = cont # se for, guardo o indice
                directory.children[index].add_archive(filename) #insiro no indice certo
            #print("filename "+ filename)
            #directory[dirname].append(filename)
        isRoot = False      
    directory.dump()

def list (archive): #funcao que lista os diretorios do arquivo .sar
	pass

def extract (archive): #funcao que extrai os arquivos do arquivo .sar
	pass


if __name__ == '__main__': #define a funcao main
    create('abc')
