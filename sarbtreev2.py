import os
import pickle

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
                print ('\npai: '+self.name)
                child.dump()

    def insert_archive(self, nomepasta, archive):
        here = False
        for pasta in self.children:
            if nomepasta == pasta.name:
                pasta.archives.append(archive)
                here = True
                break
        if here:
            return True
        else:
            for pasta in self.children:
                found = pasta.insert_archive(nomepasta, archive)
                if found:
                    break
            return True

    def insert_directory(self, father, child):
        here = False
        for pasta in self.children:
            if father == pasta.name:
                aux = Tree(os.path.join(father, child))
                pasta.children.append(aux)
                here = True
                break
        if here:
            return True
        else:
            for pasta in self.children:
                found = pasta.insert_directory(father, child)
                if found:
                    break
            return True




def create(path):  # funcao que cria o arquivo .sar
    output = open(path+'.sar', 'wb')
    directory = Tree(path)
    is_root = True
    # dirname: pasta atual, dirnames: subpastas, filenames: nomes de arquivo
    for dirname, dirnames, filenames in os.walk(path, topdown=True):
        if '.git' in dirnames:
            # isso aqui eh soh pra ele nao entrar na pasta .git e imprimir um monte de coisa chata
            dirnames.remove('.git')
        
        for subdirname in dirnames:
            if is_root:
                subdir = Tree(os.path.join(dirname, subdirname))
                directory.add_child(subdir)
            else:
                directory.insert_directory(dirname, subdirname)
                # cont = 0
                # index = 0
                # here = False
                # for pasta in directory.children:  # navego por todos os filhos
                #     if dirname != pasta.name:  # se nao for o que eu to procurando, continuo procurando
                #         cont += 1
                #     else:
                #         here = True
                #         index = cont  # se for, guardo o indice
                # if not here:
                #     for pasta in directory.children:
                #         for subpasta in pasta.children:
                #
                # directory.children[index].add_child(subdir)  # insiro no indice certo

            # print("subdirname "+ subdirname)

        for filename in filenames:
            if is_root:  # quer dizer que ta na pasta raiz
                directory.add_archive(filename)
            
            else:  # senao ta em subpasta
                directory.insert_archive(dirname,filename)
            #     cont = 0
            #     index = 0
            #     for pasta in directory.children:  # navego por todos os filhos
            #         if dirname != pasta.name:  # se nao for o que eu to procurando, continuo procurando
            #             cont += 1
            #         else:
            #             index = cont  # se for, guardo o indice
            #     directory.children[index].add_archive(filename)  # insiro no indice certo
            # # print("filename "+ filename)
            # # directory[dirname].append(filename)
        is_root = False
    directory.dump()
    pickle.dump(directory,output)



def list_dir(archive):  # funcao que lista os diretorios do arquivo .sar
    dir_input = open(archive, 'rb')
    tree = pickle.load(dir_input)
    tree.dump()


def extract(archive):  # funcao que extrai os arquivos do arquivo .sar
    pass


if __name__ == '__main__':  # define a funcao main
    create('.')
    list_dir('..sar')
