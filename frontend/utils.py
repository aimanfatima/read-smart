# import convertapi
import sys
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams
import io
import requests
import json

def pdfparser(filename):
    fp = open(filename, 'rb')
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    # codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    # device = HTMLConverter(rsrcmgr, retstr, laparams=laparams)
    
    # Create a PDF interpreter object.
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    
    # Process each page contained in the document.
    # TO HANDLE DATA PAGE WISE
    text_page_wise = []
    page_no = 0
    for pageNumber, page in enumerate(PDFPage.get_pages(fp)):
        if pageNumber == page_no:
            interpreter.process_page(page)
            data = retstr.getvalue()
            retstr.truncate(0)
            retstr.seek(0)
            print("Page Number - ", pageNumber)
            # print(data)
            text_page_wise.append(data)

        page_no += 1
    return text_page_wise


def get_questions_page_wise(text_page_wise):
    questions_page_wise = []

    for page in text_page_wise:
        ## TO DO - separate paragraphs here and send data paragraph wise

        data = list(filter(lambda x : x != '', page.split('\n\n')))
        # print("Heyoooo Here")
        # print(data)
        ## ---------------------------------------------------------- ##
        for para in data:
            if len(para)>0:
                ques_response = requests.post('https://readex-major-project.herokuapp.com/get_fill_ups/', data={"text":para})
                json_response = json.loads(ques_response.text)
                if ques_response.status_code==200:
                    questions_page_wise.append(json_response)
    
    return questions_page_wise
    
def doc_to_pdf_converter(infile):
    # result = convertapi.convert('pdf', { 'File': infile })
    # result.file.save(outfile)
    print("File created")