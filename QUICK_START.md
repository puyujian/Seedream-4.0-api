# 快速开始 - 使用发布的 Docker 镜像

只需 4 步即可运行 Volcengine 图像生成器！

## 🚀 快速启动（5 分钟）

### 步骤 1：下载配置文件

```bash
# 创建项目目录
mkdir volcengine-app && cd volcengine-app

# 下载 docker-compose 配置（替换 <your-username> 和 <your-repo>）
curl -O https://github.com/<your-username>/<your-repo>/releases/latest/download/docker-compose.release.yml
mv docker-compose.release.yml docker-compose.yml

# 下载环境变量模板
curl -O https://github.com/<your-username>/<your-repo>/releases/latest/download/.env.example
mv .env.example .env
```

### 步骤 2：配置环境变量（可选）

编辑 `.env` 文件：

```bash
nano .env
```

填入你的火山引擎凭证（如果没有，应用会以 Demo 模式运行）：

```env
VOLCENGINE_ACCESS_KEY=your_access_key_here
VOLCENGINE_SECRET_KEY=your_secret_key_here
VOLCENGINE_REGION=cn-beijing
```

### 步骤 3：启动应用

```bash
docker-compose up -d
```

### 步骤 4：访问应用

打开浏览器访问：

```
http://localhost:3000
```

🎉 完成！开始生成图像吧！

## 📝 常用命令

```bash
# 查看日志
docker-compose logs -f

# 查看服务状态
docker-compose ps

# 停止服务
docker-compose stop

# 启动服务
docker-compose start

# 重启服务
docker-compose restart

# 停止并删除容器
docker-compose down

# 更新到最新版本
docker-compose pull
docker-compose up -d
```

## 🔧 端口配置

默认端口：
- **前端**：3000
- **后端 API**：8000

如需修改，编辑 `docker-compose.yml` 的 `ports` 部分：

```yaml
services:
  frontend:
    ports:
      - "8080:80"  # 修改为其他端口
```

## 📦 选择特定版本

默认使用最新版本 (`latest`)。要使用特定版本：

```bash
# 下载特定版本的配置文件
curl -O https://github.com/<your-username>/<your-repo>/releases/download/v1.0.0/docker-compose.release.yml
```

或者手动编辑 `docker-compose.yml`，将 `latest` 改为具体版本号：

```yaml
services:
  backend:
    image: ghcr.io/<your-username>/<your-repo>-backend:1.0.0  # 指定版本
  frontend:
    image: ghcr.io/<your-username>/<your-repo>-frontend:1.0.0  # 指定版本
```

## 🐛 故障排查

### 端口被占用

如果 3000 或 8000 端口已被使用：

```bash
# 检查端口占用
sudo lsof -i :3000
sudo lsof -i :8000

# 停止冲突的服务或修改 docker-compose.yml 中的端口
```

### 无法拉取镜像

如果镜像是私有的，需要先登录：

```bash
# 创建 GitHub Personal Access Token (with read:packages permission)
# 然后登录
echo $GITHUB_TOKEN | docker login ghcr.io -u <your-username> --password-stdin
```

### 查看详细日志

```bash
# 查看所有服务日志
docker-compose logs

# 查看特定服务日志
docker-compose logs backend
docker-compose logs frontend

# 实时跟踪日志
docker-compose logs -f --tail=100
```

## 📖 更多信息

- [完整文档](README.md)
- [发布指南](RELEASE_GUIDE.md)
- [查看所有版本](https://github.com/<your-username>/<your-repo>/releases)
- [API 文档](http://localhost:8000/docs) (启动后访问)

## 💡 提示

1. **Demo 模式**：无需火山引擎凭证即可体验应用（使用占位图像）
2. **数据持久化**：生成的图片保存在 `./data` 目录
3. **备份数据**：升级前记得备份 `./data` 目录
4. **健康检查**：服务启动后会自动进行健康检查，初次启动可能需要 1-2 分钟

---

**祝你使用愉快！如有问题，欢迎提交 Issue。** ❤️
