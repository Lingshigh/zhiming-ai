from ZhiMing.models import Base
from sqlalchemy.orm import mapped_column,Mapped
from sqlalchemy import String,Integer,DateTime
from datetime import datetime
from passlib.hash import pbkdf2_sha256 as password_hash


class User(Base):
    __tablename__ = "user"
    __table_args__ = {'extend_existing': True}  #防止报错

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password_hash: Mapped[str] = mapped_column(String(128))


    def __init__(self, *args, **kwargs):
        password = kwargs.pop("password", None)
        super().__init__(*args, **kwargs)   
        if password:
            self.password = password
    
    @property
    def password(self):
        return self._password
    

    @password.setter
    def password(self, raw_password):
        self.password_hash = password_hash.hash(raw_password)

    def verify_password(self, raw_password):
        return password_hash.verify(raw_password, self.password_hash)
    
class EmailCode(Base):
    __tablename__ = "email_code"
    __table_args__ = {'extend_existing': True}  # 补上这一行

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(100))
    code: Mapped[str] = mapped_column(String(10))
    created_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)