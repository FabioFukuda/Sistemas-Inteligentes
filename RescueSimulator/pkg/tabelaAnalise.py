import pandas as pd

tabela = pd.DataFrame(columns=[['eval','num_vitimas','num_vizinhos','num_trocas','tempo']])
tabela.to_csv('analise.csv',sep = ';',index=False)