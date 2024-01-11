# file_handler.py

import io
from PyPDF2 import PdfReader
from docx import Document
from openpyxl import load_workbook
from pptx import Presentation
from PIL import Image
import pytesseract

def handle_uploaded_file(uploaded_file):
    """
    处理上传的文件并返回文本内容。
    支持PDF、DOCX、XLSX、XLS、PPTX、PPT、TXT文件格式以及图片格式。
    """
    try:
        # 根据文件类型处理文件
        if uploaded_file.type == "text/plain":
            # 处理文本文件
            text = io.TextIOWrapper(uploaded_file, encoding='utf-8').read()
        
        elif uploaded_file.type in ["application/pdf"]:
            # 处理PDF文件
            reader = PdfReader(uploaded_file)
            text = ''
            for page in reader.pages:
                text += page.extract_text()

        elif uploaded_file.type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
            # 处理DOCX文件
            doc = Document(uploaded_file)
            text = '\n'.join([para.text for para in doc.paragraphs])

        elif uploaded_file.type in ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/vnd.ms-excel"]:
            # 处理XLSX和XLS文件
            workbook = load_workbook(filename=uploaded_file)
            text = ''
            for sheet in workbook.sheetnames:
                worksheet = workbook[sheet]
                for row in worksheet.iter_rows():
                    for cell in row:
                        text += str(cell.value) + '\t'
                    text += '\n'

        elif uploaded_file.type in ["application/vnd.openxmlformats-officedocument.presentationml.presentation", "application/vnd.ms-powerpoint"]:
            # 处理PPTX和PPT文件
            presentation = Presentation(uploaded_file)
            text = ''
            for slide in presentation.slides:
                for shape in slide.shapes:
                    if hasattr(shape, "text"):
                        text += shape.text + '\n'

        elif uploaded_file.type in ["image/jpeg", "image/png"]:
            # 处理图片文件
            image = Image.open(uploaded_file)
            text = pytesseract.image_to_string(image)

        else:
            raise ValueError("不支持的文件类型")

        return text

    except Exception as e:
        return str(e)

