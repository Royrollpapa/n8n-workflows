# 循环溯源数字化平台

## 项目简介
本项目是一个基于Markdown的演示文稿转换工具，支持将Markdown文档转换为HTML和PowerPoint格式。主要用于生成循环溯源数字化平台相关的演示文稿。

## 功能特点
- 📝 Markdown转HTML
- 📊 HTML转PowerPoint
- 🎨 自定义主题和样式
- 🔄 自动化转换流程
- 📱 响应式设计支持

## 项目结构（2024新版）

```
project/
├── config/                # 配置文件目录
│   └── config.yaml
├── resources/             # 静态资源目录（如logo、图标等）
│   └── images/
├── src/
│   ├── input/             # 用户输入文件（仅支持.md）
│   ├── output/            # 输出文件（.html, .pptx等）
│   ├── templates/         # Jinja2等模板文件
│   └── scripts/           # 所有核心脚本和主程序
│       ├── md_to_html.py  # Markdown转HTML（自动图表/表格）
│       ├── md_to_ppt.py   # Markdown转PPT（自动图表/表格）
│       ├── interactive.py # 图形界面主程序（可选）
│       └── ...
├── requirements.txt       # 依赖包列表
└── README.md              # 项目说明
```

## 推荐使用流程

1. 将待转换的Markdown文档放入 `src/input/` 目录。
2. 运行 `md_to_html.py`，一键将md转为html，自动插入图表和表格。
3. 运行 `md_to_ppt.py`，一键将md转为pptx，自动插入图表和表格。
4. 所有输出文件统一保存在 `src/output/` 目录。

## 入口说明
- Markdown转HTML：`src/scripts/md_to_html.py`
- Markdown转PPT：`src/scripts/md_to_ppt.py`
- 图形界面（可选）：`src/scripts/interactive.py`

## 自动图表与表格说明
- 支持标准Markdown表格、数字列表、代码块等多种数据格式，自动识别并生成最佳图表（柱状图、折线图、堆积柱状图、饼图等）。
- 原始数字数据自动渲染为HTML表格或PPT表格，附在图表下方。
- 具体格式和示例详见文档结尾"自动图表与表格测试用例"。

## 注意事项
- 仅支持.md为源文档，建议每组数据单独成表，避免合并单元格。
- 输出目录需有写入权限。
- 若遇到无法识别的数据块，脚本会输出友好提示。

## 工作流程

### 1. 准备阶段
1. 将Markdown文件放入 `src/input/` 目录
2. 确保Markdown文件格式正确，包含适当的标题层级和列表格式
3. 检查 `config/config.yaml` 中的配置是否符合需求

### 2. 转换流程
1. 运行主程序：
   ```bash
   cd src/scripts
   python main.py
   ```
2. 程序将自动执行以下步骤：
   - 读取Markdown文件
   - 转换为HTML格式
   - 生成PowerPoint演示文稿
   - 保存输出文件到 `src/output/` 目录

### 3. 输出文件
- HTML文件：`src/output/[文件名].html`
- PowerPoint文件：`src/output/[文件名].pptx`
- 日志文件：`src/output/conversion.log`

## 配置说明

### 配置文件位置
`config/config.yaml`

### 主要配置项
```yaml
ppt:
  fonts:
    title: "Microsoft YaHei"
    content: "Microsoft YaHei"
  sizes:
    title: 44
    subtitle: 32
    content: 24

html:
  theme: "light"
  font_family: "Microsoft YaHei"
  colors:
    primary: "#1976D2"
    secondary: "#424242"

output:
  path: "src/output"
  format: "pptx"
  quality: "high"
```

## 使用要求
- Python 3.8+
- 依赖包：
  - markdown
  - pyyaml
  - python-pptx
  - beautifulsoup4
  - jinja2

## 安装依赖
```bash
pip install -r requirements.txt
```

## 常见问题
1. 中文显示问题
   - 确保使用支持中文的字体
   - 检查文件编码为UTF-8

2. 样式问题
   - 检查config.yaml中的配置
   - 确保模板文件完整

3. 转换失败
   - 检查日志文件
   - 验证Markdown格式
   - 确认文件权限

## 贡献指南
1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证
MIT License

## 支持的Markdown数字数据格式（自动生成图表/表格）

本工具支持以下Markdown格式的数字数据自动识别和可视化：

### 1. 标准Markdown表格

```
| 年份 | 销量 |
|------|------|
| 2021 | 120  |
| 2022 | 150  |
| 2023 | 180  |
```
- 适合：折线图、柱状图（时间序列、对比数据）

### 2. 多组对比表格

```
| 类别 | 一季度 | 二季度 | 三季度 | 四季度 |
|------|--------|--------|--------|--------|
| A    | 10     | 20     | 30     | 40     |
| B    | 15     | 25     | 35     | 45     |
```
- 适合：堆积柱状图、分组柱状图

### 3. 占比/比例数据表格

```
| 类别 | 占比 |
|------|------|
| 男   | 60   |
| 女   | 40   |
```
- 适合：饼图、扇形图

### 4. 列表/代码块中的数字

```
- 2021年：120
- 2022年：150
- 2023年：180
```
或
```
数据：
2021,120
2022,150
2023,180
```
- 适合：折线图、柱状图

### 5. 复杂嵌套表格
- 推荐使用标准Markdown表格格式，支持多列多行。

> **注意：**
> - 表头需明确，建议用"年份""类别""占比"等常用字段。
> - 数字列必须为纯数字。
> - 不支持合并单元格。
> - 建议每组数据单独成表，便于自动识别。

---