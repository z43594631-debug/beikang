from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# 读取数据库地址
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    connect_args={"connect_timeout":5}
)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
Base.metadata.creat_all(bind=engine)

app = FastAPI()
@app.get("/")
def root():
    return {"message": "Backend is running"}

# ===== 数据表 =====
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)

# 创建表
Base.metadata.create_all(bind=engine)

# ===== 请求模型 =====
class UserCreate(BaseModel):
    username: str
    password: str

# ===== 注册 =====
@app.post("/register")
def register(user: UserCreate):
    db = SessionLocal()
    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="用户已存在")

    new_user = User(username=user.username, password=user.password)
    db.add(new_user)
    db.commit()
    return {"message": "注册成功"}

# ===== 登录 =====
@app.post("/login")
def login(user: UserCreate):
    db = SessionLocal()
    existing = db.query(User).filter(User.username == user.username).first()

    if not existing or existing.password != user.password:
        raise HTTPException(status_code=401, detail="用户名或密码错误")

    return {"message": "登录成功"}

