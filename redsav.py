'''from docx import Document
from fpdf import FPDF
import random

def generate_random_paragraphs(num_paragraphs=3):
    # Replace with your desired random paragraph generator
    sample_paragraphs = [
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque interdum, urna vel fringilla hendrerit, est metus egestas nunc, in commodo elit lorem sed arcu.",
        "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Pellentesque sit amet consectetur quam. Integer scelerisque risus id nisi aliquet, a suscipit mi congue.",
        "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Nulla facilisi. Aenean posuere lacus id volutpat accumsan.",
        "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Curabitur cursus nibh sit amet justo ultrices, ac pretium tortor efficitur.",
        "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Phasellus imperdiet velit eu arcu vehicula, ac dapibus justo tincidunt.",
        "Vivamus nec ante ut orci dignissim consequat. Fusce eget libero eget nisi fermentum luctus a in metus. Proin dapibus ex vitae convallis posuere.",
        "Maecenas eget risus sed felis consequat gravida. Etiam vel lorem vitae risus posuere dictum. In hac habitasse platea dictumst.",
        "Praesent vehicula, nisl eget suscipit convallis, ligula felis pharetra lorem, ac varius sapien ligula ut lectus. Ut auctor quam sit amet odio vehicula posuere.",
        "Aliquam erat volutpat. Nam id urna vel nulla facilisis lacinia. Cras a semper lacus, nec suscipit sem.",
        "Morbi quis odio tincidunt, accumsan metus sed, suscipit erat. Integer posuere, lorem non condimentum tincidunt, nulla felis luctus nulla, vitae tempor libero velit sed erat."
    ]
    return "\n\n".join(random.choices(sample_paragraphs, k=num_paragraphs))



def write_to_txt(content, file_path):
    with open(file_path, 'w') as file:
        file.write(content)

def write_to_docx(content, file_path):
    doc = Document()
    for paragraph in content.split('\n\n'):
        doc.add_paragraph(paragraph)
    doc.save(file_path)

def write_to_pdf(content, file_path):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for paragraph in content.split('\n\n'):
        pdf.multi_cell(0, 10, paragraph)
        pdf.ln(10)
    pdf.output(file_path)


output_txt = "output.txt"
output_docx = "output.docx"
output_pdf = "output.pdf"

new_content = generate_random_paragraphs()
write_to_pdf(new_content, output_pdf)

print(f"Files saved: {output_txt}, {output_docx}, {output_pdf}")'''

import requests

# Fetch location data
response = requests.get("https://ipinfo.io")
data = response.json()

# Parse the location
if 'loc' in data:
    latitude, longitude = data['loc'].split(',')
    print("Latitude:", latitude)
    print("Longitude:", longitude)
else:
    print("Unable to determine location.")