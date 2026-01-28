import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from datetime import datetime
from enum import Enum
from ZhiMing import setting
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN
from threading import Lock


# --- 工具类与枚举定义 ---

class SingletonMeta (type):
    """
    这是一个线程安全的单例模式实现。
    """
    _instances = {}
    _lock: Lock = Lock ()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super ().__call__ (*args, **kwargs)
                cls._instances[cls] = instance
            return cls._instances[cls]


class TokenTypeEnum (Enum):
    ACCESS_TOKEN = 1
    REFRESH_TOKEN = 2


# --- 核心认证处理器(单例设计模式) ---

class AuthHandler (metaclass=SingletonMeta):
    security = HTTPBearer ()
    # Authorization: Bearer {token}

    secret = setting.JWT_SECRET_KEY

    def _encode_token(self, user_id: int, type: TokenTypeEnum):
        payload = dict (
            iss=user_id,
            sub=int (type.value)
        )
        to_encode = payload.copy ()

        # 设置过期时间
        if type == TokenTypeEnum.ACCESS_TOKEN:
            exp = datetime.now () + setting.JWT_ACCESS_TOKEN_EXPIRES
        else:
            exp = datetime.now () + setting.JWT_REFRESH_TOKEN_EXPIRES

        to_encode.update ({"exp": int (exp.timestamp ())})
        return jwt.encode (to_encode, self.secret, algorithm='HS256')

    def encode_login_token(self, user_id: int):
        """生成登录所需的 Access 和 Refresh Token"""
        access_token = self._encode_token (user_id, TokenTypeEnum.ACCESS_TOKEN)
        refresh_token = self._encode_token (user_id, TokenTypeEnum.REFRESH_TOKEN)
        login_token = dict (
            #会生成两个token
            access_token=f"{access_token}",
            refresh_token=f"{refresh_token}"
        )
        return login_token

    def encode_update_token(self, user_id: int):
        """仅更新 Access Token"""
        access_token = self._encode_token (user_id, TokenTypeEnum.ACCESS_TOKEN)
        update_token = dict (
            access_token=f"{access_token}"
        )
        return update_token

    def decode_access_token(self, token):
        """验证 Access Token (失败返回 403)"""
        # ACCESS TOKEN: 不可用（过期，或有问题），都用403错误
        try:
            payload = jwt.decode (token, self.secret, algorithms=['HS256'])
            if payload['sub'] != int (TokenTypeEnum.ACCESS_TOKEN.value):
                raise HTTPException (status_code=HTTP_403_FORBIDDEN, detail='Token类型错误！')
            return payload['iss']
        except jwt.ExpiredSignatureError:
            raise HTTPException (status_code=HTTP_403_FORBIDDEN, detail='Access Token已过期')
        except jwt.InvalidTokenError as e:
            raise HTTPException (status_code=HTTP_403_FORBIDDEN, detail='Access Token不可用')

    def decode_refresh_token(self, token):
        """验证 Refresh Token (失败返回 401)"""
        # REFRESH TOKEN: 不可用（过期，或有问题），都用401错误
        try:
            payload = jwt.decode (token, self.secret, algorithms=['HS256'])
            if payload['sub'] != int (TokenTypeEnum.REFRESH_TOKEN.value):
                raise HTTPException (status_code=HTTP_401_UNAUTHORIZED, detail='Token类型错误！')
            return payload['iss']
        except jwt.ExpiredSignatureError:
            raise HTTPException (status_code=HTTP_401_UNAUTHORIZED, detail='Refresh Token已过期')
        except jwt.InvalidTokenError as e:
            raise HTTPException (status_code=HTTP_401_UNAUTHORIZED, detail='Refresh Token不可用')

    # --- FastAPI 依赖注入项 ---

    def auth_access_dependency(self, auth: HTTPAuthorizationCredentials = Security (security)):
        """用于保护需要登录的接口"""
        return self.decode_access_token (auth.credentials)

    def auth_refresh_dependency(self, auth: HTTPAuthorizationCredentials = Security (security)):
        """用于刷新 Token 的接口"""
        return self.decode_refresh_token (auth.credentials)