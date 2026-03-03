from fastapi import FastAPI
from .api.routes import router
from .database.session import engine, Base
from .database.schema import CaseRecord, ResultRecord # ensure models are loaded
from fastapi.middleware.cors import CORSMiddleware

# Create database tables (simple approach for prototype)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Fatemi Wirasat Engine")

# Configure CORS for Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

@app.get("/")
def read_root():
    return {"status": "Fatemi Wirasat Engine is online"}
