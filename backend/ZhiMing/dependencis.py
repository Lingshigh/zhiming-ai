from core.mail import create_mail_instance
from fastapi_mail import FastMail
from sqlalchemy.ext.asyncio import AsyncSession
from models import AsyncSessionFactory

#获取session对象用于操作数据库，将邮箱验证码存入数据库
async def get_session() -> AsyncSession:
    session = AsyncSessionFactory()
    try:
        yield session
    finally:
        await session.close()

#将其封装成依赖项
async def get_mail()-> FastMail:
    return create_mail_instance()