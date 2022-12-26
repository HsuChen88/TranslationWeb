from PyPDF2 import PdfReader

def recognize_pdf(pdf_path):
    print("Start Scanning Pdf")
    reader = PdfReader(pdf_path)
    s = ""
    page_num = len(reader.pages)
    for i in range(page_num):
        page = reader.pages[i]
        s += page.extract_text()
    print("End Scanning Pdf")
    return s


# # extract only text oriented up
# print(page.extract_text(0))

# # extract text oriented up and turned left
# print(page.extract_text((0, 90)))