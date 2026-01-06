# 项目架构分析报告

## 📋 项目概述

**JKid** - 亲子日语可理解输入助手
- 功能：通过拍照识别绘本中的日语内容，转换为可听、可懂的输入
- 架构：FastAPI 后端 + Next.js 前端

---

## 🏗️ 核心架构

### 后端架构（FastAPI）

```
app_fastapi.py (主应用)
├── picture_to_text.py      # OCR模块（Google Cloud Vision API）
├── text_processor.py       # 文本处理模块（LLM清理和翻译）
├── text_to_speech.py       # TTS模块（Google Cloud TTS API）
└── task_manager.py         # 任务管理器（内存存储）
```

**数据流：**
1. 用户上传图片 → `/api/upload`
2. 创建任务 → `task_manager.create_task()`
3. 后台处理线程：
   - OCR识别 → `picture_to_text.extract_text()`
   - 文本处理 → `text_processor.process_ocr_text()`
   - TTS生成 → `text_to_speech.synthesize_japanese()`
4. 轮询任务状态 → `/api/task/{task_id}`

### 前端架构（Next.js）

```
frontend/
├── app/                    # Next.js App Router
│   ├── page.tsx           # 主页面
│   ├── upload/page.tsx    # 上传页面
│   └── api/images/        # API路由
├── components/             # React组件
│   ├── CameraCapture.tsx
│   ├── UploadProgress.tsx
│   ├── ProcessedTextSection.tsx
│   └── ...
└── lib/                    # 工具库
    ├── api.ts             # API客户端
    └── hooks/             # React Hooks
```

---

## 📁 文件分类

### ✅ 核心文件（必须保留）

**后端核心：**
- `app_fastapi.py` - FastAPI主应用
- `picture_to_text.py` - OCR功能
- `text_processor.py` - 文本处理
- `text_to_speech.py` - TTS功能
- `task_manager.py` - 任务管理

**前端核心：**
- `frontend/` - Next.js应用（整个目录）

**配置文件：**
- `requirements.txt` - Python依赖
- `Dockerfile` - Docker配置
- `deploy-config.json.example` - 部署配置示例
- `.gitignore` - Git忽略规则

**启动脚本（实用）：**
- `start_fastapi.sh` - 启动FastAPI服务
- `restart_fastapi.sh` - 重启FastAPI服务
- `check_services.sh` - 检查服务状态

**文档（重要）：**
- `README.md` - 项目主文档

---

### ⚠️ 测试文件（可选保留）

**保留建议：**
- `test_ocr.py` - OCR功能测试（保留，用于调试）
- `test_fastapi.py` - FastAPI后端测试（保留，用于调试）
- `test_segmentation.py` - 分段功能测试（保留，用于调试）

**可删除：**
- `test_segmentation_simple.py` - 与 `test_segmentation.py` 功能重复

---

### ❌ 不需要的文件（建议删除）

#### 1. 示例文件
- `example_usage.py` - 仅展示如何使用.env，未被引用

#### 2. 迁移/清理文档（历史文档）
- `CLEANUP_PLAN.md` - 清理计划（已完成）
- `CLEANUP_SUMMARY.md` - 清理总结（已完成）
- `FASTAPI_MIGRATION.md` - FastAPI迁移文档（已完成）
- `NEXTJS_MIGRATION.md` - Next.js迁移文档（已完成）
- `CONNECTION_EXPLAINED.md` - 连接说明（调试文档）
- `DEBUG_UPLOAD.md` - 上传调试文档（调试文档）

#### 3. 过时的启动指南
- `START_NEXTJS.md` - Next.js启动指南（信息可能已过时）
- `START_SERVICES.md` - 服务启动指南（信息可能已过时）
- `QUICK_START.md` - 快速开始（可能与README重复）
- `QUICK_TEST_GUIDE.md` - 快速测试指南（可能与README重复）

#### 4. 其他文档
- `GITHUB_SETUP.md` - GitHub设置（一次性文档）
- `TEST_CHECKLIST.md` - 测试清单（可能已过时）
- `UPLOAD_FEATURE.md` - 上传功能文档（功能已实现）
- `DEPLOYMENT.md` - 部署文档（可能与README重复）
- `DEPLOYMENT_READY.md` - 部署就绪（状态文档）
- `PRODUCT_BRIEF.md` - 产品简介（可能与README重复）

#### 5. 一次性脚本
- `prepare-github.sh` - GitHub准备脚本（一次性使用）

#### 6. 测试文件
- `test_audio.mp3` - 测试音频文件（可删除）

#### 7. 配置文件（需确认）
- `deploy-config.json` - 实际部署配置（如果包含敏感信息，应删除或添加到.gitignore）

---

## 🔍 依赖关系分析

### 核心模块依赖图

```
app_fastapi.py
├── picture_to_text.py (独立)
├── text_processor.py (独立)
├── text_to_speech.py (独立)
└── task_manager.py (独立)

所有测试文件都是独立的，不依赖其他测试文件
```

### 未使用的文件

- `example_usage.py` - 未被任何文件导入或引用
- 所有测试文件 - 仅用于手动测试，不被主应用引用

---

## 📊 文件统计

| 类别 | 数量 | 状态 |
|------|------|------|
| 核心Python文件 | 5 | ✅ 保留 |
| 测试文件 | 4 | ⚠️ 保留3个，删除1个 |
| 文档文件 | 15+ | ❌ 建议删除大部分 |
| 脚本文件 | 4 | ✅ 保留3个，删除1个 |
| 配置文件 | 4 | ✅ 保留 |

---

## 🎯 清理建议

### 立即删除（安全）
1. `example_usage.py`
2. `test_segmentation_simple.py`
3. `test_audio.mp3`
4. 所有迁移/清理文档（`*_MIGRATION.md`, `CLEANUP_*.md`）
5. `prepare-github.sh`

### 评估后删除（建议）
1. 过时的启动指南文档
2. 重复的快速开始文档
3. 一次性调试文档

### 保留但整理
1. 将重要信息合并到 `README.md`
2. 保留 `DEPLOYMENT.md` 如果包含重要部署信息
3. 测试文件可以移到 `tests/` 目录（如果项目规模扩大）

---

## 💡 架构优化建议

### 1. 目录结构优化
```
JKid/
├── backend/              # 后端代码
│   ├── app_fastapi.py
│   ├── picture_to_text.py
│   ├── text_processor.py
│   ├── text_to_speech.py
│   └── task_manager.py
├── frontend/            # 前端代码（已存在）
├── tests/               # 测试文件
│   ├── test_ocr.py
│   ├── test_fastapi.py
│   └── test_segmentation.py
├── scripts/             # 脚本文件
│   ├── start_fastapi.sh
│   ├── restart_fastapi.sh
│   └── check_services.sh
└── docs/                # 文档（如果需要）
    └── README.md
```

### 2. 任务管理器改进
- 当前使用内存存储，建议考虑持久化（Redis/数据库）
- 添加任务清理机制（已有基础实现）

### 3. 错误处理
- 统一错误处理格式
- 添加日志记录

### 4. 配置管理
- 使用环境变量统一管理配置
- 添加配置验证

---

## ✅ 总结

**项目架构清晰，核心功能完整。主要问题是：**
1. 大量历史文档文件需要清理
2. 测试文件可以更好地组织
3. 目录结构可以进一步优化

**建议优先清理文档文件，保持项目整洁。**

