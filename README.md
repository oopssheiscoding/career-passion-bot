# AI创业助理 (Career Passion Bot)

一个智能聊天机器人，帮助女性发现自己的热情与才能，并提供创业指导和资源推荐。

## 项目描述

AI创业助理是一个基于Claude AI的聊天应用，旨在帮助女性用户：
- 探索自己的兴趣爱好和技能
- 发现适合自己的自由职业方向
- 获取相关领域的学习资源和入门指南
- 提供创业过程中的心理支持和实用建议

应用采用自然对话形式，通过引导性问题帮助用户自我探索，并根据用户的反馈提供个性化的建议。

## 主要特点

- 💬 自然对话界面，易于使用
- 🧠 基于Claude AI的智能对话能力
- 📚 内置各领域学习资源推荐
- 🚀 自由职业类型详解和入门指南
- 📱 移动端友好的响应式设计

## 技术栈

- Python
- Streamlit (前端界面)
- Anthropic Claude API (AI对话引擎)
- dotenv (环境变量管理)

## 安装指南

1. 克隆项目
```bash
git clone https://github.com/oopssheiscoding/career-passion-bot.git
cd career-passion-bot
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 设置环境变量
```bash
# 复制示例环境文件
cp .env.example .env

# 编辑.env文件，添加你的Anthropic API密钥
# ANTHROPIC_API_KEY=your_key_here
```

4. 运行应用
```bash
streamlit run fixed_welcome_app.py
```

## 使用方法

1. 启动应用后，AI会以预设的欢迎消息开始对话
2. 分享你的兴趣、技能和创业想法
3. AI会提供引导性问题帮助你思考
4. 根据对话内容，你可以获取相关领域的资源推荐
5. 探索不同的自由职业类型和入门建议

## 欢迎贡献

欢迎通过Issue和Pull Request贡献代码或提出建议。你可以：
- 添加更多领域的资源推荐
- 改进对话体验
- 优化UI界面
- 修复bug或添加新功能

## 许可证

MIT

## 联系方式

GitHub: [@oopssheiscoding](https://github.com/oopssheiscoding) 