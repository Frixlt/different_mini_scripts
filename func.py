import math

print("Программа для вычисления значений функций")

def calculate(r):
    if func_num == 1:
        return math.sin(r)
    elif func_num == 2:
        return math.cos(r)
    else:
        return complex(math.cos(r), math.sin(r))

while True:
    func_num = int(input("Введите номер функции (1 - sin, 2 - cos, 3 - cis): "))
    
    try:
        r = float(input("Введите аргумент R: "))
        result = calculate(r)
        print(f"{func_name}(R) = {result}") 
    except ValueError:
        print(f"Ошибка при вычислении {func_name} с аргументом {r}")
    except Exception as e:
        print(f"Возникла ошибка: {e}")

    choice = input("Q - выход, Enter - продолжить: ")
    if choice.lower() == 'q':
        break
