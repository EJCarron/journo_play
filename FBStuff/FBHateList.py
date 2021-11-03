from PyPDF2 import PdfFileReader

print("FACEBOOK’S SECRET BLACKLIST OF “DANGEROUS INDIVIDUALS AND ORGANIZATIONS ".lower())

pdf_path = '/Users/edcarron/DataSets/FacebookStuff/facebook-dangerous-individuals-and-organizations-list-reproduced-snapshot.pdf'

pages_text = []

with open(pdf_path, 'rb') as f:
    pdf = PdfFileReader(f)
    info = pdf.getDocumentInfo()
    number_of_pages = pdf.getNumPages()
    for i in range(pdf.numPages):

        page = pdf.getPage(i)

        page






pdf
