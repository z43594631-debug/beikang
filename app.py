from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# ========================
# 数据库配置
# ========================
DATABASE_URL = os.getenv("DATABASE_URL")

# Railway 必须加这个（非常关键）
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# ========================
# FastAPI 实例
# ========================
app = FastAPI()

# ========================
# 健康检查（关键接口）
# ========================
@app.get("/")
def root():
    return {"status": "ok"}

# ========================
# 数据表
# ========================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)

# ========================
# 启动时初始化数据库（避免阻塞）
# ========================
@app.on_event("startup")
def startup():
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database connected & tables created")
    except Exception as e:
        print("❌ Database init failed:", e)

# ========================
# 请求模型
# ========================
class UserCreate(BaseModel):
    username: str
    password: str

# ========================
# 注册接口
# ========================
@app.post("/register")
def register(user: UserCreate):
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.username == user.username).first()
        if existing:
            raise HTTPException(status_code=400, detail="用户已存在")

        new_user = User(username=user.username, password=user.password)
        db.add(new_user)
        db.commit()

        return {"message": "注册成功"}

    finally:
        db.close()

# ========================
# 登录接口
# ========================
@app.post("/login")
def login(user: UserCreate):
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.username == user.username).first()

        if not existing or existing.password != user.password:
            raise HTTPException(status_code=401, detail="用户名或密码错误")

        return {"message": "登录成功"}

    finally:
        db.close()
