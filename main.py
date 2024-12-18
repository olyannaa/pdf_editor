import customtkinter as ctk
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os
from PyPDF2 import PdfReader, PdfWriter
import subprocess

# Регистрация шрифта
pdfmetrics.registerFont(TTFont('GOST', 'gost.ttf'))

# Функция для редактирования PDF
def edit_pdf():
    pdf_path = pdf_entry.get()
    developer = developer_entry.get()
    artist = artist_entry.get()

    if not os.path.exists(pdf_path):
        result_label.configure(text="PDF файл не найден!")
        return

    # Чтение оригинального PDF
    reader = PdfReader(pdf_path)
    writer = PdfWriter()

    # Обработка каждой страницы оригинального PDF
    for i in range(len(reader.pages)):
        page = reader.pages[i]
        writer.add_page(page)

        # Создание временного PDF для добавления текста на текущую страницу
        temp_pdf_path = "temp.pdf"
        c = canvas.Canvas(temp_pdf_path, pagesize=letter)
        c.setFont('GOST', 12)  # Установите размер шрифта по вашему усмотрению

        # Добавление текста на текущую страницу
        c.drawString(100, 750, f"Разработчик: {developer}")
        c.drawString(100, 730, f"Художник: {artist}")
        c.showPage()
        c.save()

        # Чтение временного PDF и добавление текста на текущую страницу
        temp_reader = PdfReader(temp_pdf_path)
        temp_page = temp_reader.pages[0]
        writer.add_page(temp_page)

    # Сохранение отредактированного PDF
    output_path = r"D:\test_python\расчет (С2 и Т1)2.pdf"
    with open(output_path, "wb") as output_pdf:
        writer.write(output_pdf)

    result_label.configure(text="Файл успешно отредактирован!")

    # Открытие отредактированного PDF файла
    subprocess.Popen([output_path], shell=True)

# Создание основного окна
app = ctk.CTk()
app.title("Редактор PDF")
app.geometry("400x300")

# Поле для ввода пути к PDF
pdf_label = ctk.CTkLabel(app, text="Путь к PDF файлу:")
pdf_label.pack(pady=10)
pdf_entry = ctk.CTkEntry(app, width=300)
pdf_entry.pack(pady=10)

# Поле для ввода разработчика
developer_label = ctk.CTkLabel(app, text="Разработчик:")
developer_label.pack(pady=10)
developer_entry = ctk.CTkEntry(app, width=300)
developer_entry.pack(pady=10)

# Поле для ввода художника
artist_label = ctk.CTkLabel(app, text="Художник:")
artist_label.pack(pady=10)
artist_entry = ctk.CTkEntry(app, width=300)
artist_entry.pack(pady=10)

# Кнопка для редактирования PDF
edit_button = ctk.CTkButton(app, text="Отредактировать файл", command=edit_pdf)
edit_button.pack(pady=20)

# Метка для отображения результата
result_label = ctk.CTkLabel(app, text="")
result_label.pack(pady=10)

# Запуск приложения
app.mainloop()