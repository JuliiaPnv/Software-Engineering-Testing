import pytest
from unittest.mock import patch, MagicMock, mock_open
import subprocess
from parser.utils.pdf_extractor import extract_text_from_pdf
from parser.utils.docx_extractor import extract_text_from_docx
from parser.utils.doc_extractor import extract_text_from_doc
from parser.utils.djvu_extractor import extract_text_from_djvu
from parser.utils.html_extractor import parse_html
from parser.utils.text_analyzer import analyze_text
from parser.Exceptions import LanguageError
from langdetect.lang_detect_exception import LangDetectException

# Тесты для извлечения текста из PDF файлов
def test_extract_text_from_pdf_success():
    """
    Проверяет успешное извлечение текста из PDF файла.
    Тест симулирует работу библиотеки PyMuPDF (fitz) для чтения PDF.
    """
    mock_document = MagicMock()
    mock_page = MagicMock()
    mock_page.get_text.return_value = "Test text"
    mock_document.load_page.return_value = mock_page
    mock_document.__len__.return_value = 1
    
    with patch('parser.utils.pdf_extractor.fitz.open', return_value=mock_document):
        result = extract_text_from_pdf("test_sample.pdf")
        assert result == "Test text"

def test_extract_text_from_pdf_error():
    """
    Проверяет обработку ошибки при чтении PDF файла.
    Тест проверяет, что функция возвращает пустую строку при возникновении исключения.
    """
    with patch('parser.utils.pdf_extractor.fitz.open', side_effect=Exception("Test error")):
        result = extract_text_from_pdf("test_sample.pdf")
        assert result == ""

# Тесты для извлечения текста из DOCX файлов
def test_extract_text_from_docx_success():
    """
    Проверяет успешное извлечение текста из DOCX файла.
    Тест симулирует работу библиотеки python-docx для чтения DOCX.
    """
    mock_document = MagicMock()
    mock_paragraph = MagicMock()
    mock_paragraph.text = "Test text"
    mock_document.paragraphs = [mock_paragraph]
    
    with patch('parser.utils.docx_extractor.Document', return_value=mock_document):
        result = extract_text_from_docx("test_sample.docx")
        assert result == "Test text"

def test_extract_text_from_docx_error():
    """
    Проверяет обработку ошибки при чтении DOCX файла.
    Тест проверяет, что функция возвращает пустую строку при возникновении исключения.
    """
    with patch('parser.utils.docx_extractor.Document', side_effect=Exception("Test error")):
        result = extract_text_from_docx("test_sample.docx")
        assert result == ""

# Тесты для извлечения текста из DOC файлов
def test_extract_text_from_doc_success():
    """
    Проверяет успешное извлечение текста из DOC файла.
    Тест симулирует работу утилиты antiword через subprocess для чтения DOC.
    """
    mock_process = MagicMock()
    mock_process.stdout = b"Test text"
    
    with patch('parser.utils.doc_extractor.subprocess.run', return_value=mock_process):
        result = extract_text_from_doc("test_sample.doc")
        assert result == "Test text"

def test_extract_text_from_doc_error():
    """
    Проверяет обработку ошибки при чтении DOC файла.
    Тест проверяет, что функция возвращает пустую строку при возникновении исключения.
    """
    with patch('parser.utils.doc_extractor.subprocess.run', side_effect=Exception("Test error")):
        result = extract_text_from_doc("test_sample.doc")
        assert result == ""

# Тесты для извлечения текста из DJVU файлов
def test_extract_text_from_djvu_success():
    """
    Проверяет успешное извлечение текста из DJVU файла.
    Тест симулирует работу утилиты djvutxt через subprocess для чтения DJVU.
    """
    mock_process = MagicMock()
    mock_process.stdout = b"Test text"
    
    with patch('parser.utils.djvu_extractor.subprocess.run', return_value=mock_process) as mock_run:
        with patch('builtins.open', mock_open(read_data="Test text")):
            result = extract_text_from_djvu("test_sample.djvu")
            assert result == "Test text"
            mock_run.assert_called_once_with(['djvutxt', 'test_sample.djvu', 'output.txt'], 
                                           stdout=subprocess.PIPE, check=True)

def test_extract_text_from_djvu_error():
    """
    Проверяет обработку ошибки при чтении DJVU файла.
    Тест проверяет, что функция возвращает пустую строку при возникновении исключения.
    """
    with patch('parser.utils.djvu_extractor.subprocess.run', side_effect=Exception("Test error")):
        result = extract_text_from_djvu("test_sample.djvu")
        assert result == ""

# Тесты для парсинга HTML страниц
def test_parse_html_success():
    """
    Проверяет успешное извлечение текста из HTML страницы.
    Тест симулирует работу библиотек requests и BeautifulSoup для парсинга HTML.
    """
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b"<html><body><p>Test text</p></body></html>"
    mock_response.apparent_encoding = "utf-8"
    
    with patch('parser.utils.html_extractor.requests.get', return_value=mock_response):
        with patch('parser.utils.html_extractor.BeautifulSoup') as mock_soup:
            mock_paragraph = MagicMock()
            mock_paragraph.text = "Test text"
            mock_soup.return_value.find_all.return_value = [mock_paragraph]
            result = parse_html("http://test.com")
            assert result is None  # Функция не возвращает значение

def test_parse_html_error():
    """
    Проверяет обработку ошибки при парсинге HTML страницы.
    Тест проверяет, что функция возвращает None при возникновении исключения.
    """
    with patch('parser.utils.html_extractor.requests.get', side_effect=Exception("Test error")):
        result = parse_html("http://test.com")
        assert result is None

# Тесты для анализа текста
def test_analyze_text_success():
    """
    Проверяет успешный анализ текста.
    Тест симулирует работу библиотеки spaCy для лингвистического анализа.
    """
    mock_doc = MagicMock()
    mock_token = MagicMock()
    mock_token.text = "Test"
    mock_token.pos_ = "NOUN"
    mock_token.dep_ = "nsubj"
    mock_token.lemma_ = "test"
    mock_doc.__iter__.return_value = [mock_token]
    
    with patch('parser.utils.text_analyzer.spacy.load') as mock_spacy:
        mock_spacy.return_value.return_value = mock_doc
        result = list(analyze_text("Test text"))
        assert len(result) == 1
        assert result[0]['text'] == "Test"
        assert result[0]['position'] == "NOUN"
        assert result[0]['dependency'] == "nsubj"
        assert result[0]['lemma'] == "test"

def test_analyze_text_unknown_language():
    """
    Проверяет обработку текста на неизвестном языке.
    Тест проверяет, что функция выбрасывает LanguageError при невозможности определить язык.
    """
    with patch('parser.utils.text_analyzer.detect', side_effect=LangDetectException(code=0, message="Unknown language")):
        with pytest.raises(LanguageError) as exc_info:
            analyze_text("Test text")
        assert exc_info.value.message == "Не удалось определить язык текста: Unknown language"

# Параметризованные тесты для грамматического анализа
@pytest.mark.parametrize("text,expected_pos,expected_dep,expected_lemma", [
    ("жжилой", "ADJ", "amod", "жилой"),  # Проверка исправления опечатки
    ("NASA", "PROPN", "nsubj", "NASA"),  # Проверка обработки аббревиатур
])
def test_analyze_text_grammar(text, expected_pos, expected_dep, expected_lemma):
    """
    Проверяет грамматический анализ различных типов слов.
    Тест использует параметризацию для проверки разных случаев:
    - Исправление опечаток
    - Обработка аббревиатур
    """
    mock_doc = MagicMock()
    mock_token = MagicMock()
    mock_token.text = text
    mock_token.pos_ = expected_pos
    mock_token.dep_ = expected_dep
    mock_token.lemma_ = expected_lemma
    mock_doc.__iter__.return_value = [mock_token]
    
    with patch('parser.utils.text_analyzer.detect', return_value='en'):
        with patch('parser.utils.text_analyzer.spacy.load') as mock_spacy:
            mock_spacy.return_value.return_value = mock_doc
            result = list(analyze_text(text))
            assert len(result) == 1
            assert result[0]['text'] == text
            assert result[0]['position'] == expected_pos
            assert result[0]['dependency'] == expected_dep
            assert result[0]['lemma'] == expected_lemma

# Тесты граничных случаев и особых сценариев
def test_analyze_text_empty():
    """
    Проверяет обработку пустого текста.
    Граничный случай: пустая строка должна вызывать LanguageError.
    """
    with pytest.raises(LanguageError) as exc_info:
        analyze_text("")
    assert exc_info.value.message == "Текст для анализа не может быть пустым."

def test_analyze_text_only_spaces():
    """
    Проверяет обработку текста, состоящего только из пробельных символов.
    Граничный случай: строка с пробелами, табуляциями и переносами строк должна вызывать LanguageError.
    """
    with pytest.raises(LanguageError) as exc_info:
        analyze_text("   \t\n  ")
    assert exc_info.value.message == "Текст для анализа не может быть пустым."

def test_analyze_text_mixed_language():
    """
    Проверяет обработку текста с двумя языками.
    Особый случай: текст содержит слова на разных языках (английский и русский).
    """
    mock_doc = MagicMock()
    mock_token1 = MagicMock()
    mock_token1.text = "Hello"
    mock_token1.pos_ = "INTJ"
    mock_token1.dep_ = "discourse"
    mock_token1.lemma_ = "hello"
    
    mock_token2 = MagicMock()
    mock_token2.text = "мир"
    mock_token2.pos_ = "NOUN"
    mock_token2.dep_ = "root"
    mock_token2.lemma_ = "мир"
    
    mock_doc.__iter__.return_value = [mock_token1, mock_token2]
    
    with patch('parser.utils.text_analyzer.detect', return_value='ru'):
        with patch('parser.utils.text_analyzer.spacy.load') as mock_spacy:
            mock_spacy.return_value.return_value = mock_doc
            result = list(analyze_text("Hello мир"))
            assert len(result) == 2
            assert result[0]['text'] == "Hello"
            assert result[1]['text'] == "мир"

def test_analyze_text_special_characters():
    """
    Проверяет обработку текста со специальными символами.
    Особый случай: текст содержит знаки препинания и другие специальные символы.
    """
    mock_doc = MagicMock()
    mock_token = MagicMock()
    mock_token.text = "Hello!"
    mock_token.pos_ = "INTJ"
    mock_token.dep_ = "discourse"
    mock_token.lemma_ = "hello"
    mock_doc.__iter__.return_value = [mock_token]
    
    with patch('parser.utils.text_analyzer.detect', return_value='en'):
        with patch('parser.utils.text_analyzer.spacy.load') as mock_spacy:
            mock_spacy.return_value.return_value = mock_doc
            result = list(analyze_text("Hello!"))
            assert len(result) == 1
            assert result[0]['text'] == "Hello!"

def test_analyze_text_very_long():
    """
    Проверяет обработку очень длинного текста.
    Граничный случай: текст содержит 5000 символов (1000 повторяющихся слов).
    """
    long_text = "word " * 1000  # 5000 символов
    mock_doc = MagicMock()
    mock_tokens = []
    for i in range(1000):
        mock_token = MagicMock()
        mock_token.text = "word"
        mock_token.pos_ = "NOUN"
        mock_token.dep_ = "nsubj"
        mock_token.lemma_ = "word"
        mock_tokens.append(mock_token)
    mock_doc.__iter__.return_value = mock_tokens
    
    with patch('parser.utils.text_analyzer.detect', return_value='en'):
        with patch('parser.utils.text_analyzer.spacy.load') as mock_spacy:
            mock_spacy.return_value.return_value = mock_doc
            result = list(analyze_text(long_text))
            assert len(result) == 1000
            assert all(token['text'] == "word" for token in result)

def test_analyze_text_unicode_emojis():
    """
    Проверяет обработку текста с эмодзи.
    Особый случай: текст содержит Unicode-символы эмодзи.
    """
    mock_doc = MagicMock()
    mock_token = MagicMock()
    mock_token.text = "Hello 👋"
    mock_token.pos_ = "INTJ"
    mock_token.dep_ = "discourse"
    mock_token.lemma_ = "hello"
    mock_doc.__iter__.return_value = [mock_token]
    
    with patch('parser.utils.text_analyzer.detect', return_value='en'):
        with patch('parser.utils.text_analyzer.spacy.load') as mock_spacy:
            mock_spacy.return_value.return_value = mock_doc
            result = list(analyze_text("Hello 👋"))
            assert len(result) == 1
            assert result[0]['text'] == "Hello 👋"

# Тесты для анализа текста с особыми форматами
def test_analyze_text_with_html():
    """
    Проверяет обработку текста, содержащего HTML-теги.
    Особый случай: текст содержит HTML-разметку, которая должна быть проигнорирована.
    """
    mock_doc = MagicMock()
    mock_token = MagicMock()
    mock_token.text = "Hello world"
    mock_token.pos_ = "NOUN"
    mock_token.dep_ = "nsubj"
    mock_token.lemma_ = "hello"
    mock_doc.__iter__.return_value = [mock_token]
    
    with patch('parser.utils.text_analyzer.detect', return_value='en'):
        with patch('parser.utils.text_analyzer.spacy.load') as mock_spacy:
            mock_spacy.return_value.return_value = mock_doc
            result = list(analyze_text("Hello <b>world</b>"))
            assert len(result) == 1
            assert result[0]['text'] == "Hello world"

def test_analyze_text_with_numbers():
    """
    Проверяет обработку текста с числами и единицами измерения.
    Особый случай: текст содержит числовые значения с единицами измерения.
    """
    mock_doc = MagicMock()
    mock_tokens = []
    
    # Создаем токены для "100 кг"
    mock_token1 = MagicMock()
    mock_token1.text = "100"
    mock_token1.pos_ = "NUM"
    mock_token1.dep_ = "nummod"
    mock_token1.lemma_ = "100"
    
    mock_token2 = MagicMock()
    mock_token2.text = "кг"
    mock_token2.pos_ = "NOUN"
    mock_token2.dep_ = "nsubj"
    mock_token2.lemma_ = "килограмм"
    
    mock_tokens.extend([mock_token1, mock_token2])
    mock_doc.__iter__.return_value = mock_tokens
    
    with patch('parser.utils.text_analyzer.detect', return_value='ru'):
        with patch('parser.utils.text_analyzer.spacy.load') as mock_spacy:
            mock_spacy.return_value.return_value = mock_doc
            result = list(analyze_text("100 кг"))
            assert len(result) == 2
            assert result[0]['text'] == "100"
            assert result[0]['position'] == "NUM"
            assert result[1]['text'] == "кг"
            assert result[1]['position'] == "NOUN"

def test_analyze_text_with_dates():
    """
    Проверяет обработку текста с датами и временем.
    Особый случай: текст содержит даты и временные метки в разных форматах.
    """
    mock_doc = MagicMock()
    mock_tokens = []
    
    # Создаем токены для "01.01.2024 15:30"
    mock_token1 = MagicMock()
    mock_token1.text = "01.01.2024"
    mock_token1.pos_ = "NUM"
    mock_token1.dep_ = "nummod"
    mock_token1.lemma_ = "01.01.2024"
    
    mock_token2 = MagicMock()
    mock_token2.text = "15:30"
    mock_token2.pos_ = "NUM"
    mock_token2.dep_ = "nummod"
    mock_token2.lemma_ = "15:30"
    
    mock_tokens.extend([mock_token1, mock_token2])
    mock_doc.__iter__.return_value = mock_tokens
    
    with patch('parser.utils.text_analyzer.detect', return_value='ru'):
        with patch('parser.utils.text_analyzer.spacy.load') as mock_spacy:
            mock_spacy.return_value.return_value = mock_doc
            result = list(analyze_text("01.01.2024 15:30"))
            assert len(result) == 2
            assert result[0]['text'] == "01.01.2024"
            assert result[0]['position'] == "NUM"
            assert result[1]['text'] == "15:30"
            assert result[1]['position'] == "NUM"

# Тесты для обработки ошибок при работе с файлами
def test_extract_text_from_pdf_corrupted():
    """
    Проверяет обработку поврежденного PDF файла.
    Граничный случай: файл существует, но его содержимое повреждено.
    """
    with patch('parser.utils.pdf_extractor.fitz.open', side_effect=Exception("PDF file is corrupted")):
        result = extract_text_from_pdf("corrupted.pdf")
        assert result == ""

def test_extract_text_from_docx_permission_error():
    """
    Проверяет обработку ошибки доступа к DOCX файлу.
    Граничный случай: файл существует, но нет прав на его чтение.
    """
    with patch('parser.utils.docx_extractor.Document', side_effect=PermissionError("Access denied")):
        result = extract_text_from_docx("restricted.docx")
        assert result == ""

def test_extract_text_from_doc_encoding_error():
    """
    Проверяет обработку ошибки кодировки при чтении DOC файла.
    Граничный случай: файл имеет неверную кодировку.
    """
    with patch('parser.utils.doc_extractor.subprocess.run', side_effect=UnicodeDecodeError("utf-8", b"", 0, 1, "invalid continuation byte")):
        result = extract_text_from_doc("invalid_encoding.doc")
        assert result == "" 