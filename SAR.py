import os
import pickle
import sys

class Tree(object):
	def __init__(self, name='root', archives=None, children=None):
		self.name = name
		self.archives = []
		self.children = []
		self.content_files = []
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
				pasta.archives.append(os.path.join(nomepasta,archive))
				filecontent = open(os.path.join(nomepasta,archive), 'rb')
				print (filecontent.read())
				pasta.content_files.append(filecontent.read())
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

	def extract_tree(self):
		if not os.path.isdir(self.name):
			os.mkdir(self.name)
		for filename in self.archives:
			print filename
			output_file = open(filename, 'wb')
			index = self.archives.index(filename)
			output_file.write(self.content_files[index])
			
		if self.children is not None:
			for child in self.children:
				child.extract_tree()



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
               

        for filename in filenames:
            if is_root:  # quer dizer que ta na pasta raiz
                directory.add_archive(os.path.join(dirname,filename))
                filecontent = open(os.path.join(dirname,filename), 'rb')
                directory.content_files.append(filecontent.read())
            
            else:  # senao ta em subpasta
                directory.insert_archive(dirname,filename)
           
        is_root = False
    directory.dump()
    pickle.dump(directory,output)



def list_dir(archive):  # funcao que lista os diretorios do arquivo .sar
    sar_input = open(archive, 'rb')
    tree = pickle.load(sar_input)
    tree.dump()


def extract(archive):  # funcao que extrai os arquivos do arquivo .sar
    sar_input = open(archive, 'rb')
    tree = pickle.load(sar_input)
    tree.extract_tree()



def main (argv): 
	if len(argv) < 2: 
		return 3
	elif argv[1].upper() == 'C':
		create('./'+argv[2])
	elif argv[1].upper() == 'L':
		if argv[2][-3:] == 'sar':
			list_dir(argv[2])
		else:
			return 2
	elif argv[1].upper() == 'E':
		if argv[2][-3:] == 'sar':
			extract(argv[2])
		else:
			return 2

if __name__ == '__main__':  # define a funcao main
	main(sys.argv)