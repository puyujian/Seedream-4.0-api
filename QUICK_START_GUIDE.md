# ⚡ 快速开始指南

> 5分钟快速了解并启动火山引擎图像生成Docker应用

## 📦 这是什么？

一个**开箱即用**的AI图像生成Web应用，基于火山引擎视觉智能API构建。

### 🎯 核心特性

```
✅ 文生图 (Text-to-Image)        ✅ 美观的Web界面
✅ 多种AI模型支持                 ✅ 深色/浅色主题
✅ 实时进度展示                   ✅ 响应式设计
✅ 历史记录管理                   ✅ 一键部署
✅ 图片下载导出                   ✅ 完善的文档
```

## 🚀 3步快速启动

### 步骤 1: 准备环境

```bash
# 确保已安装
✅ Docker 20.x+
✅ Docker Compose 2.x+

# 验证安装
docker --version
docker-compose --version
```

### 步骤 2: 配置密钥

```bash
# 1. 克隆项目
git clone <repository-url>
cd volcengine-image-generator

# 2. 复制配置文件
cp .env.example .env

# 3. 编辑 .env，填入你的火山引擎API密钥
nano .env  # 或使用其他编辑器

# 必填项：
# VOLC_ACCESS_KEY=你的AccessKey
# VOLC_SECRET_KEY=你的SecretKey
```

**获取API密钥**: https://console.volcengine.com/iam/keymanage/

### 步骤 3: 启动应用

```bash
# 一键启动
docker-compose up -d

# 查看日志（可选）
docker-compose logs -f

# 访问应用
# 浏览器打开: http://localhost:8080
```

就这么简单！🎉

## 🎨 使用指南

### 基本操作流程

```
1. 输入提示词
   ↓
2. 选择参数（可选）
   ↓
3. 点击"生成图像"
   ↓
4. 等待生成完成
   ↓
5. 查看/下载图片
```

### 示例提示词

```
✅ 好的提示词（详细、具体）:
"一只可爱的橘猫坐在木质窗台上，温暖的阳光透过玻璃窗照射进来，
柔和的光影效果，电影级质感，高清细节，8K分辨率，温馨的氛围"

❌ 不好的提示词（过于简单）:
"一只猫"

💡 提示词公式:
主体 + 动作/状态 + 环境/背景 + 光线 + 风格 + 质量词
```

### 常用参数说明

| 参数 | 说明 | 推荐值 | 影响 |
|------|------|--------|------|
| **模型** | AI生成模型 | general_v2.0 | 风格和质量 |
| **尺寸** | 图片分辨率 | 1024×1024 | 清晰度 |
| **数量** | 一次生成几张 | 2-3 | 选择空间 |
| **步数** | 采样迭代次数 | 20-30 | 质量和时间 |
| **引导系数** | 遵循提示词程度 | 7-10 | 准确度 |

## 🛠️ 常用命令

### Docker操作

```bash
# 启动服务
docker-compose up -d

# 停止服务
docker-compose down

# 重启服务
docker-compose restart

# 查看状态
docker-compose ps

# 查看日志
docker-compose logs -f backend

# 更新镜像
docker-compose pull
docker-compose up -d
```

### 数据管理

```bash
# 备份数据
tar -czf backup-$(date +%Y%m%d).tar.gz data/

# 恢复数据
tar -xzf backup-20240101.tar.gz

# 清理旧数据（释放空间）
docker-compose exec backend python scripts/cleanup.py

# 查看存储使用
du -sh data/
```

### 故障排查

```bash
# 检查容器状态
docker-compose ps

# 查看错误日志
docker-compose logs backend --tail 100

# 进入容器调试
docker-compose exec backend bash

# 测试API连接
curl http://localhost:8080/api/v1/health

# 重置环境
docker-compose down -v
docker-compose up -d
```

## 🔧 配置说明

### 重要环境变量

```bash
# === 必填 ===
VOLC_ACCESS_KEY=你的AccessKey     # 火山引擎访问密钥
VOLC_SECRET_KEY=你的SecretKey     # 火山引擎私密密钥

# === 可选 ===
APP_PORT=8080                     # 对外访问端口
MAX_CONCURRENT_TASKS=5            # 最大并发任务数
MAX_HISTORY_DAYS=30               # 历史保留天数
APP_LOG_LEVEL=INFO                # 日志级别
```

### 修改端口

```bash
# 方式1: 修改 .env 文件
APP_PORT=9000

# 方式2: 启动时指定
APP_PORT=9000 docker-compose up -d

# 访问: http://localhost:9000
```

## 📊 系统要求

### 最低配置

```
CPU:      2核
内存:     2GB
磁盘:     20GB
网络:     10Mbps
系统:     Linux/macOS/Windows
```

### 推荐配置

```
CPU:      4核
内存:     4GB
磁盘:     50GB SSD
网络:     50Mbps
系统:     Linux (Ubuntu 20.04+)
```

## 🔗 快速链接

| 链接 | 说明 |
|------|------|
| http://localhost:8080 | 主应用界面 |
| http://localhost:8080/docs | API文档 (Swagger) |
| http://localhost:8080/redoc | API文档 (ReDoc) |
| http://localhost:8080/api/v1/health | 健康检查 |

## 📝 API快速参考

### 生成图像

```bash
curl -X POST http://localhost:8080/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "一只可爱的猫咪",
    "model": "general_v2.0",
    "width": 1024,
    "height": 1024,
    "num_images": 1
  }'

# 返回: {"task_id": "xxx", "status": "pending"}
```

### 查询任务状态

```bash
curl http://localhost:8080/api/v1/task/{task_id}

# 返回任务详情和生成的图片
```

### 下载图片

```bash
curl http://localhost:8080/api/v1/images/{image_id} \
  --output image.png
```

## 🐛 常见问题

### Q1: 容器启动失败？

```bash
# 检查端口占用
lsof -i :8080

# 检查Docker日志
docker-compose logs

# 重置环境
docker-compose down -v && docker-compose up -d
```

### Q2: API调用失败？

```bash
# 检查环境变量
docker-compose exec backend env | grep VOLC

# 测试API连接
curl http://localhost:8080/api/v1/system/info

# 查看详细错误
docker-compose logs backend -f
```

### Q3: 生成速度慢？

```
原因可能：
1. 网络不稳定 → 检查网络连接
2. API配额不足 → 查看火山引擎控制台
3. 并发任务过多 → 减少 MAX_CONCURRENT_TASKS
```

### Q4: 图片无法加载？

```bash
# 检查存储权限
ls -la data/images/

# 检查磁盘空间
df -h

# 查看后端日志
docker-compose logs backend
```

## 🎓 学习路径

### 新手 (第1天)

```
1. ✅ 阅读 README.md
2. ✅ 启动应用
3. ✅ 尝试生成第一张图片
4. ✅ 熟悉基本参数
```

### 进阶 (第2-3天)

```
1. ✅ 理解提示词技巧
2. ✅ 尝试高级参数
3. ✅ 查看API文档
4. ✅ 调整配置优化
```

### 高级 (第4-7天)

```
1. ✅ 阅读架构文档
2. ✅ 理解代码结构
3. ✅ 自定义开发
4. ✅ 性能调优
```

## 📚 文档导航

```
入门级:
├── README.md                    ← 从这里开始
├── QUICK_START_GUIDE.md         ← 你在这里
└── .env.example                 ← 配置示例

进阶级:
├── PROPOSAL.md                  ← 技术方案
├── ARCHITECTURE.md              ← 系统架构
└── IMPLEMENTATION_PLAN.md       ← 实施计划

高级:
├── UI_UX_DESIGN.md              ← UI/UX设计
├── RECOMMENDATION_SUMMARY.md    ← 方案推荐
└── 源代码                       ← backend/frontend/
```

## 🎯 下一步

完成快速启动后，你可以：

### 1. 探索功能
- 尝试不同的提示词
- 调整生成参数
- 查看历史记录
- 切换主题模式

### 2. 深入学习
- 阅读 [技术方案](PROPOSAL.md)
- 了解 [系统架构](ARCHITECTURE.md)
- 查看 [API文档](http://localhost:8080/docs)
- 研究源代码

### 3. 自定义开发
- 添加新功能
- 修改UI样式
- 集成其他服务
- 优化性能

### 4. 生产部署
- 配置HTTPS
- 设置域名
- 添加监控
- 备份策略

## 💡 提示词技巧

### 基础结构

```
[主体] + [细节] + [环境] + [风格] + [质量]

示例:
一只橘猫 + 毛茸茸的，蓝色眼睛 + 坐在窗台上，阳光照射 + 
油画风格，梵高 + 高清，8K，细节丰富
```

### 质量提升词

```
正面词: 高清, 8K, 细节丰富, 专业摄影, 电影级, 获奖作品,
       大师之作, 精美, 史诗级, 震撼, 完美构图

负面词: 模糊, 低质量, 变形, 噪点, 失真, 低分辨率,
       业余, 粗糙, 丑陋, watermark
```

### 风格参考

```
写实: 专业摄影, 4K, HDR, 真实感
动漫: anime style, studio ghibli, manga
艺术: 油画, 水彩, 印象派, 抽象派
科技: cyberpunk, futuristic, sci-fi, neon
古典: 文艺复兴, 巴洛克, 古典主义
```

## 🎨 使用场景

### 个人创作
- 🎭 艺术创作和灵感探索
- 📱 社交媒体内容生成
- 🖼️ 壁纸和头像制作
- 📚 故事配图

### 商业应用
- 📢 营销素材快速生成
- 🎬 创意方案可视化
- 🏢 品牌形象设计
- 📊 演示文稿配图

### 教育研究
- 🎓 AI技术教学演示
- 🔬 图像生成研究
- 💻 编程实践项目
- 📖 技术文档配图

## 🏆 最佳实践

### 提示词编写
1. ✅ 详细描述 (50-200字)
2. ✅ 使用英文关键词
3. ✅ 添加质量词
4. ✅ 设置负面提示词

### 参数调整
1. ✅ 从默认值开始
2. ✅ 逐步调整观察效果
3. ✅ 记录好的配置组合
4. ✅ 使用历史记录快速重试

### 系统维护
1. ✅ 定期备份数据
2. ✅ 清理旧文件释放空间
3. ✅ 监控日志查找问题
4. ✅ 更新到最新版本

## 🤝 获取帮助

### 遇到问题？

1. **查看文档**
   - README.md - 基础使用
   - 本文档 - 快速参考
   - ARCHITECTURE.md - 技术细节

2. **检查日志**
   ```bash
   docker-compose logs backend -f
   ```

3. **提交Issue**
   - 描述问题
   - 附加日志
   - 说明环境

4. **社区讨论**
   - GitHub Discussions
   - 技术论坛

## 📞 联系方式

- 🐛 报告Bug: [GitHub Issues](../../issues)
- 💡 功能建议: [GitHub Discussions](../../discussions)
- 📧 邮件联系: [项目维护者]
- 📚 文档首页: [README.md](README.md)

---

<div align="center">

**🎉 开始你的AI图像生成之旅！🎉**

Made with ❤️ by AI Assistant

[⬆️ 返回顶部](#-快速开始指南)

</div>
