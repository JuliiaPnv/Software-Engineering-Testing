class FileNames:
    '''
        Пути до тестовых файлов
    '''
    error_encoding = '1.pdf'                                                                    # ошибка кодировки
    unknown_language = '3.docx'                                                                 # иностранный язык
    empty_file = '4.doc'                                                                        # пустой документ
    not_exists = '5.docx'                                                                       # несуществующий файл
    basic_docs = {'djvu': '6.djvu', 'doc': '6.doc', 'docx': '6.docx', 'pdf': '6.pdf'}           # моковые данные
    undefined_format = '9.zip'                                                                  # некорректный формат
    abbreviation = {'djvu': '8.djvu', 'doc': '8.doc', 'docx': '8.docx', 'pdf': '8.pdf'}         # аббревиатуры
    big_file = '10.pdf'                                                                         # большой файл
    grammatical_errors = {'djvu': '7.djvu', 'doc': '7.doc', 'docx': '7.docx', 'pdf': '7.pdf'}   # грамматические ошибки

class SiteUrls:
    '''
        Ссылки до сайтов
    '''
    success = 'https://lic-politexicheskij-murmansk-r47.gosweb.gosuslugi.ru/'                   # корректная url
    not_found = 'http//74.ru'                                                                   # некорректная url
