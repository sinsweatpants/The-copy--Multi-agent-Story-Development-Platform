from fastapi import FastAPI

app = FastAPI(title="Jules Narrative Development Platform")


@app.get("/")
def read_root():
    return {"message": "Welcome to the Jules Narrative Development Platform API"}