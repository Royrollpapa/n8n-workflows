import os
import logging
from pathlib import Path
from typing import Dict, Optional, Union
from md_to_html import MarkdownToHTML
from html_to_ppt import HTMLToPPT

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DocumentConverter:
    """文档转换器，支持多种转换路径"""
    
    def __init__(self, config_path: str):
        """
        初始化转换器
        Args:
            config_path: 配置文件路径
        """
        self.config_path = str(Path(__file__).parent / ".." / ".." / "config" / "config.yaml")
        self.converters = {
            'md_to_html': MarkdownToHTML(self.config_path),
            'html_to_ppt': HTMLToPPT(self.config_path)
        }
        
    def convert_step(self, source_path: str, step: str, output_path: Optional[str] = None) -> str:
        """
        执行单步转换
        Args:
            source_path: 源文件路径
            step: 转换步骤 (md_to_html 或 html_to_ppt)
            output_path: 输出文件路径（可选）
        Returns:
            str: 输出文件路径
        """
        if step not in self.converters:
            raise ValueError(f"不支持的转换步骤: {step}")
        
        logger.info(f"开始执行转换步骤: {step}")
        converter = self.converters[step]
        
        if not output_path:
            # 自动生成输出路径
            source_file = Path(source_path)
            if step == 'md_to_html':
                output_path = str(source_file.with_suffix('.html'))
            elif step == 'html_to_ppt':
                output_path = str(source_file.with_suffix('.pptx'))
        
        # 关键修正：根据step调用不同方法
        if step == 'md_to_html':
            return converter.convert_to_html(source_path, output_path)
        elif step == 'html_to_ppt':
            return converter.convert_to_ppt(source_path, output_path)
        else:
            raise ValueError(f"不支持的转换步骤: {step}")
    
    def convert(self, source_path: str, target_format: str, output_path: Optional[str] = None) -> str:
        """
        执行完整转换流程
        Args:
            source_path: 源文件路径
            target_format: 目标格式 (html 或 ppt)
            output_path: 输出文件路径（可选）
        Returns:
            str: 输出文件路径
        """
        source_file = Path(source_path)
        
        if target_format == 'html':
            return self.convert_step(source_path, 'md_to_html', output_path)
        elif target_format == 'ppt':
            # 先转换为HTML，再转换为PPT
            html_path = self.convert_step(source_path, 'md_to_html')
            return self.convert_step(html_path, 'html_to_ppt', output_path)
        else:
            raise ValueError(f"不支持的目标格式: {target_format}")
            
    def get_supported_formats(self) -> Dict[str, list]:
        """获取支持的转换格式"""
        return {
            'source_formats': ['md', 'html'],
            'target_formats': ['html', 'ppt']
        }
        
    def get_supported_steps(self) -> list:
        """获取支持的转换步骤"""
        return list(self.converters.keys())

def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='文档转换工具')
    parser.add_argument('--source', required=True, help='源文件路径')
    parser.add_argument('--format', choices=['html', 'ppt'], help='目标格式')
    parser.add_argument('--step', choices=['md_to_html', 'html_to_ppt'], help='转换步骤')
    parser.add_argument('--output', help='输出文件路径')
    parser.add_argument('--config', default='config/config.yaml', help='配置文件路径')
    
    args = parser.parse_args()
    
    # 获取项目根目录
    project_root = Path(__file__).parent.parent.parent
    config_path = project_root / args.config
    
    converter = DocumentConverter(str(config_path))
    
    try:
        if args.step:
            # 单步转换
            output = converter.convert_step(args.source, args.step, args.output)
        else:
            # 完整转换
            output = converter.convert(args.source, args.format, args.output)
            
        logger.info(f"转换完成: {output}")
        
    except Exception as e:
        logger.error(f"转换失败: {str(e)}")
        raise

if __name__ == "__main__":
    main() 