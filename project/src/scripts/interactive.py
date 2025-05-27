import os
import sys
from pathlib import Path
import logging
from converter import DocumentConverter
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk, ImageEnhance
import urllib.request
import json
from ai_md_to_html import generate_html_with_ai_for_gui

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("文档转换工具")
        self.root.geometry("700x600")
        self.root.minsize(700, 600)
        self.root.resizable(True, True)
        self.config_path = str(Path(__file__).parent / ".." / ".." / "config" / "config.yaml")
        self.converter = DocumentConverter(self.config_path)
        
        # 主题色与字体
        self.colors = {
            'primary': '#007AFF',      # 苹果蓝
            'background': '#F5F5F7',   # 背景色
            'surface': '#FFFFFF',      # 卡片色
            'text': '#1D1D1F',         # 文本色
            'border': '#D2D2D7',       # 边框色
        }
        self.fonts = {
            'title': ('SF Pro Display', 20, 'bold'),
            'subtitle': ('SF Pro Text', 16, 'bold'),
            'body': ('SF Pro Text', 15),
            'button': ('SF Pro Text', 16, 'bold')
        }
        self.conversion_types = {
            "md_to_html": "Markdown转HTML",
            "md_to_ppt": "Markdown转PPT",
            "md_to_html_ppt": "Markdown转HTML+PPT",
            "ai_md_to_html": "AI优化Markdown转HTML"
        }
        self.load_resources()
        self.setup_ui()

    def load_resources(self):
        """加载logo资源"""
        try:
            resource_dir = Path(__file__).parent / ".." / "resources" / "images"
            resource_dir.mkdir(parents=True, exist_ok=True)
            drive_icon_path = resource_dir / "drive_icon.png"
            # 若本地无drive_icon则下载Google Drive图标
            if not drive_icon_path.exists():
                url = "https://img.icons8.com/color/48/google-drive--v2.png"
                urllib.request.urlretrieve(url, drive_icon_path)
            # 转换类型logo
            drive_logo_img = Image.open(drive_icon_path).resize((32, 32), Image.Resampling.LANCZOS)
            self.drive_logo = ImageTk.PhotoImage(drive_logo_img)
        except Exception as e:
            logger.error(f"加载logo失败: {e}")
            self.drive_logo = None

    def create_card(self, parent, **kwargs):
        frame = tk.Frame(
            parent,
            bg=self.colors['surface'],
            bd=0,
            highlightthickness=1,
            highlightbackground=self.colors['border'],
            **kwargs
        )
        return frame

    def create_button(self, parent, text, command, **kwargs):
        button = tk.Button(
            parent,
            text=text,
            command=command,
            font=self.fonts['button'],
            bg=self.colors['primary'],
            fg='white',
            relief=tk.FLAT,
            padx=20,
            pady=10,
            cursor="hand2",
            borderwidth=0,
            highlightthickness=0,
            **kwargs
        )
        button.configure(overrelief=tk.FLAT)
        button.bind("<Enter>", lambda e: button.config(bg="#005BBB"))
        button.bind("<Leave>", lambda e: button.config(bg=self.colors['primary']))
        return button

    def setup_ui(self):
        # 只用Frame，不用Canvas和背景logo
        self.main_container = tk.Frame(self.root, bg=self.colors['background'])
        self.main_container.pack(fill=tk.BOTH, expand=True)
        # 标题栏（无logo，仅文字）
        title_frame = self.create_card(self.main_container)
        title_frame.pack(fill=tk.X, pady=(10, 10), padx=10)
        title_label = tk.Label(
            title_frame,
            text="文档转换工具",
            font=self.fonts['title'],
            bg=self.colors['surface'],
            fg=self.colors['text']
        )
        title_label.pack(side=tk.LEFT, padx=0, pady=8)
        # 源文件选择
        source_frame = self.create_card(self.main_container)
        source_frame.pack(fill=tk.X, pady=(10, 10), padx=10)
        tk.Label(
            source_frame,
            text="选择源文件",
            font=self.fonts['subtitle'],
            bg=self.colors['surface'],
            fg=self.colors['text']
        ).pack(side=tk.LEFT, padx=16, pady=12)
        self.source_entry = tk.Entry(
            source_frame,
            width=22,
            font=self.fonts['body'],
            relief=tk.GROOVE,
            bd=2
        )
        self.source_entry.pack(side=tk.LEFT, padx=8, pady=12, ipady=8, fill=tk.X, expand=True)
        self.create_button(
            source_frame,
            "浏览",
            self.select_source_file
        ).pack(side=tk.LEFT, padx=16, pady=12, fill=tk.X, expand=True)
        # 转换类型（drive logo+下拉菜单）
        type_frame = self.create_card(self.main_container)
        type_frame.pack(fill=tk.X, pady=(10, 10), padx=10)
        if hasattr(self, 'drive_logo') and self.drive_logo:
            logo_label2 = tk.Label(type_frame, image=self.drive_logo, bg=self.colors['surface'])
            logo_label2.pack(side=tk.LEFT, padx=(16, 8), pady=8)
        self.type_var = tk.StringVar()
        self.type_var.set(self.conversion_types["md_to_html"])
        self.type_menu = ttk.Combobox(
            type_frame,
            textvariable=self.type_var,
            state="readonly",
            font=self.fonts['body'],
            width=25
        )
        self.type_menu['values'] = list(self.conversion_types.values())
        self.type_menu.pack(side=tk.LEFT, padx=10, pady=8, ipady=8, fill=tk.X, expand=True)
        # 输出文件
        output_frame = self.create_card(self.main_container)
        output_frame.pack(fill=tk.X, pady=(10, 10), padx=10)
        tk.Label(
            output_frame,
            text="输出文件路径",
            font=self.fonts['subtitle'],
            bg=self.colors['surface'],
            fg=self.colors['text']
        ).pack(side=tk.LEFT, padx=16, pady=12)
        self.output_entry = tk.Entry(
            output_frame,
            width=22,
            font=self.fonts['body'],
            relief=tk.GROOVE,
            bd=2
        )
        self.output_entry.pack(side=tk.LEFT, padx=8, pady=12, ipady=8, fill=tk.X, expand=True)
        self.create_button(
            output_frame,
            "选择路径",
            self.select_output_file
        ).pack(side=tk.LEFT, padx=16, pady=12, fill=tk.X, expand=True)
        # 转换按钮
        convert_button = self.create_button(
            self.main_container,
            "开始转换",
            self.run_convert
        )
        convert_button.pack(pady=10, fill=tk.X, expand=True, padx=10)
        # 进度条
        style = ttk.Style()
        style.configure(
            "Custom.Horizontal.TProgressbar",
            troughcolor=self.colors['background'],
            background=self.colors['primary'],
            thickness=8
        )
        self.progress = ttk.Progressbar(
            self.main_container,
            orient=tk.HORIZONTAL,
            length=300,
            mode='determinate',
            style="Custom.Horizontal.TProgressbar"
        )
        self.progress.pack(pady=10, fill=tk.X, expand=True, padx=10)
        # 结果显示
        result_frame = self.create_card(self.main_container)
        result_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 10), padx=10)
        self.result_text = tk.Text(
            result_frame,
            height=6,
            width=30,
            font=self.fonts['body'],
            bg=self.colors['surface'],
            fg=self.colors['text'],
            relief=tk.FLAT,
            highlightthickness=1,
            highlightbackground=self.colors['border']
        )
        self.result_text.pack(padx=16, pady=16, fill=tk.BOTH, expand=True)
        self.create_tooltips()

    def create_tooltips(self):
        tooltips = {
            self.source_entry: "选择要转换的源文件",
            self.type_menu: "选择转换类型",
            self.output_entry: "选择输出文件路径",
            self.progress: "显示转换进度"
        }
        for widget, text in tooltips.items():
            self.create_tooltip(widget, text)

    def create_tooltip(self, widget, text):
        def show_tooltip(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            label = tk.Label(
                tooltip,
                text=text,
                background="#2C2C2E",
                fg="white",
                relief=tk.FLAT,
                font=self.fonts['body']
            )
            label.pack()
            def hide_tooltip():
                tooltip.destroy()
            widget.bind('<Leave>', lambda e: hide_tooltip())
            tooltip.bind('<Leave>', lambda e: hide_tooltip())
        widget.bind('<Enter>', show_tooltip)

    def select_source_file(self):
        filetypes = [("Markdown/HTML 文件", "*.md *.html"), ("所有文件", "*.*")]
        filename = filedialog.askopenfilename(title="选择源文件", filetypes=filetypes)
        if filename:
            self.source_entry.delete(0, tk.END)
            self.source_entry.insert(0, filename)
            ext = os.path.splitext(filename)[1].lower()
            if ext == '.md':
                self.type_var.set(self.conversion_types["md_to_ppt"])
            elif ext == '.html':
                self.type_var.set(self.conversion_types["md_to_html_ppt"])
            output_filename = os.path.splitext(filename)[0]
            if ext == '.md':
                output_filename += '.pptx'
            elif ext == '.html':
                output_filename += '.pptx'
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, output_filename)

    def select_output_file(self):
        conv_type = self.type_var.get()
        if conv_type in [self.conversion_types["md_to_html"], self.conversion_types["md_to_ppt"], self.conversion_types["md_to_html_ppt"]]:
            filetypes = [("HTML 文件", "*.html"), ("所有文件", "*.*")]
            default_ext = ".html"
        elif conv_type == self.conversion_types["ai_md_to_html"]:
            filetypes = [("Markdown文件", "*.md"), ("所有文件", "*.*")]
            default_ext = ""
        else:
            filetypes = [("所有文件", "*.*")]
            default_ext = ""
        filename = filedialog.asksaveasfilename(title="选择输出文件", filetypes=filetypes)
        if filename:
            if not os.path.splitext(filename)[1]:
                filename += default_ext
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, filename)

    def run_convert(self):
        source = self.source_entry.get().strip()
        output = self.output_entry.get().strip()
        conv_type = self.type_var.get()
        try:
            if conv_type == self.conversion_types["ai_md_to_html"]:
                input_path = filedialog.askopenfilename(
                    title="请选择要转换的Markdown文件",
                    filetypes=[("Markdown文件", "*.md"), ("所有文件", "*.*")]
                )
                if not input_path:
                    self.result_text.insert(tk.END, "未选择输入文件，已取消。\n")
                    return
                output_path = filedialog.asksaveasfilename(
                    title="保存生成的HTML文件",
                    defaultextension=".html",
                    filetypes=[("HTML文件", "*.html"), ("所有文件", "*.*")],
                    initialfile="ai_generated.html"
                )
                if not output_path:
                    self.result_text.insert(tk.END, "未选择输出文件名，已取消。\n")
                    return
                try:
                    self.result_text.insert(tk.END, "[AI] 正在生成HTML，请稍候...\n")
                    generate_html_with_ai_for_gui(input_path, output_path)
                    self.result_text.insert(tk.END, f"[AI] 已生成HTML：{output_path}\n")
                except Exception as e:
                    self.result_text.insert(tk.END, f"AI生成HTML失败: {e}\n")
                return
            if not os.path.isfile(source):
                raise Exception("源文件不存在")
            if not output:
                raise Exception("请指定输出文件路径")
            ext = os.path.splitext(source)[1].lower()
            # 新架构下的转换逻辑
            if conv_type == self.conversion_types["md_to_html"]:
                from md_to_html import MarkdownToHTML
                converter = MarkdownToHTML(self.config_path)
                result = converter.convert_to_html(source, output)
                self.result_text.insert(tk.END, f"转换成功！输出HTML文件：{result}\n")
            elif conv_type == self.conversion_types["md_to_ppt"]:
                from md_to_ppt import md_to_ppt
                result = md_to_ppt(source, output)
                self.result_text.insert(tk.END, f"转换成功！输出PPT文件：{output}\n")
            elif conv_type == self.conversion_types["md_to_html_ppt"]:
                from md_to_html import MarkdownToHTML
                from md_to_ppt import md_to_ppt
                converter = MarkdownToHTML(self.config_path)
                html_path = output if output.endswith('.html') else os.path.splitext(output)[0]+'.html'
                ppt_path = output if output.endswith('.pptx') else os.path.splitext(output)[0]+'.pptx'
                result_html = converter.convert_to_html(source, html_path)
                result_ppt = md_to_ppt(source, ppt_path)
                self.result_text.insert(tk.END, f"转换成功！输出HTML文件：{result_html}\n输出PPT文件：{ppt_path}\n")
            else:
                raise Exception("不支持的转换类型")
        except Exception as e:
            self.result_text.insert(tk.END, f"转换失败：{e}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = ConverterGUI(root)
    root.mainloop() 