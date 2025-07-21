from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Previsao, Base
from pydantic import BaseModel
import joblib
import numpy as np
import json
from fastapi.responses import JSONResponse

app = FastAPI()

# Criação da tabela ao rodar o servidor
Base.metadata.create_all(bind=engine)

# Carrega o modelo de Machine Learning
modelo = joblib.load("previsao_casas.pkl")

# Schema para receber os dados via API
class DadosCasa(BaseModel):
    tamanhos: int
    quartos: int
    banheiros: int
    vagas: int
    preco_medio: float

# Dependência de banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint GET para ler um JSON auxiliar
@app.get("/precos")
async def ler_json():
    with open("bairros_preco_medio.json", encoding='utf-8') as f:
        dados = json.load(f)
    return JSONResponse(content=dados)

# Endpoint POST para prever preço e salvar no banco
@app.post("/prever_preco")
async def prever(dados: DadosCasa, db: Session = Depends(get_db)):
    entrada = np.array([[dados.tamanhos, dados.quartos, dados.banheiros, dados.vagas, dados.preco_medio]])
    preco_previsto = float(modelo.predict(entrada)[0])  # Conversão garantida

    registro = Previsao(
        tamanhos=dados.tamanhos,
        quartos=dados.quartos,
        banheiros=dados.banheiros,
        vagas=dados.vagas,
        preco_medio=dados.preco_medio,
        preco_previsto=preco_previsto
    )

    try:
        db.add(registro)
        db.commit()
        db.refresh(registro)
        return {
            "preco_previsto": round(preco_previsto, 2),
            "id_registro": registro.id
        }
    except Exception as e:
        db.rollback()
        return {"erro": str(e)}