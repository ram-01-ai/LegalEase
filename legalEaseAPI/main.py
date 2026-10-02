from fastapi import FastAPI
from legalEaseAPI.routes import router

app = FastAPI(title="LegalEase API")

app.include_router(router)


@app.get("/")
def home():
    return {"message": "LegalEase API is running!"}