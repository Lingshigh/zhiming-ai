# 智名 AI (ZhiMing AI) 🔮

> 一个基于 FastAPI + Vue 3 的智能起名系统，集成了完整的用户认证与 AI 生成能力。

## 📖 项目介绍

**智名 AI** 是一款结合了现代 Web 技术与 AI 代理的项目。它允许用户通过邮箱验证码注册账户，登录后使用 AI 算法生成个性化的名字。项目采用前后端分离架构，后端使用高性能的 FastAPI 框架，前端使用 Vue 3 (Uni-app) 构建。

## ✨ 核心功能

* **🔐 用户认证系统**
    * 支持邮箱验证码注册 (FastAPI Mail + SMTP)。
    * JWT (JSON Web Token) 登录认证与令牌刷新。
    * 密码加密存储 (Passlib + PBKDF2)。
* **🤖 AI 智能起名**
    * 集成 LangChain/LLM Agent (根据代码推测)。
    * 根据用户输入生成个性化名字建议。
* **🛠 稳健的后端架构**
    * 完全异步的数据库操作 (SQLAlchemy Async + MySQL)。
    * 标准的 Pydantic 数据模型校验。
    * RESTful API 设计风格。

## 🏗 技术栈

### 后端 (Backend)
* **框架**: [FastAPI](https://fastapi.tiangolo.com/) - 高性能 Python Web 框架
* **数据库**: MySQL 8.0
* **ORM**: SQLAlchemy (AsyncIO)
* **认证**: Python-Jose / Passlib
* **工具**: Pydantic, Uvicorn, Aiosmtplib

### 前端 (Frontend)
* **框架**: Vue 3
* **构建**: Uni-app (Vite)
* **样式**: CSS3 Flexbox

### 目录结构（后端）
<img width="791" height="1278" alt="image" src="https://github.com/user-attachments/assets/8c2ac472-a8ba-4de4-8bc6-5b8b24d16f20" />


### 目录结构（前端）
<img width="489" height="612" alt="image" src="https://github.com/user-attachments/assets/9419319e-f2f3-4471-be8f-1ec41973f8d5" />

### 登录注册展示
<img width="754" height="1000" alt="image" src="https://github.com/user-attachments/assets/aa413f3a-6fa4-4600-93f6-4313e62c029c" />
<img width="2520" height="1399" alt="image" src="https://github.com/user-attachments/assets/ac7ad5c6-698a-4c40-abf5-4c400e1bbbcb" />


### ai命名功能展示
<img width="1258" height="835" alt="企业微信截图_17695860601552" src="https://github.com/user-attachments/assets/40c9dbb2-6e17-4be7-887a-74bc7b4dedcc" />
<img width="1258" height="934" alt="企业微信截图_17695864586975" src="https://github.com/user-attachments/assets/13b8d227-5d7b-46eb-975a-d5c49cc593da" />
<img width="2504" height="1416" alt="企业微信截图_17701703003433" src="https://github.com/user-attachments/assets/df873666-5efa-4065-b032-2420aaf5e575" />
<img width="2504" height="1416" alt="企业微信截图_17701703299026" src="https://github.com/user-attachments/assets/7a247ca6-7b2d-4f81-bd28-3111d77516fc" />

### 模型配置功能展示
<img width="2504" height="1416" alt="企业微信截图_17701707869096" src="https://github.com/user-attachments/assets/7830b01c-9533-4d44-9b2a-1c3a36512935" />



## 🚀 快速开始

### 1. 环境准备
* Python 3.10+
* MySQL 5.7+
* Node.js (用于前端)

### 2. 后端设置

```bash
# 克隆项目
git clone [https://github.com/your-username/zhiming-ai.git](https://github.com/your-username/zhiming-ai.git)
cd zhiming-ai

# 创建虚拟环境
python -m venv venv
# Windows 激活
venv\Scripts\activate
# Mac/Linux 激活
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt


### 3.配置文件
# 示例配置
SQLALCHEMY_DATABASE_URL = "mysql+aiomysql://root:password@localhost:3306/zhiname"
MAIL_USERNAME = "your_qq_email@qq.com"
MAIL_PASSWORD = "your_auth_code"


# 在项目根目录下运行
uvicorn main:app --reload --host 127.0.0.1 --port 8000

5. 数据库初始化
确保 MySQL 中已创建数据库 zhiname，并导入提供的 SQL 文件（如果有）或等待 ORM 自动建表


