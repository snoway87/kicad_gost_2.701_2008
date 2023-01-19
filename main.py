import sys
import os
import re
import datetime
from fpdf import FPDF
from sexpdata import loads, dumps, Symbol

class PDF:
    A4_W = 210
    A4_H = 297
    FIRST_PAGE_LINES = 25
    OTHER_PAGE_LINES = 31
    def __init__(self,
        document_title='Название схемы',
        document_number='АБВГ.ХХХХХХ.ХХХ ПЭ3',
        document_character='У',
        document_date='',
        company_code='ИКБ БПМО-01-21',
        engineer_title='Полевский И.С.',
        checker_title='Куликов А.К.',
        approver_title='Снедков А.Б.',
        output_file="component_list.pdf", total_pages=0):

        self.engineer_title = engineer_title
        self.checker_title = checker_title
        self.approver_title = approver_title
        self.document_title = document_title
        self.document_number = document_number
        self.document_character = document_character
        self.document_date = document_date
        self.company_code = company_code

        self.total_pages = total_pages
        self.pages = 0
        self.lines = 0

        self.page_number = 0
        self.page_lines = 0
        self.output_file = output_file
        self.pdf = FPDF(orientation="P",unit="mm", format="A4")

    def draw_frame(self):
        self.pdf.set_text_color(0, 0, 0)
        self.pdf.set_draw_color(0, 0, 0)

        # left
        self.pdf.set_line_width(0.5)
        self.pdf.line(20, 5, 20, self.A4_H - 5)
        self.pdf.line(13, self.A4_H - 5, 13, self.A4_H - 150)
        self.pdf.line(8, self.A4_H - 5, 8, self.A4_H - 150)

        y_offset = 0
        self.pdf.line(8, self.A4_H - (5 + y_offset), 20, self.A4_H - (5 + y_offset))
        y_offset += 25
        self.pdf.line(8, self.A4_H - (5 + y_offset), 20, self.A4_H - (5 + y_offset))
        y_offset += 35
        self.pdf.line(8, self.A4_H - (5 + y_offset), 20, self.A4_H - (5 + y_offset))
        y_offset += 25
        self.pdf.line(8, self.A4_H - (5 + y_offset), 20, self.A4_H - (5 + y_offset))
        y_offset += 25
        self.pdf.line(8, self.A4_H - (5 + y_offset), 20, self.A4_H - (5 + y_offset))
        y_offset += 35
        self.pdf.line(8, self.A4_H - (5 + y_offset), 20, self.A4_H - (5 + y_offset))

        # top
        self.pdf.line(20, 5, self.A4_W - 5, 5)

        self.pdf.line(20, 20, self.A4_W - 5, 20)
        self.pdf.line(40, 5, 40, 20)
        self.pdf.line(150, 5, 150, 20)
        self.pdf.line(160, 5, 160, 20)

        # right
        self.pdf.line(self.A4_W - 5, 5, self.A4_W - 5, self.A4_H - 5)

        # bottom
        self.pdf.line(20, self.A4_H - 5, self.A4_W - 5, self.A4_H - 5)

        for w in range(25, 45, 5):
            if w == 25 or w == 30 or w == 40:
                self.pdf.set_line_width(0.5)
            else:
                self.pdf.set_line_width(0.2)
            self.pdf.line(self.A4_W - 190, self.A4_H - (5 + w - 25), self.A4_W - 125, self.A4_H - (5 + w - 25))

        self.pdf.set_line_width(0.5)
        self.pdf.line(self.A4_W - 173, self.A4_H - 5,  self.A4_W - 173, self.A4_H - 20)
        self.pdf.line(self.A4_W - 183, self.A4_H - 5,  self.A4_W - 183, self.A4_H - 20)
        self.pdf.line(self.A4_W - 150, self.A4_H - 5,  self.A4_W - 150, self.A4_H - 20)
        self.pdf.line(self.A4_W - 135, self.A4_H - 5,  self.A4_W - 135, self.A4_H - 20)
        self.pdf.line(self.A4_W - 125, self.A4_H - 5,  self.A4_W - 125, self.A4_H - 20)

        self.pdf.line(self.A4_W - 125, self.A4_H - 20, self.A4_W - 5, self.A4_H - 20)
        self.pdf.line(self.A4_W - 15, self.A4_H - 13, self.A4_W - 5, self.A4_H - 13)

        self.pdf.line(self.A4_W - 125, self.A4_H - 5,  self.A4_W - 125, self.A4_H - 20)
        self.pdf.line(self.A4_W - 15, self.A4_H - 5, self.A4_W - 15, self.A4_H - 20)

        # text
        self.pdf.set_font("GOST", size=10)

        self.pdf.set_xy(20, 5)
        self.pdf.cell(20, 5, txt="Поз.", ln=1, align="C")
        self.pdf.set_xy(20, 10)
        self.pdf.cell(20, 5, txt="обозна-", ln=1, align="C")
        self.pdf.set_xy(20, 15)
        self.pdf.cell(20, 5, txt="чение", ln=1, align="C")
        self.pdf.set_xy(40, 5)
        self.pdf.cell(110, 15, txt="Наименование", ln=1, align="C")
        self.pdf.set_xy(150, 5)
        self.pdf.cell(10, 15, txt="Кол.", ln=1, align="C")
        self.pdf.set_xy(160, 5)
        self.pdf.cell(45, 15, txt="Примечание", ln=1, align="C")

        self.pdf.rotate(90, 12, self.A4_H - 8)
        self.pdf.text(12, self.A4_H - 8,txt="Инв. № подп.")
        self.pdf.rotate(0)
        self.pdf.rotate(90, 12, self.A4_H - 37)
        self.pdf.text(12, self.A4_H - 37,txt="Подп. и дата")
        self.pdf.rotate(0)
        self.pdf.rotate(90, 12, self.A4_H - 68)
        self.pdf.text(12, self.A4_H - 68,txt="Взам. инв.№")
        self.pdf.rotate(0)
        self.pdf.rotate(90, 12, self.A4_H - 93)
        self.pdf.text(12, self.A4_H - 93,txt="Инв. № дубл.")
        self.pdf.rotate(0)
        self.pdf.rotate(90, 12, self.A4_H - 122)
        self.pdf.text(12, self.A4_H - 122,txt="Подп. и дата")
        self.pdf.rotate(0)

        self.pdf.set_xy(-185 - 5, -10)
        self.pdf.cell(7, 5, txt="Изм.", ln=1, align="C")
        self.pdf.set_xy(-178 - 5, -10)
        self.pdf.cell(10, 5, txt="Лист", ln=1, align="C")
        self.pdf.set_xy(-168 - 5, -10)
        self.pdf.cell(23, 5, txt="№ Докум.", ln=1, align="C")
        self.pdf.set_xy(-145 - 5, -10)
        self.pdf.cell(15, 5, txt="Подп.", ln=1, align="C")
        self.pdf.set_xy(-130 - 5, -10)
        self.pdf.cell(10, 5, txt="Дата", ln=1, align="C")

        self.pdf.set_xy(-15, -20)
        self.pdf.cell(10, 7, txt="Лист", ln=1, align="C")
        self.pdf.set_xy(-15, -13)
        self.pdf.cell(10, 8, txt=str(self.pages), ln=1, align="C")

        self.pdf.set_font("GOST", size=18)
        self.pdf.set_xy(-125, -20)
        self.pdf.cell(110, 15, txt=self.document_number, ln=1, align="C")

    def draw_first_frame(self):
        self.pdf.set_text_color(0, 0, 0)
        self.pdf.set_draw_color(0, 0, 0)

        # left
        self.pdf.set_line_width(0.5)
        self.pdf.line(20, 5, 20, self.A4_H - 5)
        self.pdf.line(13, self.A4_H - 5, 13, self.A4_H - 150)
        self.pdf.line(8, self.A4_H - 5, 8, self.A4_H - 150)

        y_offset = 0
        self.pdf.line(8, self.A4_H - (5 + y_offset), 20, self.A4_H - (5 + y_offset))
        y_offset += 25
        self.pdf.line(8, self.A4_H - (5 + y_offset), 20, self.A4_H - (5 + y_offset))
        y_offset += 35
        self.pdf.line(8, self.A4_H - (5 + y_offset), 20, self.A4_H - (5 + y_offset))
        y_offset += 25
        self.pdf.line(8, self.A4_H - (5 + y_offset), 20, self.A4_H - (5 + y_offset))
        y_offset += 25
        self.pdf.line(8, self.A4_H - (5 + y_offset), 20, self.A4_H - (5 + y_offset))
        y_offset += 35
        self.pdf.line(8, self.A4_H - (5 + y_offset), 20, self.A4_H - (5 + y_offset))

        # top
        self.pdf.line(20, 5, self.A4_W - 5, 5)
        self.pdf.line(13, 5, 13, 125)
        self.pdf.line(8, 5, 8, 125)

        self.pdf.line(8, 5, 20 , 5)
        self.pdf.line(8, 65, 20 , 65)
        self.pdf.line(8, 125, 20 , 125)

        self.pdf.line(20, 20, self.A4_W - 5, 20)
        self.pdf.line(40, 5, 40, 20)
        self.pdf.line(150, 5, 150, 20)
        self.pdf.line(160, 5, 160, 20)

        # right
        self.pdf.line(self.A4_W - 5, 5, self.A4_W - 5, self.A4_H - 5)

        # bottom
        self.pdf.line(20, self.A4_H - 5, self.A4_W - 5, self.A4_H - 5)


        for w in range(0, 45, 5):
            if w == 25 or w == 30 or w == 40:
                self.pdf.set_line_width(0.5)
            else:
                self.pdf.set_line_width(0.2)
            self.pdf.line(self.A4_W - 190, self.A4_H - (5 + w), self.A4_W - 125, self.A4_H - (5 + w))

        self.pdf.set_line_width(0.5)
        self.pdf.line(self.A4_W - 173, self.A4_H - 5,  self.A4_W - 173, self.A4_H - 45)
        self.pdf.line(self.A4_W - 183, self.A4_H - 30, self.A4_W - 183, self.A4_H - 45)
        self.pdf.line(self.A4_W - 150, self.A4_H - 5,  self.A4_W - 150, self.A4_H - 45)
        self.pdf.line(self.A4_W - 135, self.A4_H - 5,  self.A4_W - 135, self.A4_H - 45)
        self.pdf.line(self.A4_W - 125, self.A4_H - 5,  self.A4_W - 125, self.A4_H - 45)

        self.pdf.line(self.A4_W - 125, self.A4_H - 30, self.A4_W - 5, self.A4_H - 30)
        self.pdf.line(self.A4_W - 125, self.A4_H - 45, self.A4_W - 5, self.A4_H - 45)
        self.pdf.line(self.A4_W - 125, self.A4_H - 53, self.A4_W - 5, self.A4_H - 53)
        self.pdf.line(self.A4_W - 125, self.A4_H - 67, self.A4_W - 5, self.A4_H - 67)

        self.pdf.line(self.A4_W - 125, self.A4_H - 5,  self.A4_W - 125, self.A4_H - 67)
        self.pdf.line(self.A4_W - 111, self.A4_H - 53, self.A4_W - 111, self.A4_H - 67)
        self.pdf.line(self.A4_W - 58, self.A4_H - 53,  self.A4_W - 58, self.A4_H - 67)
        self.pdf.line(self.A4_W - 55, self.A4_H - 5,   self.A4_W - 55, self.A4_H - 30)

        self.pdf.line(self.A4_W - 55, self.A4_H - 20, self.A4_W - 5, self.A4_H - 20)
        self.pdf.line(self.A4_W - 55, self.A4_H - 25, self.A4_W - 5, self.A4_H - 25)
        self.pdf.set_line_width(0.2)
        self.pdf.line(self.A4_W - 50, self.A4_H - 20, self.A4_W - 50, self.A4_H - 25)
        self.pdf.line(self.A4_W - 45, self.A4_H - 20, self.A4_W - 45, self.A4_H - 25)
        self.pdf.set_line_width(0.5)
        self.pdf.line(self.A4_W - 40, self.A4_H - 20, self.A4_W - 40, self.A4_H - 30)
        self.pdf.line(self.A4_W - 25, self.A4_H - 20, self.A4_W - 25, self.A4_H - 30)

        # text
        self.pdf.set_font("GOST", size=10)

        self.pdf.set_xy(20, 5)
        self.pdf.cell(20, 5, txt="Поз.", ln=1, align="C")
        self.pdf.set_xy(20, 10)
        self.pdf.cell(20, 5, txt="обозна-", ln=1, align="C")
        self.pdf.set_xy(20, 15)
        self.pdf.cell(20, 5, txt="чение", ln=1, align="C")
        self.pdf.set_xy(40, 5)
        self.pdf.cell(110, 15, txt="Наименование", ln=1, align="C")
        self.pdf.set_xy(150, 5)
        self.pdf.cell(10, 15, txt="Кол.", ln=1, align="C")
        self.pdf.set_xy(160, 5)
        self.pdf.cell(45, 15, txt="Примечание", ln=1, align="C")

        self.pdf.rotate(90, 12, self.A4_H - 8)
        self.pdf.text(12, self.A4_H - 8,txt="Инв. № подп.")
        self.pdf.rotate(0)
        self.pdf.rotate(90, 12, self.A4_H - 37)
        self.pdf.text(12, self.A4_H - 37,txt="Подп. и дата")
        self.pdf.rotate(0)
        self.pdf.rotate(90, 12, self.A4_H - 68)
        self.pdf.text(12, self.A4_H - 68,txt="Взам. инв.№")
        self.pdf.rotate(0)
        self.pdf.rotate(90, 12, self.A4_H - 93)
        self.pdf.text(12, self.A4_H - 93,txt="Инв. № дубл.")
        self.pdf.rotate(0)
        self.pdf.rotate(90, 12, self.A4_H - 122)
        self.pdf.text(12, self.A4_H - 122,txt="Подп. и дата")
        self.pdf.rotate(0)
        self.pdf.rotate(90, 12, self.A4_H - 195)
        self.pdf.text(12, self.A4_H - 195,txt="Справ. №")
        self.pdf.rotate(0)
        self.pdf.rotate(90, 12, self.A4_H - 250)
        self.pdf.text(12, self.A4_H - 250,txt="Перв. примен.")
        self.pdf.rotate(0)

        self.pdf.set_xy(-185 - 5, -30 - 5)
        self.pdf.cell(7, 5, txt="Изм.", ln=1, align="C")
        self.pdf.set_xy(-178 - 5, -30 - 5)
        self.pdf.cell(10, 5, txt="Лист", ln=1, align="C")
        self.pdf.set_xy(-168 - 5, -30 - 5)
        self.pdf.cell(23, 5, txt="№ Докум.", ln=1, align="C")
        self.pdf.set_xy(-145 - 5, -30 - 5)
        self.pdf.cell(15, 5, txt="Подп.", ln=1, align="C")
        self.pdf.set_xy(-130 - 5, -30 - 5)
        self.pdf.cell(10, 5, txt="Дата", ln=1, align="C")
        self.pdf.set_xy(-190, -30)
        self.pdf.cell(17, 5, txt="Разраб.", ln=1, align="C")
        self.pdf.set_xy(-173, -30)
        self.pdf.cell(23, 5, txt=self.engineer_title, ln=1, align="L")
        self.pdf.set_xy(-185 - 5, -25)
        self.pdf.cell(17, 5, txt="Пров.", ln=1, align="C")
        self.pdf.set_xy(-173, -25)
        self.pdf.cell(23, 5, txt=self.checker_title, ln=1, align="L")
        self.pdf.set_xy(-185 - 5, -10 - 5)
        self.pdf.cell(17, 5, txt="Н.контр.", ln=1, align="C")
        self.pdf.set_xy(-185 - 5, -5 - 5)
        self.pdf.cell(17, 5, txt="Утв.", ln=1, align="C")
        self.pdf.set_xy(-173, -10)
        self.pdf.cell(23, 5, txt=self.approver_title, ln=1, align="L")

        # self.pdf.set_font("GOST", size=6)
        # self.pdf.set_xy(-135, -10)
        # self.pdf.cell(23, 5, txt=self.document_date, ln=1, align="L")
        # self.pdf.set_font("GOST", size=10)

        self.pdf.set_xy(-55, -30)
        self.pdf.cell(15, 5, txt="Лит.", ln=1, align="C")
        self.pdf.set_xy(-50, -25)
        self.pdf.cell(5, 5, txt=self.document_character, ln=1, align="C")

        self.pdf.set_xy(-40, -30)
        self.pdf.cell(15, 5, txt="Лист", ln=1, align="C")
        self.pdf.set_xy(-40, -25)
        self.pdf.cell(15, 5, txt=str(self.pages), ln=1, align="C")

        self.pdf.set_xy(-25, -30)
        self.pdf.cell(20, 5, txt="Листов", ln=1, align="C")
        self.pdf.set_xy(-25, -25)
        self.pdf.cell(20, 5, txt=str(self.total_pages), ln=1, align="C")

        self.pdf.set_font("GOST", size=18)
        self.pdf.set_xy(-125, -45)
        self.pdf.cell(120, 15, txt=self.document_number, ln=1, align="C")

        self.pdf.set_font("GOST", size=14)
        self.pdf.set_xy( -125, -30 )
        self.pdf.cell(70, 25, txt=self.document_title, ln=2, align="C")

        self.pdf.set_xy( -55, -20 )
        self.pdf.cell(50, 15, txt=self.company_code, ln=2, align="C")

    def draw_line(fn):
        def wrapper(* args, **kwargs):
            new_page = False
            self = args[0]
            if self.pages == 0:
                self.pages += 1
                self.lines = 0
                self.add_page()
                new_page = True
            else:
                if (self.pages == 1 and self.lines >= self.FIRST_PAGE_LINES) or (self.pages > 1 and self.lines >= self.OTHER_PAGE_LINES):
                    self.pages += 1
                    self.lines = 0
                    self.add_page()
                    new_page = True

            # Draw empty line before header
            res = 0
            lines = 2 if new_page == False and fn.__name__ == 'add_components_header' else 1
            for i in range(0, lines):
                line_offset = self.line_offset()
                self.pdf.set_draw_color(0, 0, 0)
                self.pdf.set_line_width(0.2)
                self.pdf.line(20, line_offset, self.A4_W - 5, line_offset)
                self.pdf.set_line_width(0.5)
                self.pdf.line(40,  line_offset, 40,  line_offset - 8)
                self.pdf.line(150, line_offset, 150, line_offset - 8)
                self.pdf.line(160, line_offset, 160, line_offset - 8)
                if i == lines - 1:
                    res = fn(*args, **kwargs)
                self.lines += 1
            return res
        return wrapper

    def line_offset(self):
        return 28 if self.lines == 0 else 28 + self.lines * 8

    def add_page(self):
        self.pdf.add_page()
        self.pdf.set_margins(5, 5, 5)
        self.pdf.set_auto_page_break(auto = True, margin = 5)
        self.pdf.add_font('GOST', '', '/Users/snoway/Library/Fonts/GOST_A_Italic.ttf', uni=True)
        if self.pages == 1:
            self.draw_first_frame()
        else:
            self.draw_frame()

    @draw_line
    def add_components_header(self, header =""):
        self.pdf.set_font("GOST", size=12)
        self.pdf.set_xy(40, self.line_offset() - 8)
        self.pdf.cell(110, 8, txt=header, ln=1, align="C")

        self.pdf.set_line_width(0.2)
        self.pdf.line(40 + 55 - (len(header)/2) * 2, self.line_offset() - 2, 40 + 55 + (len(header)/2) * 2, self.line_offset() - 2)

    @draw_line
    def add_component(self, idx, name, qty, description):
        self.pdf.set_font("GOST", size=8)
        self.pdf.set_xy(20, self.line_offset() - 8)
        self.pdf.cell(20, 8, txt=idx, ln=1, align="L")
        self.pdf.set_font("GOST", size=10)
        self.pdf.set_xy(40, self.line_offset() - 8)
        self.pdf.cell(1100, 8, txt=name, ln=1, align="L")
        self.pdf.set_xy(150, self.line_offset() - 8)
        self.pdf.cell(10, 8, txt=str(qty), ln=1, align="C")
        self.pdf.set_xy(160, self.line_offset() - 8)
        self.pdf.cell(45, 8, txt=description, ln=1, align="C")

    def save(self):
        self.pdf.output(self.output_file)



class KiCadNets:
    def __init__(self, kicad_nets_file="Mainboard.net"):
        self.kicad_nets_file = kicad_nets_file
        self.engineer_title = ""
        self.checker_title = ""
        self.approver_title = ""
        self.document_number = ""
        self.document_title = ""
        self.document_character = ""
        self.document_date = ""
        self.company_code = ""

        self.components = {
            'C' :  { 'name' : 'Конденсаторы', 'elements' : [] },
            'R' :  { 'name' : 'Резисторы', 'elements' : [] },
            'RP' : { 'name' : 'Подстроечные резисторы', 'elements' : [] },
            'BQ' : { 'name' : 'Пьезоэлектрические элементы', 'elements' : [] },
            'DA' : { 'name' : 'Аналоговые микросхемы', 'elements' : [] },
            'DD' : { 'name' : 'Цифровые микросхемы', 'elements' : [] },
            'XS' : { 'name' : 'Разъемы', 'elements' : [] },
            'VD' : { 'name' : 'Диоды', 'elements' : [] },
            'HL' : { 'name' : 'Светодиоды', 'elements' : [] },
            'L'  : { 'name' : 'Индуктивность', 'elements' : [] },
            'FB' : { 'name' : 'Ферритовые бусины', 'elements' : [] },
            'SA' : { 'name' : 'Переключатели', 'elements' : [] }
        }
        # Plus header lines
        self.total_lines = len(self.components) * 2 - 1

    def parse(self):
        with open(self.kicad_nets_file, 'r') as f:
            nets = loads(f.read())

            if nets[2][0] != Symbol('design'):
                raise Exception('Disgn section not found')
            if nets[3][0] != Symbol('components'):
                raise Exception('Title_block section not found')
            if nets[2][2][0] != Symbol('date'):
                raise Exception('Date section not found')
            if nets[2][4][0] != Symbol('sheet'):
                raise Exception('Sheet section not found')
            if nets[2][4][4][0] != Symbol('title_block'):
                raise Exception('Title_block section not found')

            title_block = nets[2][4][4]
            date_string = nets[2][2][1]

            date = datetime.datetime.strptime(date_string, "%Y %B %d, %A %H:%M:%S")
            self.document_date = date.strftime("%d.%m.%Y")

            # Parse titles
            for title in title_block:
                # gost_landscape.kicad_wks page!
                if type(title) == list and title[0] == Symbol('title'):
                    self.document_title = str(title[1])
                if type(title) == list and title[0] == Symbol('company'):
                    self.company_code = str(title[1])
                if type(title) == list and len(title) == 3 and title[0] == Symbol('comment'):
                    if title[1][0] == Symbol('number') and int(title[1][1]) == 2:
                        self.engineer_title = str(title[2][1])
                    if title[1][0] == Symbol('number') and int(title[1][1]) == 3:
                        self.checker_title = str(title[2][1])
                    if title[1][0] == Symbol('number') and int(title[1][1]) == 4:
                        self.approver_title = str(title[2][1])
                    if title[1][0] == Symbol('number') and int(title[1][1]) == 1:
                        self.document_number = str(title[2][1])
                    if title[1][0] == Symbol('number') and int(title[1][1]) == 9:
                        self.document_character = str(title[2][1])

            # Parse components
            components = nets[3]
            for comp in components:
                if type(comp) == list:

                    if comp[1][0] != Symbol('ref'):
                        raise Exception('Ref section not found')
                    if comp[2][0] != Symbol('value'):
                        raise Exception('Value section not found')
                    if comp[3][0] != Symbol('footprint'):
                        raise Exception('Footprint section not found')

                    ref = comp[1][1]
                    value = comp[2][1]
                    footprint = comp[3][1].split(':')[1]
                    precision = ''
                    for field in comp:
                        if type(field) == list and len(title) == 3 and field[0] == Symbol('property'):
                            if field[1][1] == 'Precision' and field[2][0] == Symbol('value'):
                                precision = str(field[2][1])

                    match = re.match(r'^C[0-9].*$', ref)
                    if match != None:
                        ref = match.group(0)
                        self.add_componet(self.components['C']['elements'], ref, value, footprint, precision=precision)

                    match = re.match(r'^R[0-9].*$', ref)
                    if match != None:
                        ref = match.group(0)
                        self.add_componet(self.components['R']['elements'], ref, value, footprint, precision=precision)

                    match = re.match(r'^RP[0-9].*$', ref)
                    if match != None:
                        ref = match.group(0)
                        self.add_componet(self.components['RP']['elements'], ref, value, footprint, precision=precision)

                    match = re.match(r'^BQ[0-9].*$', ref)
                    if match != None:
                        ref = match.group(0)
                        self.add_componet(self.components['BQ']['elements'], ref, value, footprint)

                    match = re.match(r'^DA[0-9].*$', ref)
                    if match != None:
                        ref = match.group(0)
                        self.add_componet(self.components['DA']['elements'], ref, value, footprint)

                    match = re.match(r'^DD[0-9].*$', ref)
                    if match != None:
                        ref = match.group(0)
                        self.add_componet(self.components['DD']['elements'], ref, value, footprint)

                    match = re.match(r'^XS[0-9].*$', ref)
                    if match != None:
                        ref = match.group(0)
                        self.add_componet(self.components['XS']['elements'], ref, value, footprint)

                    match = re.match(r'^VD[0-9].*$', ref)
                    if match != None:
                        ref = match.group(0)
                        self.add_componet(self.components['VD']['elements'], ref, value, footprint)

                    match = re.match(r'^HL[0-9].*$', ref)
                    if match != None:
                        ref = match.group(0)
                        self.add_componet(self.components['HL']['elements'], ref, value, footprint)

                    match = re.match(r'^L[0-9].*$', ref)
                    if match != None:
                        ref = match.group(0)
                        self.add_componet(self.components['L']['elements'], ref, value, footprint)

                    match = re.match(r'^SA[0-9].*$', ref)
                    if match != None:
                        ref = match.group(0)
                        self.add_componet(self.components['SA']['elements'], ref, value, footprint)

            # GOST sorting for element groups
            self.gost_sort_elements()


    def gost_sort_elements(self):
        for key, value in self.components.items():
            for idx, comp in enumerate(value['elements']):

                i = j = 0
                refs_digits = []
                refs_sorted = []
                for ref in comp['refs']:
                    refs_digits.append(int(''.join(i for i in ref if i.isdigit())))

                def add_element(arr, elements, qty):
                    if len(arr) > 0 and len(arr[-1][0] + ', ' + elements ) < 14:
                        arr[-1][0] += ', ' + elements
                        arr[-1][1] += qty
                    else:
                        arr.append([ elements, qty])

                while i < len(refs_digits):
                    found = False
                    j = i + 1
                    while j < len(refs_digits) and len(refs_digits) -  (i + 1) >= 2:
                        if refs_digits[j] - refs_digits[i] == j - i:
                            if j - i >= 2:
                                found = True
                            j += 1
                            if j == len(refs_digits):
                                add_element(refs_sorted, key + str(refs_digits[i]) + '-' + key + str(refs_digits[j - 1]),  j - i)
                                i = j - 1
                                break
                            else:
                                continue
                        else:
                            if found == True:
                                add_element(refs_sorted, key + str(refs_digits[i]) + '-' + key + str(refs_digits[j - 1]),  j - i)
                                i = j - 1
                            break

                    if found == False:
                        add_element(refs_sorted, key + str(refs_digits[i]), 1)
                    i += 1

                self.components[key]['elements'][idx]['refs'] = refs_sorted
                self.total_lines += len(refs_sorted) # Fix

    def add_componet(self, arr, ref, value, footprint, precision=''):
        found = False
        for comp in arr:
            if comp['value'] == value and comp['footprint'] == footprint:
                comp['refs'].append(ref)
                found = True
                break
        if found == False:
            arr.append({'value' : value, 'refs'  : [ref], 'footprint' : footprint, 'precision' : precision})




if __name__ == '__main__':
    kicad_nets_file = sys.argv[1]
    try:
        if not os.path.isfile(kicad_nets_file):
            raise Exception(kicad_nets_file + ': file not found')

        nets = KiCadNets(kicad_nets_file=kicad_nets_file)
        nets.parse()
        total_pages = (nets.total_lines - PDF.FIRST_PAGE_LINES) // PDF.OTHER_PAGE_LINES + int((nets.total_lines - PDF.FIRST_PAGE_LINES) % PDF.OTHER_PAGE_LINES > 0) + 1
        pdf = PDF(
            document_title=nets.document_title,
            document_number=nets.document_number,
            document_character=nets.document_character,
            document_date=nets.document_date,
            company_code=nets.company_code,
            engineer_title=nets.engineer_title,
            checker_title=nets.checker_title,
            approver_title=nets.approver_title,
            output_file=kicad_nets_file.replace(".net", ".pdf"),
            total_pages=total_pages)
        # Sort keys by alphabet
        for key in sorted(nets.components.keys()):
            value = nets.components[key]
            if len(value['elements']):
                pdf.add_components_header(header=value['name'])
                for comp in value['elements']:
                    for ref in comp['refs']:
                        title = comp['value']
                        title += ', ' + comp['precision'] if comp['precision'] else ''
                        title += ', ' + comp['footprint']
                        pdf.add_component( ref[0], title, ref[1], "")

        pdf.save()
    except:
        pass

