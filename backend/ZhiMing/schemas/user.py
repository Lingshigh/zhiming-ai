from pydantic import BaseModel, Field, EmailStr, model_validator, ConfigDict
from typing import Annotated

# ❌ 删除这行，不要在 Schema 中引入数据库模型，会导致循环引用和序列化错误
# from ZhiMing.models.user import User

# --- 类型别名定义 ---
UsernameStr = Annotated[str, Field (..., min_length=4, max_length=20, description="用户名")]
RawPasswordStr = Annotated[str, Field (min_length=6, max_length=20, description="密码")]


# --- 注册输入 ---
class RegisterIn (BaseModel):
    email: EmailStr
    username: UsernameStr
    password: RawPasswordStr
    confirm_password: RawPasswordStr
    code: Annotated[str, Field (..., min_length=4, max_length=4)]

    @model_validator (mode="after")
    def password_is_match(self) -> "RegisterIn":
        if self.password != self.confirm_password:
            raise ValueError ("密码不一致！")
        return self


# --- 创建用户（Service层可能用到） ---
class UserCreateSchema (BaseModel):
    email: EmailStr
    username: UsernameStr
    password: str


# --- 登录输入 ---
class LoginIn (BaseModel):
    email: EmailStr
    password: RawPasswordStr


# --- 用户信息输出 (修正点 1) ---
class UserSchema (BaseModel):
    id: int
    email: EmailStr
    username: str


    # ✅ 关键配置：允许从 ORM 对象 (数据库模型) 读取数据
    model_config = ConfigDict (from_attributes=True)


# --- 登录返回结果 (修正点 2) ---
class LoginOut (BaseModel):
    # ✅ 这里必须使用 Pydantic 的 UserSchema，不能用 User
    user: UserSchema

    # ✅ 建议根据 auth.py 的返回修改字段名 (通常是 access_token)
    # 如果你的后端确实只返回 'token'，请保留原样；
    # 但根据通常的 JWT 实现，这里通常是 access_token 和 refresh_token
    token: str
    #refresh_token: str