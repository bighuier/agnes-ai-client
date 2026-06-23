# Agnes AI 客户端

基于 Flask 的 Agnes AI 本地客户端，支持文生图、图生图、文生视频、图生视频等功能。

## 功能特性

- **Agnes Chat** - 与 Agnes AI 模型对话
- **文生图** - 输入提示词生成图片
- **图生图** - 上传图片进行编辑，支持图片反推提示词
- **文生视频** - 输入提示词生成视频
- **图生视频** - 上传图片生成视频
- **提示词库** - 管理和保存提示词，支持分类和评分
- **主题切换** - 支持深空黑和极简白两种主题风格

## 系统要求

- Windows 10/11 系统
- 已安装依赖：
  - flask
  - cryptography

## 快速开始

### 方法一：双击启动（推荐）

1. 双击运行 `start.bat`
2. 打开浏览器访问 http://localhost:3001
3. 在设置页面输入你的 Agnes AI API Key

### 方法二：命令行启动

```bash
pip install -r requirements.txt
python app/server.py
```

## 配置 API Key

1. 启动应用后，访问 http://localhost:3001
2. 点击右上角"设置"按钮
3. 输入你的 Agnes AI API Key 并保存

## 文件结构

```
agnes-ai-client/
├── app/
│   ├── server.py      # 主服务程序
│   └── diagnose.py    # 诊断工具
├── data/              # 数据目录（运行后自动创建）
│   ├── config.json    # 配置文件（API Key，已加密）
│   └── prompts.db     # 提示词数据库
├── static/js/         # 前端增强脚本
├── templates/         # HTML模板
├── generated-images/  # 生成的图片存储
├── start.bat          # Windows启动脚本
├── build.spec         # PyInstaller打包配置
├── requirements.txt   # Python依赖
└── README.md          # 说明文档
```

## 功能说明

### 提示词增强
在文生图或图生图页面，可以点击"增强"按钮将简单描述扩展为专业提示词。

### 图片反推提示词
在图生图或图生视频页面，上传图片后可以点击"反推"按钮，让AI分析图片生成对应的提示词。

### 提示词库
1. 切换到「提示词库」标签
2. 可以搜索、筛选提示词
3. 点击提示词可以查看详情、复制或复用
4. 支持评分（1-5星）和收藏功能

## 注意事项

- API Key 使用 Fernet 加密保存在本地 `data/config.json` 文件中
- 密钥文件保存在 `data/.key`，请勿删除
- 生成的图片保存在 `generated-images/` 目录
- 提示词保存在本地 SQLite 数据库中
- 首次使用需要配置有效的 Agnes AI API Key

## 获取 API Key

请访问 Agnes AI 官方网站获取 API Key：
https://www.agnes-ai.com

## 技术支持

如有问题，请联系 Agnes AI 官方客服。