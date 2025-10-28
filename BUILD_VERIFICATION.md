# 构建验证清单

本文档用于验证 Docker 构建脚本和配置是否正确设置。

## ✅ 文件清单

### 新增的构建脚本

- [x] `scripts/build.sh` - 完整构建脚本（无缓存）
- [x] `scripts/build-simple.sh` - 快速构建脚本（有缓存）
- [x] `scripts/test-build.sh` - 端到端测试脚本
- [x] `scripts/clean.sh` - 资源清理脚本

### 更新的脚本

- [x] `scripts/start.sh` - 添加了 Docker Compose V1/V2 兼容性

### Docker 配置文件

- [x] `docker-compose.yml` - 生产环境配置（已优化）
- [x] `docker-compose.dev.yml` - 开发环境配置（新增）
- [x] `.dockerignore` - 根目录忽略规则（新增）
- [x] `backend/.dockerignore` - 后端忽略规则（新增）

### Dockerfile 优化

- [x] `backend/Dockerfile` - 后端镜像优化
  - 参数化 Python 版本
  - 非 root 用户运行
  - 轻量健康检查（使用 Python 标准库）
  
- [x] `nginx/Dockerfile` - 前端镜像优化
  - 多阶段构建
  - 参数化 Node.js 和 Nginx 版本
  - 优化依赖安装和缓存

### 文档

- [x] `docs/DOCKER_BUILD.md` - 详细构建指南
- [x] `DOCKER_BUILD_SUMMARY.md` - 更新总结
- [x] `BUILD_VERIFICATION.md` - 本文件
- [x] `README.md` - 更新快速开始章节

### 环境配置

- [x] `.env.example` - 环境变量模板

## 🧪 验证步骤

### 1. 脚本权限验证

所有脚本应具有执行权限：

```bash
ls -l scripts/
# 应显示 -rwxr-xr-x (可执行)
```

### 2. Docker Compose 兼容性验证

脚本应自动检测并使用正确的 Docker Compose 命令：

```bash
# 测试脚本检测
./scripts/build-simple.sh
# 应显示 "✅ Using: docker compose" 或 "✅ Using: docker-compose"
```

### 3. 构建脚本验证

#### 方式 A: 快速构建测试（推荐）

```bash
./scripts/build-simple.sh
```

**预期输出**：
- ✅ 检测到 Docker Compose
- ✅ 开始构建后端镜像
- ✅ 开始构建前端镜像
- ✅ 构建完成

#### 方式 B: 完整构建测试

```bash
./scripts/build.sh
```

**预期输出**：
- ✅ Docker 运行检查通过
- ✅ Docker Compose 版本检测
- ✅ 后端镜像构建（无缓存）
- ✅ 前端镜像构建（无缓存）
- ✅ 显示构建的镜像列表

#### 方式 C: 端到端测试（完整验证）

```bash
./scripts/test-build.sh
```

**预期流程**：
1. ✅ 调用 build.sh 构建镜像
2. ✅ 启动所有容器
3. ✅ 等待 60 秒
4. ✅ 健康检查（最多重试 10 次）
5. ✅ 验证前后端响应
6. ✅ 自动清理容器

**注意**: 由于网络连接问题，构建可能会失败。这是正常的，可以稍后重试。

### 4. 配置文件验证

#### docker-compose.yml

```bash
docker compose config
```

**预期结果**：
- 无语法错误
- 显示解析后的配置

#### 环境变量

```bash
cat .env.example
```

**预期内容**：
- VOLCENGINE_ACCESS_KEY
- VOLCENGINE_SECRET_KEY
- VOLCENGINE_REGION
- 其他应用配置

### 5. Dockerfile 验证

#### 后端 Dockerfile

```bash
docker build -t test-backend -f backend/Dockerfile ./backend
```

**预期结果**：
- ✅ 成功拉取基础镜像
- ✅ 安装 Python 依赖
- ✅ 创建非 root 用户
- ✅ 设置健康检查

#### 前端 Dockerfile

```bash
docker build -t test-frontend -f nginx/Dockerfile .
```

**预期结果**：
- ✅ 第一阶段：构建 Vue 3 应用
- ✅ 第二阶段：配置 Nginx
- ✅ 多阶段构建成功

## 🔍 常见问题检查

### 问题 1: 网络连接超时

**症状**: 构建时出现 "Temporary failure resolving"

**原因**: Docker 容器内网络连接问题

**解决方案**:
1. 检查宿主机网络连接
2. 重启 Docker 服务：`sudo systemctl restart docker`
3. 稍后重试构建

### 问题 2: 端口冲突

**症状**: 容器启动失败，提示端口已占用

**解决方案**:
```bash
# 检查端口占用
sudo lsof -i :3000
sudo lsof -i :8000

# 停止占用端口的进程或修改 docker-compose.yml 中的端口映射
```

### 问题 3: 权限问题

**症状**: 无法执行脚本或写入数据目录

**解决方案**:
```bash
# 添加执行权限
chmod +x scripts/*.sh

# 修复数据目录权限
sudo chown -R 1000:1000 backend/app/data
```

## 📊 构建成功标志

构建成功后，应看到：

### 镜像列表

```bash
docker images | grep volcengine
```

**预期输出**:
```
volcengine-backend   latest   <image-id>   <time>   ~300MB
volcengine-frontend  latest   <image-id>   <time>   ~50MB
```

### 容器状态

```bash
docker compose ps
```

**预期输出**（如果已启动）:
```
NAME                  STATUS              PORTS
volcengine-backend    Up (healthy)        0.0.0.0:8000->8000/tcp
volcengine-frontend   Up (healthy)        0.0.0.0:3000->80/tcp
```

### 健康检查

```bash
# 后端健康检查
curl http://localhost:8000/health

# 前端响应检查
curl -I http://localhost:3000
```

## ✅ 验证完成清单

完成以下检查项，确保构建配置正确：

- [ ] 所有脚本文件存在且可执行
- [ ] Docker Compose 配置文件语法正确
- [ ] Dockerfile 可以成功构建
- [ ] 脚本能正确检测 Docker Compose 版本
- [ ] 环境变量模板存在
- [ ] .dockerignore 文件配置正确
- [ ] 文档完整且易于理解

## 🎯 下一步

1. **本地开发**: 使用 `docker-compose.dev.yml` 启动开发环境
2. **生产部署**: 使用 `docker-compose.yml` 部署生产环境
3. **持续集成**: 可选择集成 GitHub Actions 自动构建

## 📝 注意事项

1. **网络依赖**: 构建过程需要稳定的网络连接（下载依赖）
2. **磁盘空间**: 确保有足够的磁盘空间（至少 2GB）
3. **Docker 版本**: 推荐使用 Docker 20.10+ 和 Docker Compose 2.0+
4. **构建时间**: 首次构建可能需要 3-5 分钟

---

**验证日期**: 2025-10-28  
**验证状态**: ✅ 配置已就绪，等待网络稳定后进行完整构建测试  
**分支**: feat/docker-build-scripts-update-compose-local-test
