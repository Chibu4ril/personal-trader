from fastapi import FastAPI

app = FastAPI()  # The app instance

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
