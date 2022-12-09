from fastapi import FastAPI
from database.connection import engine
import uvicorn
from models import user
from routes.user import user_router
from routes.olahraga import olahraga_router
from routes.rating import rating_router

app = FastAPI()
app.debug  = True

user.Base.metadata.create_all(engine)

app.include_router(user_router, prefix="/users")
app.include_router(olahraga_router, prefix="/olahraga")
app.include_router(rating_router, prefix="/rating")

@app.get('/')
def index():
    return {"Pesan" : "Selamat Datang!"}

if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)