# -*- coding: utf-8 -*-
import os
import io
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import Color
from PyPDF2 import PdfReader, PdfWriter

class ProtocolDesignConstructor:
    def __init__(self, output_dir='reports'):
        # Создаем директорию для отчетов
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Регистрация шрифтов
        try:
            pdfmetrics.registerFont(TTFont('DejaVuSans', 'arial.ttf'))
        except Exception:
            pdfmetrics.registerStandardFonts()

    def create_protocol_template(self, 
                                 protocol_number,
                                 protocol_date,
                                 title='Протокол теплового обследования',
                                 logo_path=None,
                                 color_scheme=None):
        """
        Создание шаблона протокола с настраиваемым дизайном
        """
        # Параметры дизайна по умолчанию
        if color_scheme is None:
            color_scheme = {
                'background': Color(0.95, 0.95, 0.95),  # Светло-серый
                'header': Color(0.2, 0.4, 0.6),  # Синий
                'text': Color(0, 0, 0)  # Черный
            }
        
        width, height = A4
        filename = os.path.join(
            self.output_dir, 
            f'protocol_{protocol_number}_{protocol_date.replace("/", "-")}.pdf'
        )
        
        c = canvas.Canvas(filename, pagesize=A4)
        
        # Фон
        c.setFillColor(color_scheme['background'])
        c.rect(0, 0, width, height, fill=1, stroke=0)
        
        # Логотип
        if logo_path and os.path.exists(logo_path):
            c.drawImage(logo_path, 
                        width - 50*mm, 
                        height - 20*mm, 
                        width=40*mm, 
                        preserveAspectRatio=True)
        
        # Колонтитулы
        c.setFont('Helvetica', 10)
        c.setFillColor(color_scheme['text'])
        c.drawString(20*mm, height - 10*mm, f"Протокол №{protocol_number}")
        c.drawRightString(width - 20*mm, height - 10*mm, protocol_date)
        
        # Заголовок
        c.setFont('Helvetica', 16)
        c.setFillColor(color_scheme['header'])
        c.drawCentredString(width/2, height - 30*mm, title)
        
        c.save()
        return filename

    def add_thermogram_page(self, 
                             protocol_file, 
                             thermogram_data, 
                             protocol_number,
                             protocol_date):
        """
        Добавление страницы с термограммой
        """
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=A4)
        width, height = A4
        
        # Колонтитулы
        can.setFont('Helvetica', 10)
        can.drawString(20*mm, height - 10*mm, f"Протокол №{protocol_number}")
        can.drawRightString(width - 20*mm, height - 10*mm, protocol_date)
        
        # Данные термограммы
        can.setFont('Helvetica', 12)
        can.drawString(20*mm, height - 30*mm, f"Объект: {thermogram_data.get('equipment_name', 'Не указан')}")
        can.drawString(20*mm, height - 40*mm, f"Макс. температура: {thermogram_data.get('max_temp', 'н/д')}°C")
        can.drawString(20*mm, height - 50*mm, f"Мин. температура: {thermogram_data.get('min_temp', 'н/д')}°C")
        
        # Вставка термограммы
        if thermogram_data.get('thermogram_path') and os.path.exists(thermogram_data['thermogram_path']):
            can.drawImage(thermogram_data['thermogram_path'], 
                          20*mm, 50*mm, 
                          width=170*mm)
        
        can.save()
        
        # Объединение PDF
        packet.seek(0)
        new_pdf = PdfReader(packet)
        existing_pdf = PdfReader(open(protocol_file, 'rb'))
        output = PdfWriter()
        
        # Добавляем существующие страницы
        for page in existing_pdf.pages:
            output.add_page(page)
        
        # Добавляем новую страницу
        output.add_page(new_pdf.pages[0])
        
        # Сохраняем
        with open(protocol_file, 'wb') as f:
            output.write(f)

    def generate_full_protocol(self, 
                               protocol_data, 
                               thermograms,
                               logo_path=None):
        """
        Полная генерация протокола
        
        :param protocol_data: Словарь с данными протокола
        :param thermograms: Список словарей с данными термограмм
        :param logo_path: Путь к логотипу
        """
        # Создаем базовый шаблон протокола
        protocol_file = self.create_protocol_template(
            protocol_number=protocol_data['number'],
            protocol_date=protocol_data['date'],
            logo_path=logo_path
        )
        
        # Добавляем страницы с термограммами
        for thermogram in thermograms:
            self.add_thermogram_page(
                protocol_file, 
                thermogram, 
                protocol_data['number'],
                protocol_data['date']
            )
        
        return protocol_file

# Пример использования
if __name__ == "__main__":
    constructor = ProtocolDesignConstructor(output_dir='c:/protokol/reports')
    
    protocol_data = {
        'number': '123-ТО',
        'date': '22.12.2024'
    }
    
    thermograms = [
        {
            'equipment_name': 'Трансформатор Т-1',
            'max_temp': 85,
            'min_temp': 60,
            'thermogram_path': None  # Убираем путь к термограмме
        },
        {
            'equipment_name': 'Трансформатор Т-2',
            'max_temp': 75,
            'min_temp': 55,
            'thermogram_path': None  # Убираем путь к термограмме
        }
    ]
    
    protocol_path = constructor.generate_full_protocol(
        protocol_data, 
        thermograms, 
        logo_path=None  # Убираем путь к логотипу
    )
    print(f"Протокол сгенерирован: {protocol_path}")
