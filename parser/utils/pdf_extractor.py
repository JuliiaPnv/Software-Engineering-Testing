import fitz  # PyMuPDF

def extract_text_from_pdf(file_path):
    try:
        document = fitz.open(file_path)
        text = ""
        for page_num in range(len(document)):
            page = document.load_page(page_num)
            text += page.get_text()
        return text
    except Exception as e:
        print(f"Ошибка при чтении PDF: {e}")
        return ""
