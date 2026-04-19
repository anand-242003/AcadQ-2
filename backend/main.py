from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):

    from services import ml_service, rag_service
    print("[Startup] Loading ML models...")
    ml_service.load_models()
    print("[Startup] Initializing RAG vector store...")
    rag_service.initialize_vector_store()
    print("[Startup] Ready.")
    yield



app = FastAPI(
    title="AcadIQ API",
    version="2.0.0",
    description="AcadIQ Milestone 2 — ML Predictions + AI Study Coach",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from routes import auth, predict, coach, quiz, resources

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(predict.router, prefix="/predict", tags=["Predict"])
app.include_router(coach.router, prefix="/coach", tags=["Coach"])
app.include_router(quiz.router, prefix="/quiz", tags=["Quiz"])
app.include_router(resources.router, prefix="/resources", tags=["Resources"])


@app.get("/", tags=["Health"])
async def root():
    return {"status": "ok", "message": "AcadIQ API v2.0.0"}


@app.get("/health", tags=["Health"])
async def health():
    from services.ml_service import get_models
    models = get_models()
    return {
        "status": "ok",
        "models_loaded": models.get("loaded", False),
    }
