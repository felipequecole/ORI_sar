arqbin = open('bin.exe', 'rb')
arqtarget = open('copy.exe', 'wb')
arqtarget.write(arqbin.read())
