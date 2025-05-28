from document_processor import DocumentProcessor
import os

def print_menu():
    print("\n=== Word文档处理工具 ===")
    print("1. 读取文档")
    print("2. 显示文档内容")
    print("3. 优化文档格式")
    print("4. 添加文档摘要")
    print("5. 提取关键词")
    print("6. 添加水印")
    print("7. 保存文档")
    print("0. 退出")
    print("=====================")

def main():
    processor = DocumentProcessor()
    
    while True:
        print_menu()
        choice = input("请选择操作 (0-7): ")
        
        if choice == "0":
            break
            
        elif choice == "1":
            file_path = input("请输入Word文档路径: ")
            if os.path.exists(file_path):
                if processor.read_document(file_path):
                    print("文档读取成功！")
                else:
                    print("文档读取失败！")
            else:
                print("文件不存在！")
                
        elif choice == "2":
            content = processor.get_document_content()
            print("\n文档内容:")
            print(content)
            
        elif choice == "3":
            if processor.optimize_content():
                print("文档格式优化成功！")
            else:
                print("文档格式优化失败！")
                
        elif choice == "4":
            summary = input("请输入文档摘要: ")
            if processor.add_summary(summary):
                print("摘要添加成功！")
            else:
                print("摘要添加失败！")
                
        elif choice == "5":
            keywords = processor.extract_keywords()
            print("\n文档关键词:")
            for word, freq in keywords:
                print(f"{word}: {freq}次")
                
        elif choice == "6":
            watermark = input("请输入水印文字: ")
            if processor.add_watermark(watermark):
                print("水印添加成功！")
            else:
                print("水印添加失败！")
                
        elif choice == "7":
            file_path = input("请输入保存路径: ")
            if processor.save_document(file_path):
                print("文档保存成功！")
            else:
                print("文档保存失败！")
                
        else:
            print("无效的选择！")
            
        input("\n按回车键继续...")

if __name__ == "__main__":
    main() 