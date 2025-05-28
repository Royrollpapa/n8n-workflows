import os
import sys
import subprocess

def convert_md_to_docx():
    print("========== Markdown 转 Word 调试信息 ==========")
    # 获取当前脚本所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"当前脚本目录: {current_dir}")
    # 获取项目根目录
    project_root = os.path.dirname(current_dir)
    print(f"项目根目录: {project_root}")
    
    # 构建输入和输出文件路径
    input_file = os.path.join(project_root, 'Docs', 'wen_speech.md')
    output_file = os.path.join(project_root, 'Docs', 'wen_speech.docx')
    reference_doc = os.path.join(project_root, 'Docs', '250527_SUS Panel.docx')
    print(f"输入文件: {input_file}")
    print(f"输出文件: {output_file}")
    print(f"参考文档: {reference_doc}")
    
    # 检查文件是否存在
    if not os.path.exists(input_file):
        print(f"错误：找不到输入文件 {input_file}")
        return False
    else:
        print(f"输入文件存在，大小: {os.path.getsize(input_file)} 字节")
    
    if not os.path.exists(reference_doc):
        print(f"错误：找不到参考文档 {reference_doc}")
        return False
    else:
        print(f"参考文档存在，大小: {os.path.getsize(reference_doc)} 字节")
    
    # 构建pandoc命令
    cmd = [
        'pandoc',
        input_file,
        '-o', output_file,
        '--toc',
        f'--reference-doc={reference_doc}'
    ]
    print(f"即将执行的pandoc命令: {' '.join(cmd)}")
    
    try:
        # 使用Popen运行命令并实时捕获输出
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        # 实时读取输出
        while True:
            output = process.stdout.readline()
            error = process.stderr.readline()
            
            if output:
                print(f"[pandoc stdout] {output.strip()}")
            if error:
                print(f"[pandoc stderr] {error.strip()}")
                
            # 检查进程是否结束
            if process.poll() is not None:
                # 读取剩余输出
                for line in process.stdout:
                    print(f"[pandoc stdout] {line.strip()}")
                for line in process.stderr:
                    print(f"[pandoc stderr] {line.strip()}")
                break
        
        # 获取返回码
        return_code = process.poll()
        print(f"pandoc 返回码: {return_code}")
        
        if return_code == 0:
            print(f"成功：已将 {input_file} 转换为 {output_file}")
            if os.path.exists(output_file):
                print(f"输出文件已生成，大小: {os.path.getsize(output_file)} 字节")
            else:
                print(f"警告：pandoc返回成功但未找到输出文件 {output_file}")
            return True
        else:
            print(f"错误：转换失败，返回码 {return_code}")
            return False
            
    except Exception as e:
        print(f"错误：执行pandoc命令时出错 - {str(e)}")
        return False

if __name__ == '__main__':
    success = convert_md_to_docx()
    sys.exit(0 if success else 1) 