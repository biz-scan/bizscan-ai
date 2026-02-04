from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# from app.core.database import get_db
from app.schemas.catchphrase_schema import CatchphraseResponse
from app.schemas.common_schema import CommonResponse
from app.services.catchphrase_service import generate_catchphrase

router = APIRouter(
    prefix="/api/analysis",
    tags=["Catchphrase"],
)

# @router.get("/stores/{store_id}/catchphrase")
# async def get_store_catchphrase(
#     store_id: int,
#     db: Session = Depends(get_db),
# ):
#     catchphrase = generate_catchphrase(db, store_id)

#     return CommonResponse(
#         result=CatchphraseResponse(catchphrase=catchphrase)
#     )
