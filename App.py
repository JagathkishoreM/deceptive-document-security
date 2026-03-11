from flask import Flask, render_template, flash, request, session, send_file, jsonify
from flask import render_template, redirect, url_for, request
import mysql.connector
from ecies.utils import generate_key
from ecies import encrypt, decrypt
import base64, os, sys

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

app = Flask(__name__)
app.config['DEBUG']
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


@app.route("/")
def homepage():
    return render_template('index.html')


@app.route("/ServerLogin")
def ServerLogin():
    return render_template('ServerLogin.html')


@app.route('/NewUser')
def NewUser():
    return render_template('NewUser.html')


@app.route('/UserLogin')
def UserLogin():
    return render_template('UserLogin.html')


@app.route("/serverlogin", methods=['GET', 'POST'])
def serverlogin():
    if request.method == 'POST':
        if request.form['uname'] == 'server' and request.form['password'] == 'server':

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1fakedocclouddb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb where status='waiting'")
            data = cur.fetchall()

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1fakedocclouddb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb where status='Active'")
            data1 = cur.fetchall()
            return render_template('ServerHome.html', data=data, data1=data1)

        else:
            flash('Username or Password is wrong')
            return render_template('ServerLogin.html')


@app.route("/ServerHome")
def ServerHome():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1fakedocclouddb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb where status='waiting'")
    data = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1fakedocclouddb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb where status !='waiting'")
    data1 = cur.fetchall()

    return render_template('ServerHome.html', data=data, data1=data1)


def randStrr(chars=string.ascii_uppercase + string.digits, N=10):
    return ''.join(random.choice(chars) for _ in range(N))


@app.route("/Approved")
def Approved():
    id = request.args.get('lid')
    email = request.args.get('email')
    loginkey = randStrr(chars='abcdefghijklmnopqrstuvwxyz0123456789')

    message = "Your Login Key : " + str(loginkey)

    sendmail(email, message)

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1fakedocclouddb')
    cursor = conn.cursor()
    cursor.execute("Update regtb set Status='Active',LoginKey='" + str(loginkey) + "' where id='" + id + "' ")
    conn.commit()
    conn.close()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1fakedocclouddb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb where status='waiting'")
    data = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1fakedocclouddb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb where status !='waiting'")
    data1 = cur.fetchall()

    return render_template('ServerHome.html', data=data, data1=data1)


@app.route("/Reject")
def Reject():
    id = request.args.get('lid')
    email = request.args.get('email')

    message = "Your Request Was Rejected"

    sendmail(email, message)

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1fakedocclouddb')
    cursor = conn.cursor()
    cursor.execute("Update regtb set Status='reject' where id='" + id + "' ")
    conn.commit()
    conn.close()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1fakedocclouddb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb where status='waiting'")
    data = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1fakedocclouddb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb where status !='waiting'")
    data1 = cur.fetchall()

    return render_template('ServerHome.html', data=data, data1=data1)


@app.route("/SFileInfo")
def SFileInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1fakedocclouddb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM filetb ")
    data = cur.fetchall()
    return render_template('SFileInfo.html', data=data)


@app.route("/newuser", methods=['GET', 'POST'])
def newuser():
    if request.method == 'POST':
        uname = request.form['uname']
        mobile = request.form['mobile']
        email = request.form['email']
        address = request.form['address']
        username = request.form['username']
        password = request.form['password']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1fakedocclouddb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from regtb where username='" + username + "'  ")
        data = cursor.fetchone()
        if data is None:
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1fakedocclouddb')
            cursor = conn.cursor()
            query = """ INSERT INTO regtb (name, mobile, email, address, username, password, status) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            values = (uname, mobile, email, address, username, password, 'waiting')
            cursor.execute(query, values)
            conn.commit()
            conn.close()

            flash('Record Saved!')
            return render_template('NewUser.html')
        else:
            flash('Already Register This  UserName!')
            return render_template('NewUser.html')


@app.route("/userlogin", methods=['GET', 'POST'])
def userlogin():
    if request.method == 'POST':

        username = request.form['uname']
        password = request.form['password']
        loginkey = request.form['loginkey']
        session['uname'] = request.form['uname']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1fakedocclouddb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from regtb where username='" + username + "' and Password='" + password + "' ")
        data = cursor.fetchone()
        if data is None:

            #flash('Username or Password is wrong')
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1fakedocclouddb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM filetb")
            data1 = cur.fetchall()

            return render_template('UserHome1.html',data=data1)

        else:

            Status = data[7]
            lkey = data[8]
            session['email'] = data[3]

            if Status == "waiting":

                flash('Waiting For Server Approved!')
                return render_template('UserLogin.html')

            else:

                if lkey == loginkey:

                    conn = mysql.connector.connect(user='root', password='', host='localhost',
                                                   database='1fakedocclouddb')
                    cur = conn.cursor()
                    cur.execute("SELECT * FROM regtb where username='" + session['uname'] + "'")
                    data1 = cur.fetchall()
                    flash('Login Successfully')
                    return render_template('UserHome.html', data=data1)

                else:
                    flash('Login Key Incorrect')
                    return render_template('UserLogin.html')


@app.route("/UserHome")
def UserHome():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1fakedocclouddb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb where UserName='" + session['uname'] + "'")
    data = cur.fetchall()
    return render_template('UserHome.html', data=data)


@app.route("/UserFileUpload")
def UserFileUpload():
    return render_template('UserFileUpload.html', uname=session['uname'])


import hmac
import hashlib
import binascii


def create_sha256_signature(key, message):
    byte_key = binascii.unhexlify(key)
    message = message.encode()
    return hmac.new(byte_key, message, hashlib.sha256).hexdigest().upper()


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


from docx import Document
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


# Main function to handle both file types
def process_file(file_path, fname):
    # Determine file type and read accordingly
    if file_path.endswith('.docx'):
        text = read_docx(file_path)
        output_pdf = "./static/dupload/" + fname
        new_content = generate_random_paragraphs()
        write_to_docx(new_content, output_pdf)

    elif file_path.endswith('.pdf'):
        text = read_pdf(file_path)
        output_pdf = "./static/dupload/" + fname
        new_content = generate_random_paragraphs()
        write_to_pdf(new_content, output_pdf)
    elif file_path.endswith('.txt'):
        text = read_text_file(file_path)

        output_pdf = "./static/dupload/" + fname
        new_content = generate_random_paragraphs()
        write_to_txt(new_content, output_pdf)
    else:
        raise ValueError("Unsupported file format. Only .docx ,.txt and .pdf are supported.")
        # flash("Unsupported file format. Only .docx ,.txt and .pdf are supported.")
        # return render_template('UserFileUpload.html', uname=session['uname'])

    # Compute term frequency
    tf = compute_term_frequency(text)
    return tf


@app.route("/ufileupload", methods=['GET', 'POST'])
def ufileupload():
    if request.method == 'POST':
        uname = session['uname']
        info = request.form['info']
        file = request.files['file']
        import random
        # fnew = random.randint(111, 999)
        savename = file.filename

        file.save("static/upload/" + savename)

        secp_k = generate_key()
        privhex = secp_k.to_hex()
        pubhex = secp_k.public_key.format(True).hex()

        filepath = "./static/upload/" + savename
        head, tail = os.path.split(filepath)

        # file_path = '333.pdf'  # or 'path_to_your_file.pdf'
        tf = process_file(filepath, savename)
        keywo = ''
        mailkey = ''
        for word, frequency in tf:
            print(f"Word: {word}, Frequency: {frequency}")
            if keywo == '':
                keywo = word 
            else:
                keywo = keywo + "," + word 
            if mailkey == "":
                mailkey = word + " - " + str(frequency) + "(Frequency)"
            else:
                mailkey = mailkey + "\n" + "\b" + word + " - " + str(frequency) + "(Frequency)"

        print(keywo)
        print(mailkey)
        print("Term Frequency:", tf)

        newfilepath1 = './static/Encrypt/' + str(tail)
        newfilepath2 = './static/Decrypt/' + str(tail)

        data = 0
        with open(filepath, "rb") as File:
            data = base64.b64encode(File.read())  # convert binary to string data to read file

        print("Private_key:", privhex, "\nPublic_key:", pubhex, "Type: ", type(privhex))

        if privhex == 'null':
            flash('Please Choose Another File,file corrupted!')
            return render_template('OwnerFileUpload.html')

        else:
            print("Binary of the file:", data)
            encrypted_secp = encrypt(pubhex, data)
            print("Encrypted binary:", encrypted_secp)

            with open(newfilepath1, "wb") as EFile:
                EFile.write(base64.b64encode(encrypted_secp))

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1fakedocclouddb')
            cursor = conn.cursor()
            cursor.execute("SELECT  *  FROM filetb ")
            data2 = cursor.fetchone()

            if data2:

                conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='1fakedocclouddb')
                cursor1 = conn1.cursor()
                cursor1.execute("select max(id) from filetb")
                da = cursor1.fetchone()
                if da:
                    d = da[0]
                    print(d)

                conn = mysql.connector.connect(user='root', password='', host='localhost', database='1fakedocclouddb')
                cursor = conn.cursor()
                cursor.execute("SELECT  *  FROM filetb where  id ='" + str(d) + "'   ")
                data1 = cursor.fetchone()
                if data1:
                    hash1 = data1[8]
                    num1 = random.randrange(1111, 9999)
                    hash2 = create_sha256_signature("E49756B4C8FAB4E48222A3E7F3B97CC3", str(num1))

                    conn = mysql.connector.connect(user='root', password='', host='localhost',
                                                   database='1fakedocclouddb')
                    cursor = conn.cursor()
                    query = """ INSERT INTO filetb (username, FileInfo, FileName, keyword, publicKey, privateKey, hash1, hash2)VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
                    values = (uname, info, savename, keywo, pubhex, privhex, hash1, hash2)
                    cursor.execute(query, values)

                    conn.commit()
                    conn.close()
                    flash('File Upload And Encrypt Successfully ')

                    conn1 = mysql.connector.connect(user='root', password='', host='localhost',
                                                    database='1fakedocclouddb')
                    cursor1 = conn1.cursor()
                    cursor1.execute("select max(id) from filetb")
                    da = cursor1.fetchone()
                    if da:
                        d = da[0]

                    mcon = "FileID : " + str(d) + "\nFileName : " + savename + "\n" + "Keywords :\n " + mailkey

                    sendmail(session['email'], mcon)
                    return render_template('UserFileUpload.html', pkey=privhex, uname=uname, tf=tf)

            else:

                hash1 = '0'
                num1 = random.randrange(1111, 9999)
                hash2 = create_sha256_signature("E49756B4C8FAB4E48222A3E7F3B97CC3", str(num1))
                conn = mysql.connector.connect(user='root', password='', host='localhost', database='1fakedocclouddb')
                cursor = conn.cursor()
                query = """ INSERT INTO filetb (username, FileInfo, FileName, keyword, publicKey, privateKey, hash1, hash2)VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
                values = (uname, info, savename, keywo, pubhex, privhex, hash1, hash2)
                cursor.execute(query, values)
                conn.commit()
                conn.close()
                flash('File Upload And Encrypt Successfully ')

                conn1 = mysql.connector.connect(user='root', password='', host='localhost',
                                                database='1fakedocclouddb')
                cursor1 = conn1.cursor()
                cursor1.execute("select max(id) from filetb")
                da = cursor1.fetchone()
                if da:
                    d = da[0]

                mcon = "FileID : " + str(d) + "\nFileName : " + savename + "\n" + "Keywords :\n " + mailkey

                sendmail(session['email'], mcon)
                return render_template('UserFileUpload.html', pkey=privhex, uname=uname, tf=tf)


@app.route('/UFileInfo')
def UFileInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1fakedocclouddb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM filetb where username='" + session['uname'] + "'")
    data1 = cur.fetchall()
    return render_template('UFileInfo.html', data=data1)


@app.route('/USearch')
def USearch():
    return render_template('USearch.html')


@app.route("/search", methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        fname = request.form['uname']
        uname = session['uname']
        conn = mysql.connector.connect(user='root', password='', host='localhost',
                                       database='1fakedocclouddb')
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM filetb where keyword like '%" + fname + "%' and UserName='" + uname + "'")
        data1 = cur.fetchall()
        return render_template('USearch.html', data=data1)


@app.route("/search1", methods=['GET', 'POST'])
def search1():
    if request.method == 'POST':
        fname = request.form['uname']
        conn = mysql.connector.connect(user='root', password='', host='localhost',
                                       database='1fakedocclouddb')
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM filetb where (FileName like '%" + fname + "%' or FileInfo like '%" + fname + "%') ")
        data1 = cur.fetchall()
        return render_template('UserHome1.html', data=data1)


@app.route("/Download1")
def Download1():
    lid = request.args.get('lid')

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1fakedocclouddb')
    cursor = conn.cursor()
    cursor.execute("SELECT  *  FROM  filetb where  id='" + str(lid) + "'")
    data = cursor.fetchone()
    if data:
        fname = data[3]
        uname = data[1]

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1fakedocclouddb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from regtb where username='" + uname + "'  ")
        data1 = cursor.fetchone()
        if data1:
            sendmail(data1[3], "Unknown User Access Your File..!")

        newfilepath1 = './static/dupload/' + str(fname)

        return send_file(newfilepath1, as_attachment=True)

@app.route("/Download")
def Download():
    lid = request.args.get('lid')

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1fakedocclouddb')
    cursor = conn.cursor()
    cursor.execute("SELECT  *  FROM  filetb where  id='" + str(lid) + "'")
    data = cursor.fetchone()
    if data:
        fname = data[3]
        privhex = data[6]
        #newfilepath1 = './static/upload/' + str(fname)

        filepath = "./static/Encrypt/" + fname
        head, tail = os.path.split(filepath)

        newfilepath1 = './static/Encrypt/' + str(tail)
        newfilepath2 = './static/Decrypt/' + str(tail)

        data = 0
        with open(newfilepath1, "rb") as File:
            data = base64.b64decode(File.read())

        print(data)
        decrypted_secp = decrypt(privhex, data)
        print("\nDecrypted:", decrypted_secp)
        with open(newfilepath2, "wb") as DFile:
            DFile.write(base64.b64decode(decrypted_secp))

        return send_file(newfilepath2, as_attachment=True)



        #return send_file(newfilepath1, as_attachment=True)


def sendmail(Mailid, message):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders

    fromaddr = "projectalertmail@gmail.com"
    toaddr = Mailid

    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = fromaddr

    # storing the receivers email address
    msg['To'] = toaddr

    # storing the subject
    msg['Subject'] = "Alert"

    # string to store the body of the mail
    body = message

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login(fromaddr, "humo kckd hlyr llct")

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(fromaddr, toaddr, text)

    # terminating the session
    s.quit()


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
