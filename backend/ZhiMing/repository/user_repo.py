# 指明从 ZhiMing 这个大包里导入
from ZhiMing.models import AsyncSession
from ZhiMing.models.user import User, EmailCode
from sqlalchemy import select, update, delete, exists
from datetime import datetime, timedelta
from ZhiMing.schemas.user import UserCreateSchema
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exists
# 注意：你需要根据实际路径导入 User 模型和 UserCreateSchema
# from models.user import User

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_email(self, email: str) -> "User | None":
        async with self.session.begin():
            return await self.session.scalar(select(User).filter(User.email == email))

    async def email_is_exist(self, email: str) -> bool:
        async with self.session.begin():
            stmt = select(exists().where(User.email == email))
            return await self.session.scalar(stmt)

    async def create(self, user_schema: "UserCreateSchema") -> "User":
        async with self.session.begin():
            user = User(**user_schema.model_dump())
            self.session.add(user)
            return user

class EmailCodeRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

#自动将emailcode的送人数据库中
    async def create(self, email: str, code: str) -> EmailCode:
        async with self.session.begin ():
            email_code = EmailCode (email=email, code=code)
            self.session.add (email_code)
            return email_code

    async def check_email_code(self, email: str, code: str) -> bool:
        async with self.session.begin ():
            # 查询数据库中是否存在该邮箱对应的验证码
            stmt = select(EmailCode).where(EmailCode.email == email,EmailCode.code==code)
            email_code: EmailCode | None = await self.session.scalar (
                select (EmailCode).filter_by (email=email, code=code)
            )

            if not email_code:
                return False

            # 校验验证码是否过期（有效期 10 分钟）
            if (datetime.now () - email_code.created_time) > timedelta (minutes=10):
                return False

            return True