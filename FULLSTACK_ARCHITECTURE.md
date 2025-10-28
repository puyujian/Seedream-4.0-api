# 🏗️ 全栈单镜像架构说明

本文档详细说明全栈单镜像版本的架构设计和技术实现。

## 📐 架构设计

### 整体架构

```
┌─────────────────────────────────────────────────────────────┐
│                    Docker 容器                               │
│  volcengine-fullstack:latest                                │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │              Supervisor (进程管理)                      │ │
│  │  - 管理多个进程                                         │ │
│  │  - 进程监控和自动重启                                    │ │
│  │  - 统一日志管理                                         │ │
│  └─────────┬─────────────────────────┬────────────────────┘ │
│            │                         │                       │
│  ┌─────────▼─────────┐    ┌─────────▼──────────┐           │
│  │   Nginx (80)      │    │  Uvicorn (8000)    │           │
│  │  - 前端静态文件    │    │  - FastAPI 后端     │           │
│  │  - 反向代理        │◄───┤  - 图像生成 API     │           │
│  │  - Gzip 压缩      │    │  - 业务逻辑处理     │           │
│  └───────────────────┘    └────────────────────┘           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
                  火山引擎图像 API
```

### 进程管理

使用 **Supervisor** 管理容器内的多个进程：

1. **Nginx** - 前端服务和反向代理
   - 端口：80
   - 服务前端静态文件
   - 反向代理 API 请求到后端

2. **Uvicorn** - Python ASGI 服务器
   - 端口：8000（内部）
   - 运行 FastAPI 应用
   - 处理图像生成请求

### 网络通信

```
外部请求 → 端口3000 (主机) → 端口80 (容器)
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                静态文件 (/)              API 请求 (/api)
                    │                           │
                    ▼                           ▼
               Nginx 直接服务              127.0.0.1:8000
                                              (Uvicorn)
```

## 🔧 技术实现

### 多阶段构建

#### 阶段 1：前端构建

```dockerfile
FROM node:20-alpine AS frontend-build
WORKDIR /app
COPY frontend/package*.json ./
RUN npm ci --ignore-scripts
COPY frontend/ ./
RUN npm run build
# 输出：/app/dist
```

#### 阶段 2：最终镜像

```dockerfile
FROM python:3.11-slim

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    nginx supervisor wget curl net-tools

# 安装 Python 依赖
COPY backend/requirements.txt .
RUN pip install -r requirements.txt

# 复制应用代码
COPY backend/app/ ./app/

# 复制前端构建产物
COPY --from=frontend-build /app/dist /usr/share/nginx/html

# 配置 Nginx 和 Supervisor
COPY nginx/nginx.conf.fullstack /etc/nginx/conf.d/default.conf
COPY nginx/nginx-main.conf /etc/nginx/nginx.conf
COPY supervisor/supervisord.conf /etc/supervisor/conf.d/

# 启动 Supervisor
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
```

### Nginx 配置

**主配置** (`nginx-main.conf`):
- Worker 进程配置
- Gzip 压缩
- 日志设置
- MIME 类型

**站点配置** (`nginx.conf.fullstack`):
```nginx
server {
    listen 80;
    
    # 前端 SPA
    location / {
        root /usr/share/nginx/html;
        try_files $uri $uri/ /index.html;
    }
    
    # 后端 API
    location /api/ {
        proxy_pass http://127.0.0.1:8000/api/;
    }
    
    # 健康检查
    location /health {
        proxy_pass http://127.0.0.1:8000/health;
    }
}
```

### Supervisor 配置

```ini
[supervisord]
nodaemon=true
logfile=/var/log/supervisor/supervisord.log

[program:uvicorn]
command=uvicorn app.main:app --host 0.0.0.0 --port 8000
directory=/app
autorestart=true
stdout_logfile=/var/log/supervisor/uvicorn.log

[program:nginx]
command=/usr/sbin/nginx -g "daemon off;"
autorestart=true
stdout_logfile=/var/log/supervisor/nginx.log
```

## 📦 构建过程

### 构建流程

```
1. 前端构建阶段
   ├── 安装 Node.js 依赖
   ├── 构建 Vue 应用 (npm run build)
   └── 生成静态文件到 /app/dist

2. 最终镜像阶段
   ├── 安装系统包 (nginx, supervisor, 工具)
   ├── 安装 Python 依赖
   ├── 复制后端代码
   ├── 复制前端构建产物
   ├── 配置 Nginx
   └── 配置 Supervisor

3. 启动
   └── Supervisor 启动并管理 Nginx 和 Uvicorn
```

### 文件结构

```
/                                  # 容器内文件系统
├── app/                          # 后端应用
│   ├── app/                      # Python 代码
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── routers/
│   │   └── services/
│   └── data/                     # 数据目录（挂载点）
│       └── output/               # 生成的图片
├── usr/share/nginx/html/         # 前端静态文件
│   ├── index.html
│   ├── assets/
│   └── ...
├── etc/
│   ├── nginx/
│   │   ├── nginx.conf           # Nginx 主配置
│   │   └── conf.d/
│   │       └── default.conf     # 站点配置
│   └── supervisor/
│       └── conf.d/
│           └── supervisord.conf  # Supervisor 配置
└── var/log/
    ├── nginx/                    # Nginx 日志
    │   ├── access.log
    │   └── error.log
    └── supervisor/               # Supervisor 日志
        ├── supervisord.log
        ├── uvicorn.log
        └── nginx.log
```

## 🚀 启动流程

### 容器启动序列

```
1. Docker 启动容器
   ↓
2. 执行 CMD: supervisord
   ↓
3. Supervisor 读取配置
   ↓
4. Supervisor 启动子进程
   ├── 启动 Uvicorn (FastAPI)
   │   └── 监听 0.0.0.0:8000
   └── 启动 Nginx
       └── 监听 0.0.0.0:80
   ↓
5. 应用就绪
   └── 健康检查通过
```

### 健康检查

Docker 健康检查：
```bash
wget --quiet --tries=1 --spider http://localhost:80/health
```

健康检查流程：
```
1. Docker 发起健康检查
   ↓
2. 请求 http://localhost:80/health
   ↓
3. Nginx 接收请求
   ↓
4. Nginx 反向代理到 http://127.0.0.1:8000/health
   ↓
5. FastAPI 处理健康检查
   ↓
6. 返回 {"status": "healthy", ...}
```

## 🔄 请求处理流程

### 前端资源请求

```
浏览器 → http://localhost:3000/
         ↓
Docker 端口映射 (3000:80)
         ↓
Nginx (端口 80)
         ↓
try_files $uri $uri/ /index.html
         ↓
返回 /usr/share/nginx/html/index.html
```

### API 请求

```
浏览器 → http://localhost:3000/api/v1/generate/text2image
         ↓
Docker 端口映射 (3000:80)
         ↓
Nginx (端口 80)
         ↓
location /api/ 匹配
         ↓
proxy_pass http://127.0.0.1:8000/api/
         ↓
Uvicorn (端口 8000)
         ↓
FastAPI 路由处理
         ↓
调用火山引擎 API
         ↓
返回生成的图片
```

## 📊 资源使用

### 镜像大小

- **基础镜像**: Python 3.11-slim (~150MB)
- **系统包**: Nginx, Supervisor (~50MB)
- **Python 依赖**: FastAPI, Uvicorn 等 (~100MB)
- **前端构建产物**: Vue 应用 (~5MB)
- **总计**: ~500MB

### 运行时资源

- **CPU**: 建议 1-2 核
- **内存**: 建议 512MB-1GB
- **磁盘**: 
  - 系统: ~500MB
  - 数据: 根据生成的图片数量

## 🔍 监控和调试

### 查看进程状态

```bash
docker exec volcengine-app supervisorctl status
```

输出示例：
```
nginx                            RUNNING   pid 25, uptime 0:05:12
uvicorn                          RUNNING   pid 24, uptime 0:05:12
```

### 查看日志

```bash
# 容器总日志
docker logs volcengine-app

# Supervisor 主日志
docker exec volcengine-app cat /var/log/supervisor/supervisord.log

# 后端日志
docker exec volcengine-app tail -f /var/log/supervisor/uvicorn.log

# Nginx 日志
docker exec volcengine-app tail -f /var/log/supervisor/nginx.log
docker exec volcengine-app tail -f /var/log/nginx/access.log
docker exec volcengine-app tail -f /var/log/nginx/error.log
```

### 进入容器调试

```bash
docker exec -it volcengine-app bash

# 在容器内：
ps aux                           # 查看进程
netstat -tlnp                    # 查看端口监听
curl http://localhost:8000/health  # 测试后端
curl http://localhost:80/health    # 测试 Nginx
supervisorctl status             # 查看服务状态
supervisorctl restart uvicorn    # 重启后端
supervisorctl restart nginx      # 重启 Nginx
```

## 🆚 与分离式架构对比

### 全栈单镜像

**优势**:
- ✅ 部署简单，只需一个容器
- ✅ 配置简单，无需容器间通信
- ✅ 资源占用相对较少
- ✅ 适合小型部署、开发、测试

**劣势**:
- ❌ 无法独立扩展前后端
- ❌ 升级需要重建整个镜像
- ❌ 不适合大规模生产环境

### 分离式架构

**优势**:
- ✅ 可以独立扩展服务
- ✅ 前后端可独立更新
- ✅ 更符合微服务架构
- ✅ 适合生产环境

**劣势**:
- ❌ 部署相对复杂
- ❌ 需要管理多个容器
- ❌ 需要配置网络

## 🎯 适用场景

### 推荐使用全栈单镜像

- 个人项目或小型应用
- 开发和测试环境
- 快速原型验证
- 简单的生产部署
- 容器化学习

### 推荐使用分离式架构

- 生产环境部署
- 需要高可用性
- 需要独立扩展
- 大型企业应用
- 微服务架构

## 🔐 安全考虑

### 容器内安全

1. **进程权限**
   - Nginx 以 www-data 用户运行
   - Uvicorn 以 root 运行（可改进为非 root）

2. **文件权限**
   - 前端文件: www-data 权限
   - 后端代码: root 权限
   - 数据目录: 755 权限

3. **网络隔离**
   - 后端仅监听 localhost:8000
   - 仅 Nginx 80 端口对外暴露

### 部署安全

1. **环境变量**
   - 使用 `.env` 文件
   - 不在镜像中硬编码凭证

2. **HTTPS**
   - 建议使用反向代理添加 SSL
   - 或使用 Caddy 自动 HTTPS

3. **访问控制**
   - 配置防火墙规则
   - 限制访问来源

## 📝 总结

全栈单镜像版本通过以下技术实现：

1. **多阶段构建** - 分离构建和运行环境
2. **Supervisor** - 管理多个进程
3. **Nginx** - 高效的静态文件服务和反向代理
4. **本地通信** - 使用 localhost 通信，无需网络配置

这种架构适合简单部署场景，提供了良好的性能和易用性平衡。

---

**相关文档**:
- [快速部署指南](QUICK_DEPLOY.md)
- [使用文档](README.fullstack.md)
- [主文档](README.md)
