#!/usr/bin/env python3

#
import os
import csv
import time
from types import NoneType

# 
import textract
import pandas as pd
from tabulate import tabulate
from PyPDF2 import PdfFileReader
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.validator import PathValidator
from InquirerPy.separator import Separator


__author__ = "Jason M. Pittman"
__copyright__ = "Copyright 2022, Jason M. Pittman"
__credits__ = ["Jason M. Pittman"]
__license__ = "GPLv3"
__version__ = "0.1.0"
__maintainer__ = "Jason M. Pittman"
__email__ = "jason.pittman@umgc.edu"
__status__ = "Development"

class PdfConvertor():
    def __init__(self):
        self.pdfs = os.listdir('pdfs')

    def convert_to_text(self):
        page = 0

        if len(self.pdfs) == 0:
            print('No PDF in directory')
        else:
            for pdf in self.pdfs:
                try:
                    pdf_text = textract.process(os.path.join('pdfs', pdf)).decode('utf-8')
                except Exception as e:
                    print(str(e))
                finally:
                    file_text = open(os.path.join('texts', pdf + '.txt'), 'a', encoding="utf-8")
                    file_text.writelines(str(pdf_text))
                    
                    file_text.close()
                


class PdfMetadata():
    def __init__(self):
        self.pdfs = os.listdir('pdfs')

    def get_metadata(self):
        if len(self.pdfs) == 0:
            print('No PDF in directory')

            return 0
        else:
            metadata = {}
            
            for pdf in self.pdfs:
                try:
                    pdf_object = PdfFileReader(os.path.join('pdfs', pdf))
                    info = pdf_object.metadata

                    metadata[pdf] = {}
                    metadata[pdf]['id'] = pdf 
                    metadata[pdf]['path'] = os.path.join('texts', pdf)
                    metadata[pdf]['source'] = os.path.join('pdfs', pdf)
                    metadata[pdf]['author'] = info.author
                    metadata[pdf]['title'] = info.title
                    metadata[pdf]['keywords'] = self.__get_keywords(info)
                    
                    # if we ever want to include the full text here is the statement
                    #metadata['text'] = open(os.path.join('text', pdf + '.txt'), encoding='utf-8').read()

                except Exception as e:
                    print(str(e))

            return metadata

    def __get_keywords(self, pdf_info):
        if '/Keywords' in pdf_info:
            return pdf_info['/Keywords']


    def get_abstract(self, pdf):
        pdf_text = open(os.path.join('texts', pdf + '.txt'), encoding='utf-8').read()

        abstract = pdf_text.split("ABSTRACT")[1].split("INTRODUCTION")[0]

        return abstract

class PdfAnalyzer():
    def __init__(self):
        self.pm = PdfMetadata()

    def get_page_count(self, pdf):
        with open(os.path.join('pdfs', pdf), 'rb') as pdf_object:
            pdf_file = PdfFileReader(pdf_object)
            page_count = pdf_file.numPages

        return page_count

    def get_pdf_keyword_frequency(self, keywords, text):
        keyword_frequency = {}

        with open(text + '.txt', 'r') as text_object:
            text_file = text_object.read().lower()

        if keywords is not None:
            words = keywords.split(',')
            
            for word in words:
                keyword_frequency[word] = text_file.count(word.lower())
        else:
            keyword_frequency = ''

        return keyword_frequency

    def serialize_to_csv(self):
        metadata = self.pm.get_metadata()
        stamp = time.time()

        if metadata != 0: 
            csv_header = ['id', 'authors', 'title', 'keywords', 'frequency']
            rows = []

            with open(os.path.join('data', 'pdf_metadata' + str(stamp) + '.csv'), 'w') as f:
                writer = csv.writer(f)
                writer.writerow(csv_header)

                for entry in metadata:

                    if metadata[entry]['keywords'] == '':
                        frequency = 0
                    else:
                        frequency = self.get_pdf_keyword_frequency(metadata[entry]['keywords'], metadata[entry]['path'])

                    row = [metadata[entry]['id'], metadata[entry]['author'], metadata[entry]['title'], metadata[entry]['keywords'], frequency]
                    rows.append(row)
                
                writer.writerows(rows)
        else:
            pass

class CsvDisplay():
    def __init__(self):
        self.csvs = os.listdir('data')

    def pad_col(self, col, max_width):
        return col.ljust(max_width)

    def display_csv(self):

        pd.set_option('max_colwidth', 1000)

        df = pd.read_csv(os.path.join('data', max(self.csvs)), usecols = ['id','frequency'])
        pd.options.display.max_columns = len(df.columns)
        
        print(tabulate(df, headers='keys', tablefmt='github'))

def loop():
    operation = inquirer.select(
        message="Select a bibliometric operation:",
        choices=[
            "Process PDF to Text",
            "Process Text to CSV",
            "Cleanup PDFs and Texts",
            "Display CSV",
            Choice(value="Exit", name="Exit")
        ],
        default=None,
    ).execute()

    if operation == "Process PDF to Text":
        print("Converting pdfs to text files...")
        convertor = PdfConvertor()
        convertor.convert_to_text()

    if operation == "Process Text to CSV":
        print("Converting to csv")
        processor = PdfAnalyzer()
        processor.serialize_to_csv()

    if operation == "Cleanup PDFs and Texts":
        print("Moving PDF and Text files to processed direectories")

        pdfs = os.listdir('pdfs')
        texts = os.listdir('texts')

        try:
            for pdf in pdfs:
                os.rename(os.path.join('pdfs', pdf), os.path.join('processed_pdfs', pdf))
            
            for text in texts:
                os.rename(os.path.join('texts', text), os.path.join('processed_texts', text))
        except Exception as e:
           print(str(e))

    if operation == "Display CSV":
        display = CsvDisplay()
        display.display_csv()

    if operation == "Exit":
        quit()

def main():
    loop()

    proceed = inquirer.confirm(message="Continue?", default=True).execute()
    if proceed:
        main()

if __name__ == "__main__":
    main()

