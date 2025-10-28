# 🎨 火山引擎图像生成 Docker 应用

<div align="center">

[![Docker](https://img.shields.io/badge/Docker-Ready-blue?logo=docker)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-green?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-teal?logo=fastapi)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

一个功能完善、界面美观的Docker化AI图像生成应用  
基于火山引擎视觉智能API

[功能特性](#-功能特性) • [快速开始](#-快速开始) • [文档](#-文档) • [截图](#-界面预览)

</div>

---

## ✨ 功能特性

### 🖼️ 图像生成
- **文生图 (Text-to-Image)**: 通过文本描述生成精美图像
- **多模型支持**: 支持火山引擎多种AI模型
- **参数自定义**: 完整的生成参数控制（尺寸、数量、步数等）
- **批量生成**: 一次生成多张图片
- **实时进度**: 异步任务处理，实时显示生成进度

### 🎯 用户体验
- **现代化UI**: 基于Tailwind CSS的精美界面
- **响应式设计**: 完美支持PC和移动设备
- **主题切换**: 深色/浅色模式自由切换
- **快速操作**: 直观的交互流程，键盘快捷键支持
- **历史管理**: 自动保存生成历史，便于回溯

### 🛠️ 系统功能
- **一键部署**: Docker Compose 自动化部署
- **安全可靠**: API密钥加密存储，完善的错误处理
- **性能优化**: 异步处理，图片缓存，快速响应
- **监控日志**: 完整的日志记录和系统监控
- **配额管理**: API使用统计和配额展示

## 🚀 快速开始

### 前置要求

- Docker 20.x 或更高版本
- Docker Compose 2.x 或更高版本
- 火山引擎账号和API密钥 ([获取密钥](https://www.volcengine.com/docs/82379/1541523))

### 安装部署

```bash
# 1. 克隆项目
git clone <repository-url>
cd volcengine-image-generator

# 2. 配置环境变量
cp .env.example .env

# 编辑 .env 文件，填入你的火山引擎API密钥
# VOLC_ACCESS_KEY=你的AccessKey
# VOLC_SECRET_KEY=你的SecretKey

# 3. 启动应用
docker-compose up -d

# 4. 访问应用
# 浏览器打开 http://localhost:8080
```

就这么简单！🎉

### 验证安装

```bash
# 查看容器状态
docker-compose ps

# 查看日志
docker-compose logs -f

# 健康检查
curl http://localhost:8080/api/v1/health
```

## 📖 使用指南

### 基本操作

1. **输入提示词**: 在左侧面板输入你想生成的图像描述
2. **选择参数**: 设置模型、尺寸、数量等参数
3. **点击生成**: 点击"生成图像"按钮
4. **查看结果**: 中间面板会实时显示生成的图片
5. **下载保存**: 点击图片下方的下载按钮保存到本地

### 高级功能

#### 参数说明

| 参数 | 说明 | 推荐值 |
|------|------|--------|
| **提示词 (Prompt)** | 描述想要生成的图像内容 | 详细、具体的描述 |
| **负面提示词** | 不想在图像中出现的内容 | 质量差、模糊等 |
| **模型** | 使用的AI模型 | general_v2.0 (通用) |
| **尺寸** | 图像分辨率 | 1024x1024 |
| **生成数量** | 一次生成的图片数 | 1-4 |
| **采样步数** | 生成迭代次数 | 20-50 |
| **引导系数** | 遵循提示词的程度 | 7-12 |
| **随机种子** | 用于复现结果 | 留空自动生成 |

#### 提示词技巧

```
✅ 好的提示词：
"一只可爱的橘猫坐在木质窗台上，阳光透过窗户洒在它身上，柔和的光影，电影级质感，高清细节，温馨氛围"

❌ 不好的提示词：
"猫"
```

**提示词公式**: `主体 + 细节 + 环境 + 风格 + 质量词`

#### 快捷键

- `Ctrl + Enter`: 快速生成
- `Ctrl + S`: 下载当前选中图片
- `Ctrl + H`: 查看历史记录
- `T`: 切换主题

## 🏗️ 架构说明

### 技术栈

**后端**
- FastAPI 0.104+ - 高性能Web框架
- Python 3.11+ - 核心语言
- SQLAlchemy - ORM框架
- volcengine-python-sdk - 官方SDK

**前端**
- HTML5 + Tailwind CSS - 界面框架
- Alpine.js - 轻量级JS框架
- Heroicons - 图标库

**基础设施**
- Docker + Docker Compose - 容器化
- Nginx - 反向代理
- SQLite - 轻量级数据库

### 项目结构

```
.
├── backend/              # 后端服务
│   ├── app/             # 应用代码
│   │   ├── api/         # API路由
│   │   ├── services/    # 业务逻辑
│   │   ├── models/      # 数据模型
│   │   └── utils/       # 工具函数
│   ├── data/            # 数据存储（挂载）
│   └── requirements.txt # Python依赖
├── frontend/            # 前端资源
│   ├── static/         # 静态资源
│   └── templates/      # HTML模板
├── docker-compose.yml  # Docker编排
├── .env.example        # 环境变量模板
└── README.md           # 本文档
```

### API文档

应用启动后，访问以下地址查看完整API文档：

- **Swagger UI**: http://localhost:8080/docs
- **ReDoc**: http://localhost:8080/redoc

主要端点：

- `POST /api/v1/generate` - 创建图像生成任务
- `GET /api/v1/task/{task_id}` - 查询任务状态
- `GET /api/v1/history` - 获取历史记录
- `GET /api/v1/images/{image_id}` - 下载图片

## ⚙️ 配置说明

### 环境变量

```bash
# ============ 火山引擎配置 ============
VOLC_ACCESS_KEY=your-access-key-here      # 必填
VOLC_SECRET_KEY=your-secret-key-here      # 必填
VOLC_REGION=cn-beijing                    # 区域

# ============ 应用配置 ============
APP_NAME=VolcEngine Image Generator
APP_PORT=8080                              # 对外端口
APP_DEBUG=false                            # 调试模式
APP_LOG_LEVEL=INFO                         # 日志级别

# ============ 存储配置 ============
DATA_DIR=./data                            # 数据目录
MAX_HISTORY_DAYS=30                        # 历史保留天数
MAX_STORAGE_GB=100                         # 最大存储空间

# ============ 安全配置 ============
SECRET_KEY=change-this-to-a-random-secret  # 应用密钥
ALLOWED_ORIGINS=*                          # CORS配置

# ============ 性能配置 ============
MAX_CONCURRENT_TASKS=5                     # 最大并发任务
REQUEST_TIMEOUT=300                        # 请求超时（秒）
```

### Docker Compose 配置

```yaml
# 开发环境
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

# 生产环境
docker-compose up -d

# 自定义端口
APP_PORT=9000 docker-compose up -d
```

## 🔧 开发指南

### 本地开发

```bash
# 1. 克隆项目
git clone <repository-url>
cd volcengine-image-generator

# 2. 安装Python依赖
cd backend
pip install -r requirements.txt

# 3. 配置环境变量
cp .env.example .env

# 4. 启动后端服务
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 5. 访问前端
# 打开 frontend/templates/index.html
```

### 代码规范

```bash
# 格式化代码
black backend/

# 代码检查
flake8 backend/

# 类型检查
mypy backend/
```

### 测试

```bash
# 运行测试
pytest backend/tests/

# 测试覆盖率
pytest --cov=backend/app backend/tests/
```

## 🐛 故障排查

### 常见问题

**问题 1: 容器启动失败**
```bash
# 检查日志
docker-compose logs backend

# 常见原因：
# - 端口被占用：修改 .env 中的 APP_PORT
# - 环境变量未配置：检查 .env 文件
```

**问题 2: API调用失败**
```bash
# 检查API密钥
docker-compose exec backend env | grep VOLC

# 测试连接
curl http://localhost:8080/api/v1/system/info
```

**问题 3: 图片生成失败**
```bash
# 查看详细错误
docker-compose logs -f backend

# 常见原因：
# - API配额不足
# - 提示词包含敏感内容
# - 网络连接问题
```

### 日志查看

```bash
# 实时日志
docker-compose logs -f

# 只看后端日志
docker-compose logs -f backend

# 最近100行
docker-compose logs --tail=100 backend
```

### 数据备份

```bash
# 备份数据库和图片
tar -czf backup.tar.gz data/

# 恢复数据
tar -xzf backup.tar.gz
```

## 📊 性能优化

### 建议配置

**小规模使用** (个人/小团队)
- CPU: 2核
- 内存: 2GB
- 存储: 20GB
- 并发: 3

**中等规模使用** (团队/部门)
- CPU: 4核
- 内存: 4GB
- 存储: 100GB
- 并发: 10

### 优化建议

1. **启用缓存**: 配置Redis缓存热点数据
2. **CDN加速**: 将图片存储到OSS+CDN
3. **负载均衡**: 部署多个后端实例
4. **数据库升级**: 大量数据时升级到PostgreSQL

## 🔐 安全建议

1. **保护API密钥**: 不要将 `.env` 提交到代码库
2. **使用HTTPS**: 生产环境配置SSL证书
3. **限制访问**: 配置防火墙规则
4. **定期更新**: 及时更新依赖包
5. **监控告警**: 配置异常监控和告警

## 📚 相关文档

- [火山引擎文档 - 视觉智能](https://www.volcengine.com/docs/82379/1541523)
- [火山引擎文档 - API参考](https://www.volcengine.com/docs/82379/1824121)
- [FastAPI文档](https://fastapi.tiangolo.com/)
- [Docker文档](https://docs.docker.com/)
- [技术方案详情](PROPOSAL.md)

## 🤝 贡献

欢迎贡献！请遵循以下步骤：

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

- 感谢 [火山引擎](https://www.volcengine.com/) 提供强大的AI服务
- 感谢所有开源项目的贡献者

## 📮 联系方式

- 提交Issue: [GitHub Issues](../../issues)
- 项目主页: [GitHub Repository](../../)

---

<div align="center">

**⭐ 如果这个项目对你有帮助，请给我一个星标！⭐**

Made with ❤️ by AI Assistant

</div>
