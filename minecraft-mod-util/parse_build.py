import json
import os
import requests
import argparse

# Функция для парсинга файла и вывода модов, необходимых для сервера
def parse_mods(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    required_mods = []
    for mod in data.get('files', []):
        if mod['env'].get('server') == 'required':
            required_mods.append({
                'name': mod['path'].split('/')[-1],
                'url': mod['downloads'][0]
            })

    if required_mods:
        print("Моды, необходимые для сервера:")
        for mod in required_mods:
            print(f"Название: {mod['name']}")
    else:
        print("Нет модов, необходимых для сервера.")

    return required_mods

# Функция для загрузки модов в папку downloads
def download_mods(mods):
    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    for mod in mods:
        download_path = os.path.join('downloads', mod['name'])
        if not os.path.exists(download_path):
            print(f"Скачивание {mod['name']}...")
            response = requests.get(mod['url'], stream=True)
            with open(download_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"{mod['name']} скачан в папку downloads.")
        else:
            print(f"{mod['name']} уже скачан.")

if __name__ == '__main__':
    # Аргументы командной строки
    parser = argparse.ArgumentParser(description="Парсинг файла сборки Minecraft и загрузка модов.")
    parser.add_argument('file', nargs='?', default='modrinth.index.json', help='Путь к файлу сборки JSON (по умолчанию modrinth.index.json)')
    parser.add_argument('--download', action='store_true', help='Скачать моды для сервера')

    args = parser.parse_args()

    # Проверка существования файла
    if not os.path.exists(args.file):
        print(f"Файл {args.file} не найден. Проверьте путь.")
    else:
        # Парсим моды из указанного или дефолтного файла
        mods = parse_mods(args.file)

        # Если указан флаг --download, загружаем моды
        if args.download:
            download_mods(mods)
