from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)

@router.get("")
def health_check():
    return "Hello, World!"