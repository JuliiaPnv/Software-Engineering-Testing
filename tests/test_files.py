import pytest
from helpers import FileNames, SiteUrls
from config import RECOURSE_DIR
import os

from parser.Exceptions import LanguageError
from parser.pdf_processor import extract_text_from_pdf
from parser.text_analyzer import analyze_text
from parser.utils.html_parser import parse_html
from parser.doc_processor import extract_text_from_doc
from parser.docx_processor import extract_text_from_docx
from parser.djvu_processor import extract_text_from_djvu

import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)


def test_encoding():
    file_path = os.path.join(RECOURSE_DIR, FileNames.error_encoding)
    text = extract_text_from_pdf(file_path=file_path)

    with pytest.raises(LanguageError) as e:
        analyze_text(text)

    assert e.typename == 'LanguageError', ('При обработке файла с ошибочной кодировкой не выведена ошибка с неизвестным'
                                           ' языком')


def test_success_url():
    url = SiteUrls.success
    html_text = parse_html(url)
    analyze = analyze_text(html_text)

    assert analyze is not None, 'При вводе корректного url текст страницы не анализируется '


def test_not_found_url():
    url = SiteUrls.not_found
    html_text = parse_html(url)

    assert html_text is None, 'Выводится текст при вводе некорректного url'


def test_unknown_language():
    file_path = os.path.join(RECOURSE_DIR, FileNames.error_encoding)
    text = extract_text_from_pdf(file_path=file_path)

    with pytest.raises(LanguageError) as e:
        analyze_text(text)

    assert e.typename == 'LanguageError', ('При обработке файла с иностранным языком не выведена ошибка с неизвестным '
                                           'языком')


def test_empty_file():
    file_path = os.path.join(RECOURSE_DIR, FileNames.empty_file)
    print(file_path)
    text = extract_text_from_doc(file_path)

    assert text is None or len(text) == 0, ('При обработке пустого файла не выведено сообщение об ошибке или пустая '
                                            'строка')

def test_not_exist():
    file_path = os.path.join(RECOURSE_DIR, FileNames.not_exists)
    text = extract_text_from_docx(file_path)

    assert not text, 'При вводе несуществующего пути до файла программа не вывела сообщение об ошибке'


def test_undefined_format_docx():
    file_path = os.path.join(RECOURSE_DIR, FileNames.undefined_format)
    text = extract_text_from_docx(file_path)
    assert text is None, 'При вводе пути до файла zip программа считывает текст .docx'

def test_undefined_format_doc():
    file_path = os.path.join(RECOURSE_DIR, FileNames.undefined_format)
    text = extract_text_from_doc(file_path)
    assert text is None, 'При вводе пути до файла zip программа считывает текст .doc'

def test_undefined_format_pdf():
    file_path = os.path.join(RECOURSE_DIR, FileNames.undefined_format)
    text = extract_text_from_pdf(file_path)
    assert text is None, 'При вводе пути до файла zip программа считывает текст .pdf'

def test_undefined_format_djvu():
    file_path = os.path.join(RECOURSE_DIR, FileNames.undefined_format)
    text = extract_text_from_djvu(file_path)
    assert text is None, 'При вводе пути до файла zip программа считывает текст .djvu'

def test_basic_doc():
    file_path = os.path.join(RECOURSE_DIR, FileNames.basic_docs['doc'])
    text = extract_text_from_doc(file_path)
    analyze = analyze_text(text)

    assert analyze is not None, 'Формат .doc не прошёл проверку на базовую функциональность'


def test_basic_docx():
    file_path = os.path.join(RECOURSE_DIR, FileNames.basic_docs['docx'])
    text = extract_text_from_docx(file_path)
    analyze = analyze_text(text)

    assert analyze is not None, 'Формат .docx не прошёл проверку на базовую функциональность'


def test_basic_pdf():
    file_path = os.path.join(RECOURSE_DIR, FileNames.basic_docs['pdf'])
    text = extract_text_from_pdf(file_path)
    analyze = analyze_text(text)

    assert analyze is not None, 'Формат .pdf не прошёл проверку на базовую функциональность'


def test_basic_djvu():
    file_path = os.path.join(RECOURSE_DIR, FileNames.basic_docs['djvu'])
    text = extract_text_from_djvu(file_path)
    analyze = analyze_text(text)

    assert analyze is not None, 'Формат .djvu не прошёл проверку на базовую функциональность'


def test_abbreviation_doc():
    file_path = os.path.join(RECOURSE_DIR, FileNames.abbreviation['doc'])
    text = extract_text_from_doc(file_path)
    analyze = analyze_text(text)

    nasa = [analiz for analiz in analyze][0]

    assert nasa['text'] == 'NASA' and nasa['position'] == 'PROPN', 'Некорректно определена часть речи аббревиатуры'


def test_abbreviation_docx():
    file_path = os.path.join(RECOURSE_DIR, FileNames.abbreviation['docx'])
    text = extract_text_from_docx(file_path)
    analyze = analyze_text(text)

    nasa = [analiz for analiz in analyze][0]

    assert nasa['text'] == 'NASA' and nasa['position'] == 'PROPN', 'Некорректно определена часть речи аббревиатуры'


def test_abbreviation_pdf():
    file_path = os.path.join(RECOURSE_DIR, FileNames.abbreviation['pdf'])
    text = extract_text_from_pdf(file_path)
    analyze = analyze_text(text)

    nasa = [analiz for analiz in analyze][0]

    assert nasa['text'] == 'NASA' and nasa['position'] == 'PROPN', 'Некорректно определена часть речи аббревиатуры'


def test_abbreviation_djvu():
    file_path = os.path.join(RECOURSE_DIR, FileNames.abbreviation['djvu'])
    text = extract_text_from_djvu(file_path)
    analyze = analyze_text(text)

    nasa = [analiz for analiz in analyze][0]

    assert nasa['text'] == 'NASA' and nasa['position'] == 'PROPN', 'Некорректно определена часть речи аббревиатуры'

def test_big_file():
    file_path = os.path.join(RECOURSE_DIR, FileNames.big_file)

    with pytest.raises(Exception) as e:
        text = extract_text_from_pdf(file_path)
        analyze = analyze_text(text)
    assert e.value is None or analyze is not None, 'Большой файл не анализируется'

def check_base_form(x):
    return x['text'] == 'жжилой' and x['lemma'] == 'жилой'

def check_part_of_speech(x):
    return x['text'] == 'жжилой' and x['position'] == 'ADJ'

def check_dependency_type(x):
    return x['text'] == 'жжилой' and x['dependency'] == 'amod'

@pytest.mark.parametrize(
    "condition, message",
    [
        (check_base_form, 'Некорректно определена базовая форма'),
        (check_part_of_speech, 'Некорректно определена часть речи'),
        (check_dependency_type, 'Некорректно определен тип синтаксической зависимости'),
    ]
)

def test_grammatical_errors_docx(condition, message):
    file_path = os.path.join(RECOURSE_DIR, FileNames.grammatical_errors['docx'])
    text = extract_text_from_docx(file_path)
    analyze = analyze_text(text)

    lively = [analiz for analiz in analyze][3]

    assert condition(lively), message

@pytest.mark.parametrize(
    "condition, message",
    [
        (check_base_form, 'Некорректно определена базовая форма'),
        (check_part_of_speech, 'Некорректно определена часть речи'),
        (check_dependency_type, 'Некорректно определен тип синтаксической зависимости'),
    ]
)

def test_grammatical_errors_doc(condition, message):
    file_path = os.path.join(RECOURSE_DIR, FileNames.grammatical_errors['doc'])
    text = extract_text_from_doc(file_path)
    analyze = analyze_text(text)

    lively = [analiz for analiz in analyze][3]

    assert condition(lively), message

@pytest.mark.parametrize(
    "condition, message",
    [
        (check_base_form, 'Некорректно определена базовая форма'),
        (check_part_of_speech, 'Некорректно определена часть речи'),
        (check_dependency_type, 'Некорректно определен тип синтаксической зависимости'),
    ]
)

def test_grammatical_errors_pdf(condition, message):
    file_path = os.path.join(RECOURSE_DIR, FileNames.grammatical_errors['pdf'])
    text = extract_text_from_pdf(file_path)
    analyze = analyze_text(text)

    lively = [analiz for analiz in analyze][3]

    assert condition(lively), message

@pytest.mark.parametrize(
    "condition, message",
    [
        (check_base_form, 'Некорректно определена базовая форма'),
        (check_part_of_speech, 'Некорректно определена часть речи'),
        (check_dependency_type, 'Некорректно определен тип синтаксической зависимости'),
    ]
)

def test_grammatical_errors_djvu(condition, message):
    file_path = os.path.join(RECOURSE_DIR, FileNames.grammatical_errors['djvu'])
    text = extract_text_from_djvu(file_path)
    analyze = analyze_text(text)

    lively = [analiz for analiz in analyze][3]

    assert condition(lively), message

