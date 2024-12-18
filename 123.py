import tkinter as tk
from tkinter import filedialog, messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from PyPDF2 import PdfReader, PdfWriter
import os
import subprocess
import threading

def edit_pdf():
    # Показываем значок загрузки
    loading_label.pack()
    root.update()  # Обновляем интерфейс

    pdf_path = pdf_entry.get()
    developer = developer_entry.get()
    artist = artist_entry.get()

    if not os.path.exists(pdf_path):
        messagebox.showerror("Ошибка", "PDF файл не найден.")
        loading_label.pack_forget()  # Скрываем значок загрузки
        return

    # Создаем временный PDF файл с текстом
    temp_pdf_path = "temp.pdf"
    c = canvas.Canvas(temp_pdf_path, pagesize=letter)
    width, height = letter

    # Регистрация шрифта
    pdfmetrics.registerFont(TTFont('GOST', 'gost.ttf'))
    c.setFont('GOST', 12)  # Устанавливаем шрифт и размер

    # Добавляем текст на каждую страницу
    for i in range(len(PdfReader(pdf_path).pages)):
        c.drawString(100, 50, f"Разработчик: {developer}")
        c.drawString(100, 70, f"Художник: {artist}")
        c.showPage()

    c.save()

    # Объединяем оригинальный PDF с временным
    output_pdf_path = r"D:\test_python\расчет (С2 и Т1)2.pdf"
    writer = PdfWriter()

    original_pdf = PdfReader(pdf_path)
    temp_pdf = PdfReader(temp_pdf_path)

    for i in range(len(original_pdf.pages)):
        original_page = original_pdf.pages[i]
        temp_page = temp_pdf.pages[i] if i < len(temp_pdf.pages) else None

        if temp_page:
            original_page.merge_page(temp_page)

        writer.add_page(original_page)

    with open(output_pdf_path, "wb") as output_pdf:
        writer.write(output_pdf)

    # Удаляем временный файл
    os.remove(temp_pdf_path)

    # Открываем отредактированный PDF файл
    subprocess.Popen([output_pdf_path], shell=True)
    messagebox.showinfo("Успех", "PDF файл успешно отредактирован!")
    
    # Скрываем значок загрузки
    loading_label.pack_forget()

# Создаем главное окно
root = tk.Tk()
root.title("Редактор PDF")

# Поля для ввода
tk.Label(root, text="Путь к PDF файлу:").pack()
pdf_entry = tk.Entry(root, width=50)
pdf_entry.pack()

tk.Label(root, text="Разработчик:").pack()
developer_entry = tk.Entry(root, width=50)
developer_entry.pack()

tk.Label(root, text="Художник:").pack()
artist_entry = tk.Entry(root, width=50)
artist_entry.pack()

# Кнопка для редактирования файла
edit_button = tk.Button(root, text="Отредактировать файл", command=lambda: threading.Thread(target=edit_pdf).start())
edit_button.pack()

# Значок загрузки
loading_label = tk.Label(root, text="Загрузка...", fg="blue")
loading_label.pack_forget()  # Скрываем его изначально

# Запуск приложения
root.mainloop()