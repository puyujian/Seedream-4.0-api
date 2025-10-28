# 发布指南

本指南介绍如何使用 GitHub Actions 工作流发布 Docker 镜像和创建版本发布。

## 📋 前置准备

在发布之前，请确保：

1. **代码已经过测试**：所有功能正常工作
2. **更新了文档**：README.md 等文档已更新
3. **提交了所有更改**：没有未提交的改动
4. **设置了仓库权限**：
   - 进入仓库 Settings > Actions > General
   - 在 Workflow permissions 中选择 "Read and write permissions"
   - 勾选 "Allow GitHub Actions to create and approve pull requests"
   - 点击 Save

## 🚀 发布 1.0 版本

### 方法一：使用 Git 标签（推荐）

这是最简单和推荐的方法：

```bash
# 1. 确保在主分支上
git checkout main  # 或 master

# 2. 拉取最新代码
git pull origin main

# 3. 创建版本标签
git tag -a v1.0.0 -m "Release version 1.0.0 - 初始发布"

# 4. 推送标签到 GitHub
git push origin v1.0.0
```

推送标签后，GitHub Actions 会自动：
- 构建后端和前端 Docker 镜像
- 推送镜像到 GitHub Container Registry
- 创建 v1.0.0 的 Release
- 生成发布说明
- 附加 docker-compose.release.yml 和 .env.example

### 方法二：手动触发工作流

如果你想手动控制发布过程：

1. 访问你的 GitHub 仓库
2. 点击顶部的 **Actions** 标签
3. 在左侧选择 **Docker Build, Push and Release** 工作流
4. 点击右侧的 **Run workflow** 下拉按钮
5. 在弹出的对话框中：
   - 选择分支（通常是 main）
   - 输入版本号：`1.0.0`（不需要 'v' 前缀）
6. 点击绿色的 **Run workflow** 按钮

## 📊 监控构建过程

1. 在 **Actions** 页面查看工作流运行状态
2. 点击正在运行的工作流查看详细日志
3. 构建通常需要 10-15 分钟完成

工作流包含以下步骤：
- ✅ 检出代码
- ✅ 设置 Docker Buildx
- ✅ 登录到 GHCR
- ✅ 构建并推送后端镜像
- ✅ 构建并推送前端镜像
- ✅ 创建 Release
- ✅ 上传文件到 Release

## 🎯 验证发布

### 1. 检查 Release

1. 访问 `https://github.com/你的用户名/你的仓库/releases`
2. 应该能看到 **v1.0.0** 的发布
3. 检查发布说明是否正确
4. 确认附件包含：
   - `docker-compose.release.yml`
   - `.env.example`

### 2. 检查 Docker 镜像

1. 访问 `https://github.com/你的用户名/你的仓库/pkgs/container/你的仓库-backend`
2. 查看 backend 镜像是否已推送
3. 检查标签：1.0.0, 1.0, 1, latest
4. 重复以上步骤检查 frontend 镜像

### 3. 测试镜像

```bash
# 拉取镜像
docker pull ghcr.io/你的用户名/你的仓库-backend:1.0.0
docker pull ghcr.io/你的用户名/你的仓库-frontend:1.0.0

# 验证镜像
docker images | grep volcengine
```

## 🐳 使用发布的镜像

### 快速开始

```bash
# 1. 创建工作目录
mkdir volcengine-app && cd volcengine-app

# 2. 下载 docker-compose 配置
curl -O https://github.com/你的用户名/你的仓库/releases/download/v1.0.0/docker-compose.release.yml
mv docker-compose.release.yml docker-compose.yml

# 3. 下载环境变量模板
curl -O https://github.com/你的用户名/你的仓库/releases/download/v1.0.0/.env.example
mv .env.example .env

# 4. 编辑 .env 文件，填入火山引擎凭证
nano .env  # 或使用其他编辑器

# 5. 启动服务
docker-compose up -d

# 6. 查看日志
docker-compose logs -f

# 7. 访问应用
# 打开浏览器访问 http://localhost:3000
```

### 停止服务

```bash
docker-compose down
```

### 更新到新版本

```bash
# 拉取新版本镜像
docker-compose pull

# 重启服务
docker-compose up -d
```

## 🔧 镜像可见性设置

默认情况下，推送到 GHCR 的镜像是私有的。如果要公开镜像：

### 公开后端镜像

1. 访问 `https://github.com/你的用户名?tab=packages`
2. 点击 `你的仓库-backend` 包
3. 点击右侧的 **Package settings**
4. 滚动到 **Danger Zone**
5. 点击 **Change visibility**
6. 选择 **Public**
7. 输入仓库名称确认
8. 点击确认按钮

### 公开前端镜像

重复以上步骤，但选择 `你的仓库-frontend` 包。

## 📝 版本号规范

遵循[语义化版本控制](https://semver.org/lang/zh-CN/)：

- **主版本号**：不兼容的 API 修改
- **次版本号**：向后兼容的功能性新增  
- **修订号**：向后兼容的问题修正

示例：
- `v1.0.0` - 首次正式发布
- `v1.0.1` - Bug 修复
- `v1.1.0` - 添加新功能
- `v2.0.0` - 重大更新（可能包含破坏性变更）

## 🎓 最佳实践

1. **测试后发布**
   ```bash
   # 在本地测试构建
   docker-compose build
   docker-compose up -d
   # 测试所有功能
   docker-compose down
   ```

2. **保持版本一致**
   - 确保 `backend/app/config.py` 中的 `APP_VERSION` 与发布版本一致
   - 可以考虑自动化这个过程

3. **编写发布说明**
   - 使用有意义的标签消息
   - 描述新功能、修复和改进

4. **备份数据**
   - 升级前备份 `./data` 目录
   ```bash
   cp -r ./data ./data.backup
   ```

5. **渐进式部署**
   - 先在测试环境验证
   - 再部署到生产环境

## 🐛 常见问题

### 问题 1：工作流权限错误

**错误信息**：
```
Error: Resource not accessible by integration
```

**解决方法**：
1. 进入 Settings > Actions > General
2. 选择 "Read and write permissions"
3. 保存设置
4. 重新运行工作流

### 问题 2：无法推送镜像

**错误信息**：
```
Error: denied: permission_denied
```

**解决方法**：
- 确保 GitHub Token 有 packages:write 权限（工作流已配置）
- 检查仓库的 Package 设置

### 问题 3：标签已存在

**错误信息**：
```
fatal: tag 'v1.0.0' already exists
```

**解决方法**：
```bash
# 删除本地标签
git tag -d v1.0.0

# 删除远程标签（谨慎操作！）
git push origin :refs/tags/v1.0.0

# 重新创建标签
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

### 问题 4：Docker 镜像拉取失败

**错误信息**：
```
Error response from daemon: pull access denied
```

**解决方法**：
- 如果镜像是私有的，需要先登录：
```bash
echo $GITHUB_TOKEN | docker login ghcr.io -u 你的用户名 --password-stdin
```
- 或者将镜像设置为公开（参见"镜像可见性设置"部分）

## 📚 相关文档

- [GitHub Actions 工作流文档](.github/workflows/README.md)
- [项目 README](README.md)
- [Docker 构建文档](DOCKER_BUILD_SUMMARY.md)

## 🎉 完成！

现在你已经成功发布了 1.0.0 版本！

下一步：
- 将发布链接分享给用户
- 在社交媒体宣布发布
- 收集用户反馈
- 规划下一个版本

如有问题，请在 GitHub Issues 中提出。
