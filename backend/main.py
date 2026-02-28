from fastapi import FastAPI
from routes.auth import router as auth_router
from models import user  # this ensures table creation

app = FastAPI()

app.include_router(auth_router)

@app.get("/")
def home():
    return {"message": "AI Interview Coach Backend Running 🚀"}