from pydantic import BaseModel, Field
from typing import Annotated, List, Literal

class NameSchema(BaseModel):
    name: Annotated[str, Field(..., description="建议的名字")]
    style: Annotated[Literal["中式典雅", "西式博雅", "跨文化融合"], Field(..., description="名字风格")]
    reference: Annotated[str, Field(..., description="具体出处（如《诗经·周南》或希腊神话）")]
    moral: Annotated[str, Field(..., description="深度寓意解读")]

class NameResultSchema(BaseModel):
    # 这样可以确保模型输出的结果包含多个风格的名字
    names: List[NameSchema]