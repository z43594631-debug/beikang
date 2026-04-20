from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pickle
import numpy as np
import os

app = FastAPI()

# ✅ 解决跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ 加在 import 后面也可以（更清晰）
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "validated_model.pkl")

# ✅ 第二步：打印日志（放在加载前）
print("当前工作目录：", os.getcwd())
print("模型路径：", model_path)

# ✅ 第三步：防止程序崩溃（try 包住加载）
try:
    with open(model_path, "rb") as f:
        data = pickle.load(f)
    print("模型加载成功 ✅")
except Exception as e:
    print("模型加载失败 ❌：", e)
    data = None
    
sub = data["breast_cancer_wisconsin_original"]

while isinstance(sub, dict):
    if "model" in sub:
        sub = sub["model"]
    else:
        break

model = sub


# ✅ 测试接口（很重要！）
@app.get("/")
def home():
    return {"message": "API running"}


# ✅ 预测接口
@app.post("/predict")
def predict(data: dict):
    try:
        features = np.array(data["features"]).reshape(1, -1)
        result = model.predict(features)

        return {
            "success": True,
            "result": result.tolist()
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


