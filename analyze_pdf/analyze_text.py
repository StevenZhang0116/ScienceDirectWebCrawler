import io
import glob
import os
import json

from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams

def extract_text_by_page(pdf_path):
    with open(pdf_path, "rb") as fh:
        for page in PDFPage.get_pages(fh, caching = True, check_extractable = True):
            resource_manager = PDFResourceManager()
            fake_file_handle = io.StringIO()
            laparams = LAParams()
            converter = TextConverter(resource_manager, fake_file_handle, laparams = laparams)
            page_interpreter = PDFPageInterpreter(resource_manager, converter)
            page_interpreter.process_page(page)

            text = fake_file_handle.getvalue()
            yield text

            converter.close()
            fake_file_handle.close()

def extract_text(pdf_path):
    for page in extract_text_by_page(pdf_path):
        print(page)
        print()

def export_as_json(pdf_path, json_path):
    filename = os.path.splitext(os.path.basename(pdf_path))[0]
    data = {"Filename": filename}
    data["Pages"] = []

    counter = 1
    for page in extract_text_by_page(pdf_path):
        lst = ["\u000f", "\u00a9", "\u00ae", "\n", "\f", "- ", "\u00df", "\u00a7", "\u2217"]
        for i in lst:
            page = page.replace(i, " ")

        page = page.replace("\ufb01", "fi")
        page = page.replace("\u0014", "<=")
        page = page.replace("\u0015", ">=")
        page = page.replace("\u2265", "≥")
        page = page.replace("\u00bc", "=")
        page = page.replace("\ufb02", "fl")
        page = page.replace("\u201c", "'")
        page = page.replace("\u201d", "'")
        page = page.replace("\u00b1", "+-")
        page = page.replace("\u2019", "'")
        page = page.replace("\u0000", "-")
        page = page.replace("\u2013", "-")
        page = page.replace("\u2018", "'")
        page = page.replace("\u00fe", "+")
        page = page.replace("\u00f6", "o")
        page = page.replace("\u00e4", "a")
        page = page.replace("\u00d7", "x")
        page = page.replace("\u00b4", "x")
        page = page.replace("\u2014", "——")

        page = {"page_{}".format(counter):page}
        data["Pages"].append(page)
        counter +=1

    with open(json_path, "w") as fh:
        json.dump(data,fh)




if __name__ == "__main__":
    path = "./allPDF"
    pdfs = os.listdir(path)

    os.makedirs("./jsons")
    for i in range(len(pdfs)):
        if pdfs[i] != ".DS_Store":
            pdfName = pdfs[i][0:-4]
            pdfPath = "./allPDF/" + pdfs[i]
            print(pdfName)
            json_path = "./jsons/" + pdfName + ".json"
            try: 
                export_as_json(pdfPath, json_path)  
            except TypeError:
                print("##########################")














