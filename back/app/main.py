# back/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.Api.rfp_routes import router as rfp_router
from app.Api.tech_routes import router as tech_router
from app.Api.pricing_routes import router as pricing_router


app = FastAPI(title="RFP Intelligence Engine")

# ✅ CORS (frontend access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # later restrict
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Register routes
app.include_router(rfp_router)
app.include_router(tech_router)
app.include_router(pricing_router)

@app.get("/")
def root():
    return {"message": "RFP backend is running"}
