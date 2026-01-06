# 脚本文件说明

本目录包含项目使用的各种脚本文件。

## 脚本列表

### start_fastapi.sh
启动 FastAPI 后端服务。

**使用方法：**
```bash
./scripts/start_fastapi.sh
```

### restart_fastapi.sh
重启 FastAPI 后端服务（先停止现有服务，再启动）。

**使用方法：**
```bash
./scripts/restart_fastapi.sh
```

### check_services.sh
检查 FastAPI 后端和 Next.js 前端的运行状态。

**使用方法：**
```bash
./scripts/check_services.sh
```

## 注意事项

- 所有脚本都会自动切换到项目根目录执行
- 确保脚本有执行权限：`chmod +x scripts/*.sh`
- 脚本会检查并创建虚拟环境（如果需要）

