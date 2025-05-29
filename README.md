# n8n-workflows

本文件夹用于存放 n8n 工作流模板，便于统一管理和版本控制。

## 当前工作流列表

- **Telegram_FaceSwap_Bot.json**：Telegram 人脸交换机器人工作流

## 如何导入到 n8n

1. 打开您的 n8n 实例
2. 点击左侧菜单的 "Workflows"
3. 点击右上角的 "Import from URL"
4. 粘贴如下 URL（以 Telegram FaceSwap Bot 为例）：
   ```
   https://raw.githubusercontent.com/Royrollpapa/n8n-workflows/main/n8n-workflows/Telegram_FaceSwap_Bot.json
   ```
5. 点击导入即可

## 注意事项
- 请根据工作流说明配置好相关环境变量和凭证
- 建议导入后先测试功能是否正常
- 如需协作或备份，直接同步本文件夹即可 