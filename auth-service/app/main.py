from fastapi import FastAPI
from app.api.routes import router
from app.db.database import Base, engine

app = FastAPI(title="Enterprise Auth Service")

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

app.include_router(router)