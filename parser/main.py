from utils.pdf_extractor import extract_text_from_pdf
from utils.docx_extractor import extract_text_from_docx
from utils.doc_extractor import extract_text_from_doc
from utils.djvu_extractor import extract_text_from_djvu
from utils.text_analyzer import analyze_text
from utils.html_parser import parse_html
import os

def print_analysis_results(analysis_results):
    print("\nРезультаты анализа текста:")
    print("-" * 50)
    print(f"{'Слово':<15} {'Лемма':<15} {'Часть речи':<15} {'Зависимость':<15}")
    print("-" * 50)
    for token in analysis_results:
        print(f"{token['text']:<15} {token['lemma']:<15} {token['position']:<15} {token['dependency']:<15}")
    print("-" * 50)

def main():
    # Запрос путей к файлам и URL у пользователя
    pdf_path = input("Введите путь к PDF файлу (или нажмите Enter, чтобы пропустить): ")
    docx_path = input("Введите путь к DOCX файлу (или нажмите Enter, чтобы пропустить): ")
    doc_path = input("Введите путь к DOC файлу (или нажмите Enter, чтобы пропустить): ")
    djvu_path = input("Введите путь к DJVU файлу (или нажмите Enter, чтобы пропустить): ")
    url = input("Введите URL веб-страницы (или нажмите Enter, чтобы пропустить): ")

    # Извлечение и анализ текста
    if pdf_path and os.path.exists(pdf_path):
        try:
            pdf_text = extract_text_from_pdf(pdf_path)
            if pdf_text:
                print("Извлеченный текст из PDF:")
                print(pdf_text)
                analysis_results = analyze_text(pdf_text)
                print_analysis_results(analysis_results)
            else:
                print("Не удалось извлечь текст из PDF файла")
        except Exception as e:
            print(f"Ошибка при обработке PDF файла: {str(e)}")

    if docx_path and os.path.exists(docx_path):
        try:
            docx_text = extract_text_from_docx(docx_path)
            if docx_text:
                print("Извлеченный текст из DOCX:")
                print(docx_text)
                analysis_results = analyze_text(docx_text)
                print_analysis_results(analysis_results)
            else:
                print("Не удалось извлечь текст из DOCX файла")
        except Exception as e:
            print(f"Ошибка при обработке DOCX файла: {str(e)}")

    if doc_path and os.path.exists(doc_path):
        try:
            doc_text = extract_text_from_doc(doc_path)
            if doc_text:
                print("Извлеченный текст из DOC:")
                print(doc_text)
                analysis_results = analyze_text(doc_text)
                print_analysis_results(analysis_results)
            else:
                print("Не удалось извлечь текст из DOC файла")
        except Exception as e:
            print(f"Ошибка при обработке DOC файла: {str(e)}")

    if djvu_path and os.path.exists(djvu_path):
        try:
            djvu_text = extract_text_from_djvu(djvu_path)
            if djvu_text:
                print("Извлеченный текст из DJVU:")
                print(djvu_text)
                analysis_results = analyze_text(djvu_text)
                print_analysis_results(analysis_results)
            else:
                print("Не удалось извлечь текст из DJVU файла")
        except Exception as e:
            print(f"Ошибка при обработке DJVU файла: {str(e)}")

    if url:
        try:
            parse_html(url)
        except Exception as e:
            print(f"Ошибка при обработке URL: {str(e)}")

if __name__ == "__main__":
    main()
