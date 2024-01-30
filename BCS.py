# libraries
import cv2
import pytesseract
import re
# import spacy
import pandas as pd
import os
import csv
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, send_file, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = "super secret key"

pytesseract.pytesseract.tesseract_cmd = r"C:\Users\pande\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
# nlp = spacy.load("en_core_web_sm")

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    csv_filename = 'CardScrape.csv'
    csv_contents = []
    if os.path.exists(csv_filename):
        with open(csv_filename, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file)
            csv_contents = list(csv_reader)
    return render_template('index.html', csv_contents=csv_contents)


@app.route('/upload', methods=['POST'])
def uploadImage():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        print("YOO")
        # Read the uploaded image using OpenCV
        image = cv2.imread(file_path)

        # Use pytesseract to extract text from the image
        extracted_text = pytesseract.image_to_string(image)

        data = testFunction(file_path)
        csv_filename = excel(data)

        # Save the extracted text into a CSV file
        #csv_filename = os.path.join(app.config['UPLOAD_FOLDER'], "CardScrape.csv")
        # with open(csv_filename, mode='w', newline='') as csv_file:
        #     writer = csv.writer(csv_file)
        #     writer.writerow(['Extracted Text'])
        #     writer.writerow([extracted_text])

        # Return the CSV file for download
        flash('Image scraped and data appended to CSV file successfully')
        return redirect(url_for('index'))
    else:
        flash('File not allowed')
        return redirect(request.url)

@app.route('/download')
def download_file():
    csv_filename = "CardScrape.csv"
    return send_file(csv_filename, as_attachment=True, download_name="CardScrape.csv")

def testFunction(imgPath):
    #imgPath = "./BloombergCard.jpeg"
    img = cv2.imread(imgPath)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if img is None:
        print(f"Error: failed to load {imgPath}")
    else:
        print("Image loaded successfully")
    data = image(gray_img)
    print(data)
    return data

def image(image):
    # take image and get text from it.
    # returns text
    text = pytesseract.image_to_string(image)
    return text

def scrapeNumber(number):
    phone_pattern = r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})'
    officeNum = re.findall(phone_pattern, number)
    Number = officeNum
    if len(Number) != 0:
        Number = " : ".join(Number)
    else:
        Number = "N/A"
    return Number

def scrapeEmailAddress(string):
    r = re.compile(r'[\w\.-]+@[\w\.-]+')
    data =  r.findall(string)
    EmailAddress = data
    if len(EmailAddress) != 0:
        EmailAddress = " ".join(EmailAddress)
    else:
        EmailAddress = "N/A"
    return EmailAddress

def scrapeCompanyName(word):
    # doc = nlp(word)
    # # Check if the word is recognized as an organization (company name) by spaCy
    # name = []
    # for ent in doc.ents:
    #     if ent.label_ == "ORG":
    #         name.append(ent)
    regex = r"\b[A-Z]\w+(?:\.com?)?(?:[ -]+(?:&[ -]+)?[A-Z]\w+(?:\.com?)?){0,2}[,\s]+(?i:ltd|llc|inc|plc|co(?:rp)?|group|holding|gmbh)\b"

    name = re.findall(regex, word)
    CompanyName = name
    if len(CompanyName) != 0:
        #CompanyName = [(name.text.split(' ', 1) if len(name.text.split(' ', 1)) > 1 else "") for name in CompanyName]
        CompanyName = " ".join(CompanyName)
    else:
        CompanyName = "N/A"
    return CompanyName

def scrapeCompanyUrl(URl):
    url_pattern = r"\b((?:https?://)?(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b"

    # Find all matches in the text
    matches = re.findall(url_pattern, URl)

    # Return the first match (you may need to adjust based on your specific case)

    if len(matches) == 0:
        CompanyUrl = "N/A"
    else:
        CompanyUrl = matches[0]
    return CompanyUrl

def scrapeRecruiterName(word):
    # doc = nlp(word)
    # # Check if the word is recognized as a PERSON (name) by spaCy
    # name = []
    # for ent in doc.ents:
    #     if ent.label_ == "PERSON":
    #         name.append(ent)
    # return name
    pattern = "([A-Z][a-z]+\s[A-Z][a-z]+)"
    name = re.findall(pattern,word)
    if len(name) == 0:
        name = "N/A"
    else:
        name = name
    return name

def scrapePhysicalAddress(address):
    regex = re.compile(r'[A-Za-z]{2,25} [A-Za-z]{2,25}')
    location = re.findall(regex, address)
    PhysicalAddress = location
    if len(PhysicalAddress) != 0:
        PhysicalAddress = " ".join(PhysicalAddress)
        PhysicalAddress = PhysicalAddress.replace('\n', '')
        PhysicalAddress = PhysicalAddress.replace(',', ' ')
    else:
        PhysicalAddress = "N/A"
    return PhysicalAddress

def excel(data):
    CompanyName = scrapeCompanyName(data)
    RecruiterName = scrapeRecruiterName(data)
    FirstName = ""
    LastName = ""
    # split_recruiter_names = [
    #     (name.text.split(' ', 1)[0], name.text.split(' ', 1)[1].strip() if len(name.text.split(' ', 1)) > 1 else "") for
    #     name in RecruiterName]
    # if len(split_recruiter_names[0][0]) != 0 and len(split_recruiter_names[0][1]) != 0:
    #     LastName = split_recruiter_names[0][1]
    #     FirstName = split_recruiter_names[0][0]
    # elif len(split_recruiter_names[0][0]) == 0:
    #     FirstName = "N/A"
    #     LastName = "N/A"
    # elif len(split_recruiter_names[0][0]) != 0 and len(split_recruiter_names[0][1]) == 0:
    #     LastName = "N/A"
    #     FirstName = split_recruiter_names[0][0]
    if len(RecruiterName) == 0:
        RecruitersName = "N/A"
        LastName = "N/A"
    elif len(RecruiterName) == 1:
        RecruitersName = RecruiterName[0]
        LastName = "N/A"
    else:
        RecruitersName = RecruiterName[0]
        #LastName = RecruiterName[1]
    CompanyUrl = scrapeCompanyUrl(data)
    PhysicalAddress = scrapePhysicalAddress(data)
    Number = scrapeNumber(data)
    EmailAddress = scrapeEmailAddress(data)
    input = [CompanyName, RecruitersName, CompanyUrl, PhysicalAddress, Number, EmailAddress]
    csv_file = 'CardScrape.csv'
    HeaderVal = True
    if os.path.exists(csv_file) and os.path.getsize(csv_file) > 0:
        HeaderVal = False
    else:
        HeaderVal = True
    with open(csv_file, 'a', newline='') as file:
        df = pd.DataFrame([input],
                          columns=['CompanyName', 'RecruiterName', 'CompanyUrl', 'PhysicalAddress', 'Number',
                                   'EmailAddress'])
        df.to_csv(file, mode='a', index=False, header=HeaderVal)
    return csv_file

# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     app.run(debug=True)
