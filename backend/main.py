from fastapi import FastAPI, HTTPException

app = FastAPI()

# Banco de dados falso
produtos_db = {
    1: {"nome": "Teclado", "preco": 150.0},
    2: {"nome": "Mouse", "preco": 80.0},
    3: {"nome": "Monitor", "preco": 1200.0}
}

@app.get("/")
def home():
    return {"message": "Olá, Sistemas Distribuídos!"}

@app.get("/lucas")
def hello_lucas():
    return {"message": "Olá, Lucas!"}

@app.get("/produtos/{produto_id}")
def buscar_produto(produto_id: int):
    if produto_id < 0:
        raise HTTPException(status_code=400, detail="ID do produto não pode ser negativo")
    
    if produto_id not in produtos_db:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
        
    return produtos_db[produto_id]
