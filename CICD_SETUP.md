# CI/CD 设置完成

## 📦 创建的文件

本次设置创建了以下文件：

### GitHub Actions 工作流
- `.github/workflows/docker-build-and-release.yml` - 主工作流文件
- `.github/workflows/README.md` - 工作流详细文档

### 用户文档
- `RELEASE_GUIDE.md` - 发布指南（中文）
- `QUICK_START.md` - 快速开始指南
- `.env.example` - 环境变量模板

### 更新的文件
- `README.md` - 添加了 CI/CD 和发布相关说明
- `.gitignore` - 更新以包含 .env.example

## 🚀 工作流功能

### 自动化流程

当推送版本标签（如 `v1.0.0`）时，工作流会自动：

1. **构建 Docker 镜像**
   - 后端镜像（FastAPI + Python）
   - 前端镜像（Vue 3 + Nginx）

2. **推送到 GitHub Container Registry**
   - 使用语义化版本标签
   - 包含 `latest` 标签

3. **创建 GitHub Release**
   - 自动生成发布说明
   - 包含部署指南
   - 附加配置文件

4. **上传部署文件**
   - `docker-compose.release.yml` - 生产环境配置
   - `.env.example` - 环境变量模板

## 📋 使用方法

### 发布 1.0 版本

```bash
# 方法 1：使用 Git 标签（推荐）
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# 方法 2：手动触发
# 访问 GitHub Actions 页面，手动运行工作流并输入版本号 1.0.0
```

### 验证发布

1. 检查 Actions 页面查看构建状态
2. 查看 Releases 页面确认发布
3. 查看 Packages 页面确认镜像

### 部署发布的版本

```bash
# 下载配置文件
curl -O https://github.com/<your-username>/<your-repo>/releases/download/v1.0.0/docker-compose.release.yml
curl -O https://github.com/<your-username>/<your-repo>/releases/download/v1.0.0/.env.example

# 配置并启动
mv docker-compose.release.yml docker-compose.yml
mv .env.example .env
nano .env  # 填入凭证
docker-compose up -d
```

## 🔧 配置要求

### GitHub 仓库设置

在首次运行工作流之前，需要配置仓库权限：

1. 访问仓库 Settings > Actions > General
2. 在 Workflow permissions 部分：
   - 选择 **Read and write permissions**
   - 勾选 **Allow GitHub Actions to create and approve pull requests**
3. 点击 Save

### 镜像可见性

默认情况下，镜像是私有的。要公开镜像：

1. 访问 Packages 页面
2. 选择镜像包
3. 点击 Package settings
4. 更改可见性为 Public

## 📊 工作流输出

### Docker 镜像

**后端镜像**：
```
ghcr.io/<username>/<repo>-backend:1.0.0
ghcr.io/<username>/<repo>-backend:1.0
ghcr.io/<username>/<repo>-backend:1
ghcr.io/<username>/<repo>-backend:latest
```

**前端镜像**：
```
ghcr.io/<username>/<repo>-frontend:1.0.0
ghcr.io/<username>/<repo>-frontend:1.0
ghcr.io/<username>/<repo>-frontend:1
ghcr.io/<username>/<repo>-frontend:latest
```

### Release 资源

- 发布说明（Markdown 格式）
- `docker-compose.release.yml` - 生产配置
- `.env.example` - 环境变量模板

## 🎯 特性亮点

### 1. 自动化构建
- 无需手动构建和推送镜像
- 利用 Docker Buildx 进行高效构建
- 使用 GitHub Actions 缓存加速构建

### 2. 语义化版本
- 自动生成多个版本标签
- 支持主版本、次版本和修订号
- 提供 latest 标签用于最新版本

### 3. 完整的发布流程
- 自动创建 GitHub Release
- 生成详细的发布说明
- 包含部署指南和镜像信息

### 4. 生产就绪
- 预配置的 docker-compose 文件
- 健康检查配置
- 环境变量模板
- 数据持久化支持

## 📚 文档结构

- **RELEASE_GUIDE.md** - 完整的发布指南，包括：
  - 前置准备
  - 发布步骤
  - 验证方法
  - 故障排查
  
- **QUICK_START.md** - 快速开始指南，包括：
  - 5 分钟部署流程
  - 常用命令
  - 故障排查
  
- **.github/workflows/README.md** - 技术文档，包括：
  - 工作流详细说明
  - 触发方式
  - 权限配置
  - 最佳实践

## 🔄 工作流触发条件

### 自动触发
- 推送以 `v` 开头的标签（如 `v1.0.0`, `v2.1.3`）

### 手动触发
- GitHub Actions 页面手动运行
- 可指定任意版本号

## ⏱️ 预计时间

- **构建时间**：10-15 分钟
  - 后端镜像：3-5 分钟
  - 前端镜像：5-8 分钟
  - Release 创建：1-2 分钟

## 🎓 最佳实践

1. **测试后发布**
   - 本地测试通过后再创建标签
   - 使用 `docker-compose build` 验证构建

2. **语义化版本**
   - 遵循 MAJOR.MINOR.PATCH 格式
   - 破坏性变更增加主版本号
   - 新功能增加次版本号
   - Bug 修复增加修订号

3. **保持一致性**
   - Git 标签与应用版本号一致
   - 更新 `backend/app/config.py` 中的 `APP_VERSION`

4. **备份数据**
   - 升级前备份 data 目录
   - 测试新版本后再删除备份

## 🐛 故障排查

### 权限错误
```
Error: Resource not accessible by integration
```
**解决方案**：配置仓库的 Actions 权限为读写模式

### 构建失败
**解决方案**：
- 检查 Dockerfile 语法
- 验证依赖项是否可用
- 查看详细的构建日志

### 推送失败
**解决方案**：
- 确认 GITHUB_TOKEN 权限
- 检查网络连接
- 验证镜像名称格式

## 📞 获取帮助

- **发布问题**：查看 RELEASE_GUIDE.md
- **部署问题**：查看 QUICK_START.md
- **工作流问题**：查看 .github/workflows/README.md
- **其他问题**：提交 GitHub Issue

## ✅ 检查清单

发布前确认：
- [ ] 所有代码已提交
- [ ] 本地测试通过
- [ ] 文档已更新
- [ ] 版本号正确
- [ ] 仓库权限已配置

发布后验证：
- [ ] Actions 工作流成功
- [ ] Release 已创建
- [ ] 镜像已推送
- [ ] 配置文件可下载
- [ ] 部署测试通过

## 🎉 完成

CI/CD 设置已完成！现在你可以：

1. 推送 `v1.0.0` 标签开始首次发布
2. 查看 Actions 页面监控构建进度
3. 从 Releases 页面下载并部署

---

**祝发布顺利！** 🚀
