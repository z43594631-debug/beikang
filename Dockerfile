# 使用 Node.js 官方镜像作为基础镜像
FROM node:18-alpine

# 设置工作目录
WORKDIR /app

# 复制 package.json 和 package-lock.json
COPY package*.json ./

# 安装 Node.js 依赖
RUN npm install --production

# 关键修改：安装 Python 环境和 pip（用于模型调用）
RUN apk add --no-cache python3 py3-pip
# 复制模型相关文件和依赖
COPY model/ ./model/
# 安装 Python 模型依赖
RUN pip3 install -r ./model/requirements.txt

# 复制所有服务器代码
COPY . .

# 暴露端口（Railway 会自动分配 PORT，这里只是声明）
EXPOSE 5000

# 启动应用
CMD ["node", "index.js"]
