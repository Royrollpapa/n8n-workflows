# AI PPT生成器执行指南

## 环境准备

1. 确保已安装Python 3.8或更高版本：
```bash
python --version
```

2. 安装项目依赖：
```bash
pip install -r requirements.txt
```

3. 配置OpenAI API密钥：
   - 在项目根目录创建 `.env` 文件
   - 添加以下内容：
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## 运行步骤

1. 准备输入文档：
   - 将需要转换的文档（支持.docx、.pdf、.txt格式）放入 `src/input` 目录
   - 示例文档已提供：`src/input/example.txt`

2. 创建PPT模板：
```bash
python src/scripts/create_template.py
```

3. 运行PPT生成器：
```bash
python src/scripts/ppt_generator.py
```

4. 查看输出：
   - 生成的PPT文件将保存在 `src/output` 目录
   - 输出文件名将与输入文件名相同，但扩展名为.pptx

## 示例运行

1. 使用示例文档：
   - 示例文档 `example.txt` 已包含在 `src/input` 目录
   - 文档内容是关于"人工智能在医疗领域的应用"

2. 预期输出：
   - 将生成一个包含以下内容的PPT：
     - 标题页：人工智能在医疗领域的应用
     - 内容页：医学影像诊断、药物研发、个性化医疗、医疗管理、未来展望
   - 每个章节包含3-5个关键点

## 故障排除

1. 如果遇到依赖安装问题：
   - 确保pip已更新：`python -m pip install --upgrade pip`
   - 尝试单独安装每个依赖：`pip install package_name`

2. 如果遇到API密钥问题：
   - 检查 `.env` 文件是否正确配置
   - 确保API密钥有效且有足够的额度

3. 如果遇到文件权限问题：
   - 确保对项目目录有读写权限
   - 检查输入输出目录是否存在

## 注意事项

1. 文件大小限制：
   - 输入文档大小不应超过10MB
   - 建议使用结构清晰的文档

2. 格式要求：
   - 支持的输入格式：.docx、.pdf、.txt
   - 输出格式：.pptx

3. 性能考虑：
   - 处理大文件可能需要较长时间
   - 建议先使用小文件测试 