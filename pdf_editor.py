import customtkinter as ctk
from tkinter import messagebox
from tkinter import filedialog

import fitz  # PyMuPDF
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
from datetime import datetime

font_path = "gost.ttf"
pdfmetrics.registerFont(TTFont('GOST_I', font_path))

class File:
    def __init__(self, pdf_path, font, razrab, drafted, normctrl, Reg_Doc_Ctrl, utv, Approved):
        self.pdf_path = pdf_path
        self.font = font
        self.razrab = razrab
        self.drafted = drafted
        self.normctrl = normctrl
        self.Reg_Doc_Ctrl = Reg_Doc_Ctrl
        self.utv = utv
        self.Approved = Approved
        self.temp_pdf_path = "temp_output.pdf"
        self.date = datetime.now().strftime("%d.%m.%Y")

        # Регистрируем шрифт
        pdfmetrics.registerFont(TTFont('GOST_I', self.font))



    def add_text(self):

        file_path = self.pdf_path
        print(file_path)
        if os.path.exists(file_path):
            document = fitz.open(file_path)
            for page_num in range(document.page_count):
                page = document.load_page(page_num)
                self._process_page(page)
            

            # Сохранение изменений в новый PDF
            document.save(str(self.pdf_path)[:-4]+"new.pdf")
            document.close()
            print("ok")
            
        else:
            print("Файл не найден.")


    def _process_page(self, page):
        text = page.get_text("text")
        rect = page.rect  # Получаем размер страницы
        print("procs")

        if "Формат А4" in text:
            if "Разраб" in text:
                self._add_normal_text(page, razrab, 108, 75)
                self._add_normal_text(page, drafted, 108, 63)
                self._add_normal_text(page, normctrl, 108, 52)
                self._add_normal_text(page, Reg_Doc_Ctrl, 108, 40)
                self._add_normal_text(page, utv, 108, 29)
                self._add_normal_text(page, Approved, 108, 17)
                self._add_date(page, self.date, 212, 70)
                self._add_date(page, self.date, 212, 45)
                self._add_date(page, self.date, 212, 22)
                self._add_rotated_text(page, "09/1383/2/У.0097.1-01", 60, 5)
                self._add_rotated_text(page, self.date, 60, 140)
                #self.add_image(page, "/content/pic.png", 50, 50, 100, 100)
            else:
                self._add_rotated_text(page, "09/1383/2/У.0097.1-01", 60, 5)
                self._add_rotated_text(page, self.date, 60, 140)



        if "Формат А3" in text:
            if "Разраб" in text:
                self._add_normal_text(page, razrab, 705, 88)
                self._add_normal_text(page, drafted, 705, 74)
                self._add_normal_text(page, normctrl, 705, 60)
                self._add_normal_text(page, Reg_Doc_Ctrl, 705, 46)
                self._add_normal_text(page, utv, 705, 32)
                self._add_normal_text(page, Approved, 705, 17)
                self._add_date(page, self.date, 810, 80)
                self._add_date(page, self.date, 810, 55)
                self._add_date(page, self.date, 810, 27)
                self._add_rotated_text(page, "09/1383/2/У.0097.1-01", 60, 5)
                self._add_rotated_text(page, self.date, 60, 140)
            else:
                self._add_rotated_text(page, "09/1383/2/У.0097.1-01", 60, 5)
                self._add_rotated_text(page, self.date, 60, 140)

    def _add_rotated_text(self, page, text, x, y):
        c = canvas.Canvas(self.temp_pdf_path, pagesize=(page.rect.width, page.rect.height))
        c.setFont('GOST_I', 8)
        c.setFillColorRGB(1, 0, 0)

        # Поворот текста на 90 градусов
        c.saveState()
        c.translate(x, y)
        c.rotate(90)
        c.drawString(10, 10, text)
        c.restoreState()

        c.save()
        self._add_temp_pdf_to_page(page)

    def _add_normal_text(self, page, text, x, y): #Добавляем Разработчика, Н.контр, Утв
        c = canvas.Canvas(self.temp_pdf_path, pagesize=(page.rect.width, page.rect.height))
        c.setFont('GOST_I', 12)
        c.setFillColorRGB(1, 0, 0)
        c.drawString(x, y, text)
        c.save()
        self._add_temp_pdf_to_page(page)


    def _add_date(self, page, text, x, y): #Добавляем Разработчика, Н.контр, Утв
        c = canvas.Canvas(self.temp_pdf_path, pagesize=(page.rect.width, page.rect.height))
        c.setFont('GOST_I', 8)
        c.setFillColorRGB(1, 0, 0)
        c.drawString(x, y, text)
        c.save()
        self._add_temp_pdf_to_page(page)


    def add_image(self, page, image_path, x, y, width, height):
        """Вставляет изображение в PDF документ."""
        c = canvas.Canvas(self.temp_pdf_path, pagesize=(page.rect.width, page.rect.height))
        c.drawImage(image_path, x, y, width=width, height=height)
        c.save()
        self._add_temp_pdf_to_page(page)


    def _add_temp_pdf_to_page(self, page):
        temp_document = fitz.open(self.temp_pdf_path)
        page.show_pdf_page(page.rect, temp_document, 0)
        temp_document.close()

    

def open_file():
    filepath = filedialog.askopenfilename()
    if filepath != "":
        with open(filepath, "r") as file:
            text_editor.insert("0.0", filepath)



ctk.set_appearance_mode("light")  # Установка светлой темы
ctk.set_default_color_theme("blue")  # Установка цветовой темы
window = ctk.CTk()  # Создание окна с использованием customtkinter
window.title('pdf_editor')
window.geometry('1000x600')

# Создание фрейма
frame = ctk.CTkFrame(window, width=1000, height=800)
frame.pack(padx=10, pady=10, expand=True)

# Метки и поля ввода

text_editor = ctk.CTkTextbox(frame,  width=200, height=40)
text_editor.grid(column=1, row=0)

input_file_lb = ctk.CTkLabel(frame, text="Выберите файл")
input_file_lb.grid(row=0, column=0, padx=10, pady=5)

open_button = ctk.CTkButton(frame, text="Открыть файл", command=open_file)
open_button.grid(column=2, row=0, padx=10, pady=5)


razrab_lb = ctk.CTkLabel(frame, text="Введите имя разработчика")
razrab_lb.grid(row=1, column=0, padx=10, pady=5)

razrab = ctk.CTkEntry(frame)
razrab.grid(row=1, column=1, pady=5)

drafted = ctk.CTkEntry(frame)
drafted.grid(row=1, column=2, pady=5)

normctrl_lb = ctk.CTkLabel(frame, text="Введите имя норм.контролера")
normctrl_lb.grid(row=2, column=0, padx=10, pady=5)

normctrl = ctk.CTkEntry(frame)
normctrl.grid(row=2, column=1, pady=5)

Reg_Doc_Ctrl = ctk.CTkEntry(frame)
Reg_Doc_Ctrl.grid(row=2, column=2, pady=5)

utv_lb = ctk.CTkLabel(frame, text="Введите имя утв-го")
utv_lb.grid(row=3, column=0, padx=10, pady=5)

utv = ctk.CTkEntry(frame)
utv.grid(row=3, column=1, pady=5)

Approved = ctk.CTkEntry(frame)
Approved.grid(row=3, column=2, pady=5)

# Кнопка для расчета ИМТ


def pdf_path_get():
    pdf_adder = File(pdf_path = "КОВ-АСп-4-II-1200х600-У-Ф.pdf", #text_editor.get("0.0", "end"), 
                     font = font_path, 
                     razrab = str(razrab.get()), 
                     drafted = str(drafted.get()), 
                     normctrl = str(normctrl.get()), 
                     Reg_Doc_Ctrl = str(Reg_Doc_Ctrl.get()), 
                     utv = str(utv.get()), 
                     Approved = str(utv.get()))
    pdf_adder.add_text()


add_button = ctk.CTkButton(frame, text="Добавить текст", command=pdf_path_get)
add_button.grid(row=4, column=0, columnspan=3, pady=10)

# Запуск основного цикла
window.mainloop()