# Agnes AI 客户端

基于 Flask 的 Agnes AI 本地客户端，支持文生图、图生图、文生视频、图生视频等功能。

## 功能特性

- **Agnes Chat** - 与 Agnes AI 模型对话
- **文生图** - 输入提示词生成图片
- **图生图** - 上传图片进行编辑
- **文生视频** - 输入提示词生成视频
- **图生视频** - 上传图片生成视频
- **提示词库** - 管理和保存提示词

## 系统要求

- Python 3.8+
- 已安装以下 Python 标准库：
  - flask
  - json
  - os
  - sqlite3
  - uuid
  - urllib
  - datetime
  - re

## 快速开始

### 方法一：双击启动（推荐）

1. 双击运行 `start.bat`
2. 打开浏览器访问 http://localhost:3001
3. 在设置页面输入你的 Agnes AI API Key

### 方法二：命令行启动

```bash
python app/server.py
```

## 配置 API Key

1. 启动应用后，访问 http://localhost:3001
2. 如果没有配置 API Key，会自动跳转到设置页面
3. 输入你的 Agnes AI API Key 并保存

## 文件结构

```
agnes-ai-frontend/
├── app/
│   ├── server.py      # 主服务程序
│   └── diagnose.py    # 诊断工具
├── data/
│   ├── config.json    # 配置文件（API Key）
│   └── prompts.db     # 提示词数据库
├── static/js/         # 前端增强脚本
├── templates/         # HTML模板
├── generated-images/  # 生成的图片存储
├── start.bat          # Windows启动脚本
└── README.md          # 说明文档
```

## 使用说明

### 文生图
1. 切换到「文生图」标签
2. 输入提示词
3. 调整宽度、高度和数量
4. 点击「生成」按钮

### 图生图
1. 切换到「图生图」标签
2. 点击上传区域上传图片
3. 输入提示词
4. 点击「编辑」按钮

### 文生视频
1. 切换到「文生视频」标签
2. 输入提示词
3. 调整参数
4. 点击「生成」按钮

### 图生视频
1. 切换到「图生视频」标签
2. 上传图片
3. 输入提示词
4. 点击「生成」按钮

### 提示词库
1. 切换到「提示词库」标签
2. 可以搜索、筛选提示词
3. 点击提示词可以查看详情、复制或复用

## 注意事项

- API Key 保存在本地 `data/config.json` 文件中
- 生成的图片保存在 `generated-images/` 目录
- 提示词保存在本地 SQLite 数据库中
- 首次使用需要配置有效的 Agnes AI API Key

## 获取 API Key

请访问 Agnes AI 官方网站获取 API Key：
https://www.agnes-ai.com

## 技术支持

如有问题，请联系 Agnes AI 官方客服。