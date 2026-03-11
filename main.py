# Import necessary libraries
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import string
import docx  # for reading .docx files
import fitz  # PyMuPDF, for reading .pdf files

# Ensure necessary NLTK packages are downloaded
nltk.download('punkt')
nltk.download('stopwords')


# Function to read text from .docx files
def read_docx(file_path):
    doc = docx.Document(file_path)
    text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
    return text


# Function to read text from .pdf files
def read_pdf(file_path):
    text = ""
    with fitz.open(file_path) as pdf:
        for page_num in range(pdf.page_count):
            page = pdf[page_num]
            text += page.get_text()
    return text


# Function to compute term frequency
def compute_term_frequency(text):
    # Tokenize the text into words
    words = word_tokenize(text)

    # Convert words to lowercase and remove punctuation and stopwords
    stop_words = set(stopwords.words('english'))
    words = [word.lower() for word in words if word.isalpha() and word.lower() not in stop_words]

    # Calculate term frequency (TF)
    term_frequency = Counter(words)
    top_terms = term_frequency.most_common(5)

    return top_terms


def read_text_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:  # specify UTF-8 encoding
            text = file.read()
    except UnicodeDecodeError:
        # Fallback if UTF-8 fails, using a more flexible encoding
        with open(file_path, 'r', encoding='ISO-8859-1') as file:
            text = file.read()
    return text
# Main function to handle both file types
def process_file(file_path):
    # Determine file type and read accordingly
    if file_path.endswith('.docx'):
        text = read_docx(file_path)
    elif file_path.endswith('.pdf'):
        text = read_pdf(file_path)
    elif file_path.endswith('.txt'):
        text = read_text_file(file_path)
    else:
        raise ValueError("Unsupported file format. Only .docx ,.txt and .pdf are supported.")

    # Compute term frequency
    tf = compute_term_frequency(text)
    return tf


# Usage example
file_path = '333.pdf'  # or 'path_to_your_file.pdf'
tf = process_file(file_path)
keywo = ''
mailkey = ''
for word, frequency in tf:
    print(f"Word: {word}, Frequency: {frequency}")
    if keywo=='':
        keywo = word
    else:
        keywo = keywo + " "+ word

    if mailkey =="":
        mailkey = word + " " +  str(frequency)
    else:
        mailkey = mailkey + " " + word + " " + str(frequency)


print(keywo)
print(mailkey)
print("Term Frequency:", tf)



'''from ecies.utils import generate_key
from ecies import encrypt, decrypt
import  os
import base64, os
secp_k = generate_key()
privhex = secp_k.to_hex()
pubhex = secp_k.public_key.format(True).hex()
savename ='cta-bg.jpg'
filepath = "./static/Upload/" + savename
head, tail = os.path.split(filepath)

newfilepath1 = './static/Encrypt/' + str(tail)
newfilepath2 = './static/Decrypt/' + str(tail)

data = 0
with open(filepath, "rb") as File:
    data = base64.b64encode(File.read())  # convert binary to string data to read file

print("Private_key:", privhex, "\nPublic_key:", pubhex, "Type: ", type(privhex))


print("Binary of the file:", data)
encrypted_secp = encrypt(pubhex, data)
print("Encrypted binary:", encrypted_secp)

with open(newfilepath1, "wb") as EFile:
    EFile.write(base64.b64encode(encrypted_secp))'''