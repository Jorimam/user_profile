from fastapi import FastAPI
import logging
from .database import engine
from .models.base import Base
from .routes.users import router as user_routes



logger = logging.getLogger(__name__)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title='User profile',

)
app.include_router(user_routes)

@app.get('/')
def home():
    return{
        "message":"Welcome to User Profile"
    }

