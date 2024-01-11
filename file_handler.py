# file_handler.py

import io
import PyPDF2
from docx import Document

def handle_uploaded_file(uploaded_file):
    """
    处理上传的文件并返回文本内容。
    支持PDF、DOCX和TXT文件格式。
    """
    try:
        # 根据文件类型处理文件
        if uploaded_file.type == "text/plain":
            # 处理文本文件
            text = io.TextIOWrapper(uploaded_file, encoding='utf-8').read()
        
        elif uploaded_file.type in ["application/pdf"]:
            # 处理PDF文件
            reader = PyPDF2.PdfFileReader(uploaded_file)
            text = ''
            for page in range(reader.numPages):
                text += reader.getPage(page).extractText()

        elif uploaded_file.type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
            # 处理DOCX文件
            doc = Document(uploaded_file)
            text = '\n'.join([para.text for para in doc.paragraphs])

        else:
            raise ValueError("不支持的文件类型")

        return text

    except Exception as e:
        return str(e)
