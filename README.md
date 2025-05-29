# n8n Workflows

这个仓库包含了各种 n8n 工作流模板。

## Telegram FaceSwap Bot

这是一个基于 n8n 的 Telegram 机器人工作流，它可以：
1. 接收用户发送的图片
2. 使用 Segmind API 进行人脸交换处理
3. 将处理后的图片发送回用户

### 使用方法

1. 在 n8n 中导入工作流：
   - 打开您的 n8n 实例
   - 点击左侧菜单的 "Workflows"
   - 点击右上角的 "Import from URL"
   - 使用以下 URL：
     ```
     https://raw.githubusercontent.com/Royrollpapa/n8n-workflows/main/n8n/Telegram_FaceSwap_Bot.json
     ```

2. 配置必要的环境变量：
   - `SEGMIND_API_KEY`：您的 Segmind API 密钥

3. 配置 Telegram Bot：
   - 通过 BotFather 创建一个新的 Telegram 机器人
   - 获取机器人的 API Token
   - 在 n8n 中配置 Telegram 凭证

4. 激活工作流并开始使用！

### 注意事项

- 确保您的 n8n 实例可以访问互联网
- 确保已正确配置所有必要的凭证
- 建议在正式使用前先进行测试 