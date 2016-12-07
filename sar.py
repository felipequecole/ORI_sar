import os
import sys


class Tree(object):
	def __init__(self, name='root', archives=None, children=None):
		self.name = name 						# nome da pasta 
		self.archives = []						# lista de nomes de arquivo
		self.children = []						# lista de subpastas
		self.content_files = []					# lista com conteudo dos arquivos
		if archives is not None: 
			for archive in archives:
				self.archives.append(archive)
		if children is not None:
			for child in children:
				self.add_child(child)


	def add_child(self, node):
		if isinstance(node, Tree):
			self.children.append(node)
			return True
		else:
			return False


	def add_archive(self, archive):	
		self.archives.append(archive)


	def insert_archive(self, nomepasta, archive):	# funcao para inserir um arquivo na hierarquia
		here = False
		for pasta in self.children:			# procura em todos os filhos
			if nomepasta == pasta.name:
				pasta.archives.append(os.path.join(nomepasta,archive))	# se for um lugar certo, insere o arquivo
				filecontent = open(os.path.join(nomepasta,archive), 'rb')
				pasta.content_files.append(filecontent.read())
				here = True
				break
		if here:
			return True
		else:
			for pasta in self.children:
				found = pasta.insert_archive(nomepasta, archive)	# se nao, chama recursivamente a funcao para todas as subpastas
				if found:
					break
			return True


	def insert_directory(self, father, child):		# funcao para inserir subpasta na hierarquia
		here = False
		for pasta in self.children:			# procura em todos os filhos (subpastas)
			if father == pasta.name:		# se for o lugar certo, insere a subpasta
				aux = Tree(os.path.join(father, child))
				pasta.children.append(aux)
				here = True
				break
		if here:
			return True
		else:				
			for pasta in self.children:
				found = pasta.insert_directory(father, child)	# se nao, chamo recursivamente para cada filho(subpasta) dos filhos
				if found:
					break
			return True

	
	def save_to_file(self, output_file):
		output_file.write('{')					# simbolo que marca inicio de pasta
		output_file.write(self.name.encode('utf8', 'ignore'))
		output_file.write('$')					# simbolo que marca fim de nome de pasta
		if len(self.archives) > 0: 
			for file in self.archives:
				output_file.write('#')			# simbolo que marca inicio de arquivo
				output_file.write(file.encode('utf8', 'ignore'))
				current_index = self.archives.index(file)
				output_file.write('|')			# simbolo que marca inicio do offset
				output_file.write(str(len(str(self.content_files[current_index]))))
				output_file.write('*')			# simbolo que marca inicio dos dados do arquivo
				output_file.write(self.content_files[current_index])
		if self.children is not None:
			for child in self.children:
				child.save_to_file(output_file)		# chama recursivamente a funcao para cada subpasta
		
				
		output_file.write('}')	#fecha pasta 		
		





def create(path):  # funcao que cria o arquivo .sar
    output = open(path+'.sar', 'wb')
    directory = Tree(path)
    is_root = True
    # dirname: pasta atual, dirnames: subpastas, filenames: nomes de arquivo
    for dirname, dirnames, filenames in os.walk(unicode(path), topdown=True):
                
        for subdirname in dirnames:
            if is_root:		#se ta na pasta raiz, cria primeiro filho
                subdir = Tree(os.path.join(dirname, subdirname))
                directory.add_child(subdir)
            else:		#ou chama funcao para inserir no filho correto
                directory.insert_directory(dirname, subdirname)
               
        for filename in filenames:
            if is_root:  # se ta na pasta raiz, cria primeiro node
                directory.add_archive(os.path.join(dirname,filename))
                filecontent = open(os.path.join(dirname,filename), 'rb')
                directory.content_files.append(filecontent.read())
                filecontent.close()
            
            else:  # ou chama funcao para inserir no filho correto
                directory.insert_archive(dirname,filename)
           
        is_root = False
    directory.save_to_file(output)
    print ("Created "+path+'.sar')
    return 0



def list_dir(archive):  # funcao que lista os diretorios do arquivo .sar
	print ('Listando diretorio salvo em: '+archive)
	sar_input = open(archive, 'rb')
	file_sar = sar_input.read()
	current_offset = 0
	begin = 0
	end = 0
	j_begin = 0
	j_end = 0
	flag = False
	tab_counter = 0
	while current_offset < len(file_sar):
		if file_sar[current_offset] == '{':					# inicio de pasta
			begin = current_offset

		elif (file_sar[current_offset]== '$'):				# fim do do nome da pasta
			end = current_offset
			dir_name = file_sar[begin+1:end].split('\\')
			print ('\n'+('\t'*tab_counter)+'+ '+dir_name[-1].decode('utf8', 'ignore'))					# imprime nome da pasta
			tab_counter += 1

		elif (file_sar[current_offset] == '#'):				# inicio do arquivo
			begin = current_offset

		elif (file_sar[current_offset] == '|'):				# inicio do offset do arquivo
			end = current_offset
			file_name = file_sar[begin+1:end].split('\\')
			print (('\t'*tab_counter)+'- '+file_name[-1].decode('utf8', 'ignore'))	# imprime nome do arquivo
			j_begin = current_offset

		elif (file_sar[current_offset] == '*'):				# inicio dos dados do arquivo
			j_end = current_offset
			jump = int(file_sar[j_begin+1:j_end])
			current_offset += jump

		elif (file_sar[current_offset] == '}'):
			tab_counter -= 1

		current_offset += 1 # aponto para a proxima posicao

	
	sar_input.close()
	return 0


def extract(archive):  # funcao que extrai os arquivos do arquivo .sar
    sar_input = open(archive, 'rb')
    print ('Extraindo diretorio salvo em: '+archive)
    file_sar = sar_input.read()
    current_offset = 0
    begin = 0
    end = 0
    j_begin = 0
    j_end = 0
    open_dir = False
    while current_offset < len(file_sar):
    	if file_sar[current_offset] == '{':					# inicio de pasta
    		begin = current_offset

    	elif (file_sar[current_offset]== '$'):				# fim do do nome da pasta
    		end = current_offset
    		if not os.path.isdir(file_sar[begin+1:end].decode('utf8','ignore')):
    			os.mkdir(file_sar[begin+1:end].decode('utf8', 'ignore'))		# cria a pasta, se ela nao existir
    	

    	elif (file_sar[current_offset] == '#'):				# inicio do arquivo
    		begin = current_offset

    	elif (file_sar[current_offset] == '|'):				# inicio do offset do arquivo
    		end = current_offset
    		arq_dest = open(file_sar[begin+1:end].decode('utf8','ignore'), 'wb')	# abro o arquivo em modo de escrita
    		j_begin = current_offset

    	elif (file_sar[current_offset] == '*'):				# inicio dos dados do arquivo
    		j_end = current_offset
    		jump = int(file_sar[j_begin+1:j_end])			# leio e calculo o offset
    		arq_dest.write(file_sar[current_offset+1:current_offset+jump])	# coloco o conteudo no arquivo
    		arq_dest.close()
    		current_offset += jump		# pulo para a proxima posicao valida

    	current_offset += 1 	# aponta para proxima posicao

    print ('Extracao completa.')
    sar_input.close()
    return 0

def sar_help():		#imprime instrucoes para usuario
	print("\t\t\t\t\tComandos: ")
	print("\t -c caminho_diretorio : cria um arquivo .sar contendo toda a hierarquia e arquivos do diretorio passado")
	print("\t -l nome_arquivo.sar : exibe hierarquia de pastas e arquivos salva no arquivo.sar")
	print("\t -e nome_arquivo.sar : extrai o conteudo do arquivo.sar")


def main (argv):
	if len(argv) <= 2: 
		if len(argv) == 2 and argv[1].upper() == '-H':
			sar_help()
			return 3
		print("Entrada invalida \nDigite -h para ajuda")
		return 3

	elif argv[1].upper() == '-C':
		if os.path.isdir(argv[2]):
			return create(argv[2])
		else:
			print('Caminho invalido.\nUse -h para ajuda')
			return 1
	elif argv[1].upper() == '-L':
		if argv[2][-3:] == 'sar':
			return list_dir(argv[2])
		else:
			print('Arquivo invalido.\nUse -h para ajuda')
			return 2
	elif argv[1].upper() == '-E':
		if argv[2][-3:] == 'sar':
			return extract(argv[2])
		else:
			print('Arquivo invalido.\nUse -h para ajuda')
			return 2
	else: 
		print('Entrada invalida.\nUse -h para ajuda')


if __name__ == '__main__':  # define a funcao main
	main(sys.argv)
