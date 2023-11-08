import random
print(f"Минимальный положительный элемент: {min([num for num in [random.uniform(-10, 10) for _ in range(10)] if num > 0])}")
