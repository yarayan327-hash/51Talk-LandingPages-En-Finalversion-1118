#!/bin/bash

# 51Talk 多语言落地页一键部署脚本
# 作者: 51Talk 部署工程助手
# 版本: 1.0

echo "🚀 开始 51Talk 多语言落地页部署..."
echo ""

# 检查当前目录
CURRENT_DIR=$(pwd)
EXPECTED_DIR="/Users/jin/landing-pages-deploy"

if [[ "$CURRENT_DIR" != "$EXPECTED_DIR" ]]; then
    echo "❌ 错误: 请在正确的目录中运行此脚本"
    echo "当前目录: $CURRENT_DIR"
    echo "期望目录: $EXPECTED_DIR"
    echo ""
    echo "请运行:"
    echo "cd /Users/jin/landing-pages-deploy"
    echo "./deploy.sh"
    exit 1
fi

echo "✅ 目录检查通过: $CURRENT_DIR"
echo ""

# 初始化 Git 仓库
echo "📝 步骤 1: 初始化 Git 仓库..."
if [ ! -d ".git" ]; then
    git init
    echo "✅ Git 仓库初始化完成"
else
    echo "ℹ️  Git 仓库已存在"
fi
echo ""

# 添加所有文件
echo "📦 步骤 2: 添加文件到 Git..."
git add .
echo "✅ 文件添加完成"
echo ""

# 提交文件
echo "💾 步骤 3: 提交文件..."
git commit -m "Initial deploy version - 51Talk multilingual landing pages

🎯 包含页面:
- SpeakUp.html (口语提升课程)
- GradeUp.html (成绩提升课程)
- ScoreBoost.html (分数提升课程)
- i18n-test-suite.html (多语言测试套件)
- page-template.html (新页面模板)

🌐 支持语言: 中文、英文、阿拉伯语

🤖 Generated with [Claude Code](https://claude.com/claude-code)
Co-Authored-By: Claude <noreply@anthropic.com>"
echo "✅ 文件提交完成"
echo ""

# 检查是否有远程仓库
if ! git remote get-url origin >/dev/null 2>&1; then
    echo "🔗 步骤 4: 配置远程仓库..."
    echo ""
    echo "📋 接下来您需要:"
    echo ""
    echo "1️⃣  在 GitHub 上创建新仓库:"
    echo "   - 访问 https://github.com/new"
    echo "   - 仓库名称建议: 51talk-landing-pages"
    echo "   - 选择 Public"
    echo "   - 不要添加 README、.gitignore 或 license"
    echo "   - 点击 'Create repository'"
    echo ""
    echo "2️⃣  添加远程仓库并推送:"
    read -p "请输入您的 GitHub 用户名: " GITHUB_USERNAME
    read -p "请输入仓库名称 (建议: 51talk-landing-pages): " REPO_NAME

    if [[ -z "$REPO_NAME" ]]; then
        REPO_NAME="51talk-landing-pages"
    fi

    REPO_URL="https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"

    echo ""
    echo "🔧 添加远程仓库..."
    git remote add origin "$REPO_URL"

    echo "📤 推送到 GitHub..."
    git push -u origin main

    if [[ $? -eq 0 ]]; then
        echo ""
        echo "🎉 代码推送成功!"
        echo "📍 仓库地址: https://github.com/$GITHUB_USERNAME/$REPO_NAME"
    else
        echo ""
        echo "❌ 推送失败，请检查:"
        echo "   - GitHub 用户名是否正确"
        echo "   - 仓库名称是否正确"
        echo "   - 是否有 GitHub 访问权限"
        echo ""
        echo "您可以手动推送:"
        echo "git push -u origin main"
    fi
else
    echo "ℹ️  远程仓库已存在"
    echo ""
    echo "📤 推送到远程仓库..."
    git push origin main
fi

echo ""
echo "🌐 步骤 5: Vercel 部署指南..."
echo ""
echo "📋 接下来请在 Vercel 上部署:"
echo ""
echo "1️⃣  登录 Vercel:"
echo "   - 访问 https://vercel.com"
echo "   - 点击 'Login' → 使用 GitHub 账号登录"
echo ""
echo "2️⃣  导入项目:"
echo "   - 点击 'Add New...' → 'Project'"
echo "   - 选择刚才的 GitHub 仓库"
echo "   - 点击 'Import'"
echo ""
echo "3️⃣  配置部署:"
echo "   - Framework Preset: Other"
echo "   - Root Directory: . (保持默认)"
echo "   - Output Directory: public"
echo "   - Install Command: (留空)"
echo "   - Build Command: (留空)"
echo "   - 点击 'Deploy'"
echo ""
echo "4️⃣  等待部署完成 (通常 1-2 分钟)"
echo ""

# 预期的访问链接
GITHUB_USERNAME=$(git config user.name || echo "YOUR_USERNAME")
REPO_NAME=$(git remote get-url origin 2>/dev/null | sed 's/.*\/\([^\/]*\)\.git/\1/' || echo "51talk-landing-pages")

echo "🔗 预期的线上访问链接:"
echo "   - SpeakUp: https://$REPO_NAME.vercel.app/SpeakUp.html"
echo "   - GradeUp: https://$REPO_NAME.vercel.app/GradeUp.html"
echo "   - ScoreBoost: https://$REPO_NAME.vercel.app/ScoreBoost.html"
echo "   - 测试套件: https://$REPO_NAME.vercel.app/i18n-test-suite.html"
echo ""

echo "✅ 部署脚本执行完成!"
echo "🎯 现在请按照上述指南在 GitHub 和 Vercel 上完成部署"
echo ""
echo "如有问题，请查看 README_DEPLOY.md 获取详细帮助"