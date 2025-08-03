import json

from pypdf import PdfReader
import re
INPUT_DIRECTORY = 'invoices'
OUTPUT_FILE = 'output.json'

def extract_text(pdf_path):
    reader = PdfReader(pdf_path)
    page = reader.pages[0]
    text = page.extract_text()
    return text

def text_invoice(text):
    invoice_data ={}
    invoice_number_found = re.search('(Invoice #: )', text)
    if invoice_number_found:
        invoice_data['invoice_number'] = invoice_number_found.group()

    invoice_date_found = re.search(r'Data: ', text)
    if invoice_date_found:
        invoice_data['invoice_date'] = invoice_date_found.group()

    invoice_amount = re.findall(r'[0-9]+\.[0-9]{2}', text)
    if invoice_amount:
        invoice_data['invoice_amount'] = [float(x) for x in invoice_amount]

    if "invoice_amount" in invoice_data and len(invoice_data['invoice_amount']) >= 2:
        subtotal = sum(invoice_data['invoice_amount'][:-1])
        total = invoice_data['invoice_amount'][-1]
        invoice_data['validated']=abs(total-subtotal) < 0.01
    else:
        invoice_data['validated'] = False
    return invoice_data

text_extras = extract_text('invoices/invoice_template_1.pdf')
date_finale = text_invoice(text_extras)
print(date_finale)

json_response = json.dumps(date_finale)
print(json_response)