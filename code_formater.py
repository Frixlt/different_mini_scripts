import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox as messagebox


def read_code_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        code = file.read()
    return code.replace('\n', '')


def process_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        code = read_code_file(file_path)
        output_text.delete(1.0, tk.END)  # Очистить поле вывода
        output_text.insert(tk.END, code)


def copy_to_clipboard():
    code = output_text.get(1.0, tk.END)
    root.clipboard_clear()
    root.clipboard_append(code)
    # messagebox.showinfo("Копирование", "Текст скопирован в буфер обмена")


# Создание графического интерфейса
root = tk.Tk()
root.title("Прочитать код из файла")

# Создание кнопки для выбора файла
select_button = tk.Button(root, text="Выбрать файл", command=process_file)
select_button.pack(pady=5)

# Создание кнопки для копирования текста
copy_button = tk.Button(root, text="Копировать", command=copy_to_clipboard)
copy_button.pack(pady=5)

# Создание поля для вывода кода
output_text = tk.Text(root, height=20, width=80)
output_text.pack(padx=10, pady=5)

root.mainloop()
