# 📐 系统架构设计文档

## 1. 总体架构

### 1.1 系统架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                         客户端层 (Client)                         │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  Web浏览器   │  │  移动浏览器   │  │   API客户端   │         │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘         │
│         │                  │                  │                  │
└─────────┼──────────────────┼──────────────────┼─────────────────┘
          │                  │                  │
          └──────────────────┴──────────────────┘
                             │
                    HTTPS (Port 443/8080)
                             │
┌────────────────────────────▼──────────────────────────────────┐
│                      接入层 (Gateway)                          │
│                                                                 │
│                    ┌─────────────────┐                         │
│                    │  Nginx (Alpine) │                         │
│                    │  - 反向代理      │                         │
│                    │  - 静态资源      │                         │
│                    │  - SSL终止       │                         │
│                    └────────┬────────┘                         │
└─────────────────────────────┼──────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                    应用层 (Application)                        │
│                                                                │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │           FastAPI Application (Python 3.11)             │ │
│  │                                                           │ │
│  │  ┌──────────────────────────────────────────────────┐   │ │
│  │  │              API路由层 (Routes)                   │   │ │
│  │  │  - /api/v1/generate  (生成图像)                  │   │ │
│  │  │  - /api/v1/task      (任务管理)                  │   │ │
│  │  │  - /api/v1/history   (历史记录)                  │   │ │
│  │  │  - /api/v1/system    (系统信息)                  │   │ │
│  │  └─────────────────────┬────────────────────────────┘   │ │
│  │                        │                                 │ │
│  │  ┌─────────────────────▼────────────────────────────┐   │ │
│  │  │            业务逻辑层 (Services)                  │   │ │
│  │  │                                                    │   │ │
│  │  │  ┌──────────────────┐  ┌───────────────────┐     │   │ │
│  │  │  │ ImageGenerator   │  │  TaskManager      │     │   │ │
│  │  │  │ - 图像生成逻辑    │  │  - 任务队列管理   │     │   │ │
│  │  │  │ - 参数验证       │  │  - 状态追踪       │     │   │ │
│  │  │  └──────────────────┘  └───────────────────┘     │   │ │
│  │  │                                                    │   │ │
│  │  │  ┌──────────────────┐  ┌───────────────────┐     │   │ │
│  │  │  │ VolcEngineService│  │  StorageService   │     │   │ │
│  │  │  │ - SDK封装        │  │  - 文件管理       │     │   │ │
│  │  │  │ - API调用        │  │  - 图片存储       │     │   │ │
│  │  │  └──────────────────┘  └───────────────────┘     │   │ │
│  │  └─────────────────────┬────────────────────────────┘   │ │
│  │                        │                                 │ │
│  │  ┌─────────────────────▼────────────────────────────┐   │ │
│  │  │           数据访问层 (Data Access)                │   │ │
│  │  │  - SQLAlchemy ORM                                │   │ │
│  │  │  - Repository Pattern                            │   │ │
│  │  └───────────────────────────────────────────────────┘   │ │
│  └─────────────────────────────────────────────────────────┘ │
└────────┬───────────────────────────────────────┬─────────────┘
         │                                       │
         ▼                                       ▼
┌─────────────────────┐              ┌─────────────────────┐
│   数据层 (Data)      │              │  外部服务 (External) │
│                     │              │                     │
│  ┌───────────────┐  │              │ ┌─────────────────┐ │
│  │ SQLite3 DB    │  │              │ │ VolcEngine API  │ │
│  │ - 任务记录    │  │              │ │ - Visual AI     │ │
│  │ - 历史数据    │  │              │ │ - Image Gen     │ │
│  └───────────────┘  │              │ └─────────────────┘ │
│                     │              │                     │
│  ┌───────────────┐  │              │ https://open.       │
│  │ File System   │  │              │   volcengineapi.com │
│  │ - 生成图片    │  │              │                     │
│  │ - 缩略图      │  │              └─────────────────────┘
│  └───────────────┘  │
└─────────────────────┘
```

## 2. 数据流设计

### 2.1 图像生成流程

```
用户 → Web界面 → API网关 → 后端服务 → 火山引擎 → 返回图片 → 存储 → 展示

详细步骤：

┌──────────┐
│  用户输入  │  1. 用户在Web界面填写提示词和参数
└─────┬────┘
      │
      ▼
┌──────────────┐
│  参数验证     │  2. 前端JavaScript验证输入
└─────┬────────┘
      │
      ▼
┌──────────────┐
│ POST /generate│  3. 发送HTTP请求到后端API
└─────┬────────┘
      │
      ▼
┌──────────────┐
│  创建任务     │  4. 后端创建异步任务记录
│  (Pending)   │     - 生成task_id
└─────┬────────┘     - 存入数据库
      │              - 返回task_id给前端
      ▼
┌──────────────┐
│  异步处理     │  5. 后台异步处理任务
│              │     - 从队列获取任务
└─────┬────────┘     - 更新状态为Processing
      │
      ▼
┌──────────────┐
│ 调用火山引擎  │  6. 通过SDK调用火山引擎API
│     API      │     - 传递参数
└─────┬────────┘     - 等待响应
      │
      ▼
┌──────────────┐
│  处理响应     │  7. 处理火山引擎返回的图片
│              │     - 下载图片到本地
└─────┬────────┘     - 生成缩略图
      │              - 保存文件路径
      ▼
┌──────────────┐
│  更新任务     │  8. 更新任务状态
│ (Completed)  │     - 状态改为Completed
└─────┬────────┘     - 记录图片路径
      │              - 保存到历史记录
      ▼
┌──────────────┐
│  前端轮询     │  9. 前端定时查询任务状态
│  GET /task   │     - 获取最新状态
└─────┬────────┘     - 显示进度
      │
      ▼
┌──────────────┐
│  展示图片     │  10. 任务完成后展示图片
└──────────────┘      - 渲染图片网格
                      - 提供下载按钮
```

### 2.2 任务状态机

```
                    ┌──────────┐
                    │  PENDING │  任务已创建，等待处理
                    └────┬─────┘
                         │
                         ▼
                    ┌──────────┐
         ┌──────────│PROCESSING│  正在生成图像
         │          └────┬─────┘
         │               │
         │               ├─────────┐
         │               ▼         ▼
         │          ┌──────────┐  ┌──────────┐
         │          │COMPLETED │  │  FAILED  │
         │          └──────────┘  └────┬─────┘
         │                              │
         │                              ▼
         │                         ┌─────────┐
         └────────────────────────▶│ RETRYING│
                                   └────┬────┘
                                        │
                                        ▼
                                   (回到PROCESSING)

状态说明：
- PENDING: 任务已创建，在队列中等待
- PROCESSING: 正在调用火山引擎API生成图像
- COMPLETED: 图像生成成功，已保存
- FAILED: 生成失败（超过最大重试次数）
- RETRYING: 临时失败，正在重试
```

## 3. 核心模块设计

### 3.1 后端模块结构

```
backend/app/
│
├── main.py                      # 应用入口
│   ├── FastAPI实例化
│   ├── 中间件配置
│   ├── 路由注册
│   └── 启动/关闭事件
│
├── config.py                    # 配置管理
│   ├── Settings (Pydantic)
│   ├── 环境变量加载
│   └── 配置验证
│
├── api/                         # API路由层
│   ├── routes.py               # 路由聚合
│   ├── generate.py             # 图像生成端点
│   │   ├── POST /generate
│   │   └── WebSocket /generate/stream
│   ├── task.py                 # 任务管理端点
│   │   ├── GET /task/{id}
│   │   ├── GET /tasks
│   │   └── DELETE /task/{id}
│   ├── history.py              # 历史记录端点
│   │   ├── GET /history
│   │   └── DELETE /history/{id}
│   ├── image.py                # 图片服务端点
│   │   ├── GET /images/{id}
│   │   └── GET /images/{id}/thumbnail
│   └── system.py               # 系统信息端点
│       ├── GET /health
│       ├── GET /info
│       └── GET /models
│
├── services/                    # 业务逻辑层
│   ├── volcengine.py           # 火山引擎服务
│   │   ├── VolcEngineClient
│   │   │   ├── initialize_sdk()
│   │   │   ├── generate_image()
│   │   │   ├── check_quota()
│   │   │   └── list_models()
│   │   └── 错误处理
│   │
│   ├── image_generator.py      # 图像生成服务
│   │   ├── ImageGeneratorService
│   │   │   ├── create_task()
│   │   │   ├── process_task()
│   │   │   ├── validate_params()
│   │   │   └── save_result()
│   │   └── 参数预处理
│   │
│   ├── task_manager.py         # 任务管理服务
│   │   ├── TaskManager
│   │   │   ├── submit_task()
│   │   │   ├── get_task_status()
│   │   │   ├── update_task()
│   │   │   └── cleanup_old_tasks()
│   │   └── 队列管理
│   │
│   └── storage.py              # 存储服务
│       ├── StorageService
│       │   ├── save_image()
│       │   ├── generate_thumbnail()
│       │   ├── get_image_path()
│       │   └── cleanup_storage()
│       └── 文件管理
│
├── models/                      # 数据模型层
│   ├── database.py             # 数据库模型 (SQLAlchemy)
│   │   ├── Task (表: tasks)
│   │   └── History (表: history)
│   │
│   ├── schemas.py              # API模型 (Pydantic)
│   │   ├── GenerateRequest
│   │   ├── GenerateResponse
│   │   ├── TaskStatus
│   │   └── HistoryItem
│   │
│   └── enums.py                # 枚举类型
│       ├── TaskStatus
│       ├── ModelType
│       └── ImageSize
│
└── utils/                       # 工具层
    ├── logger.py               # 日志工具
    ├── helpers.py              # 辅助函数
    ├── validators.py           # 验证器
    └── exceptions.py           # 自定义异常
```

### 3.2 前端模块结构

```
frontend/
│
├── static/
│   ├── css/
│   │   └── custom.css          # 自定义样式
│   │       ├── 主题变量
│   │       ├── 组件样式
│   │       └── 动画效果
│   │
│   ├── js/
│   │   ├── app.js              # 主应用逻辑
│   │   │   ├── Alpine.js组件
│   │   │   ├── 状态管理
│   │   │   └── 事件处理
│   │   │
│   │   ├── api.js              # API调用封装
│   │   │   ├── generateImage()
│   │   │   ├── getTaskStatus()
│   │   │   ├── getHistory()
│   │   │   └── 错误处理
│   │   │
│   │   └── utils.js            # 工具函数
│   │       ├── formatDate()
│   │       ├── downloadImage()
│   │       └── validateForm()
│   │
│   └── images/
│       ├── logo.svg
│       ├── placeholder.svg
│       └── icons/
│
└── templates/
    └── index.html              # 主页面
        ├── 头部导航
        ├── 参数配置面板
        ├── 图像展示区
        ├── 历史记录侧边栏
        └── 模态框组件
```

## 4. 数据库设计

### 4.1 ER图

```
┌─────────────────────────────────┐
│            tasks                │  任务表
├─────────────────────────────────┤
│ id (PK)         INTEGER         │
│ task_id         VARCHAR(36)     │  UUID
│ status          VARCHAR(20)     │  任务状态
│ prompt          TEXT            │  提示词
│ negative_prompt TEXT            │  负面提示词
│ model           VARCHAR(50)     │  模型名称
│ width           INTEGER         │  宽度
│ height          INTEGER         │  高度
│ num_images      INTEGER         │  图片数量
│ steps           INTEGER         │  采样步数
│ scale           FLOAT           │  引导系数
│ seed            INTEGER         │  随机种子
│ result_images   JSON            │  结果图片列表
│ error_message   TEXT            │  错误信息
│ retry_count     INTEGER         │  重试次数
│ created_at      DATETIME        │  创建时间
│ started_at      DATETIME        │  开始时间
│ completed_at    DATETIME        │  完成时间
└─────────────────────────────────┘
         │
         │ 1:N
         ▼
┌─────────────────────────────────┐
│           images                │  图片表
├─────────────────────────────────┤
│ id (PK)         INTEGER         │
│ image_id        VARCHAR(36)     │  UUID
│ task_id (FK)    INTEGER         │  关联任务
│ file_path       VARCHAR(255)    │  文件路径
│ thumbnail_path  VARCHAR(255)    │  缩略图路径
│ file_size       INTEGER         │  文件大小
│ width           INTEGER         │  图片宽度
│ height          INTEGER         │  图片高度
│ created_at      DATETIME        │  创建时间
└─────────────────────────────────┘
         │
         │ N:1
         ▼
┌─────────────────────────────────┐
│          user_tags              │  标签表 (可选)
├─────────────────────────────────┤
│ id (PK)         INTEGER         │
│ image_id (FK)   INTEGER         │
│ tag_name        VARCHAR(50)     │
│ created_at      DATETIME        │
└─────────────────────────────────┘
```

### 4.2 索引设计

```sql
-- 任务表索引
CREATE INDEX idx_task_id ON tasks(task_id);
CREATE INDEX idx_status ON tasks(status);
CREATE INDEX idx_created_at ON tasks(created_at);

-- 图片表索引
CREATE INDEX idx_image_id ON images(image_id);
CREATE INDEX idx_task_id_fk ON images(task_id);

-- 标签表索引
CREATE INDEX idx_image_id_fk ON user_tags(image_id);
CREATE INDEX idx_tag_name ON user_tags(tag_name);
```

## 5. API接口设计

### 5.1 接口清单

| 端点 | 方法 | 功能 | 认证 |
|------|------|------|------|
| `/api/v1/generate` | POST | 创建生成任务 | 否 |
| `/api/v1/task/{task_id}` | GET | 查询任务状态 | 否 |
| `/api/v1/tasks` | GET | 获取任务列表 | 否 |
| `/api/v1/task/{task_id}` | DELETE | 删除任务 | 否 |
| `/api/v1/history` | GET | 获取历史记录 | 否 |
| `/api/v1/history/{id}` | DELETE | 删除历史记录 | 否 |
| `/api/v1/images/{image_id}` | GET | 获取图片 | 否 |
| `/api/v1/images/{image_id}/thumbnail` | GET | 获取缩略图 | 否 |
| `/api/v1/models` | GET | 获取可用模型列表 | 否 |
| `/api/v1/system/info` | GET | 获取系统信息 | 否 |
| `/api/v1/health` | GET | 健康检查 | 否 |

### 5.2 接口详细设计

#### 创建生成任务

```http
POST /api/v1/generate HTTP/1.1
Content-Type: application/json

{
  "prompt": "一只可爱的猫咪",
  "negative_prompt": "模糊, 低质量",
  "model": "general_v2.0",
  "width": 1024,
  "height": 1024,
  "num_images": 1,
  "steps": 20,
  "scale": 7.5,
  "seed": null
}

Response 201:
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending",
  "created_at": "2024-01-01T12:00:00Z",
  "estimated_time": 30
}

Response 400:
{
  "error": "validation_error",
  "message": "提示词不能为空",
  "details": {...}
}

Response 429:
{
  "error": "rate_limit_exceeded",
  "message": "超出并发任务限制",
  "retry_after": 60
}
```

#### 查询任务状态

```http
GET /api/v1/task/550e8400-e29b-41d4-a716-446655440000 HTTP/1.1

Response 200 (Processing):
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "processing",
  "progress": 45,
  "created_at": "2024-01-01T12:00:00Z",
  "started_at": "2024-01-01T12:00:05Z"
}

Response 200 (Completed):
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "progress": 100,
  "images": [
    {
      "image_id": "img_123456",
      "url": "/api/v1/images/img_123456",
      "thumbnail_url": "/api/v1/images/img_123456/thumbnail",
      "width": 1024,
      "height": 1024,
      "file_size": 2048576
    }
  ],
  "created_at": "2024-01-01T12:00:00Z",
  "started_at": "2024-01-01T12:00:05Z",
  "completed_at": "2024-01-01T12:00:25Z"
}

Response 404:
{
  "error": "not_found",
  "message": "任务不存在"
}
```

## 6. 部署架构

### 6.1 Docker容器架构

```
┌─────────────────────────────────────────────────────────┐
│                    Docker Host                          │
│                                                           │
│  ┌───────────────────────────────────────────────────┐  │
│  │           Docker Network: app-network             │  │
│  │                                                     │  │
│  │  ┌──────────────────┐  ┌──────────────────┐      │  │
│  │  │  nginx:alpine    │  │ backend:python   │      │  │
│  │  │                  │  │                  │      │  │
│  │  │  Port: 80        │  │ Port: 8000       │      │  │
│  │  │  → 映射到 8080    │  │ (内部端口)       │      │  │
│  │  └──────────────────┘  └──────────────────┘      │  │
│  │           │                      │                 │  │
│  └───────────┼──────────────────────┼─────────────────┘  │
│              │                      │                    │
│              ▼                      ▼                    │
│  ┌─────────────────────────────────────────────────┐   │
│  │              Docker Volumes                      │   │
│  │                                                   │   │
│  │  - ./data        → /app/data      (数据持久化)  │   │
│  │  - ./logs        → /app/logs      (日志)        │   │
│  │  - ./nginx.conf  → /etc/nginx     (配置)        │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### 6.2 生产环境架构 (可选)

```
                      ┌─────────────┐
                      │  CloudFlare │  CDN + DDoS防护
                      │     CDN     │
                      └──────┬──────┘
                             │
                    ┌────────▼────────┐
                    │   Load Balancer │  负载均衡
                    │    (Nginx)      │
                    └────────┬────────┘
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
    ┌─────▼────┐      ┌─────▼────┐      ┌─────▼────┐
    │ App Node │      │ App Node │      │ App Node │
    │    #1    │      │    #2    │      │    #3    │
    └─────┬────┘      └─────┬────┘      └─────┬────┘
          │                  │                  │
          └──────────────────┼──────────────────┘
                             │
                    ┌────────▼────────┐
                    │  Shared Storage │  共享存储 (NFS/OSS)
                    │   + Database    │
                    └─────────────────┘
```

## 7. 安全架构

### 7.1 安全层次

```
┌─────────────────────────────────────────┐
│         应用层安全 (Application)         │
│  - 输入验证                              │
│  - 输出编码                              │
│  - CSRF保护                             │
│  - XSS防护                              │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│          API层安全 (API)                 │
│  - Rate Limiting                        │
│  - 请求签名验证                          │
│  - JWT Token (可选)                     │
│  - API Key管理                          │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│         网络层安全 (Network)             │
│  - HTTPS/TLS                            │
│  - 防火墙规则                            │
│  - DDoS防护                             │
│  - IP白名单                             │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│       数据层安全 (Data)                  │
│  - 密钥加密存储                          │
│  - 数据库加密                            │
│  - 定期备份                              │
│  - 访问审计日志                          │
└─────────────────────────────────────────┘
```

## 8. 监控和日志

### 8.1 日志架构

```
应用日志 → Loguru → 文件 (app.log)
         ↓
      日志轮转 (按日期/大小)
         ↓
      日志聚合 (可选: ELK Stack)
         ↓
      日志分析和告警
```

### 8.2 监控指标

- **系统指标**: CPU, 内存, 磁盘, 网络
- **应用指标**: 请求数, 响应时间, 错误率
- **业务指标**: 生成任务数, 成功率, API配额使用
- **自定义指标**: 队列长度, 并发任务数

## 9. 扩展性设计

### 9.1 水平扩展方案

```
单机版 (Phase 1)
    ↓
添加Redis缓存
    ↓
多实例 + 负载均衡
    ↓
微服务化
```

### 9.2 性能优化点

1. **缓存策略**
   - Redis缓存热点数据
   - CDN缓存静态资源
   - 浏览器缓存策略

2. **异步处理**
   - Celery任务队列
   - WebSocket实时推送
   - 批量处理优化

3. **数据库优化**
   - 索引优化
   - 查询优化
   - 分库分表

---

**版本**: v1.0  
**最后更新**: 2024-01-01
