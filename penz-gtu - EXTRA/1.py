# Функция для вычисления контрольной суммы методом контрольных сумм
def checksum_method(text):
    max_val = 256  # Максимальное значение для контрольной суммы
    total_sum = sum(ord(char) for char in text)
    return total_sum % max_val

# Функция для хеширования с использованием гаммирования
def gamma_hash(text, a, b, c, t0):
    n = len(text)
    max_val = c
    gamma_sequence = []
    t = t0

    # Генерация гаммовой последовательности
    for i in range(n):
        gamma_sequence.append(t)
        t = (a * t + b) % max_val

    # Применение гаммирования и расчет хеш-значения
    xor_sum = 0
    for i in range(n):
        xor_sum += ord(text[i]) ^ gamma_sequence[i]

    return xor_sum % max_val

# Пример текстов для обработки
texts = [
    "0123456789",
    "9876543210",
    "1000005",
    "1500000",
    "02468",
    "86420"
]

# Параметры для всех 15 вариантов
variants = [
    {"a": 17, "b": 11, "c": 256, "t0": 172},
    {"a": 13, "b": 19, "c": 256, "t0": 155},
    {"a": 23, "b": 7, "c": 256, "t0": 131},
    {"a": 19, "b": 3, "c": 256, "t0": 101},
    {"a": 17, "b": 3, "c": 256, "t0": 191},
    {"a": 31, "b": 5, "c": 256, "t0": 121},
    {"a": 29, "b": 13, "c": 256, "t0": 113},
    {"a": 11, "b": 17, "c": 256, "t0": 79},
    {"a": 37, "b": 23, "c": 256, "t0": 59},
    {"a": 41, "b": 29, "c": 256, "t0": 39},
    {"a": 43, "b": 31, "c": 256, "t0": 27},
    {"a": 47, "b": 37, "c": 256, "t0": 33},
    {"a": 53, "b": 41, "c": 256, "t0": 21},
    {"a": 59, "b": 43, "c": 256, "t0": 15},
    {"a": 61, "b": 47, "c": 256, "t0": 9}
]

# Вывод результата в консоль
for idx, text in enumerate(texts):
    print(f"Текст {idx + 1}: {text}\n")
    # Обрабатываем все варианты с 1 по 15 для каждого текста
    for var_num, variant in enumerate(variants, 1):
        # Рассчитываем контрольную сумму и хеш с гаммированием
        checksum = checksum_method(text)
        gamma_hash_value = gamma_hash(text, variant["a"], variant["b"], variant["c"], variant["t0"])

        # Вывод результата в консоль
        print(f"Вариант {var_num}:")
        print(f"Контрольная сумма (KSumm): {checksum}")
        print(f"Хеш с гаммированием (SummKodBukvOtkr): {gamma_hash_value}")
        print("-" * 40)
    print("\n" + "=" * 60 + "\n")

