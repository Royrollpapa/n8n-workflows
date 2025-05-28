from meeting_processor import MeetingDocumentProcessor
import os

def convert_document():
    # 初始化处理器
    processor = MeetingDocumentProcessor()
    
    # 读取原始文档
    input_file = os.path.join('..', 'Docs', '250527_SUS Panel.docx')
    if not processor.read_document(input_file):
        print("无法读取文档")
        return
        
    # 转换并保存文档
    output_file = os.path.join('..', 'Docs', '250527_SUS Panel_converted.docx')
    if processor.update_document(output_file):
        print(f"文档转换完成！已保存至：{output_file}")
    else:
        print("文档转换失败")

if __name__ == "__main__":
    convert_document() 