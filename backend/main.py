from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Olá, Sistemas Distribuídos!"}


@app.get("/lucas")
def hello_lucas():
    return {"message": "Olá, Lucas!"}
