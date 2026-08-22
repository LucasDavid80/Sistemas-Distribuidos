from fastapi import FastAPI

app = fastAPI()

@app.get("/")
def home():
    return {"message": "Olá, Sistemas Distribuídos!"}