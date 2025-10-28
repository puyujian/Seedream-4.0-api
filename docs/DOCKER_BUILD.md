# Docker 构建与部署指南

本文档详细说明 Volcengine Image Generator 的 Docker 构建流程、优化配置与常用脚本。

## 📋 目录

- [构建脚本](#构建脚本)
- [Docker 配置说明](#docker-配置说明)
- [本地测试流程](#本地测试流程)
- [常见问题](#常见问题)

---

## 🛠️ 构建脚本

项目在 `scripts/` 目录下提供了一组常用的 Docker 脚本，支持构建、测试与清理。所有脚本自动兼容 Docker Compose V1 (`docker-compose`) 和 V2 (`docker compose`)。

### 脚本列表

| 脚本 | 用途 | 说明 |
|------|------|------|
| `build.sh` | 完整构建镜像 | 从零开始构建前后端镜像，不使用缓存（`--no-cache`），确保使用最新依赖。 |
| `build-simple.sh` | 快速构建 | 使用缓存构建镜像，适合增量调试。 |
| `test-build.sh` | 端到端测试 | 构建镜像 → 启动容器 → 健康检查 → 自动清理。适合验证构建是否正常。 |
| `start.sh` | 启动服务 | 构建镜像并以后台模式启动所有服务。自动生成 `.env` 文件（如果不存在）。 |
| `clean.sh` | 清理资源 | 交互式清理容器、镜像、数据卷与无用资源。 |

### 使用示例

#### 1. 完整构建镜像

```bash
./scripts/build.sh
```

#### 2. 快速构建（增量调试）

```bash
./scripts/build-simple.sh
```

#### 3. 端到端测试

```bash
./scripts/test-build.sh
```

测试流程：
1. 使用 `build.sh` 重新构建镜像
2. 启动所有容器
3. 等待 60 秒并进行多次健康检查
4. 验证前后端是否正常响应
5. 自动清理容器

#### 4. 启动服务

```bash
./scripts/start.sh
```

#### 5. 清理资源

```bash
./scripts/clean.sh
```

交互式地选择需要清理的资源：
- 停止并删除容器
- 删除 Volcengine 镜像
- 删除 Docker 数据卷（⚠️ 会删除持久化数据）
- 清理无用的 Docker 资源

---

## 🐳 Docker 配置说明

### 1. docker-compose.yml（生产配置）

生产环境配置文件，包含以下优化：

#### 后端服务 (Backend)

- **镜像**: `volcengine-backend:latest`
- **健康检查**: 使用 Python 标准库检测 `/health` 端点
- **重启策略**: `unless-stopped`（除非手动停止，否则自动重启）
- **网络**: 专用桥接网络 `volcengine-net`
- **数据卷**:
  - `./backend/app/data:/app/data` - 持久化任务数据
  - `backend-cache:/root/.cache` - 缓存 pip 依赖
- **用户**: 非 root 用户运行（安全性）

#### 前端服务 (Frontend)

- **镜像**: `volcengine-frontend:latest`
- **构建**: 多阶段构建（Node.js 构建 → Nginx 部署）
- **健康检查**: 检测 Nginx HTTP 响应
- **依赖**: 等待后端服务健康后再启动
- **网络**: 共享 `volcengine-net` 网络

#### 网络与数据卷

- **网络**: `volcengine-net`（bridge 模式）
- **数据卷**: `backend-cache`（缓存 Python 依赖）

### 2. docker-compose.dev.yml（开发配置）

开发环境配置文件，额外提供：

- **代码挂载**: `./backend/app:/app/app:ro`（只读挂载）
- **热重载**: 后端使用 `--reload` 参数启动 FastAPI
- **调试模式**: 设置 `DEBUG=true` 环境变量

使用方式：

```bash
docker compose -f docker-compose.dev.yml up --build
```

### 3. Dockerfile 优化

#### 后端 Dockerfile 优化点

1. **参数化 Python 版本**: 支持通过 `ARG` 自定义 Python 版本
2. **非 root 用户运行**: 提高容器安全性
3. **轻量健康检查**: 使用 Python 标准库，不依赖 curl
4. **数据卷优化**: 持久化 `/app/data`，缓存 pip 依赖

#### 前端 Dockerfile 优化点

1. **多阶段构建**: 构建阶段与运行阶段分离，减小镜像体积
2. **参数化版本**: 支持自定义 Node.js 和 Nginx 版本
3. **依赖缓存优化**: 优先复制 `package*.json`，最大化缓存利用率
4. **Nginx 优化**: 配置缓存目录并设置合适的权限

---

## 🧪 本地测试流程

### 方式 1: 使用测试脚本（推荐）

```bash
./scripts/test-build.sh
```

该脚本会自动完成：
1. 构建镜像
2. 启动容器
3. 健康检查（重试机制）
4. 清理资源

### 方式 2: 手动测试

```bash
# 1. 构建镜像
docker compose build

# 2. 启动服务
docker compose up -d

# 3. 检查容器状态
docker compose ps

# 4. 查看后端日志
docker compose logs backend

# 5. 查看前端日志
docker compose logs frontend

# 6. 测试后端健康检查
curl http://localhost:8000/health

# 7. 测试前端访问
curl http://localhost:3000

# 8. 清理资源
docker compose down
```

### 方式 3: 开发模式测试

```bash
# 启动开发模式（支持热重载）
docker compose -f docker-compose.dev.yml up --build

# 查看实时日志
docker compose -f docker-compose.dev.yml logs -f

# 停止服务
docker compose -f docker-compose.dev.yml down
```

---

## 🔧 常见问题

### 1. 网络连接超时

**问题**: 构建时出现 `Temporary failure resolving` 错误。

**解决方案**:
```bash
# 检查 Docker 网络
docker network ls

# 重启 Docker 服务
sudo systemctl restart docker

# 或重试构建
docker compose build
```

### 2. 端口冲突

**问题**: 端口 3000 或 8000 已被占用。

**解决方案**:

编辑 `docker-compose.yml`，修改端口映射：

```yaml
services:
  backend:
    ports:
      - "8001:8000"  # 改为 8001
  frontend:
    ports:
      - "3001:80"    # 改为 3001
```

### 3. 健康检查失败

**问题**: 容器启动后健康检查失败。

**排查步骤**:

```bash
# 查看容器日志
docker compose logs backend
docker compose logs frontend

# 手动测试健康端点
docker compose exec backend curl http://localhost:8000/health
docker compose exec frontend wget -O- http://localhost:80

# 进入容器排查
docker compose exec backend bash
docker compose exec frontend sh
```

### 4. 镜像体积过大

**优化方案**:

1. 使用 `.dockerignore` 排除不必要的文件
2. 多阶段构建（已应用）
3. 清理缓存：
   ```bash
   docker system prune -a
   ```

### 5. 构建缓存问题

**问题**: 修改代码后构建未生效。

**解决方案**:

```bash
# 强制重新构建（不使用缓存）
./scripts/build.sh

# 或手动指定
docker compose build --no-cache
```

### 6. 数据卷权限问题

**问题**: 容器无法写入 `/app/data`。

**解决方案**:

```bash
# 检查宿主机目录权限
ls -la backend/app/data

# 修改权限（如果需要）
sudo chown -R 1000:1000 backend/app/data
```

---

## 📊 镜像信息

构建完成后，可查看镜像信息：

```bash
# 查看所有镜像
docker images | grep volcengine

# 预期输出
# volcengine-backend   latest   <image-id>   <time>   ~300MB
# volcengine-frontend  latest   <image-id>   <time>   ~50MB
```

---

## 🚀 生产部署建议

1. **使用特定版本标签**（不要使用 `latest`）
2. **启用 HTTPS**（配置 SSL 证书）
3. **配置反向代理**（Nginx/Caddy/Traefik）
4. **设置资源限制**（`deploy.resources` 配置）
5. **配置日志管理**（ELK/Loki/CloudWatch）
6. **启用监控**（Prometheus + Grafana）
7. **定期备份数据卷**

---

## 📝 总结

本项目提供了一套完整的 Docker 构建与部署方案：

✅ **自动化脚本** - 简化构建、测试与清理流程  
✅ **优化配置** - 健康检查、重启策略、网络隔离  
✅ **多环境支持** - 生产环境与开发环境分离  
✅ **兼容性** - 支持 Docker Compose V1/V2  
✅ **安全性** - 非 root 用户、环境变量管理  

如有问题或建议，请提交 Issue 或 Pull Request。
