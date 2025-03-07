import os
import json
import requests
import argparse
from urllib.parse import urlparse

# Путь по умолчанию для загрузок и кэша
CACHE_DIR = './mod_ids/'
DOWNLOADS_DIR = './downloads/'

# Функция для создания директории, если она не существует
def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

# Функция для загрузки данных из кэша, если они существуют
def load_from_cache(mod_id):
    cache_file = os.path.join(CACHE_DIR, f"{mod_id}.json")
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as file:
            return json.load(file)
    return None

# Функция для сохранения данных в кэш
def save_to_cache(mod_id, data):
    cache_file = os.path.join(CACHE_DIR, f"{mod_id}.json")
    with open(cache_file, 'w') as file:
        json.dump(data, file)

# Функция для получения поддерживаемых версий Minecraft для конкретного мода
def get_supported_versions(mod_id):
    cached_data = load_from_cache(mod_id)
    if cached_data:
        return cached_data

    url = f"https://api.modrinth.com/v2/project/{mod_id}/version"
    response = requests.get(url)
    
    if response.status_code == 200:
        versions = response.json()
        supported_versions = set()

        for version in versions:
            supported_versions.update(version.get('game_versions', []))
        
        save_to_cache(mod_id, list(supported_versions))
        return supported_versions
    else:
        print(f"Ошибка при получении данных для мода {mod_id}: {response.status_code}")
        return set()

# Функция для получения серверной информации о моде
def get_server_info(mod_id):
    url = f"https://api.modrinth.com/v2/project/{mod_id}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json().get('server_side', False)
    else:
        print(f"Ошибка при получении данных для мода {mod_id}: {response.status_code}")
        return False

# Функция для чтения идентификаторов модов из файла
def read_mod_ids(file_path):
    with open(file_path, 'r') as file:
        mod_ids = [line.strip() for line in file.readlines()]
    return mod_ids

# Функция для скачивания мода по его id
def download_mod(mod_id, download_path, server_required=False, mod_loader=None, target_version=None):
    server_info = get_server_info(mod_id)
    
    if server_required and not server_info:
        print(f"Пропускаем мод {mod_id}, так как он не требует серверной части.")
        return

    url = f"https://api.modrinth.com/v2/project/{mod_id}/version"
    response = requests.get(url)
    
    if response.status_code == 200:
        versions = response.json()

        # Фильтруем версии по загрузчику и по версии Minecraft
        filtered_versions = [
            version for version in versions
            if (not mod_loader or mod_loader in version.get('loaders', [])) and
               (not target_version or target_version in version.get('game_versions', []))
        ]

        if not filtered_versions:
            print(f"Нет доступных версий для мода {mod_id} с указанным загрузчиком: {mod_loader} и версией: {target_version}.")
            return

        latest_version = filtered_versions[0]
        download_url = latest_version['files'][0]['url']
        file_name = latest_version['files'][0]['filename']

        # Скачиваем файл
        print(f"Скачивание {file_name} ...")
        download_file(download_url, os.path.join(download_path, file_name))
        print(f"Мод {file_name} успешно скачан в {download_path}.")
    else:
        print(f"Ошибка при получении данных для мода {mod_id}: {response.status_code}")

# Функция для скачивания файла
def download_file(url, file_path):
    response = requests.get(url)
    with open(file_path, 'wb') as file:
        file.write(response.content)

# Функция для парсинга ссылок на моды
def parse_links(file_path):
    with open(file_path, 'r') as input_file:
        links = input_file.readlines()

    mod_ids = []
    for link in links:
        link = link.strip()
        if 'modrinth.com/mod/' in link:
            mod_id = link.split('modrinth.com/mod/')[-1].split('/')[0]
            mod_ids.append(mod_id)
    
    mod_ids.sort()
    return mod_ids

# Основная функция
def main():
    # Разбор аргументов командной строки
    parser = argparse.ArgumentParser(description="Управление модами Minecraft с помощью Modrinth API.")
    parser.add_argument('-v', '--versions', type=str, help="Укажите целевую версию Minecraft (например, '1.19.4').")
    parser.add_argument('-d', '--download', type=str, nargs='?', const=DOWNLOADS_DIR, help="Скачивание модов в указанную папку или в папку по умолчанию.")
    parser.add_argument('-id', '--id', type=str, help="Путь к файлу с id модов.")
    parser.add_argument('-l', '--links', type=str, help="Путь к файлу с ссылками на моды.")
    parser.add_argument('-s', '--server', action='store_true', help="Скачивать только моды, которые требуют серверную часть.")
    parser.add_argument('-ml', '--mod_loader', type=str, help="Укажите загрузчик модов (например, 'forge', 'fabric').")

    args = parser.parse_args()

    # Создание директорий кэша и загрузок
    create_directory(CACHE_DIR)
    create_directory(DOWNLOADS_DIR)

    # Если передан параметр links, парсим ссылки из файла
    mod_ids = []
    if args.links:
        mod_ids = parse_links(args.links)
    elif args.id:
        mod_ids = read_mod_ids(args.id)

    # Если указана версия, проверяем совместимость модов
    if args.versions:
        target_version = args.versions
        unsupported_mods = []

        for mod_id in mod_ids:
            supported_versions = get_supported_versions(mod_id)
            if target_version not in supported_versions:
                unsupported_mods.append(mod_id)

        if unsupported_mods:
            print(f"Моды, которые не поддерживают версию Minecraft {target_version}:")
            for mod in unsupported_mods:
                print(f"- {mod}")
        else:
            print(f"Все моды поддерживают версию Minecraft {target_version}.")

    # Если передан параметр download, скачиваем моды
    if args.download:
        download_path = args.download if args.download else DOWNLOADS_DIR
        create_directory(download_path)

        for mod_id in mod_ids:
            download_mod(mod_id, download_path, args.server, args.mod_loader, args.versions)

if __name__ == "__main__":
    main()
