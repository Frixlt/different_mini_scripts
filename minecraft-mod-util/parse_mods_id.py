# Открываем файл input_mods.txt и читаем ссылки
with open('input.txt', 'r') as input_file:
    links = input_file.readlines()

# Список для хранения id модов
mod_ids = []

# Проходим по каждой ссылке и извлекаем id
for link in links:
    link = link.strip()  # Убираем возможные пробелы и переносы строк
    if 'modrinth.com/mod/' in link:
        # Извлекаем id мода из ссылки
        mod_id = link.split('modrinth.com/mod/')[-1].split('/')[0]
        mod_ids.append(mod_id)

# Сортируем id модов
mod_ids.sort()

# Записываем id модов в файл output_id_mods.txt
with open('mod_ids.txt', 'w') as output_file:
    for mod_id in mod_ids:
        output_file.write(mod_id + '\n')

print("ID модов успешно записаны в output_id_mods.txt и отсортированы.")
