import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlmodel import SQLModel

# from app.dependencies.db_client import build_engine
# from app.dependencies.session_manager import session_manager
from app.api.v1 import document_ingestion


STATIC_ASSETS_PATH = os.path.join(os.path.dirname(__file__), "static")

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Initializing resources (Connecting to DB, loading ML models...)")
    # db_engine = build_engine()
    # app.state.db_engine = db_engine
    # session_manager.initialize_engine(db_engine)

    # if os.environ.get("ENV", 'dev') == "dev":
    #     async with db_engine.begin() as conn:
    #         await conn.run_sync(SQLModel.metadata.create_all)
    
    yield
    
    print("🛑 Cleaning up resources (Closing DB pools, flushing logs...)")
    if hasattr(app.state, "db_engine"):
        await app.state.db_engine.dispose()

app = FastAPI(title="bisnes demo", version="0.0.0", lifespan=lifespan)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(document_ingestion.router, prefix="/v1")

@app.get("/health")
def health():
    return {"status": "ok"}

if os.path.exists(STATIC_ASSETS_PATH):
    # 1. Mount index assets like assets/index-DI783.js or favicon images
    app.mount("/assets", StaticFiles(directory=os.path.join(STATIC_ASSETS_PATH, "assets")), name="assets")

    # 2. Catch-all fallback route to serve the SPA (Single Page Application)
    # This allows users to hit any URL path and lets React Router take over client routing.
    @app.get("/{catchall:path}")
    async def serve_react_app(catchall: str):
        # If an incoming request hits here and starts with v1/ or health,
        # it means it didn't match any valid router endpoint above.
        # Throw a proper 404 JSON error instead of crashing with None or returning index.html.
        if catchall.startswith("v1") or catchall == "health" or catchall.startswith("assets"):
            raise HTTPException(status_code=404, detail="API route endpoint not found.")

        # Serve static root files (favicon, manifest, etc.) directly
        static_file = os.path.join(STATIC_ASSETS_PATH, catchall)
        if os.path.isfile(static_file):
            return FileResponse(static_file)

        index_file = os.path.join(STATIC_ASSETS_PATH, "index.html")
        if os.path.exists(index_file):
            return FileResponse(index_file)
            
        return {"error": "Frontend build files missing from static directory."}
