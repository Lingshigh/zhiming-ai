from fastapi import APIRouter,Depends
from ZhiMing.schemas.name import NameIn,NameOut
from ZhiMing.core.agent import generate_name
from ZhiMing.core.auth import AuthHandler


auth_handler = AuthHandler()

router = APIRouter(prefix="/name")

@router.post("/")
async def take_names(
        data:NameIn,
        user_id:int=Depends(auth_handler.auth_access_dependency)):
    name_result = await generate_name(data)
    return NameOut(names=name_result.names)

