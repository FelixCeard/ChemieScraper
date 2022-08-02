from docx import Document
from docx.shared import Inches

from Scrapper import ChemieScrapper


class ChemieDocumentCreator9000:

    def __init__(self, driver=None, delays=None, append:bool = False):

        self.scrapper = None

        if driver is not None:
            self.scrapper = ChemieScrapper(driver=driver, delays=delays)
        else:
            self.scrapper = ChemieScrapper(delays=delays)

        self.delays = None
        if delays is not None:
            self.delays = delays

        self.document_name = 'Sicherheitstabelle.docx'

        if append:
            self.document = Document(self.document_name)
        else:
            self.document = Document()
        self.table_header = ["Substanz", "Gefahrenpiktrogramm", "H-Sätze", "P-Sätze", "Entsorgung"]

        self.not_found_stoffe = []

        self.content = []

    def extract_table(self, zvg:str=None):

        hs, ps, sw, srcs, name, gefahr = self.scrapper.scrape(zvg)

        if len(hs) == 0 and len(ps) == 0 and len(srcs) == 0:
            sw = gefahr

        self.content.append([hs, ps, sw, srcs, name])



    def save(self, name=None):

        #######################################
                # TEXT BEFORE THE TABLE
        #######################################
        paragraph_before_table = self.document.add_paragraph()
        paragraph_before_table = paragraph_before_table.add_run()
        paragraph_before_table.add_text("")

        # create table
        table = self.document.add_table(rows=1, cols=5)
        for i in range(5):
            table.rows[0].cells[i].text = self.table_header[i]

        for hs, ps, sw, srcs, name in self.content:
            data = [
                [name, "", ", ".join(hs), ", ".join(ps), "(1)"]
            ]

            for su, ge, hs, ps, en in data:
                cells = table.add_row().cells
                cells[0].text = su
                cells[1].text = ge
                p = cells[1].add_paragraph()
                r = p.add_run()
                for alt in srcs:
                    r.add_picture(f'./images/{alt}.gif', width=Inches(0.472441))
                r.add_text("")
                r.add_text(sw)

                cells[2].text = hs
                cells[3].text = ps
                cells[4].text = en

        # add not found elements
        for name in self.not_found_stoffe:
            cells = table.add_row().cells
            cells[0].text = name
            cells[1].text = "Stoff wurde nicht in der GESTIS-Datenbank gefunden."

        #######################################
                # TEXT AFTER THE TABLE
        #######################################
        paragraph_after_table = self.document.add_paragraph()
        paragraph_after_table = paragraph_after_table.add_run()
        paragraph_after_table.add_text("")


        self.document.save(self.document_name)

if __name__ == '__main__':
    extractor = ChemieDocumentCreator9000()
    extractor.extract_table('008230')
    extractor.save()
