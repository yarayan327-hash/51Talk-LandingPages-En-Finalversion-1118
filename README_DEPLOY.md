# 51Talk 多语言落地页 - 部署指南

## 🌟 项目简介

这是 51Talk Academy 的多语言落地页项目部署版本，支持中文、英文和阿拉伯语三种语言。

### 📱 包含的页面

- **SpeakUp.html** - SpeakUp 口语提升课程页面
- **GradeUp.html** - GradeUp 成绩提升课程页面
- **ScoreBoost.html** - ScoreBoost 分数提升课程页面
- **i18n-test-suite.html** - 多语言功能测试套件
- **page-template.html** - 新页面模板

## 🚀 本地运行

### 方法 1: 使用 Python (推荐)
```bash
# 进入项目目录
cd /Users/jin/landing-pages-deploy

# 启动本地服务器
python3 -m http.server 8080
```

### 方法 2: 使用 Node.js
```bash
# 安装 http-server (如果没有安装)
npm install -g http-server

# 启动服务器
http-server -p 8080
```

### 本地访问地址
- 主页: http://localhost:8080/SpeakUp.html
- GradeUp: http://localhost:8080/GradeUp.html
- ScoreBoost: http://localhost:8080/ScoreBoost.html
- 测试套件: http://localhost:8080/i18n-test-suite.html
- 页面模板: http://localhost:8080/page-template.html

## 📋 部署到 GitHub + Vercel

### 步骤 1: 初始化 GitHub 仓库

```bash
# 进入部署目录
cd /Users/jin/landing-pages-deploy

# 初始化 Git 仓库
git init

# 添加所有文件
git add .

# 提交初始版本
git commit -m "Initial deploy version - 51Talk multilingual landing pages"
```

### 步骤 2: 推送到 GitHub

#### 方法 A: 使用命令行
```bash
# 添加远程仓库 (替换 YOUR_USERNAME 和 REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# 推送到 GitHub
git push -u origin main
```

#### 方法 B: 使用 GitHub Desktop
1. 打开 GitHub Desktop
2. 选择 "Add Local Repository"
3. 选择 `/Users/jin/landing-pages-deploy` 目录
4. 点击 "Publish repository"
5. 输入仓库名称，选择 Public，点击 "Publish"

### 步骤 3: 在 Vercel 部署

1. **登录 Vercel**
   - 访问 https://vercel.com
   - 使用 GitHub 账号登录

2. **导入项目**
   - 点击 "Add New..." → "Project"
   - 选择刚才推送的 GitHub 仓库
   - 点击 "Import"

3. **配置部署设置**
   - **Framework Preset**: Other
   - **Root Directory**: . (保持默认)
   - **Output Directory**: public
   - **Install Command**: (留空)
   - **Build Command**: (留空)

4. **部署**
   - 点击 "Deploy" 按钮
   - 等待部署完成 (通常需要 1-2 分钟)

## 🌐 访问部署后的页面

部署成功后，您可以通过以下链接访问页面：

假设您的 Vercel 项目名称是 `51talk-landing-pages`，则访问地址为：

- **SpeakUp**: https://51talk-landing-pages.vercel.app/SpeakUp.html
- **GradeUp**: https://51talk-landing-pages.vercel.app/GradeUp.html
- **ScoreBoost**: https://51talk-landing-pages.vercel.app/ScoreBoost.html
- **测试套件**: https://51talk-landing-pages.vercel.app/i18n-test-suite.html
- **页面模板**: https://51talk-landing-pages.vercel.app/page-template.html

## 📁 项目结构

```
/Users/jin/landing-pages-deploy/
├── public/                     # 静态文件根目录
│   ├── SpeakUp.html           # SpeakUp 产品页面
│   ├── GradeUp.html           # GradeUp 产品页面
│   ├── ScoreBoost.html        # ScoreBoost 产品页面
│   ├── i18n-test-suite.html   # 多语言测试套件
│   ├── page-template.html     # 新页面模板
│   └── assets/                # 资源文件
│       ├── js/
│       │   └── i18n-final-enhanced.js  # 国际化核心库
│       ├── locales/           # 语言文件
│       │   ├── zh.json        # 中文翻译
│       │   ├── en.json        # 英文翻译
│       │   └── ar.json        # 阿拉伯语翻译
│       └── content/           # 内容映射文件
│           ├── content-mapping-SpeakUp.json
│           ├── content-mapping-GradeUp.json
│           └── content-mapping-ScoreBoost.json
├── vercel.json                # Vercel 部署配置
├── README_DEPLOY.md           # 本文档
├── .gitignore                 # Git 忽略文件
└── deploy.sh                  # 一键部署脚本
```

## 🌍 多语言支持

项目支持三种语言，会自动检测用户的浏览器语言：

- 🇨🇳 **中文** (zh) - 默认语言
- 🇺🇸 **英文** (en)
- 🇸🇦 **阿拉伯语** (ar) - 支持 RTL 布局

用户也可以通过页面右上角的语言选择器手动切换语言。

## 🔧 故障排除

### 常见问题

1. **页面显示 404 错误**
   - 检查 Vercel 配置中的 Output Directory 是否设置为 `public`
   - 确认文件路径是否正确

2. **多语言切换不工作**
   - 检查浏览器控制台是否有 JavaScript 错误
   - 确认 assets/js/i18n-final-enhanced.js 文件是否存在

3. **阿拉伯语布局问题**
   - 确认页面是否正确设置了 `dir="rtl"` 属性
   - 检查 CSS 中的 RTL 样式是否生效

### 日志查看

在 Vercel 控制台中可以查看：
- **Function Logs**: 函数执行日志
- **Build Logs**: 构建过程日志
- **Real-time Logs**: 实时访问日志

## 🚀 持续部署

Vercel 支持自动持续部署：

1. 每次向 GitHub 推送代码时，Vercel 会自动重新部署
2. 可以在 Vercel 控制台查看部署历史
3. 支持回滚到之前的部署版本

## 📞 技术支持

如遇到部署问题，请检查：

1. GitHub 仓库是否正确推送
2. Vercel 配置是否正确
3. 浏览器控制台是否有错误信息
4. 网络连接是否正常

---

**🎉 祝您部署成功！**