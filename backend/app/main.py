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
    allow_origins=[
        "http://localhost:5173",
        "https://faraiz-app.web.app",
        "https://faraiz-app.firebaseapp.com",
        "*" # Fallback (optional, but good for testing)
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

@app.get("/")
def read_root():
    return {"status": "Fatemi Wirasat Engine is online"}
