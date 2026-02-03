from fastapi import FastAPI
from fastapi_mail import FastMail, MessageSchema, MessageType
from fastapi import Depends
from dependencis import get_mail  # 注意：你的文件名似乎是 dependencis.py (少个e)，请保持一致
from aiosmtplib import SMTPResponseException
# 导入路由
from routers.user_router import router as auth_router
from routers.name_router import router as name_router
from fastapi.middleware.cors import CORSMiddleware

# 1. 实例化 APP
app = FastAPI()

# 2. 配置跨域中间件 (解决前端 Network Error)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# 3. 【关键修复】注册路由
# 缺少这两行，你的登录、注册、起名功能全部失效！
# ==========================================
app.include_router(auth_router, prefix="/auth", tags=["用户认证"])  # 对应前端 /auth/login, /auth/register
app.include_router(name_router, prefix="/name", tags=["AI起名"])    # 对应前端 /name


# --- 以下是你原本的测试接口 (保持不变) ---

@app.get("/")
async def root():
    return {"message": "Hello world"}

@app.get("/hello/{name}")
async def asy_hello(name: str):
    return {"message": f"Hello {name}"}

# 视图函数测试 mail
@app.get("/mail/test")
async def mail_test(
    email: str,
    mail: FastMail = Depends(get_mail),
):
    message = MessageSchema(
        subject="智名AI验证码",  # 我稍微改了一下标题，更像样一点
        recipients=[email],
        body=f"您的验证码是: {email} (测试用)", # 这里只是演示，实际逻辑应生成随机数字
        subtype=MessageType.plain,
    )

    # 异步等待
    try:
        await mail.send_message(message)
        return {"message": "send successful"}
    except Exception as e:
        return {"message": f"发送失败: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    # "main:app" 中的 main 对应文件名 main.py，app 对应 app = FastAPI()
    # reload=True 表示代码修改后自动重启，方便开发
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)