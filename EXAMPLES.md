# 💡 使用示例

本文档提供各种场景下的使用示例。

## 🚀 快速开始示例

### 示例 1：最快启动（全栈单镜像）

```bash
# 克隆项目
git clone https://github.com/your-username/volcengine-image-generator.git
cd volcengine-image-generator

# 一键启动
./scripts/start-fullstack.sh

# 等待启动完成后访问
# 打开浏览器：http://localhost:3000
```

就这么简单！🎉

### 示例 2：使用环境变量（生产模式）

```bash
# 创建环境变量文件
cat > .env <<EOF
VOLCENGINE_ACCESS_KEY=your_actual_access_key
VOLCENGINE_SECRET_KEY=your_actual_secret_key
VOLCENGINE_REGION=cn-beijing
EOF

# 启动（会自动读取 .env）
./scripts/start-fullstack.sh
```

### 示例 3：自定义端口

```bash
# 编辑 docker-compose.fullstack.yml，修改端口映射
# ports:
#   - "8080:80"  # 改为 8080

# 启动
docker-compose -f docker-compose.fullstack.yml up -d

# 访问 http://localhost:8080
```

## 🐳 Docker 命令示例

### 示例 4：使用纯 Docker 命令

```bash
# 构建镜像
docker build -f Dockerfile.fullstack -t volcengine-app:v1.0 .

# 运行容器
docker run -d \
  --name my-volcengine-app \
  -p 3000:80 \
  -v $(pwd)/data:/app/data \
  --restart unless-stopped \
  volcengine-app:v1.0

# 查看日志
docker logs -f my-volcengine-app
```

### 示例 5：带环境变量的运行

```bash
docker run -d \
  --name volcengine-app \
  -p 3000:80 \
  -e VOLCENGINE_ACCESS_KEY="your_key" \
  -e VOLCENGINE_SECRET_KEY="your_secret" \
  -e VOLCENGINE_REGION="cn-beijing" \
  -v $(pwd)/data:/app/data \
  volcengine-fullstack:latest
```

### 示例 6：限制资源使用

```bash
docker run -d \
  --name volcengine-app \
  -p 3000:80 \
  --memory="1g" \
  --cpus="1.0" \
  -v $(pwd)/data:/app/data \
  volcengine-fullstack:latest
```

## 🔧 管理操作示例

### 示例 7：查看和管理日志

```bash
# 查看所有日志
docker logs volcengine-app

# 实时跟踪日志
docker logs -f volcengine-app

# 只看最近 50 行
docker logs --tail 50 volcengine-app

# 查看带时间戳的日志
docker logs -t volcengine-app

# 查看后端日志（在容器内）
docker exec volcengine-app tail -f /var/log/supervisor/uvicorn.log

# 查看 Nginx 日志
docker exec volcengine-app tail -f /var/log/nginx/access.log
```

### 示例 8：进入容器调试

```bash
# 进入容器 shell
docker exec -it volcengine-app bash

# 在容器内检查进程
docker exec volcengine-app ps aux

# 检查服务状态
docker exec volcengine-app supervisorctl status

# 重启后端服务
docker exec volcengine-app supervisorctl restart uvicorn

# 重启 Nginx
docker exec volcengine-app supervisorctl restart nginx

# 测试后端 API
docker exec volcengine-app curl http://localhost:8000/health

# 查看端口监听
docker exec volcengine-app netstat -tlnp
```

### 示例 9：备份和恢复数据

```bash
# 备份生成的图片
docker cp volcengine-app:/app/data/output ./backup-$(date +%Y%m%d)

# 或使用挂载的目录
tar -czf backup-$(date +%Y%m%d).tar.gz ./backend/app/data

# 恢复数据
tar -xzf backup-20240101.tar.gz
# 然后重启容器，数据会自动加载
```

## 🌐 生产环境示例

### 示例 10：使用 Systemd 管理（Linux）

创建 systemd 服务文件：

```bash
# /etc/systemd/system/volcengine.service
cat > /etc/systemd/system/volcengine.service <<EOF
[Unit]
Description=Volcengine Image Generator
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/volcengine-image-generator
ExecStart=/usr/bin/docker-compose -f docker-compose.fullstack.yml up -d
ExecStop=/usr/bin/docker-compose -f docker-compose.fullstack.yml down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
EOF

# 启用服务
sudo systemctl enable volcengine
sudo systemctl start volcengine

# 查看状态
sudo systemctl status volcengine

# 查看日志
sudo journalctl -u volcengine -f
```

### 示例 11：使用 Nginx 反向代理 + HTTPS

```nginx
# /etc/nginx/sites-available/volcengine
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;
    
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    client_max_body_size 20M;
    
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # 超时设置（图像生成可能需要较长时间）
        proxy_connect_timeout 300;
        proxy_send_timeout 300;
        proxy_read_timeout 300;
    }
}
```

启用配置：

```bash
# 启用站点
sudo ln -s /etc/nginx/sites-available/volcengine /etc/nginx/sites-enabled/

# 测试配置
sudo nginx -t

# 重载 Nginx
sudo systemctl reload nginx
```

### 示例 12：使用 Caddy（自动 HTTPS）

```bash
# 安装 Caddy
# Ubuntu/Debian
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
sudo apt update
sudo apt install caddy

# 创建 Caddyfile
cat > /etc/caddy/Caddyfile <<EOF
your-domain.com {
    reverse_proxy localhost:3000
    
    # 可选：请求大小限制
    request_body {
        max_size 20MB
    }
    
    # 可选：超时设置
    header_up X-Forwarded-Proto {scheme}
}
EOF

# 重启 Caddy
sudo systemctl restart caddy
```

Caddy 会自动获取和更新 HTTPS 证书！

### 示例 13：Docker Swarm 部署

```bash
# 初始化 Swarm
docker swarm init

# 创建 overlay 网络
docker network create --driver overlay volcengine-net

# 部署栈
docker stack deploy -c docker-compose.fullstack.yml volcengine

# 查看服务
docker service ls

# 查看服务日志
docker service logs -f volcengine_app

# 扩展服务（注意：全栈镜像不建议直接扩展多副本，因为数据存储）
# 如需扩展，应使用分离式架构
```

### 示例 14：使用外部数据库（未来扩展）

如果将来添加数据库支持，可以这样配置：

```yaml
# docker-compose.fullstack.yml
services:
  app:
    # ... 现有配置
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres:5432/volcengine
    depends_on:
      - postgres
  
  postgres:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=volcengine
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password

volumes:
  postgres_data:
```

## 📊 监控示例

### 示例 15：健康检查脚本

```bash
#!/bin/bash
# health-check.sh

# 检查容器状态
if ! docker ps | grep -q volcengine-app; then
    echo "ERROR: Container is not running"
    exit 1
fi

# 检查健康端点
HTTP_CODE=$(curl -o /dev/null -s -w "%{http_code}" http://localhost:3000/health)
if [ "$HTTP_CODE" != "200" ]; then
    echo "ERROR: Health check failed with HTTP $HTTP_CODE"
    exit 1
fi

echo "OK: Service is healthy"
exit 0
```

### 示例 16：资源监控脚本

```bash
#!/bin/bash
# monitor.sh

while true; do
    clear
    echo "=== Volcengine Container Monitor ==="
    echo ""
    echo "--- Container Stats ---"
    docker stats volcengine-app --no-stream
    echo ""
    echo "--- Service Status ---"
    docker exec volcengine-app supervisorctl status
    echo ""
    echo "--- Disk Usage ---"
    du -sh ./backend/app/data/output 2>/dev/null || echo "No data yet"
    echo ""
    sleep 5
done
```

### 示例 17：日志轮转

```bash
# 配置 Docker 日志轮转
# 编辑 /etc/docker/daemon.json

cat > /etc/docker/daemon.json <<EOF
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
EOF

# 重启 Docker
sudo systemctl restart docker
```

## 🧪 测试示例

### 示例 18：API 测试

```bash
# 测试健康端点
curl http://localhost:3000/health

# 测试文生图 API
curl -X POST http://localhost:3000/api/v1/generate/text2image \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "a beautiful sunset over mountains",
    "width": 512,
    "height": 512,
    "steps": 20
  }'

# 查看生成历史
curl http://localhost:3000/api/v1/tasks/history
```

### 示例 19：自动化测试脚本

```bash
#!/bin/bash
# test-api.sh

BASE_URL="http://localhost:3000"

echo "Testing health endpoint..."
curl -f $BASE_URL/health || exit 1
echo "✅ Health check passed"

echo ""
echo "Testing text2image API..."
RESPONSE=$(curl -s -X POST $BASE_URL/api/v1/generate/text2image \
  -H "Content-Type: application/json" \
  -d '{"prompt":"test","width":256,"height":256}')

TASK_ID=$(echo $RESPONSE | jq -r '.task_id')
echo "Task ID: $TASK_ID"

if [ "$TASK_ID" != "null" ]; then
    echo "✅ API test passed"
else
    echo "❌ API test failed"
    exit 1
fi
```

## 🔄 更新和维护示例

### 示例 20：滚动更新

```bash
# 1. 拉取最新代码
git pull

# 2. 构建新镜像（使用新标签）
docker build -f Dockerfile.fullstack -t volcengine-app:v1.1 .

# 3. 停止旧容器（保留数据）
docker stop volcengine-app
docker rename volcengine-app volcengine-app-old

# 4. 启动新容器
docker run -d \
  --name volcengine-app \
  -p 3000:80 \
  -v $(pwd)/data:/app/data \
  --restart unless-stopped \
  volcengine-app:v1.1

# 5. 测试新版本
sleep 10
curl http://localhost:3000/health

# 6. 如果成功，删除旧容器
docker rm volcengine-app-old

# 7. 如果失败，回滚
# docker stop volcengine-app
# docker rm volcengine-app
# docker rename volcengine-app-old volcengine-app
# docker start volcengine-app
```

### 示例 21：定期清理

```bash
#!/bin/bash
# cleanup.sh

# 清理旧的生成图片（保留最近 7 天）
find ./backend/app/data/output -type f -mtime +7 -delete

# 清理 Docker 未使用的资源
docker system prune -f

# 清理旧的镜像（保留最近两个版本）
docker images | grep volcengine-app | tail -n +3 | awk '{print $3}' | xargs -r docker rmi

echo "Cleanup completed"
```

## 📚 更多资源

- [快速部署指南](QUICK_DEPLOY.md)
- [架构说明](FULLSTACK_ARCHITECTURE.md)
- [部署方式选择](DEPLOYMENT_OPTIONS.md)
- [主文档](README.md)

---

**这些示例应该能覆盖大部分使用场景！** 🚀
