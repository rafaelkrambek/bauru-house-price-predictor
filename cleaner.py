from numpy import dtype, mean
import pandas as pd
import json

df = pd.read_csv('Imoves.csv')

df['precos'] = df['precos'].str.replace('R$','').str.replace('.','').str.strip().astype(float)
df['tamanhos'] = df['tamanhos'].str.replace('m²','').str.replace('tot.','').str.strip().astype(float)
df['quartos']=df['quartos'].str.replace(r'quartos?','',regex= True).str.strip().astype(float)
df['banheiros'] = df['banheiros'].str.replace('ban.','').str.replace(r'banheiros?','',regex=True).str.strip().astype(float)
df['vagas']=df['vagas'].str.replace(r'vagas?','',regex=True).str.strip().astype(float)




df['tamanhos'] = df.groupby('bairros')['tamanhos'].transform(lambda x: x.fillna(x.mean()))
df['quartos'] = df.groupby('bairros')['quartos'].transform(lambda x:x.fillna(x.mean()))
df['banheiros'] = df.groupby('bairros')['banheiros'].transform(lambda x:x.fillna(x.mean()))
df['vagas'] = df.groupby('bairros')['vagas'].transform(lambda x:x.fillna(x.mean()))



df = df.dropna()


print(df.info())


preco_medio_bairro = df.groupby('bairros')['precos'].mean()
bairro_preco_medio = df.groupby('bairros')['precos'].mean().to_dict()


df['bairros_preco_medio'] = df['bairros'].map(preco_medio_bairro)


df = df[df['precos']<3000000]

with open('bairros_preco_medio.json', 'w', encoding='utf-8') as f:
    json.dump(bairro_preco_medio, f, ensure_ascii=False, indent=4)


clean_df = df.drop(columns = ['bairros']).to_csv('imoveis_limpo.csv')