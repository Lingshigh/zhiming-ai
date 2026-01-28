from fastapi_mail import FastMail, ConnectionConfig
from pydantic import EmailStr
# from pydantic import SecretStr
from ZhiMing import setting


def create_mail_instance() -> FastMail:
    mail_config = ConnectionConfig (
        MAIL_USERNAME=setting.MAIL_USERNAME,

        # ✅ 【修改点】直接传 setting 里的字符串，不要包 SecretStr
        MAIL_PASSWORD=setting.MAIL_PASSWORD,

        MAIL_FROM=setting.MAIL_FROM,
        MAIL_PORT=setting.MAIL_PORT,
        MAIL_SERVER=setting.MAIL_SERVER,
        MAIL_FROM_NAME=setting.MAIL_FROM_NAME,
        MAIL_STARTTLS=setting.MAIL_STARTTLS,
        MAIL_SSL_TLS=setting.MAIL_SSL_TLS,
        USE_CREDENTIALS=True,
        VALIDATE_CERTS=True,
    )
    return FastMail (mail_config)