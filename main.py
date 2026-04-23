import tkinter as tk
from tkinter import ttk, messagebox, font
import random
import string
import json

# Файл для хранения истории паролей
HISTORY_FILE = "history.json"

# --- Функции работы с историей ---
def load_history():
    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

# --- Функция генерации пароля ---
def generate_password():
    length = scale_length.get()
    use_digits = var_digits.get()
    use_letters = var_letters.get()
    use_special = var_special.get()

    # Проверка корректности ввода (минимальная длина)
    if length < 4:
        messagebox.showwarning("Ошибка", "Минимальная длина пароля — 4 символа")
        return

    # Проверка: выбран ли хотя бы один тип символов
    if not (use_digits or use_letters or use_special):
        messagebox.showwarning("Ошибка", "Выберите хотя бы один тип символов")
        return

    chars = ""
    if use_letters:
        chars += string.ascii_letters  # a-zA-Z
    if use_digits:
        chars += string.digits         # 0-9
    if use_special:
        chars += string.punctuation    # Спецсимволы

    password = ''.join(random.choices(chars, k=length))
    entry_password.delete(0, tk.END)
    entry_password.insert(0, password)
    
    # Добавление в историю
    history = load_history()
    history.append(password)
    save_history(history)
    update_history_table()

# --- Функция обновления таблицы истории ---
def update_history_table():
    for i in tree_history.get_children():
        tree_history.delete(i)
    for pwd in load_history():
        tree_history.insert("", tk.END, values=(pwd,))

# --- GUI ---
root = tk.Tk()
root.title("Random Password Generator")
root.geometry("600x500")
root.resizable(False, False)

# Настройка шрифта для поля пароля (чтобы скрыть символы)
hidden_font = font.Font(family="Courier", size=12)

# --- Фрейм настроек ---
frame_settings = tk.LabelFrame(root, text="Настройки пароля", padx=10, pady=10)
frame_settings.pack(pady=10, padx=10, fill=tk.X)

# Ползунок длины пароля (от 4 до 32)
tk.Label(frame_settings, text="Длина:").grid(row=0, column=0, sticky="e")
scale_length = tk.Scale(frame_settings, from_=4, to=32, orient=tk.HORIZONTAL)
scale_length.set(12) # Значение по умолчанию
scale_length.grid(row=0, column=1, columnspan=2, sticky="we")

# Чекбоксы символов
var_digits = tk.BooleanVar(value=True)
var_letters = tk.BooleanVar(value=True)
var_special = tk.BooleanVar(value=True)

tk.Checkbutton(frame_settings, text="Цифры", variable=var_digits).grid(row=1, column=0, sticky="w")
tk.Checkbutton(frame_settings, text="Буквы", variable=var_letters).grid(row=1, column=1, sticky="w")
tk.Checkbutton(frame_settings, text="Спецсимволы", variable=var_special).grid(row=1, column=2, sticky="w")

# Кнопка генерации и поле вывода пароля
frame_generate = tk.Frame(root)
frame_generate.pack(pady=10)

btn_generate = tk.Button(frame_generate, text="Сгенерировать", command=generate_password)
btn_generate.pack(side=tk.LEFT)

entry_password = tk.Entry(frame_generate, font=hidden_font, width=40)
entry_password.pack(side=tk.LEFT, padx=5)
entry_password.config(show="*") # Скрываем символы в поле ввода

# --- Таблица истории ---
frame_history = tk.LabelFrame(root, text="История паролей", padx=5, pady=5)
frame_history.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

columns = ("password",)
tree_history = ttk.Treeview(frame_history, columns=columns, show="headings")
tree_history.heading("password", text="Пароль")
tree_history.column("password", width=500)
tree_history.pack(fill=tk.BOTH, expand=True)

# Загрузка истории при старте приложения
update_history_table()

root.mainloop()
