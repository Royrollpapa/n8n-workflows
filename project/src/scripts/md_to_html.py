import os
import yaml
import markdown
import logging
from jinja2 import Environment, FileSystemLoader
import re
import json
import matplotlib.pyplot as plt
import base64
import io
from pathlib import Path
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MarkdownToHTML:
    """Markdown转HTML转换器，支持chart/mermaid代码块自动转图片"""
    
    def __init__(self, config_path: str):
        """
        初始化转换器
        Args:
            config_path: 配置文件路径
        """
        self.config_path = str(Path(__file__).parent / ".." / ".." / "config" / "config.yaml")
        with open(self.config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.md = markdown.Markdown(extensions=['extra', 'codehilite', 'tables'])

    def _render_chart_image(self, chart_json: str) -> str:
        """
        渲染图表为图片
        Args:
            chart_json: 图表JSON数据
        Returns:
            str: Base64编码的图片数据
        """
        try:
            # 创建输出目录
            output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output')
            os.makedirs(output_dir, exist_ok=True)
            
            # 解析图表数据
            chart_data = json.loads(chart_json)
            
            # 创建图表
            plt.figure(figsize=(10, 6))
            if chart_data['type'] == 'bar':
                plt.bar(chart_data['labels'], chart_data['data'])
            elif chart_data['type'] == 'line':
                plt.plot(chart_data['labels'], chart_data['data'])
            elif chart_data['type'] == 'pie':
                plt.pie(chart_data['data'], labels=chart_data['labels'])
            
            # 设置标题和标签
            if 'title' in chart_data:
                plt.title(chart_data['title'])
            if 'xlabel' in chart_data:
                plt.xlabel(chart_data['xlabel'])
            if 'ylabel' in chart_data:
                plt.ylabel(chart_data['ylabel'])
            
            # 保存图片
            img_path = os.path.join(output_dir, f"chart_{hash(chart_json)}.png")
            plt.savefig(img_path)
            plt.close()
            
            # 读取图片并转换为Base64
            with open(img_path, 'rb') as f:
                img_data = f.read()
            return base64.b64encode(img_data).decode()
            
        except Exception as e:
            logger.error(f"渲染图表失败: {str(e)}")
            return ""

    def _replace_code_blocks(self, md_content: str) -> str:
        """将chart/mermaid代码块替换为图片或提示"""
        # chart代码块
        def chart_repl(match):
            chart_json = match.group(1)
            return self._render_chart_image(chart_json)
        md_content = re.sub(r'```chart\s*([\s\S]*?)```', chart_repl, md_content)
        # mermaid代码块
        def mermaid_repl(match):
            return '<div style="text-align:center;color:#888;"><b>[Mermaid图表请在HTML或PPT中手动补充]</b></div>'
        md_content = re.sub(r'```mermaid[\s\S]*?```', mermaid_repl, md_content)
        return md_content

    def _convert_charts_to_images(self, html_content: str) -> str:
        """
        将HTML中的图表转换为图片
        Args:
            html_content: 包含图表的HTML内容
        Returns:
            str: 转换后的HTML内容
        """
        try:
            # 创建输出目录
            output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output')
            os.makedirs(output_dir, exist_ok=True)
            
            # 使用BeautifulSoup解析HTML
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # 查找所有图表元素
            chart_elements = soup.find_all('div', class_='chart')
            
            for chart_element in chart_elements:
                try:
                    # 获取图表数据
                    chart_data = chart_element.get('data-chart')
                    if not chart_data:
                        continue
                        
                    # 渲染图表为图片
                    img_data = self._render_chart_image(chart_data)
                    if not img_data:
                        continue
                        
                    # 创建新的图片元素
                    img_tag = soup.new_tag('img')
                    img_tag['src'] = f"data:image/png;base64,{img_data}"
                    img_tag['alt'] = "Chart"
                    img_tag['style'] = "max-width: 100%; height: auto;"
                    
                    # 替换图表元素
                    chart_element.replace_with(img_tag)
                    
                except Exception as e:
                    logger.error(f"处理单个图表时出错: {str(e)}")
                    continue
            
            return str(soup)
            
        except Exception as e:
            logger.error(f"转换图表为图片时出错: {str(e)}")
            return html_content

    def extract_numeric_blocks(self, md_content: str):
        """
        自动识别Markdown中的数字数据块（表格、列表、代码块），并结构化输出。
        返回：list，每个元素为{'type': 'table'|'list'|'code', 'data': DataFrame/list, 'raw': 原始文本}
        """
        results = []
        unsupported_blocks = []
        # 1. 识别标准Markdown表格
        table_pattern = re.compile(r'(\|.+\|\n(?:\|[-: ]+\|\n)+((?:\|.*\|\n?)+))', re.MULTILINE)
        for match in table_pattern.finditer(md_content):
            raw = match.group(0)
            try:
                lines = [line.strip() for line in raw.strip().split('\n') if line.strip()]
                # 跳过分隔线
                data_lines = [line for line in lines if not re.match(r'^\|?[-: ]+\|?$', line)]
                if len(data_lines) < 2:
                    unsupported_blocks.append(raw)
                    continue
                header = [cell.strip() for cell in data_lines[0].strip('|').split('|')]
                rows = []
                for line in data_lines[1:]:
                    row = [cell.strip() for cell in line.strip('|').split('|')]
                    if len(row) == len(header):
                        rows.append(row)
                df = pd.DataFrame(rows, columns=header)
                # 尝试将数值列转为float
                for col in df.columns:
                    try:
                        df[col] = df[col].astype(float)
                    except Exception:
                        pass
                results.append({'type': 'table', 'data': df, 'raw': raw})
            except Exception:
                unsupported_blocks.append(raw)
                continue
        # 2. 识别有数字的无序列表
        list_pattern = re.compile(r'(?:^|\n)(- .*[0-9]+.*(?:\n- .*[0-9]+.*)+)', re.MULTILINE)
        for match in list_pattern.finditer(md_content):
            raw = match.group(1)
            lines = [line.strip('- ').strip() for line in raw.strip().split('\n') if line.strip()]
            results.append({'type': 'list', 'data': lines, 'raw': raw})
        # 3. 识别代码块中的数字数据
        code_pattern = re.compile(r'```[a-zA-Z0-9]*\n([\s\S]*?\d+[\s\S]*?)```', re.MULTILINE)
        for match in code_pattern.finditer(md_content):
            raw = match.group(1)
            lines = [line for line in raw.strip().split('\n') if any(c.isdigit() for c in line)]
            if lines:
                results.append({'type': 'code', 'data': lines, 'raw': raw})
        return results

    def auto_chart_type(self, block):
        """
        根据结构化数字数据自动判断最佳图表类型。
        输入：block为extract_numeric_blocks的单个结果
        返回：'bar'|'line'|'stacked_bar'|'pie'|'table'等
        """
        if block['type'] == 'table':
            df = block['data']
            if df.shape[1] == 2:
                col1, col2 = df.columns[0], df.columns[1]
                if all(isinstance(x, (int, float, np.integer, np.floating)) or str(x).replace('.','',1).isdigit() for x in df[col2]):
                    if any(s in str(col1) for s in ['年', '月', 'date', 'time']) or all(str(x).isdigit() for x in df[col1]):
                        return 'line'
                    else:
                        return 'bar'
            elif df.shape[1] > 2:
                if any('占比' in str(c) or '比例' in str(c) for c in df.columns):
                    return 'pie'
                else:
                    return 'stacked_bar'
        if block['type'] == 'list':
            return 'bar'
        if block['type'] == 'code':
            lines = block['data']
            if all(',' in line for line in lines):
                return 'line'
            else:
                return 'bar'
        return 'table'

    def render_auto_chart(self, block):
        """
        根据block和auto_chart_type自动生成matplotlib图表，返回base64图片字符串。
        支持bar、line、stacked_bar、pie。
        """
        chart_type = self.auto_chart_type(block)
        fig, ax = plt.subplots(figsize=(8, 5))
        img_b64 = ""
        try:
            if chart_type == 'bar':
                if block['type'] == 'table':
                    df = block['data']
                    ax.bar(df.iloc[:, 0], df.iloc[:, 1])
                    ax.set_title(f"{df.columns[0]} vs {df.columns[1]}")
                elif block['type'] == 'list':
                    labels = [str(i+1) for i in range(len(block['data']))]
                    values = [float(''.join(filter(str.isdigit, s))) for s in block['data']]
                    ax.bar(labels, values)
                    ax.set_title("数据分布")
                elif block['type'] == 'code':
                    lines = [line.split(',') for line in block['data'] if ',' in line]
                    labels = [l[0] for l in lines]
                    values = [float(l[1]) for l in lines]
                    ax.bar(labels, values)
                    ax.set_title("数据分布")
            elif chart_type == 'line':
                if block['type'] == 'table':
                    df = block['data']
                    ax.plot(df.iloc[:, 0], df.iloc[:, 1], marker='o')
                    ax.set_title(f"{df.columns[0]} vs {df.columns[1]}")
                elif block['type'] == 'code':
                    lines = [line.split(',') for line in block['data'] if ',' in line]
                    labels = [l[0] for l in lines]
                    values = [float(l[1]) for l in lines]
                    ax.plot(labels, values, marker='o')
                    ax.set_title("趋势分析")
            elif chart_type == 'stacked_bar':
                df = block['data']
                x = df.iloc[:, 0]
                y = df.iloc[:, 1:]
                y.cumsum(axis=1).plot(kind='bar', stacked=True, ax=ax)
                ax.set_xticklabels(x)
                ax.set_title("多组数据对比")
            elif chart_type == 'pie':
                df = block['data']
                ax.pie(df.iloc[:, 1], labels=df.iloc[:, 0], autopct='%1.1f%%')
                ax.set_title("占比分析")
            else:
                plt.close(fig)
                return ""
            buf = io.BytesIO()
            plt.tight_layout()
            plt.savefig(buf, format='png')
            plt.close(fig)
            img_b64 = base64.b64encode(buf.getvalue()).decode()
        except Exception as e:
            plt.close(fig)
            return ""
        return img_b64

    def render_html_table(self, block):
        """
        将结构化数字数据渲染为HTML表格，支持table/list/code三种类型。
        返回HTML字符串。
        """
        html = "<div style='overflow-x:auto;'><table border='1' cellpadding='4' cellspacing='0' style='border-collapse:collapse;width:auto;'>"
        if block['type'] == 'table':
            df = block['data']
            # 表头
            html += '<tr>' + ''.join(f'<th>{col}</th>' for col in df.columns) + '</tr>'
            # 行
            for _, row in df.iterrows():
                html += '<tr>' + ''.join(f'<td>{cell}</td>' for cell in row) + '</tr>'
        elif block['type'] == 'list':
            html += '<tr><th>序号</th><th>内容</th></tr>'
            for i, item in enumerate(block['data'], 1):
                html += f'<tr><td>{i}</td><td>{item}</td></tr>'
        elif block['type'] == 'code':
            html += '<tr><th>内容</th></tr>'
            for line in block['data']:
                html += f'<tr><td>{line}</td></tr>'
        html += '</table></div>'
        return html

    def convert_to_html(self, md_path: str, output_path: str) -> str:
        """
        将Markdown文件转换为HTML
        Args:
            md_path: Markdown文件路径
            output_path: 输出HTML文件路径
        Returns:
            str: 生成的HTML文件路径
        """
        try:
            # 检查输入文件
            if not os.path.exists(md_path):
                raise FileNotFoundError(f"找不到Markdown文件: {md_path}")

            # 创建输出目录
            output_dir = os.path.dirname(output_path)
            os.makedirs(output_dir, exist_ok=True)

            # 读取Markdown文件
            with open(md_path, 'r', encoding='utf-8') as f:
                md_content = f.read()

            # 自动识别数字数据块，生成图表和表格
            numeric_blocks = self.extract_numeric_blocks(md_content)
            md_content_with_charts = md_content
            for block in numeric_blocks:
                chart_b64 = self.render_auto_chart(block)
                chart_html = f'<div style="text-align:center;margin:1em 0;">'
                if chart_b64:
                    chart_html += f'<img src="data:image/png;base64,{chart_b64}" style="max-width:100%;height:auto;"/>'
                chart_html += self.render_html_table(block)
                chart_html += '</div>'
                # 用原始数据块替换为图表+表格
                md_content_with_charts = md_content_with_charts.replace(block['raw'], chart_html)

            # 处理图表代码块（原有功能）
            md_content_with_charts = self._replace_code_blocks(md_content_with_charts)

            # 转换Markdown为HTML
            html_content = self.md.convert(md_content_with_charts)

            # 处理图表
            html_content = self._convert_charts_to_images(html_content)

            # 使用模板渲染最终HTML
            template = self.env.get_template('template.html')
            final_html = template.render(
                content=html_content,
                title=os.path.splitext(os.path.basename(md_path))[0]
            )

            # 保存HTML文件
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(final_html)

            logger.info(f"成功生成HTML文件: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"转换Markdown到HTML失败: {str(e)}")
            raise

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    config_path = os.path.join(project_root, 'config', 'config.yaml')
    converter = MarkdownToHTML(config_path)
    input_dir = os.path.join(project_root, 'src', 'input')
    for file in os.listdir(input_dir):
        if file.endswith('.md'):
            md_path = os.path.join(input_dir, file)
            try:
                converter.convert_to_html(md_path, os.path.join(os.path.dirname(md_path), os.path.basename(md_path).replace('.md', '.html')))
            except Exception as e:
                logger.error(f"处理文件 {file} 时出错: {str(e)}")

if __name__ == "__main__":
    main() 