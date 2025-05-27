# Парсер текста

## Описание
Парсер текста - это инструмент для извлечения и анализа текста из различных форматов файлов. Он поддерживает работу с PDF, DOCX, DOC, DJVU файлами, а также может анализировать текст с веб-страниц.

## Возможности
- Извлечение текста из PDF файлов
- Извлечение текста из DOCX файлов
- Извлечение текста из DOC файлов
- Извлечение текста из DJVU файлов
- Парсинг текста с веб-страниц
- Лингвистический анализ текста (определение частей речи, зависимостей)
- Автоматическое определение языка текста
- Исправление опечаток в тексте

## Требования
- Python 3.8+
- PyMuPDF
- spaCy
- langdetect
- beautifulsoup4
- requests
- python-docx
- pytest
- pywin32
- Cython>=0.20

## Установка
1. Клонируйте репозиторий:
```bash
git clone [url-репозитория]
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Загрузите модель spaCy для русского языка:
```bash
python -m spacy download ru_core_news_sm
```

## Использование
### Извлечение текста из файлов
```python
from parser.utils.pdf_extractor import extract_text_from_pdf
from parser.utils.docx_extractor import extract_text_from_docx
from parser.utils.doc_extractor import extract_text_from_doc
from parser.utils.djvu_extractor import extract_text_from_djvu

# Извлечение текста из PDF
text = extract_text_from_pdf("path/to/file.pdf")

# Извлечение текста из DOCX
text = extract_text_from_docx("path/to/file.docx")

# Извлечение текста из DOC
text = extract_text_from_doc("path/to/file.doc")

# Извлечение текста из DJVU
text = extract_text_from_djvu("path/to/file.djvu")
```

### Парсинг веб-страниц
```python
from parser.utils.html_parser import parse_html

# Парсинг текста с веб-страницы
text = parse_html("https://example.com")
```

### Анализ текста
```python
from parser.utils.text_analyzer import analyze_text

# Анализ текста
result = analyze_text("Текст для анализа")
```

## Тестирование
Для запуска тестов используйте команду:
```bash
python -m pytest tests/test_unit.py -v
```

## Структура проекта
```
parser/
├── utils/
│   ├── pdf_extractor.py
│   ├── docx_extractor.py
│   ├── doc_extractor.py
│   ├── djvu_extractor.py
│   ├── html_parser.py
│   └── text_analyzer.py
├── tests/
│   └── test_unit.py
├── requirements.txt
└── README.md
```

## Особенности реализации
- Использование моков в тестах для изоляции тестируемого кода
- Обработка граничных случаев и ошибок
- Поддержка различных форматов файлов
- Автоматическое определение языка текста
- Исправление опечаток в тексте
