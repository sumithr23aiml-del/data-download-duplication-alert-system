# Data Download Duplication Alert System

A console-based Python application that detects duplicate file uploads using MD5 hashing and stores records in a MySQL database. It allows users to register, log in, upload files, and get alerts when a file with the same content has already been uploaded.

## Features

- User registration and login system  
- Upload files from local storage  
- Generate MD5 hash for each file  
- Detect and log duplicate files based on hash  
- Store users, original files, and duplicates in MySQL tables  
- Simple console menu for all operations

## Tech Stack

- Python  
- MySQL (with MySQL Workbench for management)  
- `mysql-connector-python`, `hashlib`, `os` (and optional `tkinter` for file dialog)

## How to Run

1. Clone this repository and open the project folder.  
2. Install dependencies:  


pip install mysql-connector-python


3. Create a MySQL database (for example, `duplication_system`) and update the connection details in the script.  
4. Run the Python script:  


## Future Improvements

- Replace MD5 with a stronger hash (e.g., SHA-256)  
- Add a graphical or web interface  
- Add role-based access and detailed reports
