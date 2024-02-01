# BusinessCardOCR
Scenario:
On Campus Recruiting Event
-  Student: "I had a great time getting to know more about the work you do at WhiteStone Corporation."
-  Recruiter: "Yea, here take my business card and send me your resume."
-  Student: "alright, Thank you."
-  Student takes business card and puts it in their pocket along with the 50 other cards they received that night.

2 months later.
- Student: "Hey, where did that business card go for that one recruiter. If only I had a way of saving that information somewhere."
# The Problem
  This is a problem I, as a college student, have had to go through. You go to an event meet recruiters and put their card in your pocket. Eventually you end up losing the card because you forgot to transfer it somewhere safe. the simple solution would be to just take a picture of it, but what if you take that one step further. my proposed solution is to have an app or webpage that allows you to take a picture of a business card, scrape the data and add that data to an excel/google sheet to keep for your own record.
# The Solution(s)
In order to make this idea a reality, i need to think of the tools I am going to use. Firstly we need a way to work with images, then we need a way to scrap the data, we need to be able to take the data and put it in the correct category on a sheet. we also need a user interface to make this accessible.
# Brainstorm
![image](https://github.com/PeterGQ/BusinessCardOCR/assets/93812183/584d02d4-c1c2-428a-b6ff-36011979669c)


# Trial and Error

problem: i am trying to extract the text from the image using pytesseract but i run into an error, "pytesseract.pytesseract.TesseractNotFoundError: tesseract is not installed or it's not in your PATH. See README file for more information."
solution: i had to download the tesseract OCR and specify the path to it

Web Devlopment
I had so many issues trying to deploy my flask app to the web. My goal was to manage to do this for free so that severly limited my options.
At first I attempted to use pythonanywhere which was recommended on a forum online. Everything went well up until i had install the dependencies in the pythonanywhere console. Apparently i didnt have enough space on the free account so i could not use it. 
The next thing i tried was putting my project on render. This was another recommendation which I found on reddit. The process was generally straighforward because i had used the software previously with a streamlit application. However, for some reason the routes on flask app seemed to always throw an error. secondly, i could not use the pytesseract because of the specific need for a path specification to the Tesseract-OCR. I solved the second error by switching to easyOCR but even then

# The Results

