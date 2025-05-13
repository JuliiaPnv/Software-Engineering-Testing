from utils.pdf_extractor import extract_text_from_pdf
from utils.docx_extractor import extract_text_from_docx
from utils.doc_extractor import extract_text_from_doc
from utils.djvu_extractor import extract_text_from_djvu
from utils.text_analyzer import analyze_text
from utils.html_parser import parse_html
import os

def main():
    # Запрос путей к файлам и URL у пользователя
    pdf_path = input("Введите путь к PDF файлу (или нажмите Enter, чтобы пропустить): ") or os.path.join('tests', 'sample.pdf')
    docx_path = input("Введите путь к DOCX файлу (или нажмите Enter, чтобы пропустить): ") or os.path.join('tests', 'sample.docx')
    doc_path = input("Введите путь к DOC файлу (или нажмите Enter, чтобы пропустить): ") or os.path.join('tests', 'sample.doc')
    djvu_path = input("Введите путь к DJVU файлу (или нажмите Enter, чтобы пропустить): ") or os.path.join('tests', 'sample.djvu')
    url = input("Введите URL веб-страницы (или нажмите Enter, чтобы пропустить): ")

    # Извлечение и анализ текста
    if pdf_path:
        pdf_text = extract_text_from_pdf(pdf_path)
        print("Извлеченный текст из PDF:")
        print(pdf_text)
        analyze_text(pdf_text)

    if docx_path:
        docx_text = extract_text_from_docx(docx_path)
        print("Извлеченный текст из DOCX:")
        print(docx_text)
        analyze_text(docx_text)

    if doc_path:
        doc_text = extract_text_from_doc(doc_path)
        print("Извлеченный текст из DOC:")
        print(doc_text)
        analyze_text(doc_text)

    if djvu_path:
        djvu_text = extract_text_from_djvu(djvu_path)
        print("Извлеченный текст из DJVU:")
        print(djvu_text)
        analyze_text(djvu_text)

    if url:
        parse_html(url)

if __name__ == "__main__":
    main()
