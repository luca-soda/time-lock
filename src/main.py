from dotenv import load_dotenv
load_dotenv()

from icecream import ic
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import key_handler 

app = FastAPI()

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