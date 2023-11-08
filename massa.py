import random

size = 10
array = [random.uniform(-10, 10) for i in range(size)]
print(array)

min_pos = float('inf')
for x in array:
    if x > 0 and x < min_pos:
        min_pos = x

if min_pos != float('inf'):
    print("Минимальный положительный элемент:", min_pos)
else:
    print("Положительных элементов нет")
