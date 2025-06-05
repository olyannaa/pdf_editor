import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from PyPDF2 import PdfReader, PdfWriter
import os
import subprocess
import threading
import fitz
from datetime import datetime
import time


t = time.time()


class File:
    def __init__(self, pdf_path, font, razrab, normctrl, utv, inv_nom, date):
        self.pdf_path = pdf_path
        self.font = font
        self.razrab = razrab
        self.normctrl = normctrl
        self.utv = utv
        self.temp_pdf_path = "temp_output.pdf"
        self.inv_nom = inv_nom
        self.date = date

        # Регистрируем шрифт
        pdfmetrics.registerFont(TTFont('GOST_I', self.font))



    def add_text(self):
        loading_label.pack()
        root.update() 

        file_path = self.pdf_path
        print(file_path)
        if os.path.exists(file_path):
            document = fitz.open(file_path)
            for page_num in range(document.page_count):
                page = document.load_page(page_num)
                self._process_page(page)
            

            # Сохранение изменений в новый PDF
            document.save("расчет (С2 и Т1)2.pdf")
            document.close()
            print("ok")

            # Открываем отредактированный PDF файл
            subprocess.Popen("расчет (С2 и Т1)2.pdf", shell=True)
            messagebox.showinfo("Успех", "PDF файл успешно отредактирован!")
    
    # Скрываем значок загрузки
            loading_label.pack_forget()
            
        else:
            print("Файл не найден.")
            messagebox.showerror("Ошибка", "Файл не существует или неправильного формата")


    def _process_page(self, page):
        text = page.get_text("text")
        rect = page.rect  # Получаем размер страницы
        width_mm = rect.width * 0.352778
        height_mm = rect.height * 0.352778
        c = canvas.Canvas(self.temp_pdf_path, pagesize=(page.rect.width, page.rect.height))



        if int(width_mm) < 250:
            if "Разраб" in text:
                try:
                    self._add_normal_text(page, c,  (self.razrab).split()[0], 108, 75)
                except IndexError:
                   pass
                try:
                    self._add_normal_text(page,c, (self.razrab).split()[1], 108, 63)
                except IndexError:
                   pass
                try:
                    self._add_normal_text(page, c, (self.normctrl).split()[0], 108, 52)
                except IndexError:
                   pass
                try:
                    self._add_normal_text(page,c,  (self.normctrl).split()[1], 108, 40)
                except IndexError:
                   pass
                try:
                    self._add_normal_text(page,c,  (self.utv).split()[0], 108, 29)
                except IndexError:
                   pass
                try:
                    self._add_normal_text(page,c,  (self.utv).split()[1], 108, 17)
                except IndexError:
                   pass
                try:
                    self._add_date(page,c,  self.date, 212, 70)
                except IndexError:
                   pass
                try:
                     self._add_date(page,c, self.date, 212, 45)
                except IndexError:
                   pass
                try:
                    self._add_date(page,c, self.date, 212, 22)
                except IndexError:
                   pass
                try:
                    self._add_rotated_text(page, c, self.inv_nom, 60, 5)
                except IndexError:
                   pass
                try:
                    self._add_rotated_text(page,c,  self.date, 60, 140)
                except IndexError:
                   pass
                try:
                    self.add_image(page, c, os.path.normpath((self.razrab).split()[2]), 160, 60, 50, 30)
                except OSError:
                   pass
                except IndexError:
                    pass 
                try:
                    self.add_image(page, c, os.path.normpath((self.normctrl).split()[2]), 160, 40, 50, 30)
                except OSError:
                   pass
                except IndexError:
                    pass 
                try:
                    self.add_image(page, c, os.path.normpath((self.utv).split()[2]), 160, 20, 50, 30)
                except OSError:
                   pass
                except IndexError:
                    pass 
                
            else:
                try:
                    self._add_rotated_text(page, c, self.inv_nom, 60, 5)
                except IndexError:
                   pass
                try:
                    self._add_rotated_text(page,c,  self.date, 60, 140)
                except IndexError:
                   pass 



        else:
            if "Разраб" in text:
                try:
                    self._add_normal_text(page, c, (self.razrab).split()[0], 705, 88)
                except IndexError:
                    pass

                try:
                    self._add_normal_text(page, c, (self.razrab).split()[1], 705, 74)
                except IndexError:
                    pass

                try:
                    self._add_normal_text(page, c, (self.normctrl).split()[0], 705, 60)
                except IndexError:
                    pass

                try:
                    self._add_normal_text(page, c, (self.normctrl).split()[1], 705, 46)
                except IndexError:
                    pass

                try:
                    self._add_normal_text(page, c, (self.utv).split()[0], 705, 32)
                except IndexError:
                    pass

                try:
                    self._add_normal_text(page, c, (self.utv).split()[1], 705, 17)
                except IndexError:
                    pass

                try:
                    self._add_date(page, c, self.date, 810, 80)
                except IndexError:
                    pass

                try:
                    self._add_date(page, c, self.date, 810, 55)
                except IndexError:
                    pass

                try:
                    self._add_date(page, c, self.date, 810, 27)
                except IndexError:
                    pass

                try:
                    self._add_rotated_text(page, c, self.inv_nom, 60, 5)
                except IndexError:
                    pass

                try:
                    self._add_rotated_text(page, c, self.date, 60, 140)
                except IndexError:
                    pass

                try:
                    self.add_image(page, c, os.path.normpath((self.razrab).split()[2]), 750, 70, 50, 30)
                except OSError:
                   pass
                except IndexError:
                    pass 
                try:
                    self.add_image(page, c, os.path.normpath((self.normctrl).split()[2]), 750, 45, 50, 30)
                except OSError:
                   pass
                except IndexError:
                    pass 
                try:
                    self.add_image(page, c, os.path.normpath((self.utv).split()[2]), 750, 20, 40, 30)
                except OSError:
                   pass
                except IndexError:
                    pass 
            else:
                try:
                    self._add_rotated_text(page, c, self.inv_nom, 60, 5)
                except IndexError:
                    pass

                try:
                    self._add_rotated_text(page, c, self.date, 60, 140)
                except IndexError:
                    pass

        c.save()
        self._add_temp_pdf_to_page(page)

    def _add_rotated_text(self,page, c,  text, x, y):
        c.setFont('GOST_I', 8)

        # Поворот текста на 90 градусов
        c.saveState()
        c.translate(x, y)
        c.rotate(90)
        c.drawString(10, 10, text)
        c.restoreState()

    def _add_normal_text(self,page, c,  text, x, y): #Добавляем Разработчика, Н.контр, Утв
        c.setFont('GOST_I', 12)
        c.drawString(x, y, text)



    def _add_date(self,page, c,  text, x, y): #Добавляем Разработчика, Н.контр, Утв
        c.setFont('GOST_I', 8)
        c.drawString(x, y, text)



    def add_image(self,page, c,   image_path, x, y, width, height, mask = "auto"):
        c.drawImage(image_path, x, y, width=width, height=height, mask = "auto")


    def _add_temp_pdf_to_page(self, page):
        temp_document = fitz.open(self.temp_pdf_path)
        page.show_pdf_page(page.rect, temp_document, 0)
        temp_document.close()

# Создаем главное окно
root = tk.Tk()
root.title("Редактор PDF")


with open('names.txt', 'r', encoding='utf-8') as file:
    # Инициализируем пустой список для фамилий
    values = []
    
    # Проходим по каждой строке в файле
    for line in file:
        # Разделяем строку по пробелу и берем первую часть (фамилию)
        surname = line#.split()[0]
        # Добавляем фамилию в список
        values.append(surname)

# Поля для ввода
tk.Label(root, text="Путь к PDF файлу:").pack()
pdf_entry = tk.Entry(root, width=50)
pdf_entry.pack()

tk.Label(root, text="Разраб.").pack()
developer_entry = ttk.Combobox(root, values=values)
developer_entry.bind("<<ComboboxSelected>>")  # Привязываем событие выбора
developer_entry.pack(pady=10)

tk.Label(root, text="Н.Контр.").pack()
ctrl_entry = ttk.Combobox(root, values=values)
ctrl_entry.bind("<<ComboboxSelected>>")
ctrl_entry.pack(pady=10)

tk.Label(root, text="Утв.").pack()
utv_entry = ttk.Combobox(root, values=values)
utv_entry.bind("<<ComboboxSelected>>") 
utv_entry.pack(pady=10)

tk.Label(root, text="Инв. №").pack()
inv_num = tk.Entry(root, width=50)
inv_num.pack()

tk.Label(root, text="Дата").pack()
date = tk.Entry(root, width=50)
date.pack()


def pdf_path_get():
    pdf_adder = File(pdf_path = pdf_entry.get(),
                     font = "gost.ttf", 
                     razrab = str(developer_entry.get()),
                     normctrl = str(ctrl_entry.get()), 
                     utv = str(utv_entry.get()), 
                     inv_nom=inv_num.get(),
                     date = date.get())

    pdf_adder.add_text()

# Кнопка для редактирования файла
edit_button = tk.Button(root, text="Отредактировать файл", command=lambda: threading.Thread(target=pdf_path_get).start())
edit_button.pack()

# Значок загрузки
loading_label = tk.Label(root, text="Загрузка...", fg="blue")
loading_label.pack_forget()  # Скрываем его изначально

# Запуск приложения
root.mainloop()