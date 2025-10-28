# 🎨 Volcengine 图像生成器

一个完整且可用于生产环境的 Docker 应用，基于火山引擎视觉智能 API 实现 AI 图像生成。你可以通过文字描述创建令人惊艳的图像，也可以利用先进的 AI 技术对现有图片进行转换。

![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![Python](https://img.shields.io/badge/Python-3.11-green)
![Vue](https://img.shields.io/badge/Vue-3.5-brightgreen)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-teal)

## ✨ 功能亮点

### 🖼️ 文生图
- 根据详细的文本提示词生成图像
- 支持反向提示词排除不想要的元素
- 内置多种风格预设（动漫、摄影、数字艺术等）
- 支持批量生成（单次最多 4 张）
- 提供尺寸、步数、CFG scale、随机种子等自定义参数

### 🎨 图生图
- 对现有图片进行 AI 转换
- 可调节转换强度
- 支持风格迁移
- 拥有与文生图同样强大的控制项

### 📚 历史记录管理
- 浏览所有生成过的图片
- 查看生成所用参数
- 支持单张或批量下载
- 一键复制提示词方便复用

### 💎 精美界面
- 采用 Vue 3 与 Element Plus 构建的现代化响应式界面
- 深色主题，适合视觉创作
- 流畅的动画与过渡效果
- 实时监控任务进度

## 🏗️ 架构

```
┌─────────────────────────────────────────────────┐
│              Nginx（端口 3000）                 │
│         静态资源 + 反向代理                     │
└──────────────┬──────────────────────────────────┘
               │
       ┌───────┴────────┐
       │                │
┌──────▼─────┐   ┌─────▼──────┐
│  前端应用  │   │   后端服务 │
│  (Vue 3)   │   │  (FastAPI) │
│            │   │  端口 8000 │
└────────────┘   └─────┬──────┘
                       │
                ┌──────▼──────────┐
                │  火山引擎 API   │
                │   图像服务      │
                └─────────────────┘
```

## 📋 前置条件

- Docker 20.10+
- Docker Compose 2.0+
- 拥有火山引擎账号并开通视觉智能 API（若使用 Demo 模式可选）

## 🎯 部署方式选择

本项目提供两种部署方式：

| 方式 | 特点 | 适用场景 |
|------|------|---------|
| **全栈单镜像** 🆕 | ⭐ 最简单，一个容器运行 | 个人项目、开发测试、快速部署 |
| **分离式架构** | 可扩展，前后端独立 | 生产环境、大规模应用 |

👉 **新手推荐**：使用全栈单镜像，只需一条命令即可启动！  
📖 详细对比：[部署方式选择指南](DEPLOYMENT_OPTIONS.md)

## 🚀 快速开始

> **📦 新增：全栈单镜像版本** - 如果您想要最简单的部署方式，只运行一个镜像就能使用完整应用，请查看 [全栈单镜像文档](README.fullstack.md) 或直接使用：
> ```bash
> ./scripts/start-fullstack.sh
> ```

### 方式一：全栈单镜像（推荐，最简单）

1. **克隆仓库并配置**
```bash
git clone <repository-url>
cd volcengine-image-generator
cp .env.example .env
# 编辑 .env 填入凭证（可选）
```

2. **一键启动**
```bash
./scripts/start-fullstack.sh
```

3. **访问应用**
```
http://localhost:3000
```

✅ 优点：只需一个容器，部署最简单  
📖 详细文档：[README.fullstack.md](README.fullstack.md)

---

### 方式二：分离式架构（适合生产环境扩展）

### 1. 克隆仓库

```bash
git clone <repository-url>
cd volcengine-image-generator
```

### 2. 配置环境

```bash
cp .env.example .env
```

编辑 `.env`，填入火山引擎凭证（可选，没有凭证将以 Demo 模式运行）：

```env
VOLCENGINE_ACCESS_KEY=your_access_key_here
VOLCENGINE_SECRET_KEY=your_secret_key_here
VOLCENGINE_REGION=cn-beijing
```

**提示：** 如果未提供凭证，应用会进入 Demo 模式，使用占位图像进行演示。

### 3. 启动应用

```bash
docker-compose up -d
```

该命令将会：
- 构建后端服务（FastAPI）
- 构建前端服务（Vue 3）
- 配置 Nginx 反向代理
- 启动全部服务

### 4. 访问应用

在浏览器中打开：

```
http://localhost:3000
```

### 5. Docker 辅助脚本

仓库在 `scripts/` 目录下提供了一组常用的 Docker 脚本，方便本地构建、测试与清理：

| 脚本 | 功能 |
|------|------|
| `./scripts/start-fullstack.sh` | 🆕 构建并启动全栈单镜像版本（推荐）。 |
| `./scripts/test-fullstack.sh` | 🆕 测试全栈单镜像的构建和运行。 |
| `./scripts/build.sh` | 构建前后端分离镜像（使用最新的 Docker Compose 命令自动兼容 V1/V2）。 |
| `./scripts/build-simple.sh` | 使用缓存快速构建镜像，适合增量调试。 |
| `./scripts/test-build.sh` | 端到端测试构建流程：构建镜像、启动容器并进行健康检查，结束后自动清理。 |
| `./scripts/start.sh` | 构建并以后台方式启动所有服务（分离式架构）。 |
| `./scripts/clean.sh` | 交互式清理容器、镜像、数据卷与无用资源。 |

> 脚本会优先使用 `docker-compose`，若系统仅安装 Docker Compose V2 (`docker compose`)，也会自动适配。

### 6. 开发模式（热更新）

如果希望在本地开发时启用热更新，可使用提供的 `docker-compose.dev.yml`：

```bash
# 启动开发模式（会挂载代码目录并开启后端热重载）
DOCKER_COMPOSE="docker compose"  # 或 docker-compose
$DOCKER_COMPOSE -f docker-compose.dev.yml up --build
```

该配置会：

- 挂载 `backend/app` 代码目录，实现 FastAPI 热重载。
- 使用与生产相同的构建流程，确保环境一致性。
- 共享 `backend-cache` 卷，避免重复下载依赖。
## 📖 使用指南

### 文生图

1. 进入 **Text to Image** 页面
2. 输入提示词（例如：“夕阳下宁静的山间湖泊”）
3. 选择性填写反向提示词（例如：“模糊，低质量”）
4. 调整参数：
   - **Width/Height**：图像尺寸（64-2048 像素）
   - **Steps**：采样步数（10-100，数值越高质量越好）
   - **CFG Scale**：提示词约束力度（1-20，越高越贴合提示词）
   - **Seed**：随机种子（-1 表示随机）
   - **Style Preset**：选择艺术风格
   - **Number of Images**：生成 1-4 张图片
5. 点击 **Generate Image**
6. 等待处理完成（通常 10-30 秒）
7. 下载或查看生成结果

### 图生图

1. 进入 **Image to Image** 页面
2. 上传图片（拖拽或点击上传）
3. 输入转换提示词
4. 调整 **Strength**（0-1，数值越高变化越大）
5. 根据需要调整其他参数
6. 点击 **Transform Image**

### 历史记录

1. 打开 **History** 页面
2. 浏览所有生成的图片
3. 点击图片可查看大图
4. 复制提示词或下载图片

## 🔧 配置

### 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `VOLCENGINE_ACCESS_KEY` | 火山引擎 Access Key | - |
| `VOLCENGINE_SECRET_KEY` | 火山引擎 Secret Key | - |
| `VOLCENGINE_REGION` | API 区域 | `cn-beijing` |
| `DEFAULT_WIDTH` | 默认图像宽度 | `512` |
| `DEFAULT_HEIGHT` | 默认图像高度 | `512` |
| `DEFAULT_STEPS` | 默认采样步数 | `20` |
| `MAX_BATCH_SIZE` | 单次请求的最大图像数量 | `4` |
| `MAX_HISTORY_SIZE` | 历史记录上限 | `1000` |

### 自定义端口

编辑 `docker-compose.yml` 调整端口：

```yaml
services:
  frontend:
    ports:
      - "8080:80"  # 将 8080 替换为你希望暴露的端口
```

## 🛠️ 开发指南

### 后端开发

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API 将运行在 `http://localhost:8000`

API 文档地址：`http://localhost:8000/docs`

### 前端开发

```bash
cd frontend
npm install
npm run dev
```

前端运行地址：`http://localhost:5173`

## 📚 API 文档

后端启动后可访问：

- Swagger UI：`http://localhost:8000/docs`
- ReDoc：`http://localhost:8000/redoc`

### 核心端点

- `POST /api/v1/generate/text2image` - 根据文本生成图像
- `POST /api/v1/generate/image2image` - 基于图像进行转换
- `GET /api/v1/tasks/{task_id}` - 查询任务状态
- `GET /api/v1/tasks/history` - 获取生成历史
- `GET /health` - 健康检查

## 📦 项目结构

```
volcengine-image-generator/
├── backend/                  # FastAPI 后端
│   ├── app/
│   │   ├── main.py          # 应用入口
│   │   ├── config.py        # 配置管理
│   │   ├── schemas.py       # 数据模型
│   │   ├── routers/         # API 路由
│   │   ├── services/        # 业务逻辑
│   │   └── utils/           # 工具函数
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/                 # Vue 3 前端
│   ├── src/
│   │   ├── views/           # 页面
│   │   ├── components/      # Vue 组件
│   │   ├── api/             # API 客户端
│   │   └── styles/          # 样式
│   ├── Dockerfile
│   └── package.json
├── nginx/                    # Nginx 配置
│   ├── Dockerfile
│   └── nginx.conf
├── docs/                     # 文档
│   └── RESEARCH_PLAN.md     # 技术方案
├── docker-compose.yml        # Docker 编排
├── .env.example             # 环境变量模板
└── README.md
```

## 🔒 安全注意事项

- 切勿提交包含真实凭证的 `.env` 文件
- 生产环境务必启用 HTTPS
- 公网部署建议开启限流
- 在生产环境配置合适的 CORS 白名单
- 多用户场景建议增加身份认证

## 🚀 部署

### 使用已发布的 Docker 镜像（推荐）

我们通过 GitHub Actions 自动构建并发布 Docker 镜像到 GitHub Container Registry。

```bash
# 1. 下载最新版本的 docker-compose 配置
curl -O https://github.com/<your-username>/<your-repo>/releases/latest/download/docker-compose.release.yml
mv docker-compose.release.yml docker-compose.yml

# 2. 下载环境变量模板
curl -O https://github.com/<your-username>/<your-repo>/releases/latest/download/.env.example
mv .env.example .env

# 3. 编辑 .env 文件，填入火山引擎凭证（可选）
nano .env

# 4. 启动服务
docker-compose up -d
```

查看所有可用版本：[Releases](https://github.com/<your-username>/<your-repo>/releases)

### 从源码构建部署

1. 准备一台安装了 Docker 与 Docker Compose 的服务器
2. 克隆仓库
3. 配置生产环境变量
4. 使用生产环境 `.env` 文件
5. 通过 Let's Encrypt 配置 SSL/TLS
6. 设置防火墙规则
7. 启动服务：

```bash
docker-compose up -d
```

### 扩展能力

面向高并发场景的建议：
- 使用 Kubernetes 进行编排
- 引入 Redis 作为任务队列
- 后端服务水平扩展
- 静态资源接入 CDN
- 配置负载均衡

## 🐛 故障排查

### 无法生成图像

1. 检查火山引擎凭证是否正确
2. 确认 API 配额是否充足
3. 查看后端日志：`docker-compose logs backend`

### 前端无法访问

1. 检查后端服务状态：`docker-compose ps`
2. 核实 Nginx 配置
3. 查看前端日志：`docker-compose logs frontend`

### 端口冲突

当 3000 或 8000 端口已被占用时：

```bash
docker-compose down
# 修改 docker-compose.yml 中的端口
 docker-compose up -d
```

## 📄 许可证

本项目按“现状”提供，可用于教学与商业用途。

## 🙏 致谢

- [Volcengine](https://www.volcengine.com/) 提供强大的图像生成 API
- [FastAPI](https://fastapi.tiangolo.com/) 带来优秀的后端框架体验
- [Vue.js](https://vuejs.org/) 提供渐进式前端框架
- [Element Plus](https://element-plus.org/) 带来优雅的 UI 组件

## 📞 支持

如需寻求支持或参与贡献：
- 在 GitHub 上提交 Issue
- 查阅 [调研方案](docs/RESEARCH_PLAN.md) 获取更多技术细节
- 查看后端 `/docs` 端点的 API 文档

## 📦 发布与 CI/CD

本项目使用 GitHub Actions 自动化构建和发布流程：

- 📖 [发布指南](RELEASE_GUIDE.md) - 详细的版本发布步骤
- 🔧 [GitHub Actions 工作流文档](.github/workflows/README.md) - 工作流技术细节
- 🏷️ [查看所有发布版本](https://github.com/<your-username>/<your-repo>/releases)

**发布新版本**：
```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

## 🎉 贡献指南

欢迎任何形式的贡献！请按照以下流程：
1. Fork 仓库
2. 创建功能分支
3. 完成修改
4. 提交 Pull Request

---

**怀着对 AI 艺术社区的热爱而构建 ❤️**
