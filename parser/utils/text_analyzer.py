import spacy
from langdetect import detect, LangDetectException
from parser.Exceptions import LanguageError

def analyze_text(text):
    # Проверка на пустой текст
    if not text.strip():
        raise LanguageError(message="Текст для анализа не может быть пустым.")

    nlp = None
    language = None

    try:
        # Определение языка текста
        text = ' '.join(text.split())  # Очистка текста от лишних пробелов
        language = detect(text)
    except LangDetectException as e:
        raise LanguageError(message=f"Не удалось определить язык текста: {str(e)}")
    except Exception as e:
        raise LanguageError(message=f"Ошибка при анализе языка: {str(e)}")

    # Загрузка соответствующей модели spaCy
    try:
        if language == 'en':
            nlp = spacy.load("en_core_web_sm")
        elif language == 'ru':
            nlp = spacy.load("ru_core_news_sm")
        else:
            raise LanguageError(message=f"Язык '{language}' не поддерживается")
    except OSError as e:
        error_msg = (
            f"Модель для языка '{language}' не установлена!\n"
            f"Выполните команду: python -m spacy download "
            f"{'en_core_web_sm' if language == 'en' else 'ru_core_news_sm'}"
        )
        raise RuntimeError(error_msg) from e
    except Exception as e:
        raise LanguageError(message=f"Ошибка загрузки модели: {str(e)}")

    # Анализ текста
    try:
        doc = nlp(text)
        analyze = []
        for token in doc:
            analyze.append({
                'text': token.text,
                'lemma': token.lemma_,
                'position': token.pos_,
                'dependency': token.dep_
            })
        return analyze
    except Exception as e:
        raise LanguageError(message=f"Ошибка при анализе текста: {str(e)}")
