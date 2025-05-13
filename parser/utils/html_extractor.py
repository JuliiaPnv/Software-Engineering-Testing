from bs4 import BeautifulSoup
import requests

def parse_html(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Попробуем определить кодировку
            encoding = response.apparent_encoding
            html_content = response.content.decode(encoding)
            soup = BeautifulSoup(html_content, 'html.parser')
            paragraphs = soup.find_all('p')
            full_text = ' '.join(paragraph.text.strip() for paragraph in paragraphs)
            print("Извлеченный текст из HTML:")
            print(full_text)
            analyze_text(full_text)
        else:
            print(f"Ошибка при загрузке страницы: {response.status_code}")
    except Exception as e:
        print(f"Ошибка при парсинге HTML: {e}")
