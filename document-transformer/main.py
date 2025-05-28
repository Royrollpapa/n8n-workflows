"""
文档转换工具主程序
提供统一的图形用户界面
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path

# 添加src/scripts目录到Python路径
scripts_path = str(Path(__file__).parent / "src" / "scripts")
if scripts_path not in sys.path:
    sys.path.append(scripts_path)

from core import DocumentConverter, DocumentProcessor
from meeting_processor import MeetingProcessor

class ConverterGUI:
    """文档转换工具图形界面类"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("文档转换工具")
        self.root.geometry("800x600")
        
        # 初始化处理器
        self.converter = DocumentConverter()
        self.doc_processor = DocumentProcessor()
        self.meeting_processor = MeetingProcessor()
        self.current_doc = None
        
        # 创建主框架
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 创建选项卡
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 创建各个功能选项卡
        self.create_convert_tab()
        self.create_word_process_tab()
        self.create_meeting_tab()
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)
        
    def create_convert_tab(self):
        """创建文档转换选项卡"""
        convert_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(convert_frame, text="文档转换")
        
        # 创建转换选项
        ttk.Label(convert_frame, text="选择转换类型：").grid(row=0, column=0, sticky=tk.W)
        self.convert_type = ttk.Combobox(convert_frame, values=[
            "Markdown转HTML",
            "Markdown转PowerPoint",
            "Markdown转Word",
            "Word转Markdown",
            "Word转PDF",
            "HTML转PowerPoint"
        ])
        self.convert_type.grid(row=0, column=1, sticky=(tk.W, tk.E))
        self.convert_type.bind('<<ComboboxSelected>>', self.update_convert_ui)
        
        # 输入文件选择
        ttk.Label(convert_frame, text="输入文件：").grid(row=1, column=0, sticky=tk.W)
        self.input_path = tk.StringVar()
        ttk.Entry(convert_frame, textvariable=self.input_path).grid(row=1, column=1, sticky=(tk.W, tk.E))
        ttk.Button(convert_frame, text="浏览", command=self.select_input_file).grid(row=1, column=2)
        
        # 输出文件选择
        ttk.Label(convert_frame, text="输出文件：").grid(row=2, column=0, sticky=tk.W)
        self.output_path = tk.StringVar()
        ttk.Entry(convert_frame, textvariable=self.output_path).grid(row=2, column=1, sticky=(tk.W, tk.E))
        ttk.Button(convert_frame, text="浏览", command=self.select_output_file).grid(row=2, column=2)
        
        # 转换按钮
        ttk.Button(convert_frame, text="开始转换", command=self.convert_document).grid(row=3, column=1, pady=10)
        
        # 配置网格权重
        convert_frame.columnconfigure(1, weight=1)
        
    def create_word_process_tab(self):
        """创建Word处理选项卡"""
        word_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(word_frame, text="Word处理")
        
        # 文件选择
        ttk.Label(word_frame, text="Word文件：").grid(row=0, column=0, sticky=tk.W)
        self.word_path = tk.StringVar()
        ttk.Entry(word_frame, textvariable=self.word_path).grid(row=0, column=1, sticky=(tk.W, tk.E))
        ttk.Button(word_frame, text="浏览", command=self.select_word_file).grid(row=0, column=2)
        
        # 处理选项
        ttk.Label(word_frame, text="处理选项：").grid(row=1, column=0, sticky=tk.W)
        self.word_process_frame = ttk.Frame(word_frame)
        self.word_process_frame.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E))
        
        # 优化格式
        self.optimize_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(self.word_process_frame, text="优化格式", variable=self.optimize_var).grid(row=0, column=0, sticky=tk.W)
        
        # 添加摘要
        self.add_summary_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(self.word_process_frame, text="添加摘要", variable=self.add_summary_var).grid(row=0, column=1, sticky=tk.W)
        self.summary_text = tk.StringVar()
        ttk.Entry(self.word_process_frame, textvariable=self.summary_text).grid(row=0, column=2, sticky=(tk.W, tk.E))
        
        # 提取关键词
        self.extract_keywords_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(self.word_process_frame, text="提取关键词", variable=self.extract_keywords_var).grid(row=1, column=0, sticky=tk.W)
        
        # 添加水印
        self.add_watermark_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(self.word_process_frame, text="添加水印", variable=self.add_watermark_var).grid(row=1, column=1, sticky=tk.W)
        self.watermark_text = tk.StringVar()
        ttk.Entry(self.word_process_frame, textvariable=self.watermark_text).grid(row=1, column=2, sticky=(tk.W, tk.E))
        
        # 处理按钮
        ttk.Button(word_frame, text="开始处理", command=self.process_word).grid(row=2, column=1, pady=10)
        
        # 配置网格权重
        word_frame.columnconfigure(1, weight=1)
        self.word_process_frame.columnconfigure(2, weight=1)
        
    def create_meeting_tab(self):
        """创建会议处理选项卡"""
        meeting_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(meeting_frame, text="会议处理")
        
        # 会议文件选择
        ttk.Label(meeting_frame, text="会议文件：").grid(row=0, column=0, sticky=tk.W)
        self.meeting_path = tk.StringVar()
        ttk.Entry(meeting_frame, textvariable=self.meeting_path).grid(row=0, column=1, sticky=(tk.W, tk.E))
        ttk.Button(meeting_frame, text="浏览", command=self.select_meeting_file).grid(row=0, column=2)
        
        # 会议信息
        ttk.Label(meeting_frame, text="会议信息：").grid(row=1, column=0, sticky=tk.W)
        self.meeting_info_frame = ttk.Frame(meeting_frame)
        self.meeting_info_frame.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E))
        
        # 会议标题
        ttk.Label(self.meeting_info_frame, text="标题：").grid(row=0, column=0, sticky=tk.W)
        self.meeting_title = tk.StringVar()
        ttk.Entry(self.meeting_info_frame, textvariable=self.meeting_title).grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        # 会议日期
        ttk.Label(self.meeting_info_frame, text="日期：").grid(row=1, column=0, sticky=tk.W)
        self.meeting_date = tk.StringVar()
        ttk.Entry(self.meeting_info_frame, textvariable=self.meeting_date).grid(row=1, column=1, sticky=(tk.W, tk.E))
        
        # 参会人员
        ttk.Label(self.meeting_info_frame, text="参会人员：").grid(row=2, column=0, sticky=tk.W)
        self.meeting_attendees = tk.StringVar()
        ttk.Entry(self.meeting_info_frame, textvariable=self.meeting_attendees).grid(row=2, column=1, sticky=(tk.W, tk.E))
        
        # 处理选项
        ttk.Label(meeting_frame, text="处理选项：").grid(row=2, column=0, sticky=tk.W)
        self.meeting_process_frame = ttk.Frame(meeting_frame)
        self.meeting_process_frame.grid(row=2, column=1, columnspan=2, sticky=(tk.W, tk.E))
        
        # 提取议程
        self.extract_agenda_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(self.meeting_process_frame, text="提取议程", variable=self.extract_agenda_var).grid(row=0, column=0, sticky=tk.W)
        
        # 提取决议
        self.extract_resolutions_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(self.meeting_process_frame, text="提取决议", variable=self.extract_resolutions_var).grid(row=0, column=1, sticky=tk.W)
        
        # 生成纪要
        self.generate_summary_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(self.meeting_process_frame, text="生成纪要", variable=self.generate_summary_var).grid(row=1, column=0, sticky=tk.W)
        
        # 处理按钮
        ttk.Button(meeting_frame, text="开始处理", command=self.process_meeting).grid(row=3, column=1, pady=10)
        
        # 配置网格权重
        meeting_frame.columnconfigure(1, weight=1)
        self.meeting_info_frame.columnconfigure(1, weight=1)
        self.meeting_process_frame.columnconfigure(1, weight=1)
        
    def update_convert_ui(self, event=None):
        """更新转换界面"""
        convert_type = self.convert_type.get()
        if "Markdown" in convert_type:
            self.input_path.set("")
            self.output_path.set("")
        elif "Word" in convert_type:
            self.input_path.set("")
            self.output_path.set("")
        elif "HTML" in convert_type:
            self.input_path.set("")
            self.output_path.set("")
            
    def select_input_file(self):
        """选择输入文件"""
        convert_type = self.convert_type.get()
        if "Markdown" in convert_type:
            filetypes = [("Markdown文件", "*.md")]
        elif "Word" in convert_type:
            filetypes = [("Word文件", "*.docx")]
        elif "HTML" in convert_type:
            filetypes = [("HTML文件", "*.html")]
        else:
            filetypes = [("所有文件", "*.*")]
            
        filename = filedialog.askopenfilename(filetypes=filetypes)
        if filename:
            self.input_path.set(filename)
            
    def select_output_file(self):
        """选择输出文件"""
        convert_type = self.convert_type.get()
        if "HTML" in convert_type:
            filetypes = [("HTML文件", "*.html")]
        elif "PowerPoint" in convert_type:
            filetypes = [("PowerPoint文件", "*.pptx")]
        elif "Word" in convert_type:
            filetypes = [("Word文件", "*.docx")]
        elif "PDF" in convert_type:
            filetypes = [("PDF文件", "*.pdf")]
        elif "Markdown" in convert_type:
            filetypes = [("Markdown文件", "*.md")]
        else:
            filetypes = [("所有文件", "*.*")]
            
        filename = filedialog.asksaveasfilename(filetypes=filetypes)
        if filename:
            self.output_path.set(filename)
            
    def convert_document(self):
        """转换文档"""
        try:
            input_path = self.input_path.get()
            output_path = self.output_path.get()
            convert_type = self.convert_type.get()
            
            if not input_path or not output_path:
                messagebox.showerror("错误", "请选择输入和输出文件！")
                return
                
            if convert_type == "Markdown转HTML":
                self.converter.md_to_html(input_path, output_path)
            elif convert_type == "Markdown转PowerPoint":
                self.converter.md_to_ppt(input_path, output_path)
            elif convert_type == "Markdown转Word":
                self.converter.md_to_docx(input_path, output_path)
            elif convert_type == "Word转Markdown":
                self.converter.docx_to_md(input_path, output_path)
            elif convert_type == "Word转PDF":
                self.converter.docx_to_pdf(input_path, output_path)
            elif convert_type == "HTML转PowerPoint":
                self.converter.html_to_ppt(input_path, output_path)
                
            messagebox.showinfo("成功", "文档转换完成！")
            
        except Exception as e:
            messagebox.showerror("错误", f"转换失败：{str(e)}")
            
    def select_word_file(self):
        """选择Word文件"""
        filename = filedialog.askopenfilename(filetypes=[("Word文件", "*.docx")])
        if filename:
            self.word_path.set(filename)
            self.current_doc = self.doc_processor.read_document(filename)
            
    def process_word(self):
        """处理Word文档"""
        try:
            if not self.current_doc:
                messagebox.showerror("错误", "请先选择Word文件！")
                return
                
            # 优化格式
            if self.optimize_var.get():
                self.current_doc = self.doc_processor.optimize_format(self.current_doc)
                
            # 添加摘要
            if self.add_summary_var.get():
                summary = self.summary_text.get()
                if summary:
                    self.current_doc = self.doc_processor.add_summary(self.current_doc, summary)
                    
            # 提取关键词
            if self.extract_keywords_var.get():
                keywords = self.doc_processor.extract_keywords(self.current_doc)
                keyword_text = "\n".join([f"- {word}: {freq}次" for word, freq in keywords])
                messagebox.showinfo("关键词", keyword_text)
                
            # 添加水印
            if self.add_watermark_var.get():
                watermark = self.watermark_text.get()
                if watermark:
                    self.current_doc = self.doc_processor.add_watermark(self.current_doc, watermark)
                    
            # 保存文件
            output_path = filedialog.asksaveasfilename(filetypes=[("Word文件", "*.docx")])
            if output_path:
                self.doc_processor.save_document(self.current_doc, output_path)
                messagebox.showinfo("成功", "文档处理完成！")
                
        except Exception as e:
            messagebox.showerror("错误", f"处理失败：{str(e)}")
            
    def select_meeting_file(self):
        """选择会议文件"""
        filename = filedialog.askopenfilename(filetypes=[("Word文件", "*.docx")])
        if filename:
            self.meeting_path.set(filename)
            
    def process_meeting(self):
        """处理会议文档"""
        try:
            input_path = self.meeting_path.get()
            if not input_path:
                messagebox.showerror("错误", "请选择会议文件！")
                return
                
            # 获取会议信息
            meeting_info = {
                "title": self.meeting_title.get(),
                "date": self.meeting_date.get(),
                "attendees": self.meeting_attendees.get().split(",")
            }
            
            # 处理会议文档
            if self.extract_agenda_var.get():
                agenda = self.meeting_processor.extract_agenda(input_path)
                messagebox.showinfo("议程", agenda)
                
            if self.extract_resolutions_var.get():
                resolutions = self.meeting_processor.extract_resolutions(input_path)
                messagebox.showinfo("决议", resolutions)
                
            if self.generate_summary_var.get():
                summary = self.meeting_processor.generate_summary(input_path, meeting_info)
                output_path = filedialog.asksaveasfilename(filetypes=[("Word文件", "*.docx")])
                if output_path:
                    self.meeting_processor.save_summary(summary, output_path)
                    messagebox.showinfo("成功", "会议纪要生成完成！")
                    
        except Exception as e:
            messagebox.showerror("错误", f"处理失败：{str(e)}")

def main():
    root = tk.Tk()
    app = ConverterGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 