# GitHub Actions 工作流文档

## 📋 概述

本项目包含自动化的 Docker 镜像构建、推送和发布工作流。

## 🚀 工作流说明

### docker-build-and-release.yml

此工作流会自动：
1. 构建后端和前端 Docker 镜像
2. 推送镜像到 GitHub Container Registry (GHCR)
3. 创建 GitHub Release
4. 生成详细的发布说明
5. 上传 docker-compose.release.yml 和 .env.example 到 Release

## 🎯 触发方式

### 方式 1：推送版本标签（推荐）

```bash
# 创建并推送版本标签
git tag v1.0.0
git push origin v1.0.0
```

标签格式必须为 `v*.*.*`（例如：v1.0.0, v2.1.3）

### 方式 2：手动触发

1. 访问 GitHub 仓库的 **Actions** 页面
2. 选择 **Docker Build, Push and Release** 工作流
3. 点击 **Run workflow** 按钮
4. 输入版本号（例如：1.0.0，不需要 'v' 前缀）
5. 点击 **Run workflow** 确认

## 📦 生成的镜像

工作流会生成两个 Docker 镜像：

### 后端镜像
```
ghcr.io/[你的用户名]/[仓库名]-backend:版本号
ghcr.io/[你的用户名]/[仓库名]-backend:latest
```

### 前端镜像
```
ghcr.io/[你的用户名]/[仓库名]-frontend:版本号
ghcr.io/[你的用户名]/[仓库名]-frontend:latest
```

## 🔖 镜像标签策略

每次发布会生成以下标签：
- `版本号` - 完整版本号（例如：1.0.0）
- `主版本.次版本` - 次版本号（例如：1.0）
- `主版本` - 主版本号（例如：1）
- `latest` - 最新版本

## 📋 发布 1.0 版本的步骤

### 完整流程

```bash
# 1. 确保代码已提交
git add .
git commit -m "准备发布 v1.0.0"

# 2. 创建版本标签
git tag -a v1.0.0 -m "Release version 1.0.0"

# 3. 推送代码和标签
git push origin main  # 或你的主分支名称
git push origin v1.0.0

# 4. 等待 GitHub Actions 自动构建和发布
# 访问 https://github.com/你的用户名/你的仓库/actions 查看进度
```

### 验证发布

1. 访问仓库的 **Releases** 页面
2. 查看 v1.0.0 发布
3. 下载附件中的 `docker-compose.release.yml` 和 `.env.example`
4. 查看 **Packages** 页面确认镜像已推送

## 🐳 使用发布的镜像

### 方式 1：使用 docker-compose（推荐）

```bash
# 1. 下载 Release 中的 docker-compose.release.yml
wget https://github.com/你的用户名/你的仓库/releases/download/v1.0.0/docker-compose.release.yml

# 2. 重命名为 docker-compose.yml
mv docker-compose.release.yml docker-compose.yml

# 3. 下载 .env.example 并配置
wget https://github.com/你的用户名/你的仓库/releases/download/v1.0.0/.env.example
mv .env.example .env
# 编辑 .env 填入你的火山引擎凭证

# 4. 启动服务
docker-compose up -d
```

### 方式 2：直接使用 Docker 命令

```bash
# 拉取镜像
docker pull ghcr.io/你的用户名/你的仓库-backend:1.0.0
docker pull ghcr.io/你的用户名/你的仓库-frontend:1.0.0

# 创建网络
docker network create volcengine-net

# 启动后端
docker run -d \
  --name volcengine-backend \
  --network volcengine-net \
  -p 8000:8000 \
  -v ./data:/app/data \
  -e VOLCENGINE_ACCESS_KEY=your_key \
  -e VOLCENGINE_SECRET_KEY=your_secret \
  ghcr.io/你的用户名/你的仓库-backend:1.0.0

# 启动前端
docker run -d \
  --name volcengine-frontend \
  --network volcengine-net \
  -p 3000:80 \
  ghcr.io/你的用户名/你的仓库-frontend:1.0.0
```

## 🔑 权限要求

工作流需要以下权限（已在工作流中配置）：
- `contents: write` - 创建 Release
- `packages: write` - 推送 Docker 镜像到 GHCR
- `id-token: write` - 身份验证

这些权限会自动通过 `GITHUB_TOKEN` 提供，无需额外配置。

## 🌐 镜像可见性

默认情况下，推送到 GHCR 的镜像是私有的。要公开镜像：

1. 访问仓库的 **Packages** 页面
2. 选择镜像包
3. 点击 **Package settings**
4. 在 **Danger Zone** 中点击 **Change visibility**
5. 选择 **Public**

## 🐛 故障排查

### 工作流失败

查看失败的步骤：
1. 访问 **Actions** 页面
2. 点击失败的工作流运行
3. 查看错误日志

常见问题：
- **权限错误**：确保仓库的 Actions 设置允许读写权限
- **构建失败**：检查 Dockerfile 和依赖项
- **推送失败**：确认 GHCR 访问权限

### 权限设置

如果遇到权限问题，请检查：
1. 访问仓库的 **Settings** > **Actions** > **General**
2. 在 **Workflow permissions** 部分
3. 选择 **Read and write permissions**
4. 勾选 **Allow GitHub Actions to create and approve pull requests**
5. 点击 **Save**

## 📊 工作流执行时间

预计执行时间：
- 后端镜像构建：3-5 分钟
- 前端镜像构建：5-8 分钟
- 总时间：约 10-15 分钟

## 🔄 版本管理建议

### 语义化版本控制

- **主版本号**（MAJOR）：不兼容的 API 修改
- **次版本号**（MINOR）：向后兼容的功能性新增
- **修订号**（PATCH）：向后兼容的问题修正

示例：
- `v1.0.0` - 首次发布
- `v1.0.1` - Bug 修复
- `v1.1.0` - 新功能
- `v2.0.0` - 重大更新（破坏性变更）

## 📝 发布清单

发布前检查：
- [ ] 所有测试通过
- [ ] 更新 CHANGELOG.md
- [ ] 更新版本号（如果需要）
- [ ] 提交所有更改
- [ ] 创建并推送标签
- [ ] 验证工作流成功执行
- [ ] 测试发布的镜像
- [ ] 公开镜像（如果需要）

## 🎓 最佳实践

1. **使用标签触发**：推荐使用 Git 标签自动触发发布
2. **测试后发布**：确保代码在创建标签前已经过充分测试
3. **编写发布说明**：在 Git 标签中添加详细的说明信息
4. **保持版本一致**：应用内的版本号应与 Git 标签一致
5. **备份重要数据**：部署前备份数据卷

## 🔗 相关链接

- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [GitHub Container Registry 文档](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
- [Docker Build Push Action](https://github.com/docker/build-push-action)
- [语义化版本控制](https://semver.org/lang/zh-CN/)
