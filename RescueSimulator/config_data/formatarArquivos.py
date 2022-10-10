import os

arq = open(os.path.join("config_data","inAmbiente.txt"),"r")
configDict = {} 
ambienteDict = {}
notRead = ['Base','Parede','Vitimas']
for line in arq:
    values = line.rstrip('\n').split(" ")
    if values[0] not in notRead:
        configDict[values[0]] = values[1]
    else:
        ambienteDict[values[0]] = ' '.join(values[1:])
arq.close()

arq = open(os.path.join("config_data","inSinaisVitais.txt"),"r")
sinaisDict = []
for line in arq:
    values = line.rstrip('\n').split(",")
    values = [str(float(value)/100) for value in values]
    sinaisDict.append(' '.join(values[1:])) 
arq.close()

arquivo = open(os.path.join("config_data", "config.txt"), "w")
strSave = ''
strSave += 'maxLin=' + configDict['YMax'] + '\n'
strSave += 'maxCol=' + configDict['XMax'] + '\n'
strSave += 'Tl=' + configDict['Te'] + '\n'
strSave += 'Ts=' + configDict['Ts'] + '\n'
arquivo.writelines(strSave)
arquivo.close()

arquivo = open(os.path.join("config_data", "ambiente.txt"), "w")
strSave = ''
linhaErrada = ambienteDict['Base'].split(' ')
linhaCorrigida = ''
for posicao in linhaErrada:
    x,y=posicao.split(',')
    linhaCorrigida += str(y)+','+ str(x) + ' ' 
    pass
linhaCorrigida = linhaCorrigida[0:-1]
strSave += 'Agente ' + linhaCorrigida + '\n'

linhaErrada = ambienteDict['Parede'].split(' ')
linhaCorrigida = ''
for posicao in linhaErrada:
    x,y=posicao.split(',')
    linhaCorrigida += str(y)+','+ str(x) + ' ' 
    pass
linhaCorrigida = linhaCorrigida[0:-1]

strSave += 'Parede ' + linhaCorrigida + '\n'

linhaErrada = ambienteDict['Vitimas'].split(' ')
linhaCorrigida = ''
for posicao in linhaErrada:
    x,y=posicao.split(',')
    linhaCorrigida += str(y)+','+ str(x) + ' ' 
    pass
linhaCorrigida = linhaCorrigida[0:-1]

strSave += 'Vitima ' + linhaCorrigida+ '\n'
arquivo.writelines(strSave)
arquivo.close()

arquivo = open(os.path.join("config_data", "sinaisvitais.txt"), "w")
strSave = ''
for sinal in sinaisDict:
    arquivo.write(sinal + '\n')
arquivo.close()
