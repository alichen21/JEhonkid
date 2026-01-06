#!/bin/bash

# GitHub 仓库准备脚本
# 用于初始化 Git 仓库并准备推送到 GitHub

echo "============================================================"
echo "准备 GitHub 仓库"
echo "============================================================"

# 检查是否已经是 Git 仓库
if [ -d ".git" ]; then
    echo "✅ Git 仓库已初始化"
else
    echo "📦 初始化 Git 仓库..."
    git init
    echo "✅ Git 仓库初始化完成"
fi

# 检查是否有远程仓库
if git remote | grep -q "origin"; then
    echo "✅ 远程仓库已配置"
    git remote -v
else
    echo "⚠️  未配置远程仓库"
    echo ""
    echo "请按以下步骤操作："
    echo "1. 在 GitHub 上创建新仓库（https://github.com/new）"
    echo "2. 仓库名称建议：jkid 或 jkid-app"
    echo "3. 设置为公开仓库（Public）"
    echo "4. 不要初始化 README、.gitignore 或 license"
    echo ""
    read -p "请输入你的 GitHub 仓库 URL (例如: https://github.com/username/repo-name): " repo_url
    
    if [ -n "$repo_url" ]; then
        git remote add origin "$repo_url"
        echo "✅ 远程仓库已添加: $repo_url"
    else
        echo "⚠️  未输入仓库 URL，跳过远程仓库配置"
    fi
fi

echo ""
echo "============================================================"
echo "检查文件状态"
echo "============================================================"

# 检查是否有未提交的更改
if [ -n "$(git status --porcelain)" ]; then
    echo "📝 发现未提交的更改："
    git status --short
    
    echo ""
    read -p "是否现在提交所有更改？(y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git add .
        read -p "请输入提交信息（默认: Prepare for deployment）: " commit_msg
        commit_msg=${commit_msg:-"Prepare for deployment"}
        git commit -m "$commit_msg"
        echo "✅ 更改已提交"
    fi
else
    echo "✅ 没有未提交的更改"
fi

echo ""
echo "============================================================"
echo "准备推送到 GitHub"
echo "============================================================"

# 检查当前分支
current_branch=$(git branch --show-current 2>/dev/null || echo "main")
echo "当前分支: $current_branch"

if git remote | grep -q "origin"; then
    echo ""
    read -p "是否现在推送到 GitHub？(y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        # 设置默认分支为 main（如果当前分支不是 main）
        if [ "$current_branch" != "main" ]; then
            git branch -M main
            current_branch="main"
        fi
        
        echo "🚀 推送到 GitHub..."
        git push -u origin "$current_branch"
        
        if [ $? -eq 0 ]; then
            echo "✅ 推送成功！"
            echo ""
            echo "下一步："
            echo "1. 复制 deploy-config.json.example 为 deploy-config.json"
            echo "2. 编辑 deploy-config.json，填入你的仓库 URL 和服务名称"
            echo "3. 告诉 AI 助手：'请帮我部署到 space.ai_builder'"
        else
            echo "❌ 推送失败，请检查："
            echo "   - GitHub 仓库 URL 是否正确"
            echo "   - 是否有推送权限"
            echo "   - 网络连接是否正常"
        fi
    fi
else
    echo "⚠️  未配置远程仓库，无法推送"
    echo "请先运行此脚本配置远程仓库"
fi

echo ""
echo "============================================================"

