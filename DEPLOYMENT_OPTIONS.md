# 🚢 部署方式选择指南

本项目提供两种 Docker 部署方式，您可以根据需求选择：

## 📦 方式一：全栈单镜像（推荐新手）

### 特点
- ✅ **最简单** - 只需一个容器即可运行
- ✅ **快速部署** - 一条命令启动
- ✅ **配置简单** - 无需容器间通信配置
- ✅ **资源占用少** - 单容器运行

### 适用场景
- 个人项目或小型应用
- 开发和测试环境
- 快速原型和演示
- 学习 Docker 部署

### 快速开始
```bash
# 一键启动
./scripts/start-fullstack.sh

# 或使用 docker-compose
docker-compose -f docker-compose.fullstack.yml up -d
```

### 详细文档
- [全栈单镜像使用指南](README.fullstack.md)
- [快速部署指南](QUICK_DEPLOY.md)
- [架构说明](FULLSTACK_ARCHITECTURE.md)

---

## 🔧 方式二：分离式架构（推荐生产环境）

### 特点
- ✅ **可扩展** - 前后端可独立扩展
- ✅ **灵活部署** - 可分别更新服务
- ✅ **微服务** - 符合微服务架构
- ✅ **生产就绪** - 适合大规模部署

### 适用场景
- 生产环境部署
- 需要高可用性
- 需要独立扩展前后端
- 大型企业应用

### 快速开始
```bash
# 使用标准脚本
./scripts/start.sh

# 或使用 docker-compose
docker-compose up -d
```

### 详细文档
- [主文档](README.md)
- [Docker 构建说明](DOCKER_BUILD_SUMMARY.md)

---

## 📊 对比表格

| 特性 | 全栈单镜像 | 分离式架构 |
|------|-----------|-----------|
| 部署复杂度 | ⭐ 简单 | ⭐⭐⭐ 中等 |
| 容器数量 | 1 个 | 2 个 |
| 资源占用 | 低 | 中 |
| 可扩展性 | ❌ 不能独立扩展 | ✅ 可独立扩展 |
| 更新灵活性 | ❌ 需重建整个镜像 | ✅ 可分别更新 |
| 配置复杂度 | ⭐ 简单 | ⭐⭐ 中等 |
| 适合场景 | 小型/开发/测试 | 生产/大规模 |
| 学习成本 | ⭐ 低 | ⭐⭐ 中 |

## 🎯 选择建议

### 选择全栈单镜像，如果：
- 你是 Docker 新手
- 需要快速启动项目
- 个人项目或小型应用
- 不需要频繁独立更新前后端
- 希望简化部署流程

### 选择分离式架构，如果：
- 生产环境部署
- 需要高可用和负载均衡
- 前后端需要独立扩展
- 团队分工明确（前端/后端）
- 需要灵活的更新策略

## 🔄 迁移说明

### 从分离式迁移到全栈单镜像

```bash
# 1. 停止现有服务
docker-compose down

# 2. 启动全栈版本
docker-compose -f docker-compose.fullstack.yml up -d

# 数据会保留（如果挂载了相同的数据目录）
```

### 从全栈单镜像迁移到分离式

```bash
# 1. 停止全栈版本
docker-compose -f docker-compose.fullstack.yml down

# 2. 启动分离式版本
docker-compose up -d

# 数据会保留（如果挂载了相同的数据目录）
```

## 📝 配置文件对应

| 部署方式 | Dockerfile | docker-compose 配置 |
|---------|-----------|-------------------|
| 全栈单镜像 | `Dockerfile.fullstack` | `docker-compose.fullstack.yml` |
| 分离式架构 | `backend/Dockerfile` + `nginx/Dockerfile` | `docker-compose.yml` |

## 🚀 快速命令参考

### 全栈单镜像

```bash
# 启动
docker-compose -f docker-compose.fullstack.yml up -d

# 查看日志
docker logs volcengine-app

# 停止
docker-compose -f docker-compose.fullstack.yml down

# 重启
docker restart volcengine-app
```

### 分离式架构

```bash
# 启动
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止
docker-compose down

# 重启特定服务
docker-compose restart backend
docker-compose restart frontend
```

## 💡 常见问题

### Q: 两种方式性能有差异吗？
A: 性能基本相同。全栈单镜像使用 localhost 通信，分离式使用 Docker 网络，都很高效。

### Q: 可以同时运行两种方式吗？
A: 不建议，会有端口冲突。如需测试，请修改其中一个的端口映射。

### Q: 数据会丢失吗？
A: 不会，只要挂载相同的数据目录，数据就会保留。

### Q: 哪个更节省资源？
A: 全栈单镜像稍微节省一些资源（减少了一个容器的开销）。

### Q: 生产环境必须用分离式吗？
A: 不是必须，但推荐。如果是小规模应用，全栈单镜像也完全可以用于生产。

## 📚 更多资源

- [项目主文档](README.md) - 完整功能介绍
- [快速开始指南](QUICK_START.md) - 快速上手
- [发布指南](RELEASE_GUIDE.md) - 版本发布说明
- [CI/CD 设置](CICD_SETUP.md) - 持续集成说明

---

**选择适合您的部署方式，开始使用吧！** 🎉
