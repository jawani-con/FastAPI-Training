from fastapi import FastAPI
from fitness.database import Base, engine
from fitness.routers import fitness
from fitness.auth.oauth2 import get_current_user  # Make sure you're importing it from the correct path
from fitness.auth.oauth2 import router as auth_router  # If the router is defined

app = FastAPI()

Base.metadata.create_all(bind=engine)

# Include routes
app.include_router(fitness.router, prefix="/api", tags=["Fitness"])
app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])