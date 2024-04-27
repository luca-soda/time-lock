from dotenv import load_dotenv
load_dotenv()

import cryptography
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from icecream import ic
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from sslib import shamir
from os import getenv
from typing import TypeVar
from uuid import uuid4
from time import time
from db import init_db, add_key_entry, find_key_entry

T = TypeVar('T')
def not_none(value: T | None) -> T:
    if value is None:
        raise Exception('Value is None')
    return value

KEY_SIZE = int(not_none(getenv('KEY_SIZE'))) if getenv('KEY_SIZE') is not None else None
if (KEY_SIZE is None):
    raise Exception('KEY_SIZE is not defined in .env file')

app = FastAPI()
init_db()

class CreateKeyDTO(BaseModel):
    release_date: int

class GetKeyDTO(BaseModel):
    secret: str
@app.post('/key')
def create_key(dto: CreateKeyDTO):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=KEY_SIZE,
        backend=default_backend()
    )
    uuid = uuid4().__str__()
    while (find_key_entry(uuid) is not None):
        uuid = uuid4().__str__()
    bytes_private_key = private_key.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.PKCS8, encryption_algorithm=serialization.NoEncryption())
    secrets = shamir.to_hex(shamir.split_secret(bytes_private_key, 2, 2))
    hex_public_key = private_key.public_key().public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.PKCS1).hex()
    add_key_entry(dto.release_date, uuid, secrets['shares'][1], secrets['prime_mod'])
    return {'public_key': hex_public_key, 
            'secret': secrets['shares'][0],
            'uuid':  uuid}

@app.post('/key/{uuid}')
def get_key(uuid: str, secret: GetKeyDTO):
    key_entry = find_key_entry(uuid)
    if key_entry is None:
        raise HTTPException(status_code=404, detail='Key not found')
    if time() < key_entry['release_date']:
        raise HTTPException(status_code=400, detail='Too soon to release key')
    data = {'required_shares': 2, 'prime_mod': key_entry['prime'], 'shares': [key_entry['secret'], secret.secret]}
    return {'private_key': shamir.recover_secret(shamir.from_hex(data)).decode('utf-8')}