from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pickle
import numpy as np

app = FastAPI()

# ✅ 解决跨域（前端能访问）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ 加载模型
with open("validated_model.pkl", "rb") as f:
    data = pickle.load(f)
    print("类型:", type(data))
    print(data["breast_cancer_wisconsin_original"])

    sub = data["breast_cancer_wisconsin_original"]

    while isinstance(sub, dict):
        if "model" in sub:
            sub = sub["model"]
        else:
            break

    model = sub
    print(type(model))

# ✅ 测试接口
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