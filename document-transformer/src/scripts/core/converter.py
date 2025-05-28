"""
统一的文档转换器
支持多种文档格式之间的转换
"""

import os
from pathlib import Path
from typing import Optional, Union
from .document_processor import DocumentProcessor
from .markdown_processor import MarkdownProcessor
from .presentation_processor import PresentationProcessor

class DocumentConverter:
    """统一的文档转换器类"""
    
    def __init__(self):
        self.doc_processor = DocumentProcessor()
        self.md_processor = MarkdownProcessor()
        self.ppt_processor = PresentationProcessor()
        
    def convert(self, 
                input_path: str,
                output_path: str,
                input_format: str = None,
                output_format: str = None) -> str:
        """
        转换文档格式
        
        Args:
            input_path: 输入文件路径
            output_path: 输出文件路径
            input_format: 输入文件格式（可选，自动检测）
            output_format: 输出文件格式（可选，自动检测）
            
        Returns:
            str: 输出文件路径
        """
        # 自动检测文件格式
        if not input_format:
            input_format = Path(input_path).suffix.lower()[1:]
        if not output_format:
            output_format = Path(output_path).suffix.lower()[1:]
            
        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # 根据输入输出格式选择转换方法
        if input_format == 'md':
            if output_format == 'html':
                return self.md_to_html(input_path, output_path)
            elif output_format == 'pptx':
                return self.md_to_ppt(input_path, output_path)
            elif output_format == 'docx':
                return self.md_to_docx(input_path, output_path)
        elif input_format == 'docx':
            if output_format == 'md':
                return self.docx_to_md(input_path, output_path)
            elif output_format == 'pdf':
                return self.docx_to_pdf(input_path, output_path)
        elif input_format == 'html':
            if output_format == 'pptx':
                return self.html_to_ppt(input_path, output_path)
                
        raise ValueError(f"不支持的转换: {input_format} -> {output_format}")
    
    def md_to_html(self, input_path: str, output_path: str) -> str:
        """Markdown转HTML"""
        return self.md_processor.to_html(input_path, output_path)
    
    def md_to_ppt(self, input_path: str, output_path: str) -> str:
        """Markdown转PowerPoint"""
        return self.md_processor.to_ppt(input_path, output_path)
    
    def md_to_docx(self, input_path: str, output_path: str) -> str:
        """Markdown转Word"""
        return self.md_processor.to_docx(input_path, output_path)
    
    def docx_to_md(self, input_path: str, output_path: str) -> str:
        """Word转Markdown"""
        return self.doc_processor.to_markdown(input_path, output_path)
    
    def docx_to_pdf(self, input_path: str, output_path: str) -> str:
        """Word转PDF"""
        return self.doc_processor.to_pdf(input_path, output_path)
    
    def html_to_ppt(self, input_path: str, output_path: str) -> str:
        """HTML转PowerPoint"""
        return self.ppt_processor.from_html(input_path, output_path) 