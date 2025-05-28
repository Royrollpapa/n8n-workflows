import os
from docx import Document
import html2text
from docx.table import Table
from docx.text.paragraph import Paragraph

def iter_block_items(parent):
    """顺序遍历文档中的段落和表格"""
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    for child in parent.element.body.iterchildren():
        if child.tag == qn('w:p'):
            yield Paragraph(child, parent)
        elif child.tag == qn('w:tbl'):
            yield Table(child, parent)

class DocxToMarkdownConverter:
    def __init__(self):
        self.doc = None
        self.h = html2text.HTML2Text()
        self.h.ignore_links = True
        self.h.ignore_images = True
        self.h.ignore_tables = True
        self.h.body_width = 0

    def read_document(self, file_path):
        """读取Word文档"""
        try:
            self.doc = Document(file_path)
            return True
        except Exception as e:
            print(f"读取文档时出错: {str(e)}")
            return False

    def convert_paragraph_to_markdown(self, paragraph):
        """将段落转换为Markdown格式"""
        text = ""
        for run in paragraph.runs:
            if run.bold:
                text += f"**{run.text}**"
            elif run.italic:
                text += f"*{run.text}*"
            else:
                text += run.text
        return text

    def convert_table_to_markdown(self, table):
        """将表格转换为Markdown格式"""
        markdown = "\n"
        if len(table.rows) == 0:
            return markdown
        # 添加表头
        header = "| " + " | ".join(cell.text.strip() for cell in table.rows[0].cells) + " |"
        markdown += header + "\n"
        # 添加分隔行
        markdown += "| " + " | ".join(["---"] * len(table.rows[0].cells)) + " |\n"
        # 添加数据行
        for row in table.rows[1:]:
            row_text = "| " + " | ".join(cell.text.strip() for cell in row.cells) + " |"
            markdown += row_text + "\n"
        return markdown + "\n"

    def convert_to_markdown(self, output_file):
        """将文档转换为Markdown格式"""
        if not self.doc:
            return False

        markdown_content = []
        for block in iter_block_items(self.doc):
            if isinstance(block, Paragraph):
                if block.text.strip():
                    markdown_content.append(self.convert_paragraph_to_markdown(block))
            elif isinstance(block, Table):
                markdown_content.append(self.convert_table_to_markdown(block))

        # 写入文件
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write('\n\n'.join(markdown_content))
            return True
        except Exception as e:
            print(f"写入文件时出错: {str(e)}")
            return False

def convert_docx_to_markdown():
    """转换文档的主函数"""
    converter = DocxToMarkdownConverter()
    
    # 读取原始文档
    input_file = os.path.join('..', 'Docs', '250527_SUS Panel.docx')
    if not converter.read_document(input_file):
        print("无法读取原始文档")
        return
    
    # 转换并保存
    output_file = os.path.join('..', 'Docs', '250527_SUS Panel.md')
    if converter.convert_to_markdown(output_file):
        print(f"文档已成功转换为Markdown格式，保存在: {output_file}")
    else:
        print("转换过程中出现错误")

if __name__ == '__main__':
    convert_docx_to_markdown() 