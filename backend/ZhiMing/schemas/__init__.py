from pydantic import BaseModel,Field
from typing import Annotated,Literal


#用于视图函数
class ResponseOut(BaseModel):
    result:Annotated[Literal["success","failure"],Field("success",description="操作成功！")]