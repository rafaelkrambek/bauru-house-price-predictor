import joblib
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import r2_score,mean_squared_error
import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np 
import matplotlib.pyplot as plt
import  joblib



df = pd.read_csv('imoveis_limpo.csv')




X = df[['tamanhos','quartos','banheiros','vagas','bairros_preco_medio']]
y = df['precos']


X_train,X_test , y_train , y_test = train_test_split(X,y,random_state=0, test_size=0.2)


model = GradientBoostingRegressor(random_state=0)

model.fit(X_train,y_train)


y_pred = model.predict(X_test)

r2 = r2_score(y_test,y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))


print(f'R²: {r2:.2f}')
print(f'RMSE: {rmse:.2f}')

joblib.dump(model,'previsao_casas.pkl')