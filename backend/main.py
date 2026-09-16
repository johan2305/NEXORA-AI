import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.ai.router import router as ai_router
from backend.analytics.router import router as analytics_router
from backend.audit.router import router as audit_router
from backend.auth.router import router as auth_router
from backend.automations.router import router as automations_router
from backend.customers.router import router as customers_router
from backend.notifications.router import redis_listener
from backend.notifications.router import router as notifications_router
from backend.projects.router import router as projects_router
from backend.tasks.router import router as tasks_router

app = FastAPI(title="NEXORA AI", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://nexora-ai-bay-five.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(customers_router)
app.include_router(projects_router)
app.include_router(tasks_router)
app.include_router(ai_router)
app.include_router(automations_router)
app.include_router(notifications_router)
app.include_router(analytics_router)
app.include_router(audit_router)


@app.on_event("startup")
async def startup_event():
    app.state.notification_task = asyncio.create_task(redis_listener())


@app.get("/health")
def health_check():
    return {"status": "ok"}