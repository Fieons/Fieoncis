import PyPDF2

def pdf_to_text(file_path:str,out_file_path:str):
    # 打开PDF文件
    with open(file_path, 'rb') as file:
        # 创建一个PDF阅读器对象
        pdf_reader = PyPDF2.PdfReader(file)

        # 获取PDF文件中的文本
        text = ""
        for page_num in range(46,58):
            text += pdf_reader.pages[page_num].extract_text()

    with open(out_file_path,'w',encoding='utf-8') as f:
        f.write(text)

# 使用文件路径替换要读取的PDF文件的路径
file_path = "E:\\BaiduNetdiskDownload\Hitchhiker's Guide to the Galaxy.pdf"
out_file_path = "E:\\BaiduNetdiskDownload\\ttt.txt"
pdf_to_text(file_path,out_file_path)
