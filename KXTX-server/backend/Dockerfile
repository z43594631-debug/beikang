# 使用 Python 官方镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件
# 如果有 requirements.txt，请确保它存在。如果没有，我们将直接安装必要的包
RUN pip install --no-cache-dir fastapi uvicorn numpy

# 复制后端代码和模型
COPY app.py validated_model.pkl ./

# 暴露 FastAPI 默认端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
