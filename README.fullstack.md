# 🎨 Volcengine 图像生成器 - 全栈单镜像版本

这是一个前后端一体化的Docker镜像版本，只需运行一个容器即可使用完整的应用。

## ✨ 特点

- **单一镜像**：前端和后端打包在同一个Docker镜像中
- **开箱即用**：只需一个命令即可启动应用
- **生产就绪**：使用Nginx服务前端，FastAPI提供后端API
- **轻量高效**：使用Supervisor管理多进程

## 🏗️ 架构

```
┌─────────────────────────────────────────────────┐
│           Docker容器（端口 3000）               │
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │         Supervisor进程管理              │   │
│  │                                         │   │
│  │  ┌──────────┐        ┌──────────┐      │   │
│  │  │  Nginx   │        │ Uvicorn  │      │   │
│  │  │ (端口80) │───────▶│ (端口8000)│      │   │
│  │  │          │        │          │      │   │
│  │  │ 前端静态 │        │ FastAPI  │      │   │
│  │  │ 反向代理 │        │ 后端服务 │      │   │
│  │  └──────────┘        └──────────┘      │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
│                   ▼                             │
│          Volcengine 图像API                     │
└─────────────────────────────────────────────────┘
```

## 🚀 快速开始

### 方式一：使用Docker Compose（推荐）

1. **配置环境变量**

```bash
cp .env.example .env
nano .env  # 编辑并填入火山引擎凭证（可选）
```

2. **启动应用**

```bash
docker-compose -f docker-compose.fullstack.yml up -d
```

3. **访问应用**

打开浏览器访问：http://localhost:3000

### 方式二：使用Docker命令

1. **构建镜像**

```bash
docker build -f Dockerfile.fullstack -t volcengine-fullstack:latest .
```

2. **运行容器**

```bash
docker run -d \
  --name volcengine-app \
  -p 3000:80 \
  -v $(pwd)/backend/app/data:/app/data \
  -e VOLCENGINE_ACCESS_KEY=your_key \
  -e VOLCENGINE_SECRET_KEY=your_secret \
  volcengine-fullstack:latest
```

3. **访问应用**

打开浏览器访问：http://localhost:3000

### 方式三：使用提供的脚本

```bash
# 构建并启动
./scripts/start-fullstack.sh

# 停止应用
docker-compose -f docker-compose.fullstack.yml down

# 查看日志
docker-compose -f docker-compose.fullstack.yml logs -f
```

## 📝 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `VOLCENGINE_ACCESS_KEY` | 火山引擎 Access Key | - |
| `VOLCENGINE_SECRET_KEY` | 火山引擎 Secret Key | - |
| `VOLCENGINE_REGION` | API 区域 | `cn-beijing` |

**注意：** 如果未提供凭证，应用将以Demo模式运行。

## 🔧 管理命令

### 查看容器状态

```bash
docker ps
```

### 查看日志

```bash
# 查看所有日志
docker logs volcengine-app

# 实时跟踪日志
docker logs -f volcengine-app

# 查看后端日志
docker exec volcengine-app tail -f /var/log/supervisor/uvicorn.log

# 查看Nginx日志
docker exec volcengine-app tail -f /var/log/supervisor/nginx.log
```

### 重启服务

```bash
# 重启整个容器
docker restart volcengine-app

# 重启后端服务（在容器内）
docker exec volcengine-app supervisorctl restart uvicorn

# 重启Nginx（在容器内）
docker exec volcengine-app supervisorctl restart nginx
```

### 停止和删除

```bash
# 停止容器
docker stop volcengine-app

# 删除容器
docker rm volcengine-app

# 删除镜像
docker rmi volcengine-fullstack:latest
```

## 🎯 端口说明

- **3000**：应用访问端口（映射到容器内的80端口）
  - 前端应用：http://localhost:3000
  - 后端API：http://localhost:3000/api
  - 健康检查：http://localhost:3000/health

## 📦 镜像大小

- 构建后的镜像大小约为：~500MB
- 包含完整的前端构建和后端依赖

## 🔍 故障排查

### 容器无法启动

```bash
# 查看容器日志
docker logs volcengine-app

# 检查容器状态
docker ps -a
```

### 服务无响应

```bash
# 进入容器检查服务状态
docker exec -it volcengine-app bash

# 检查进程
docker exec volcengine-app supervisorctl status

# 查看端口
docker exec volcengine-app netstat -tlnp
```

### 健康检查失败

```bash
# 手动测试健康检查
docker exec volcengine-app wget --quiet --tries=1 --spider http://localhost:80/health

# 检查后端是否运行
docker exec volcengine-app curl http://localhost:8000/health
```

## 🆚 与分离式架构的对比

### 全栈单镜像版本（当前）
✅ 优点：
- 部署简单，只需一个容器
- 配置简单，不需要容器间网络
- 资源占用较少
- 适合小型部署和开发测试

❌ 缺点：
- 无法独立扩展前后端
- 升级需要重新构建整个镜像

### 分离式架构版本（原始）
✅ 优点：
- 可以独立扩展前后端服务
- 更灵活的部署选项
- 适合生产环境和大规模部署

❌ 缺点：
- 配置相对复杂
- 需要管理多个容器
- 需要配置容器间网络

## 🚢 生产部署建议

### 1. 使用环境变量文件

```bash
# 创建生产环境配置
cat > .env.production <<EOF
VOLCENGINE_ACCESS_KEY=your_production_key
VOLCENGINE_SECRET_KEY=your_production_secret
VOLCENGINE_REGION=cn-beijing
EOF

# 使用生产配置启动
docker run -d \
  --name volcengine-app \
  -p 80:80 \
  --env-file .env.production \
  -v /data/volcengine:/app/data \
  --restart unless-stopped \
  volcengine-fullstack:latest
```

### 2. 配置持久化存储

```bash
# 创建数据目录
mkdir -p /data/volcengine/output

# 运行时挂载
docker run -d \
  --name volcengine-app \
  -p 3000:80 \
  -v /data/volcengine:/app/data \
  volcengine-fullstack:latest
```

### 3. 使用反向代理（HTTPS）

如果需要HTTPS，建议在前面加一层反向代理（如Nginx、Traefik或Caddy）：

```nginx
# nginx配置示例
server {
    listen 443 ssl http2;
    server_name your-domain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 📊 监控和维护

### 健康检查

```bash
# HTTP健康检查
curl http://localhost:3000/health

# 响应示例
{
  "status": "healthy",
  "version": "1.0.0",
  "volcengine_configured": true
}
```

### 资源使用

```bash
# 查看容器资源使用
docker stats volcengine-app

# 限制资源使用
docker run -d \
  --name volcengine-app \
  --memory="1g" \
  --cpus="1.0" \
  -p 3000:80 \
  volcengine-fullstack:latest
```

## 🔗 相关文档

- [主README文档](README.md) - 完整功能介绍
- [快速开始指南](QUICK_START.md) - 快速上手指南
- [部署指南](DOCKER_BUILD_SUMMARY.md) - Docker构建说明

## 💡 常见问题

**Q: 全栈镜像和分离式镜像有什么区别？**
A: 全栈镜像将前后端打包在一个容器中，部署更简单；分离式镜像将前后端分开，更灵活但配置稍复杂。

**Q: 可以在生产环境使用全栈镜像吗？**
A: 可以，但建议根据规模选择：小型应用使用全栈镜像更简单；大型应用建议使用分离式架构以便扩展。

**Q: 如何更新应用版本？**
A: 重新构建镜像后，停止旧容器，启动新容器即可。建议使用版本标签管理镜像。

**Q: Demo模式是什么？**
A: 如果未提供火山引擎凭证，应用将使用占位图像进行演示，不会调用真实API。

---

**享受简单的全栈部署体验！** 🚀
