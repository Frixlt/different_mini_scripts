import tkinter as tk
from tkinter import messagebox, ttk
import threading
import subprocess
import os
from flask import Flask, request, jsonify

# Переменная для отслеживания номера ролика
video_count = 0
previous_url = None  # Переменная для хранения предыдущего URL

# Создаем папку для сохранения, если она не существует
output_directory = "./downloads"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Функция для загрузки видео через yt-dlp
def download_video(url, progress_var, url_label):
    global video_count, previous_url
    video_count += 1
    output_path = f"{output_directory}/{video_count}.mp4"

    # Проверка на дублирование URL
    if url == previous_url:
        log_message(f"Ошибка: URL {url} уже в очереди.")
        return

    previous_url = url  # Сохраняем текущий URL
    command = [
        "yt-dlp", "-o", output_path,
        "--downloader", "aria2c", "--concurrent-fragments", "16", url
    ]

    try:
        # Запускаем процесс загрузки
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        while True:
            output = process.stdout.readline()
            if output == b"" and process.poll() is not None:
                break
            if output:
                log_message(output.decode().strip())
                # Update progress bar
                progress_var.set(100)  # Simulating 100% for simplicity (adjust logic as needed)

        log_message(f"Загрузка завершена: {output_path}")
        url_label.config(text=f"{url} (Загрузка завершена)")
    except subprocess.CalledProcessError:
        log_message(f"Не удалось скачать: {url}")

# Функция для записи логов в текстовое поле
def log_message(message):
    log_text.config(state=tk.NORMAL)  # Разрешаем редактирование
    log_text.insert(tk.END, message + "\n")  # Добавляем сообщение в лог
    log_text.see(tk.END)  # Прокручиваем текстовое поле вниз
    log_text.config(state=tk.DISABLED)  # Запрещаем редактирование

# Flask приложение для получения URL и запуска загрузки
app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    log_message(f"Получены данные: {data}")  # Логируем полученные данные
    url = data.get('url')

    if url:
        log_message(f"Добавлен в очередь: {url}")

        # Создаем переменную для прогресса и метку для URL
        progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
        progress_bar.pack(fill=tk.X, pady=5)

        url_label = tk.Label(root, text="", fg="blue", cursor="hand2")
        url_label.pack(pady=5)
        
        # Toggle URL display on click
        def toggle_url():
            current_text = url_label.cget("text")
            if current_text.startswith(url):
                url_label.config(text="")  # Hide URL
            else:
                url_label.config(text=url)  # Show URL

        url_label.bind("<Button-1>", lambda e: toggle_url())

        threading.Thread(target=download_video, args=(url, progress_var, url_label)).start()
        return jsonify({"message": "Загрузка запущена"}), 200

    return jsonify({"error": "Ошибка: URL не указан"}), 400

# Создаем графический интерфейс с помощью tkinter
root = tk.Tk()
root.title("Видео Загрузчик")
root.geometry("400x400")

# Элементы интерфейса
tk.Label(root, text="Логи:").pack(pady=5)

# Создаем многострочное поле Text для отображения логов
log_text = tk.Text(root, height=15, width=50, state=tk.DISABLED)
log_text.pack(pady=5)

# Запускаем Flask приложение в отдельном потоке
def run_flask():
    app.run(port=5000)

threading.Thread(target=run_flask, daemon=True).start()

# Запуск главного цикла интерфейса
root.mainloop()
