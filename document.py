from docx import Document
from docx.shared import Inches
from Scrapper import ChemieScrapper
from name_scraper import CASsearcher


class ChemieDocumentCreator9000:

    def __init__(self, driver=None, append:bool = False):

        self.scrapper = None

        if driver is not None:
            self.scrapper = ChemieScrapper(driver=driver)
        else:
            self.scrapper = ChemieScrapper()

        self.document_name = 'Sicherheitstabelle.docx'

        if append:
            self.document = Document(self.document_name)
        else:
            self.document = Document()
        self.table_header = ["Substanz", "Gefahrenpiktrogramm", "H-Sätze", "P-Sätze", "Entsorgung"]

        self.content = []

    def extract_table(self, zvg:str=None):

        hs, ps, sw, srcs, name = self.scrapper.scrape(zvg)
        self.content.append([hs, ps, sw, srcs, name])



    def save(self, name=None):

        # create table
        table = self.document.add_table(rows=len(self.content)+1, cols=5)
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
                r.add_text(sw)

                cells[2].text = hs
                cells[3].text = ps
                cells[4].text = en


        self.document.save(self.document_name)

if __name__ == '__main__':
    extractor = ChemieDocumentCreator9000()
    extractor.extract_table('008230')
    extractor.save()