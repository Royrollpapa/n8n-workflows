from meeting_processor import MeetingDocumentProcessor
import os

def process_meeting_document():
    # 初始化处理器
    processor = MeetingDocumentProcessor()
    
    # 读取原始文档
    input_file = os.path.join('..', 'Docs', '250527_SUS Panel.docx')
    if not processor.read_document(input_file):
        print("无法读取文档")
        return
        
    # 添加温松英自我介绍部分
    processor.add_content_update(
        section="自我介绍",
        original_text="",
        updated_text_cn="""尊敬的各位嘉宾，大家好！我是奇瑞循环经济业务负责人温松英。作为奇瑞集团在循环经济领域的负责人，我致力于推动汽车产业的可持续发展转型。在过去的几年里，我们与西门子等合作伙伴一起，在智能制造、绿色工厂建设等方面取得了显著成果。特别是在循环经济领域，我们正在探索从产品设计、生产制造到回收利用的全生命周期管理新模式。""",
        updated_text_en="""Distinguished guests, good day! I am Wen Songying, Head of Circular Economy Business at Chery. As the person in charge of circular economy at Chery Group, I am committed to promoting the sustainable development transformation of the automotive industry. Over the past few years, we have achieved significant results in intelligent manufacturing and green factory construction together with partners like Siemens. Particularly in the circular economy field, we are exploring new models for full lifecycle management from product design, manufacturing to recycling."""
    )
    
    # 添加全球循环经济机遇观察
    processor.add_content_update(
        section="全球循环经济机遇",
        original_text="",
        updated_text_cn="""在全球范围内，循环经济正迎来前所未有的发展机遇。根据麦肯锡咨询公司的研究，到2030年，全球循环经济市场规模将达到4.5万亿美元。在汽车行业，我们看到了三个主要机遇：首先是新能源汽车的快速发展带来的电池回收利用需求；其次是智能制造带来的资源利用效率提升；第三是数字化技术推动的供应链优化。奇瑞正在这些领域积极布局，并与西门子等合作伙伴共同探索创新解决方案。""",
        updated_text_en="""Globally, the circular economy is facing unprecedented development opportunities. According to McKinsey's research, the global circular economy market will reach $4.5 trillion by 2030. In the automotive industry, we see three main opportunities: first, the rapid development of new energy vehicles brings demand for battery recycling; second, intelligent manufacturing improves resource utilization efficiency; third, digital technology drives supply chain optimization. Chery is actively deploying in these areas and exploring innovative solutions with partners like Siemens."""
    )
    
    # 添加技术与生态合作实践
    processor.add_content_update(
        section="技术与生态合作",
        original_text="",
        updated_text_cn="""在技术与生态合作方面，奇瑞与西门子已经建立了深入的合作关系。我们共同开发了智能工厂解决方案，通过数字化技术实现了生产过程的精准控制和资源优化。在循环经济领域，我们正在合作开发电池回收利用技术，建立完整的回收利用体系。同时，我们也与产业链上下游企业建立了紧密的合作关系，共同构建绿色供应链。这些实践不仅提升了我们的竞争力，也为行业可持续发展做出了贡献。""",
        updated_text_en="""In terms of technology and ecosystem cooperation, Chery and Siemens have established an in-depth partnership. We have jointly developed intelligent factory solutions, achieving precise control and resource optimization of production processes through digital technology. In the circular economy field, we are cooperating to develop battery recycling technology and establish a complete recycling system. Meanwhile, we have also established close cooperation with upstream and downstream enterprises in the industry chain to build a green supply chain together. These practices have not only enhanced our competitiveness but also contributed to the sustainable development of the industry."""
    )
    
    # 添加人才思考
    processor.add_content_update(
        section="人才发展",
        original_text="",
        updated_text_cn="""在人才发展方面，我们认为可持续发展需要复合型人才。奇瑞正在与西门子合作开展人才培养计划，包括技术培训、管理能力提升和可持续发展理念培养。我们特别注重培养具有创新思维和跨学科知识的人才，他们能够将循环经济理念与技术创新相结合，推动企业可持续发展。同时，我们也建立了完善的人才激励机制，鼓励员工在可持续发展领域进行创新。""",
        updated_text_en="""In terms of talent development, we believe that sustainable development requires interdisciplinary talents. Chery is cooperating with Siemens to implement talent development programs, including technical training, management capability enhancement, and sustainable development concept cultivation. We particularly focus on cultivating talents with innovative thinking and interdisciplinary knowledge, who can combine circular economy concepts with technological innovation to promote enterprise sustainable development. Meanwhile, we have also established a comprehensive talent incentive mechanism to encourage employees to innovate in the field of sustainable development."""
    )
    
    # 添加未来愿景
    processor.add_content_update(
        section="未来愿景",
        original_text="",
        updated_text_cn="""展望未来，奇瑞将继续深化与西门子的合作，共同打造汽车行业循环经济的标杆。我们的目标是到2025年，实现生产过程的零废弃物排放，建立完整的循环经济产业链。我们将继续加大在智能制造、绿色技术研发等方面的投入，推动汽车产业向更可持续的方向发展。同时，我们也期待与更多志同道合的伙伴一起，共同构建绿色、可持续的未来。""",
        updated_text_en="""Looking to the future, Chery will continue to deepen cooperation with Siemens to jointly create a benchmark for circular economy in the automotive industry. Our goal is to achieve zero waste emissions in the production process and establish a complete circular economy industry chain by 2025. We will continue to increase investment in intelligent manufacturing and green technology R&D to promote the development of the automotive industry towards a more sustainable direction. Meanwhile, we also look forward to working with more like-minded partners to build a green and sustainable future together."""
    )
    
    # 生成更新报告
    report_path = os.path.join('..', 'Docs', 'meeting_update_report.docx')
    processor.generate_update_report(report_path)
    
    # 导出到Excel
    excel_path = os.path.join('..', 'Docs', 'meeting_updates.xlsx')
    processor.export_to_excel(excel_path)
    
    print("文档处理完成！")
    print(f"更新报告已保存至：{report_path}")
    print(f"Excel文件已保存至：{excel_path}")

if __name__ == "__main__":
    process_meeting_document() 