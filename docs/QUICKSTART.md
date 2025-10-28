# 快速开始指南 (Quick Start Guide)

## 简介

这是一个完整的 Docker 化 AI 图像生成应用，基于火山引擎视觉智能 API 开发。

## 特性

✨ **文生图 (Text-to-Image)** - 根据文字描述生成图像  
🎨 **图生图 (Image-to-Image)** - 基于图片进行 AI 变换  
📚 **历史记录** - 查看和管理所有生成的图像  
🎯 **美观界面** - 现代化深色主题 UI  
🚀 **一键部署** - Docker Compose 快速启动  
🔄 **实时监控** - 任务状态实时更新  

## 系统要求

- Docker 20.10+
- Docker Compose 2.0+
- 8GB+ 内存推荐
- 10GB+ 磁盘空间

## 快速部署

### 方法 1: 使用启动脚本（推荐）

```bash
# 1. 进入项目目录
cd volcengine-image-generator

# 2. 运行启动脚本
./scripts/start.sh
```

启动脚本会自动：
- 检查 Docker 环境
- 创建 .env 配置文件
- 构建 Docker 镜像
- 启动所有服务
- 显示访问地址

### 方法 2: 手动启动

```bash
# 1. 复制环境变量配置
cp .env.example .env

# 2. （可选）编辑 .env 添加火山引擎凭证
nano .env

# 3. 启动服务
docker-compose up -d

# 4. 查看日志
docker-compose logs -f
```

### 访问应用

启动成功后，在浏览器中打开：

- **前端界面**: http://localhost:3000
- **后端 API**: http://localhost:8000
- **API 文档**: http://localhost:8000/docs

## 配置说明

### Demo 模式（无需凭证）

如果不配置火山引擎凭证，应用会自动进入 Demo 模式：
- 使用模拟服务生成占位图像
- 所有功能正常可用
- 适合演示和测试

### 生产模式（需要凭证）

编辑 `.env` 文件，添加您的火山引擎凭证：

```env
VOLCENGINE_ACCESS_KEY=your_access_key_here
VOLCENGINE_SECRET_KEY=your_secret_key_here
VOLCENGINE_REGION=cn-beijing
```

#### 获取凭证步骤

1. 访问 [火山引擎控制台](https://console.volcengine.com/)
2. 登录或注册账号
3. 进入「访问控制」→「访问密钥」
4. 创建新的访问密钥（AccessKey）
5. 复制 Access Key ID 和 Secret Access Key
6. 开通「视觉智能」服务

## 使用指南

### 1. 文生图 (Text to Image)

1. 点击顶部菜单 **Text to Image**
2. 在 **Prompt** 框输入描述，例如：
   ```
   一座宁静的山间小屋，周围是茂密的森林，夕阳西下
   ```
3. （可选）在 **Negative Prompt** 输入不想要的元素：
   ```
   模糊，低质量，噪点
   ```
4. 调整参数：
   - **Width/Height**: 图像尺寸（512x512 推荐）
   - **Steps**: 采样步数（30-50 推荐，越高质量越好）
   - **CFG Scale**: 提示词相关性（7-9 推荐）
   - **Seed**: 随机种子（-1 为随机）
   - **Style Preset**: 选择艺术风格
   - **Number of Images**: 批量生成数量（1-4）
5. 点击 **Generate Image** 按钮
6. 等待 10-30 秒，图像生成完成
7. 点击 **Download** 下载图像

### 2. 图生图 (Image to Image)

1. 点击顶部菜单 **Image to Image**
2. 拖拽或点击上传图片
3. 输入变换提示词，例如：
   ```
   转换为水彩画风格，色彩柔和
   ```
4. 调整 **Strength**（0-1）：
   - 0.3-0.5: 轻微变化
   - 0.5-0.7: 中等变化
   - 0.7-1.0: 强烈变化
5. 点击 **Transform Image**
6. 查看和下载结果

### 3. 查看历史

1. 点击顶部菜单 **History**
2. 浏览所有生成的图像
3. 点击图像查看大图
4. 使用 **Copy Prompt** 复用提示词
5. 使用 **Download All** 批量下载

## 参数说明

### Prompt (提示词)

**作用**: 描述您想要生成的图像

**技巧**:
- 使用详细、具体的描述
- 包含主体、风格、光线、色彩等
- 使用英文逗号分隔不同元素
- 示例：`山水画，水墨风格，远山，近水，小舟，宁静的氛围`

### Negative Prompt (反向提示词)

**作用**: 描述不想出现的元素

**常用词**:
- 质量相关：`模糊，低质量，噪点，失真`
- 构图相关：`截断，不完整，变形`
- 内容相关：`文字，水印，logo`

### Steps (采样步数)

- **10-20**: 快速预览，质量一般
- **20-30**: 平衡质量和速度（推荐）
- **30-50**: 高质量输出
- **50+**: 精细调整，耗时较长

### CFG Scale (提示词相关性)

- **1-3**: 创意自由，可能偏离提示词
- **5-10**: 平衡创意和准确性（推荐 7-9）
- **10-20**: 严格遵循提示词，可能过度饱和

### Seed (随机种子)

- **-1**: 完全随机，每次不同
- **固定数字**: 可重现相同结果（配合相同参数）

### Style Preset (风格预设)

- **None**: 无特定风格
- **Anime**: 动漫风格
- **Photographic**: 照片写实
- **Digital Art**: 数字艺术
- **Cinematic**: 电影感

## 常见问题

### Q: 为什么图像生成失败？

A: 检查以下几点：
1. 确认火山引擎凭证是否正确
2. 检查 API 配额是否充足
3. 查看后端日志：`docker-compose logs backend`
4. 尝试简化提示词

### Q: 如何提高图像质量？

A: 
1. 增加 Steps 到 40-50
2. 使用更详细的提示词
3. 调整 CFG Scale 到 8-10
4. 选择合适的 Style Preset

### Q: 生成速度慢怎么办？

A:
1. 降低 Steps 到 20-30
2. 减小图像尺寸
3. 减少批量生成数量
4. 检查网络连接

### Q: Demo 模式和生产模式有什么区别？

A:
- **Demo 模式**: 使用占位图片，无需凭证，适合演示
- **生产模式**: 调用真实 API，需要凭证，生成真实图像

### Q: 如何停止服务？

A:
```bash
docker-compose down
```

### Q: 如何查看日志？

A:
```bash
# 所有服务
docker-compose logs -f

# 仅后端
docker-compose logs -f backend

# 仅前端
docker-compose logs -f frontend
```

### Q: 如何更新应用？

A:
```bash
# 停止服务
docker-compose down

# 拉取最新代码
git pull

# 重新构建并启动
docker-compose build
docker-compose up -d
```

## 高级配置

### 更改端口

编辑 `docker-compose.yml`:

```yaml
services:
  frontend:
    ports:
      - "8080:80"  # 将 3000 改为 8080
  backend:
    ports:
      - "8001:8000"  # 将 8000 改为 8001
```

### 设置历史记录上限

编辑 `.env`:

```env
MAX_HISTORY_SIZE=2000  # 默认 1000
```

### 调整并发数

编辑 `.env`:

```env
MAX_BATCH_SIZE=8  # 默认 4
```

## 性能优化

### 1. 服务器部署

- 使用 SSD 存储
- 分配足够内存（建议 8GB+）
- 使用 CDN 加速静态资源

### 2. 网络优化

- 配置 HTTPS
- 启用 gzip 压缩
- 使用反向代理缓存

### 3. 扩展部署

对于高并发场景：
- 使用 Kubernetes 编排
- 配置 Redis 任务队列
- 水平扩展后端实例
- 使用负载均衡

## 故障排查

### 检查服务状态

```bash
docker-compose ps
```

### 检查容器日志

```bash
# 后端错误
docker-compose logs backend | grep ERROR

# 前端错误
docker-compose logs frontend | grep ERROR
```

### 重启服务

```bash
# 重启所有服务
docker-compose restart

# 仅重启后端
docker-compose restart backend
```

### 完全重置

```bash
# 停止并删除所有容器
docker-compose down

# 删除卷（会清空历史记录）
docker-compose down -v

# 重新启动
docker-compose up -d
```

## 安全建议

### 生产环境部署

1. **使用 HTTPS**
   ```bash
   # 使用 Let's Encrypt 获取证书
   certbot certonly --standalone -d yourdomain.com
   ```

2. **配置防火墙**
   ```bash
   # 仅开放必要端口
   ufw allow 80/tcp
   ufw allow 443/tcp
   ```

3. **设置 CORS**
   
   编辑 `.env`:
   ```env
   CORS_ORIGINS=https://yourdomain.com
   ```

4. **限制访问**
   
   添加 Nginx 基本认证或集成 OAuth

5. **定期备份**
   ```bash
   # 备份历史数据
   cp backend/app/data/history.json backup/
   ```

## 技术支持

- 📖 详细文档: [README.md](../README.md)
- 🔬 技术方案: [RESEARCH_PLAN.md](./RESEARCH_PLAN.md)
- 🐛 问题反馈: GitHub Issues
- 📧 商务合作: 联系项目维护者

## 参考资源

- [火山引擎文档](https://www.volcengine.com/docs/82379/1541523)
- [FastAPI 文档](https://fastapi.tiangolo.com/)
- [Vue 3 文档](https://vuejs.org/)
- [Docker 文档](https://docs.docker.com/)

---

**祝您使用愉快！如有问题欢迎反馈。** 🎉
