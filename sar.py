import os

def create (directory):
    dir = open(directory+'.sar', 'w')

    directory = {}
    for dirname, dirnames, filenames in os.walk('.', topdown = True):
        found = False
        #print ("mais externo "+ dirname)
        for s in directory:
            print ("s atual: "+s + " dirname atual: " + dirname)
            if (s == dirname):
                pass
                #print (s)
        directory[dirname] = []
        for subdirname in dirnames:
            directory[dirname].append(subdirname)
            #print("subdirname "+ subdirname)

        for filename in filenames:
            #print("filename "+ filename)
            directory[dirname].append(filename)
    #print (directory)


if __name__ == '__main__':
    create('abc')
