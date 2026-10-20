from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db


router = APIRouter(prefix="/clientes", tags=["clientes"])


