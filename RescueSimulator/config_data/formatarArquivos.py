import os

arq = open(os.path.join("config_data","inAmbiente.txt"),"r")
configDict = {} 
ambienteDict = {}
notRead = ['Base','Paredes','Vitimas']
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
    values = line.rstrip('\n').split(" ")
    sinaisDict.append(' '.join(values[1:])) 
arq.close()

arquivo = open(os.path.join("config_data", "config.txt"), "w")
strSave = ''
strSave += 'maxLin=' + configDict['Ymax'] + '\n'
strSave += 'maxCol=' + configDict['Xmax'] + '\n'
strSave += 'maxCol=' + configDict['Xmax'] + '\n'
strSave += 'Tl=' + configDict['Te'] + '\n'
strSave += 'Ts=' + configDict['Ts'] + '\n'
arquivo.writelines(strSave)
arquivo.close()

arquivo = open(os.path.join("config_data", "ambiente.txt"), "w")
strSave = ''
strSave += 'Agente ' + ambienteDict['Base'] + '\n'
strSave += 'Parede ' + ambienteDict['Paredes'] + '\n'
strSave += 'Vitima ' + ambienteDict['Vitimas'] + '\n'
arquivo.writelines(strSave)
arquivo.close()

arquivo = open(os.path.join("config_data", "sinaisvitais.txt"), "w")
strSave = ''
for sinal in sinaisDict:
    arquivo.write(sinal + '\n')
arquivo.close()
