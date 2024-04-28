from dotenv import load_dotenv
load_dotenv()

from icecream import ic
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import key_handler 

app = FastAPI(title="Time Lock", version="0.0.1", description="A time lock service that allows you to create a key that can only be retrieved after a certain date.")

class CreateKeyDTO(BaseModel):
    release_date: int

class GetKeyDTO(BaseModel):
    secret: str

@app.post('/key')
def create_key(dto: CreateKeyDTO):
    return key_handler.create_key(dto.release_date)

@app.post('/key/{uuid}')
def get_key(uuid: str, dto: GetKeyDTO):
    try:
        return key_handler.get_key(uuid, dto.secret)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))