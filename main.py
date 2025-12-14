from fastapi import FastAPI
import logging


logger = logging.getLogger(__name__)

app = FastAPI(
    title='User profile',

)

@app.get('/home')
def home():
    return{
        "message":"Welcome to User Profile"
    }

