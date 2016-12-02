arqbin = open('bin.exe', 'r')
arqtarget = open('copy.exe', 'w')
arqtarget.write(arqbin.read())