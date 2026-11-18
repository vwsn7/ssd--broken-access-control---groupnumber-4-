# ssd--broken-access-control---groupnumber-4-
Broken Access Control 

Group Information

* Group Number: 4
* Group Members:
    * Wasan Al Sarmi – Student ID: [2316232]
    * Mariyah Al Zakwani – Student ID: [2316218]

Project Overview

Topic: Broken Access Control – Insecure Direct Object References (IDOR)

This project demonstrates a Broken Access Control vulnerability, specifically Insecure Direct Object References (IDOR).

The vulnerable application allows an authenticated user to access another user’s private document by modifying the document ID in the URL. The fixed version implements server-side authorization checks to verify document ownership before granting access.

Tools and Technologies

* Python
* Flask
* SQLite
* Burp Suite
* Visual Studio Code

Project Structure

* vulnerable-code/: Contains the application with the intentional IDOR vulnerability.
* fixed-code/: Contains the secured application with ownership verification.
* slides/: Contains the project presentation.
* demo-video/: Contains information about the backup demonstration video.
* tests/: Contains tests for verifying access control behavior.
* references.md: Contains the references used in this project.

Test Accounts

User	Email	Password	Document ID
Alice	alice@example.com	AliceDemo123!	1
Bob	bob@example.com	BobDemo123!	2

These are fictional accounts created exclusively for this local demonstration.

Installation

Make sure Python is installed.

1. Open the project folder in Visual Studio Code.
2. Open the integrated terminal.
3. Create a virtual environment:

py -m venv .venv

4. Activate it on Windows:

.venv\Scripts\activate

5. Install the required dependencies:

py -m pip install -r requirements.txt

Running the Vulnerable Application

Open a terminal and run:

cd vulnerable-code
py app.py

Open the application at:

http://127.0.0.1:5001

Log in as Alice and access her document. Then modify the document ID in the URL from 1 to 2.

Expected result: Alice can access Bob’s document because the vulnerable application does not verify document ownership.

Running the Fixed Application

Open a second terminal and run:

cd fixed-code
py app.py

Open:

http://127.0.0.1:5002

Repeat the same attack by changing the document ID from 1 to 2.

Expected result: The application denies access and returns a 404 response because Alice does not own Bob’s document.

Security Fix

The vulnerability is fixed by checking both the document ID and the authenticated user’s ID when retrieving a document.

The authorization condition ensures that users can only access documents they own.

Backup Demo Video

Backup demonstration video: [Insert Google Drive or YouTube link]

Disclaimer

This project is developed for educational and academic purposes only. The vulnerable application is intentionally insecure and must only be executed in a controlled local environment.
