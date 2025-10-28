# 🎨 UI/UX 设计方案

## 1. 设计理念

### 1.1 核心原则
- **简洁直观**: 主要功能一目了然，操作流程简单明了
- **美观现代**: 遵循现代设计趋势，使用流行的设计元素
- **响应式**: 完美适配各种屏幕尺寸
- **高效快捷**: 减少点击次数，提供快捷操作
- **视觉反馈**: 清晰的状态提示和交互反馈

### 1.2 设计目标
- 用户无需培训即可上手
- 3 步完成图像生成
- 响应时间感知 < 1 秒
- 错误信息清晰易懂

## 2. 配色方案

### 2.1 浅色主题 (Light Mode)

```css
/* 主色调 */
--primary: #3B82F6;        /* 蓝色 - 主要按钮和链接 */
--primary-hover: #2563EB;  /* 蓝色悬停态 */
--primary-light: #DBEAFE;  /* 蓝色浅色背景 */

/* 辅助色 */
--secondary: #8B5CF6;      /* 紫色 - 次要元素 */
--accent: #10B981;         /* 绿色 - 成功状态 */
--warning: #F59E0B;        /* 橙色 - 警告 */
--error: #EF4444;          /* 红色 - 错误 */

/* 背景色 */
--bg-primary: #FFFFFF;     /* 主背景 */
--bg-secondary: #F9FAFB;   /* 次要背景 */
--bg-tertiary: #F3F4F6;    /* 三级背景 */

/* 文字色 */
--text-primary: #111827;   /* 主要文字 */
--text-secondary: #6B7280; /* 次要文字 */
--text-tertiary: #9CA3AF;  /* 三级文字 */

/* 边框色 */
--border: #E5E7EB;         /* 默认边框 */
--border-light: #F3F4F6;   /* 浅色边框 */
```

### 2.2 深色主题 (Dark Mode)

```css
/* 主色调 */
--primary: #60A5FA;        /* 蓝色 - 主要按钮和链接 */
--primary-hover: #3B82F6;  /* 蓝色悬停态 */
--primary-light: #1E3A8A;  /* 蓝色深色背景 */

/* 辅助色 */
--secondary: #A78BFA;      /* 紫色 */
--accent: #34D399;         /* 绿色 */
--warning: #FBBF24;        /* 橙色 */
--error: #F87171;          /* 红色 */

/* 背景色 */
--bg-primary: #111827;     /* 主背景 */
--bg-secondary: #1F2937;   /* 次要背景 */
--bg-tertiary: #374151;    /* 三级背景 */

/* 文字色 */
--text-primary: #F9FAFB;   /* 主要文字 */
--text-secondary: #D1D5DB; /* 次要文字 */
--text-tertiary: #9CA3AF;  /* 三级文字 */

/* 边框色 */
--border: #374151;         /* 默认边框 */
--border-light: #4B5563;   /* 浅色边框 */
```

## 3. 布局设计

### 3.1 桌面端布局 (≥1024px)

```
┌─────────────────────────────────────────────────────────────┐
│ Header (h: 64px)                                            │
│ ┌─────────┐ VolcEngine Image Gen    [Dark] [Settings] [?] │
│ │  Logo   │                                                 │
│ └─────────┘                                                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ ┌────────────┬──────────────────────┬────────────────────┐ │
│ │            │                      │                    │ │
│ │  Sidebar   │    Main Content      │   History Panel   │ │
│ │            │                      │                    │ │
│ │  (300px)   │     (Flexible)       │     (320px)       │ │
│ │            │                      │                    │ │
│ │ ┌────────┐ │  ┌──────────────┐   │  ┌──────────────┐ │ │
│ │ │ Prompt │ │  │              │   │  │   Recent     │ │ │
│ │ │  Box   │ │  │  Image Grid  │   │  │   Tasks      │ │ │
│ │ └────────┘ │  │   (2x2/3x3)  │   │  │              │ │ │
│ │            │  │              │   │  └──────────────┘ │ │
│ │ ┌────────┐ │  └──────────────┘   │                    │ │
│ │ │ Params │ │                      │  ┌──────────────┐ │ │
│ │ │        │ │  ┌──────────────┐   │  │   History    │ │ │
│ │ └────────┘ │  │  Loading...  │   │  │   Items      │ │ │
│ │            │  └──────────────┘   │  │              │ │ │
│ │ ┌────────┐ │                      │  └──────────────┘ │ │
│ │ │Generate│ │                      │                    │ │
│ │ │ Button │ │                      │                    │ │
│ │ └────────┘ │                      │                    │ │
│ └────────────┴──────────────────────┴────────────────────┘ │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│ Footer (h: 40px)                                            │
│ Status: Connected | Quota: 450/1000 | v1.0.0              │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 平板端布局 (768px - 1023px)

```
┌─────────────────────────────────────┐
│ Header                              │
├─────────────────────────────────────┤
│ ┌─────────────┐                     │
│ │   Sidebar   │                     │
│ │  (Expanded) │                     │
│ └─────────────┘                     │
│ ┌─────────────────────────────────┐ │
│ │       Main Content              │ │
│ │       (Full Width)              │ │
│ │   ┌──────────────┐              │ │
│ │   │ Image Grid   │              │ │
│ │   │   (2x2)      │              │ │
│ │   └──────────────┘              │ │
│ └─────────────────────────────────┘ │
│ ┌─────────────────────────────────┐ │
│ │   History (Collapsible)         │ │
│ └─────────────────────────────────┘ │
└─────────────────────────────────────┘
```

### 3.3 移动端布局 (<768px)

```
┌─────────────────────┐
│ Header (Compact)    │
│ ☰  VolcEngine  🌙  │
├─────────────────────┤
│                     │
│  ┌───────────────┐  │
│  │    Prompt     │  │
│  └───────────────┘  │
│                     │
│  ┌───────────────┐  │
│  │   [Generate]  │  │
│  └───────────────┘  │
│                     │
│  ┌───────────────┐  │
│  │               │  │
│  │  Image Stack  │  │
│  │   (Vertical)  │  │
│  │               │  │
│  └───────────────┘  │
│                     │
│  [Show History]     │
│                     │
└─────────────────────┘
```

## 4. 组件设计

### 4.1 主要组件

#### 导航栏 (Header)
```html
<header class="h-16 bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-700">
  <div class="flex items-center justify-between h-full px-6">
    <!-- Logo -->
    <div class="flex items-center gap-3">
      <img src="/static/images/logo.svg" alt="Logo" class="w-8 h-8">
      <h1 class="text-xl font-bold text-gray-900 dark:text-white">
        VolcEngine Image Generator
      </h1>
    </div>
    
    <!-- Actions -->
    <div class="flex items-center gap-4">
      <!-- Theme Toggle -->
      <button class="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800">
        <svg><!-- Moon/Sun Icon --></svg>
      </button>
      
      <!-- Settings -->
      <button class="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800">
        <svg><!-- Settings Icon --></svg>
      </button>
      
      <!-- Help -->
      <button class="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800">
        <svg><!-- Help Icon --></svg>
      </button>
    </div>
  </div>
</header>
```

#### 提示词输入框
```html
<div class="space-y-3">
  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
    提示词 (Prompt) *
  </label>
  <textarea 
    rows="4"
    placeholder="描述你想生成的图像，例如：一只可爱的橘猫坐在窗台上，阳光透过窗户..."
    class="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg
           focus:ring-2 focus:ring-blue-500 focus:border-transparent
           bg-white dark:bg-gray-800 text-gray-900 dark:text-white
           placeholder-gray-400 dark:placeholder-gray-500
           resize-none transition-all"
  ></textarea>
  <div class="flex items-center justify-between text-xs text-gray-500">
    <span>建议详细描述场景、风格、光线等元素</span>
    <span class="font-mono">0 / 1000</span>
  </div>
</div>
```

#### 参数配置面板
```html
<div class="space-y-4 p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
  <!-- Model Selection -->
  <div>
    <label class="block text-sm font-medium mb-2">AI 模型</label>
    <select class="w-full px-3 py-2 border rounded-lg">
      <option value="general_v2.0">通用模型 v2.0 (推荐)</option>
      <option value="anime_v1.0">动漫风格 v1.0</option>
      <option value="realistic_v1.5">写实风格 v1.5</option>
    </select>
  </div>
  
  <!-- Image Size -->
  <div>
    <label class="block text-sm font-medium mb-2">图像尺寸</label>
    <div class="grid grid-cols-3 gap-2">
      <button class="size-btn active">1:1<br><span>1024×1024</span></button>
      <button class="size-btn">16:9<br><span>1920×1080</span></button>
      <button class="size-btn">9:16<br><span>1080×1920</span></button>
    </div>
  </div>
  
  <!-- Number of Images -->
  <div>
    <label class="block text-sm font-medium mb-2">
      生成数量: <span class="font-bold text-blue-600">2</span>
    </label>
    <input type="range" min="1" max="4" value="2" 
           class="w-full accent-blue-600">
    <div class="flex justify-between text-xs text-gray-500 mt-1">
      <span>1</span>
      <span>2</span>
      <span>3</span>
      <span>4</span>
    </div>
  </div>
  
  <!-- Advanced Options (Collapsible) -->
  <details class="group">
    <summary class="cursor-pointer text-sm font-medium text-blue-600 hover:text-blue-700">
      高级参数 ▼
    </summary>
    <div class="mt-3 space-y-3">
      <!-- Steps -->
      <div>
        <label class="text-sm">采样步数: <span>20</span></label>
        <input type="range" min="10" max="50" value="20" class="w-full">
      </div>
      
      <!-- Scale -->
      <div>
        <label class="text-sm">引导系数: <span>7.5</span></label>
        <input type="range" min="1" max="20" value="7.5" step="0.5" class="w-full">
      </div>
      
      <!-- Seed -->
      <div>
        <label class="text-sm">随机种子 (可选)</label>
        <input type="number" placeholder="留空自动生成" 
               class="w-full px-3 py-2 border rounded-lg">
      </div>
      
      <!-- Negative Prompt -->
      <div>
        <label class="text-sm">负面提示词</label>
        <textarea rows="2" 
                  placeholder="不想出现的内容，如：模糊、低质量、变形..."
                  class="w-full px-3 py-2 border rounded-lg text-sm"></textarea>
      </div>
    </div>
  </details>
</div>
```

#### 生成按钮
```html
<button 
  class="w-full py-4 px-6 
         bg-gradient-to-r from-blue-600 to-blue-700 
         hover:from-blue-700 hover:to-blue-800
         text-white font-semibold text-lg rounded-lg
         transform active:scale-95 transition-all duration-200
         shadow-lg hover:shadow-xl
         disabled:opacity-50 disabled:cursor-not-allowed
         flex items-center justify-center gap-3">
  <svg class="w-6 h-6"><!-- Sparkles Icon --></svg>
  <span>生成图像</span>
</button>

<!-- Loading State -->
<button class="..." disabled>
  <svg class="animate-spin w-6 h-6"><!-- Spinner --></svg>
  <span>生成中... 45%</span>
</button>
```

#### 图片网格展示
```html
<div class="grid grid-cols-2 lg:grid-cols-3 gap-4">
  <!-- Image Card -->
  <div class="group relative aspect-square rounded-lg overflow-hidden 
              border border-gray-200 dark:border-gray-700
              hover:shadow-xl transition-all duration-300">
    <!-- Image -->
    <img src="..." alt="Generated Image" 
         class="w-full h-full object-cover">
    
    <!-- Overlay on Hover -->
    <div class="absolute inset-0 bg-black bg-opacity-0 
                group-hover:bg-opacity-40 transition-all duration-300
                flex items-center justify-center opacity-0 group-hover:opacity-100">
      <!-- Actions -->
      <div class="flex gap-2">
        <button class="action-btn" title="预览">
          <svg><!-- Eye Icon --></svg>
        </button>
        <button class="action-btn" title="下载">
          <svg><!-- Download Icon --></svg>
        </button>
        <button class="action-btn" title="删除">
          <svg><!-- Trash Icon --></svg>
        </button>
      </div>
    </div>
    
    <!-- Loading Placeholder -->
    <div class="absolute inset-0 bg-gray-100 dark:bg-gray-800 
                animate-pulse flex items-center justify-center">
      <svg class="animate-spin w-12 h-12 text-blue-600">
        <!-- Spinner -->
      </svg>
    </div>
  </div>
</div>
```

#### 历史记录面板
```html
<div class="h-full flex flex-col">
  <!-- Header -->
  <div class="flex items-center justify-between p-4 border-b">
    <h3 class="font-semibold text-gray-900 dark:text-white">历史记录</h3>
    <button class="text-sm text-blue-600 hover:text-blue-700">清空</button>
  </div>
  
  <!-- Recent Tasks -->
  <div class="p-4 space-y-3">
    <h4 class="text-xs font-medium text-gray-500 uppercase">当前任务</h4>
    <!-- Task Item -->
    <div class="p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200">
      <div class="flex items-center justify-between mb-2">
        <span class="text-sm font-medium">生成中...</span>
        <span class="text-xs text-blue-600">45%</span>
      </div>
      <div class="h-2 bg-blue-200 rounded-full overflow-hidden">
        <div class="h-full bg-blue-600 transition-all" style="width: 45%"></div>
      </div>
      <p class="text-xs text-gray-600 mt-2 truncate">
        一只可爱的橘猫坐在窗台上...
      </p>
    </div>
  </div>
  
  <!-- History List -->
  <div class="flex-1 overflow-y-auto p-4 space-y-3">
    <h4 class="text-xs font-medium text-gray-500 uppercase">最近生成</h4>
    <!-- History Item -->
    <div class="history-item group cursor-pointer 
                p-3 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800
                border border-transparent hover:border-gray-200">
      <div class="flex gap-3">
        <!-- Thumbnail -->
        <img src="..." class="w-16 h-16 rounded object-cover">
        <!-- Info -->
        <div class="flex-1 min-w-0">
          <p class="text-sm font-medium truncate">一只可爱的橘猫...</p>
          <p class="text-xs text-gray-500">2 张图片</p>
          <p class="text-xs text-gray-400">5分钟前</p>
        </div>
        <!-- Action -->
        <button class="opacity-0 group-hover:opacity-100 transition-opacity">
          <svg class="w-5 h-5 text-gray-400 hover:text-blue-600">
            <!-- Reload Icon -->
          </svg>
        </button>
      </div>
    </div>
  </div>
</div>
```

#### Toast 通知
```html
<div class="fixed top-4 right-4 z-50 space-y-2">
  <!-- Success Toast -->
  <div class="toast toast-success animate-slide-in-right">
    <div class="flex items-center gap-3 p-4 bg-white dark:bg-gray-800 
                rounded-lg shadow-lg border-l-4 border-green-500">
      <svg class="w-6 h-6 text-green-500"><!-- Check Icon --></svg>
      <div>
        <p class="font-medium text-gray-900 dark:text-white">生成成功！</p>
        <p class="text-sm text-gray-600">图片已保存到历史记录</p>
      </div>
      <button class="ml-auto text-gray-400 hover:text-gray-600">
        <svg><!-- X Icon --></svg>
      </button>
    </div>
  </div>
  
  <!-- Error Toast -->
  <div class="toast toast-error">
    <div class="flex items-center gap-3 p-4 bg-white rounded-lg shadow-lg 
                border-l-4 border-red-500">
      <svg class="w-6 h-6 text-red-500"><!-- Alert Icon --></svg>
      <div>
        <p class="font-medium text-gray-900">生成失败</p>
        <p class="text-sm text-gray-600">API 配额已用尽</p>
      </div>
    </div>
  </div>
</div>
```

#### 模态框 (图片预览)
```html
<div class="fixed inset-0 z-50 flex items-center justify-center p-4 
            bg-black bg-opacity-75 animate-fade-in">
  <!-- Modal Content -->
  <div class="relative max-w-6xl w-full bg-white dark:bg-gray-900 
              rounded-xl shadow-2xl animate-scale-in">
    <!-- Close Button -->
    <button class="absolute top-4 right-4 p-2 rounded-full 
                   bg-gray-100 dark:bg-gray-800 hover:bg-gray-200">
      <svg><!-- X Icon --></svg>
    </button>
    
    <!-- Image -->
    <div class="p-6">
      <img src="..." alt="Preview" 
           class="w-full h-auto max-h-[80vh] object-contain rounded-lg">
    </div>
    
    <!-- Info & Actions -->
    <div class="p-6 border-t border-gray-200 dark:border-gray-700">
      <div class="flex items-center justify-between">
        <div>
          <h3 class="font-semibold text-gray-900 dark:text-white">
            一只可爱的橘猫坐在窗台上
          </h3>
          <p class="text-sm text-gray-600">
            模型: general_v2.0 | 尺寸: 1024×1024 | 生成时间: 23秒
          </p>
        </div>
        <div class="flex gap-2">
          <button class="btn-secondary">复制提示词</button>
          <button class="btn-primary">下载图片</button>
        </div>
      </div>
    </div>
  </div>
</div>
```

## 5. 交互设计

### 5.1 操作流程

```
用户访问 → 展示主界面
    ↓
输入提示词 → 实时字数统计
    ↓
调整参数 → 参数预览
    ↓
点击生成 → 按钮变为加载状态
    ↓
创建任务 → Toast 提示"任务已创建"
    ↓
开始轮询 → 右侧面板显示任务进度
    ↓
生成完成 → 图片淡入动画展示
    ↓
用户操作 → 预览/下载/重新生成
```

### 5.2 动画效果

```css
/* 淡入动画 */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* 滑入动画 */
@keyframes slideInRight {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

/* 缩放动画 */
@keyframes scaleIn {
  from {
    transform: scale(0.9);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}

/* 脉冲动画 (加载) */
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

/* 旋转动画 (Spinner) */
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* 进度条填充动画 */
@keyframes progressFill {
  from { width: 0%; }
  to { width: var(--progress); }
}
```

### 5.3 状态反馈

| 状态 | 视觉反馈 | 用户提示 |
|------|----------|----------|
| **空闲** | 按钮正常 | "点击生成图像" |
| **加载** | Spinner + 进度 | "生成中... 45%" |
| **成功** | 绿色Toast + 淡入 | "生成成功！" |
| **失败** | 红色Toast | "生成失败: 原因" |
| **队列中** | 橙色徽章 | "队列中，等待处理" |

### 5.4 错误处理

```javascript
// 错误类型和对应的用户友好提示
const errorMessages = {
  'network_error': '网络连接失败，请检查网络设置',
  'api_quota_exceeded': 'API 配额已用尽，请稍后再试',
  'invalid_params': '参数设置有误，请检查输入',
  'content_policy': '提示词包含敏感内容，请修改后重试',
  'timeout': '请求超时，请重试',
  'server_error': '服务器错误，请稍后再试'
};

// 显示错误
function showError(errorType, details) {
  const message = errorMessages[errorType] || '未知错误';
  showToast('error', message, details);
  
  // 记录到控制台供调试
  console.error('[Error]', errorType, details);
}
```

## 6. 响应式断点

```css
/* 移动端优先 */
.container {
  padding: 1rem;
}

/* 平板端 (≥768px) */
@media (min-width: 768px) {
  .container {
    padding: 1.5rem;
  }
  .grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* 桌面端 (≥1024px) */
@media (min-width: 1024px) {
  .container {
    padding: 2rem;
  }
  .grid {
    grid-template-columns: repeat(3, 1fr);
  }
  .sidebar {
    display: block;
  }
}

/* 大屏幕 (≥1280px) */
@media (min-width: 1280px) {
  .grid {
    grid-template-columns: repeat(4, 1fr);
  }
}
```

## 7. 可访问性 (Accessibility)

### 7.1 键盘导航
- Tab: 聚焦下一个可交互元素
- Shift + Tab: 聚焦上一个元素
- Enter: 激活按钮/提交表单
- Esc: 关闭模态框

### 7.2 ARIA 标签
```html
<button aria-label="生成图像" aria-busy="false">
  生成图像
</button>

<div role="progressbar" aria-valuenow="45" aria-valuemin="0" aria-valuemax="100">
  <div style="width: 45%"></div>
</div>

<div role="alert" aria-live="polite">
  图片生成成功
</div>
```

### 7.3 对比度
- 文字与背景对比度 ≥ 4.5:1 (正常文字)
- 文字与背景对比度 ≥ 3:1 (大文字 ≥18px)
- 交互元素对比度 ≥ 3:1

## 8. 性能优化

### 8.1 图片优化
- 使用 WebP 格式
- 懒加载图片
- 生成缩略图
- 渐进式加载

### 8.2 资源加载
```html
<!-- 预加载关键资源 -->
<link rel="preload" href="/static/css/main.css" as="style">
<link rel="preload" href="/static/js/app.js" as="script">

<!-- 预连接外部资源 -->
<link rel="preconnect" href="https://cdn.tailwindcss.com">
<link rel="dns-prefetch" href="https://unpkg.com">

<!-- 异步加载非关键资源 -->
<script src="analytics.js" async></script>
```

### 8.3 首屏优化
- 关键CSS内联
- 骨架屏加载
- 资源压缩
- 启用 Gzip/Brotli

## 9. 用户体验细节

### 9.1 微交互
- 按钮点击缩放效果
- 图片悬停放大
- 平滑滚动
- 页面切换动画

### 9.2 加载状态
- 骨架屏
- Spinner
- 进度条
- 占位符图片

### 9.3 空状态
```html
<div class="empty-state text-center py-12">
  <svg class="w-24 h-24 mx-auto text-gray-300">
    <!-- Empty Icon -->
  </svg>
  <h3 class="mt-4 text-lg font-medium text-gray-900">
    还没有生成图片
  </h3>
  <p class="mt-2 text-sm text-gray-600">
    输入提示词，开始你的第一次创作吧！
  </p>
  <button class="mt-6 btn-primary">
    开始生成
  </button>
</div>
```

## 10. UI 组件库

使用 Tailwind CSS 预设组件：

```css
/* 按钮 */
.btn-primary {
  @apply px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white 
         font-medium rounded-lg transition-colors;
}

.btn-secondary {
  @apply px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 
         font-medium rounded-lg transition-colors;
}

/* 输入框 */
.input {
  @apply w-full px-4 py-2 border border-gray-300 rounded-lg
         focus:ring-2 focus:ring-blue-500 focus:border-transparent
         transition-all;
}

/* 卡片 */
.card {
  @apply bg-white dark:bg-gray-800 rounded-lg shadow-md 
         border border-gray-200 dark:border-gray-700;
}

/* 徽章 */
.badge {
  @apply inline-flex items-center px-2.5 py-0.5 rounded-full
         text-xs font-medium;
}

.badge-success {
  @apply bg-green-100 text-green-800;
}

.badge-warning {
  @apply bg-yellow-100 text-yellow-800;
}

.badge-error {
  @apply bg-red-100 text-red-800;
}
```

---

**设计版本**: v1.0  
**最后更新**: 2024-01-01  
**设计工具**: Figma (可选)
