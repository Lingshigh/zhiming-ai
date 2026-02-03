from datetime import timedelta

# 数据库连接
DB_URL = "mysql+aiomysql://root:root@127.0.0.1:3306/zhiname?charset=utf8mb4"

# --- 邮件配置 ---
MAIL_USERNAME = "1138003884@qq.com"
MAIL_PASSWORD = "yqygiwydouifgejj"     # 你的授权码
MAIL_FROM = "1138003884@qq.com"          # 【已修复】之前少写了一位 '4'
MAIL_PORT = 465                          # 【建议修改】QQ邮箱推荐使用 465 端口
MAIL_SERVER = "smtp.qq.com"
MAIL_FROM_NAME = "ZhiMing AI"

# 【关键修复】
MAIL_STARTTLS = False                    # 465 端口通常不需要 STARTTLS
MAIL_SSL_TLS = True                      # 【已修复】之前你写成了 SST，必须是 SSL (True)

# --- JWT 配置 ---
JWT_SECRET_KEY = "sfsadadafsj32w"
JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=15)
JWT_REFEFRESH_TOKEN_EXPIRES = timedelta(days=30)