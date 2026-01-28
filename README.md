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
<img width="431" height="194" alt="image" src="https://github.com/user-attachments/assets/7fb82607-8951-4805-80c0-b15a95700833" />

### 目录结构（前端）
<img width="274" height="198" alt="image" src="https://github.com/user-attachments/assets/c915d761-157b-4dbf-be05-d6160282c12c" />


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


