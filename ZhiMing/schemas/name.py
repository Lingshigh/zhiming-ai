# name.py
from .agent import NameSchema
from pydantic import BaseModel, Field
from typing import Annotated, List, Literal


class NameIn (BaseModel):
    category: Annotated[Literal["婴儿", "公司", "品牌"], Field (..., description="起名类型")]
    length: Annotated[Literal["不限", "单字", "两字", "四字"], Field ("不限", description="长度要求")]

    # --- 婴儿起名专用 ---
    surname: Annotated[str | None, Field (None, description="姓氏（婴儿起名必填，公司选填）")]
    gender: Annotated[Literal["不限", "男", "女"], Field ("不限", description="性别（仅婴儿起名使用）")]


    # --- 通用限制 ---
    other: Annotated[str | None, Field ("", description="其他特殊要求")]
    exclude: Annotated[List[str], Field ([], description="排除的名字")]
    vision: Annotated[str, Field (..., description="核心愿景（如：智慧、科技、平安）")]

class NameOut(BaseModel):
    names: List[NameSchema]