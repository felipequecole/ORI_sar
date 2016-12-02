import os

def create (directory): #funcao que cria o arquivo .sar
    dir = open(directory+'.sar', 'w')

    directory = {}
    for dirname, dirnames, filenames in os.walk('.', topdown = True): # dirname: pasta atual, dirnames: subpastas, filenames: nomes de arquivo
        found = False
        #print ("mais externo "+ dirname)
        for s in directory:
            print ("s atual: "+s + " dirname atual: " + dirname)
        directory[dirname] = []
        for subdirname in dirnames:
            directory[dirname].append(subdirname)
            #print("subdirname "+ subdirname)

        for filename in filenames:
            #print("filename "+ filename)
            directory[dirname].append(filename)

        if '.git' in dirnames:
        	# isso aqui eh soh pra ele nao entrar na pasta .git e imprimir um monte de coisa chata
        	dirnames.remove('.git')
    print (directory)

def list (archive): #funcao que lista os diretorios do arquivo .sar
	pass

def extract (archive): #funcao que extrai os arquivos do arquivo .sar
	pass


if __name__ == '__main__': #define a funcao main
    create('abc')
