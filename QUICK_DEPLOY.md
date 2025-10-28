# 🚀 快速部署指南 - 全栈单镜像版本

## 📦 30秒快速启动

最简单的方式启动完整应用：

```bash
# 1. 下载或克隆项目
git clone <repository-url>
cd volcengine-image-generator

# 2. 一键启动（包含构建和启动）
./scripts/start-fullstack.sh
```

访问：http://localhost:3000

就是这么简单！✨

## 🎯 手动部署步骤

如果您想手动控制每一步：

### 使用 Docker Compose

```bash
# 1. 配置环境变量（可选）
cp .env.example .env
nano .env  # 填入火山引擎凭证

# 2. 构建并启动
docker-compose -f docker-compose.fullstack.yml up -d

# 3. 查看日志
docker-compose -f docker-compose.fullstack.yml logs -f
```

### 使用纯 Docker 命令

```bash
# 1. 构建镜像
docker build -f Dockerfile.fullstack -t volcengine-fullstack:latest .

# 2. 启动容器
docker run -d \
  --name volcengine-app \
  -p 3000:80 \
  -v $(pwd)/backend/app/data:/app/data \
  -e VOLCENGINE_ACCESS_KEY=your_key \
  -e VOLCENGINE_SECRET_KEY=your_secret \
  volcengine-fullstack:latest

# 3. 查看日志
docker logs -f volcengine-app
```

## 🌐 生产环境部署

### 使用自定义端口

```bash
docker run -d \
  --name volcengine-app \
  -p 80:80 \
  -v /data/volcengine:/app/data \
  --env-file .env.production \
  --restart unless-stopped \
  volcengine-fullstack:latest
```

### 使用 HTTPS（推荐使用反向代理）

前面加一层 Nginx 或 Caddy：

```nginx
# /etc/nginx/sites-available/volcengine
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

或使用 Caddy（自动 HTTPS）：

```
your-domain.com {
    reverse_proxy localhost:3000
}
```

## 📊 验证部署

```bash
# 检查容器状态
docker ps

# 检查健康状态
curl http://localhost:3000/health

# 应返回类似：
# {"status":"healthy","version":"1.0.0","volcengine_configured":false}
```

## 🔧 管理命令

```bash
# 查看日志
docker logs volcengine-app

# 重启容器
docker restart volcengine-app

# 停止容器
docker stop volcengine-app

# 删除容器
docker rm volcengine-app

# 进入容器调试
docker exec -it volcengine-app bash

# 查看进程状态（在容器内）
docker exec volcengine-app supervisorctl status
```

## 🆙 更新应用

```bash
# 1. 拉取最新代码
git pull

# 2. 停止旧容器
docker stop volcengine-app
docker rm volcengine-app

# 3. 重新构建和启动
./scripts/start-fullstack.sh
```

## 🐳 Docker Hub 部署（如果镜像已发布）

如果您的镜像已发布到 Docker Hub 或其他镜像仓库：

```bash
# 1. 拉取镜像
docker pull your-username/volcengine-fullstack:latest

# 2. 运行
docker run -d \
  --name volcengine-app \
  -p 3000:80 \
  -v /data/volcengine:/app/data \
  --env-file .env \
  --restart unless-stopped \
  your-username/volcengine-fullstack:latest
```

## 💾 数据持久化

重要：始终挂载数据目录以保存生成的图片：

```bash
-v /your/data/path:/app/data
```

推荐的目录结构：

```
/data/volcengine/
├── output/          # 生成的图片
└── history.json     # 历史记录（如果使用）
```

## 🔒 安全建议

生产环境部署清单：

- ✅ 使用 `.env` 文件管理敏感信息
- ✅ 不要在镜像中硬编码凭证
- ✅ 使用 HTTPS（通过反向代理）
- ✅ 配置防火墙规则
- ✅ 定期更新镜像
- ✅ 设置资源限制（内存、CPU）
- ✅ 配置日志轮转

资源限制示例：

```bash
docker run -d \
  --name volcengine-app \
  --memory="1g" \
  --cpus="1.0" \
  -p 3000:80 \
  volcengine-fullstack:latest
```

## 📈 监控

### 健康检查

Docker 会自动进行健康检查，您也可以手动检查：

```bash
# 检查容器健康
docker inspect volcengine-app | grep -A 10 Health

# 手动测试健康端点
curl http://localhost:3000/health
```

### 资源监控

```bash
# 查看资源使用
docker stats volcengine-app

# 持续监控
watch docker stats volcengine-app
```

### 日志监控

```bash
# 实时查看所有日志
docker logs -f volcengine-app

# 只看最近 100 行
docker logs --tail 100 volcengine-app

# 查看特定服务日志
docker exec volcengine-app tail -f /var/log/supervisor/uvicorn.log
docker exec volcengine-app tail -f /var/log/supervisor/nginx.log
```

## 🐛 常见问题

### 容器启动失败

```bash
# 查看详细日志
docker logs volcengine-app

# 检查配置
docker exec volcengine-app supervisorctl status
```

### 端口冲突

如果 3000 端口已被占用：

```bash
# 使用其他端口
docker run -d --name volcengine-app -p 8080:80 volcengine-fullstack:latest
```

### 内存不足

```bash
# 检查内存使用
docker stats volcengine-app

# 增加内存限制
docker update --memory="2g" volcengine-app
```

## 📚 更多信息

- [完整文档](README.fullstack.md) - 全栈单镜像详细文档
- [主文档](README.md) - 项目完整介绍
- [开发指南](README.md#开发指南) - 本地开发说明

---

**享受简单的部署体验！** 🎉
