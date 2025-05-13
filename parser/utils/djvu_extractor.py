import subprocess

def extract_text_from_djvu(file_path):
    try:
        result = subprocess.run(['djvutxt', file_path, 'output.txt'], stdout=subprocess.PIPE, check=True)
        with open('output.txt', 'r') as file:
            text = file.read()
        return text
    except Exception as e:
        print(f"Ошибка при чтении DJVU: {e}")
        return ""
