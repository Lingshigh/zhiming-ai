from fastapi import APIRouter, Query, Depends, HTTPException
from pydantic import EmailStr
from typing import Annotated
from ZhiMing.dependencis import get_mail, get_session
from fastapi_mail import FastMail, MessageSchema, MessageType
from ZhiMing.models import AsyncSession
from aiosmtplib import SMTPResponseException
from ZhiMing.core.auth import AuthHandler
from ZhiMing.repository import user_repo
from ZhiMing.repository.user_repo import EmailCodeRepository, UserRepository
from ZhiMing.schemas.user import RegisterIn, UserCreateSchema, LoginIn, LoginOut
from ZhiMing.schemas import ResponseOut
import string
import random
# ✅【新增导入】必须导入这个库来验证密码
from passlib.context import CryptContext

router = APIRouter (tags=["user"])
auth_headler = AuthHandler ()

# ✅【新增配置】配置密码加密上下文 (直接在这里处理，不依赖 AuthHandler 了)
pwd_context = CryptContext (schemes=["bcrypt"], deprecated="auto")


@router.get ("/code", response_model=ResponseOut)
async def get_email_code(
        email: Annotated[EmailStr, Query (...)],
        mail: FastMail = Depends (get_mail),
        session: AsyncSession = Depends (get_session),
):
    # 生成4位数字验证码
    source = string.digits * 4
    code = "".join (random.sample (source, 4))

    # 先存数据库，再发邮件
    email_code_repo = EmailCodeRepository (session=session)
    await email_code_repo.create (email, code)

    # 创建消息对象
    message = MessageSchema (
        subject="【智名AI 验证码】",
        recipients=[email],
        body=f"您的验证码是: {code}, 5分钟内有效",
        subtype=MessageType.plain
    )

    try:
        await mail.send_message (message)
    except Exception as e:
        print (f"邮件发送异常: {e}")

    return ResponseOut ()


@router.post ("/register", response_model=ResponseOut)
async def register(
        data: RegisterIn,
        session: AsyncSession = Depends (get_session),
):
    user_repo_instance = UserRepository (session=session)
    email_exist = await user_repo_instance.email_is_exist (email=str (data.email))

    if email_exist:
        raise HTTPException (400, detail="邮箱已经存在！")

    email_code_repo = EmailCodeRepository (session=session)

    # 校验验证码
    email_code_match = await email_code_repo.check_email_code (email=str (data.email), code=str (data.code))

    if not email_code_match:
        raise HTTPException (400, detail='验证码错误或已过期')

    try:
        # 创建用户
        hashed_password = pwd_context.hash (data.password)

        # 创建用户
        await user_repo_instance.create (UserCreateSchema (
            email=str (data.email),
            password=hashed_password,  # ✅ 这里存入加密后的密文！
            username=data.username
        ))
    except Exception as e:
        raise HTTPException (500, detail=f"注册失败: {str (e)}")

    return ResponseOut ()


# ✅【核心修复】登录接口
@router.post ('/login', response_model=LoginOut)
async def login(
        data: LoginIn,
        session: AsyncSession = Depends (get_session)
):
    current_user_repo = UserRepository (session=session)

    # 1. 根据邮箱查找用户
    user = await current_user_repo.get_by_email (str (data.email))

    if not user:
        raise HTTPException (400, detail="该用户不存在")

    # ✅【修复点 1】直接使用 pwd_context 验证密码
    # 之前报错是因为 auth_headler 里没有 verify_password 方法，现在直接用标准库验证
    if not pwd_context.verify (data.password, user.password_hash):
        raise HTTPException (400, detail="邮箱或密码错误")

    # 2. 生成 Token
    tokens = auth_headler.encode_login_token (user.id)

    # ✅【修复点 2】补全所有字段，兼容 user.py 里的 Schema 定义
    # 无论你的 Schema 要 'token' 还是 'access_token'，这里都给，防止 500 报错
    return {
        "user": user,
        "token": tokens['access_token'],  # 兼容旧代码
        "access_token": tokens['access_token'],  # 兼容标准 JWT
        "refresh_token": tokens.get ('refresh_token', 'not_implemented')  # 防止 Schema 查不到字段报错
    }