# Next.js 前端应用

这是 JKid 项目的 Next.js 前端应用。

## 🚀 快速开始

### 1. 安装依赖

```bash
cd frontend
npm install
# 或
yarn install
# 或
pnpm install
```

### 2. 配置环境变量

复制 `.env.local.example` 为 `.env.local` 并配置：

```bash
cp .env.local.example .env.local
```

编辑 `.env.local`，设置 FastAPI 后端地址：

```
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

### 3. 启动开发服务器

```bash
npm run dev
# 或
yarn dev
# 或
pnpm dev
```

访问 http://localhost:3000

## 📁 项目结构

```
frontend/
├── app/                    # Next.js App Router 页面
│   ├── layout.tsx          # 根布局
│   ├── page.tsx            # 主页
│   └── upload/             # 上传页面
│       └── page.tsx
├── components/             # React 组件
│   ├── ResultCard.tsx      # 结果卡片
│   ├── StatsCards.tsx      # 统计卡片
│   ├── ProcessedTextSection.tsx  # 处理文本部分
│   ├── UploadProgress.tsx  # 上传进度
│   └── UploadResult.tsx   # 上传结果
├── lib/                    # 工具库
│   ├── api.ts              # API 客户端
│   └── hooks/              # React Hooks
│       ├── useTaskPolling.ts  # 任务轮询 Hook
│       └── useTTS.ts       # TTS Hook
├── styles/                 # 样式文件
│   └── globals.css         # 全局样式
└── public/                 # 静态文件
```

## 🔧 配置

### API 地址配置

在 `.env.local` 中设置 `NEXT_PUBLIC_API_URL`，指向 FastAPI 后端地址。

### Next.js 配置

`next.config.js` 中配置了 API 代理，将 `/api/*` 和 `/images/*` 请求代理到 FastAPI 后端。

## 📝 功能特性

- ✅ 图片上传和预览
- ✅ OCR 识别结果展示
- ✅ LLM 文本处理结果展示
- ✅ TTS 音频生成和播放
- ✅ 任务进度实时更新
- ✅ 响应式设计

## 🏗️ 构建生产版本

```bash
npm run build
npm start
```

## 📚 相关文档

- [Next.js 文档](https://nextjs.org/docs)
- [React 文档](https://react.dev)
- [FastAPI 后端文档](../FASTAPI_MIGRATION.md)

