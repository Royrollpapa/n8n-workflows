import os
import sys
import subprocess

def convert_md_to_pdf(md_file, pdf_file):
    if not os.path.exists(md_file):
        print(f"未找到Markdown文件：{md_file}")
        return False
    try:
        # 使用pandoc进行转换，添加--toc生成目录，--reference-doc指定参考文档以保持表格格式
        result = subprocess.run(
            ['pandoc', md_file, '-o', pdf_file, '--pdf-engine=xelatex', '-V', 'CJKmainfont=SimSun', '--toc', '--reference-doc=../Docs/250527_SUS Panel.docx'],
            check=False,
            capture_output=True,
            text=True
        )
        print("--- pandoc 标准输出 ---")
        print(result.stdout)
        print("--- pandoc 错误输出 ---")
        print(result.stderr)
        if result.returncode == 0 and os.path.exists(pdf_file):
            print(f"PDF文件已生成：{pdf_file}")
            return True
        else:
            print(f"pandoc运行失败，返回码：{result.returncode}")
            return False
    except FileNotFoundError:
        print("未找到pandoc命令，请先安装：pip install pandoc")
        return False

def main():
    # 支持命令行参数：python md_to_pdf.py [input.md] [output.pdf]
    current_dir = os.path.dirname(os.path.abspath(__file__))
    docs_dir = os.path.abspath(os.path.join(current_dir, "..", "Docs"))
    if len(sys.argv) > 2:
        md_file = sys.argv[1]
        pdf_file = sys.argv[2]
    else:
        md_file = os.path.join(docs_dir, "wen_speech.md")
        pdf_file = os.path.join(docs_dir, "wen_speech.pdf")
    print(f"开始转换：{md_file} -> {pdf_file}")
    convert_md_to_pdf(md_file, pdf_file)

if __name__ == "__main__":
    main() 