import mysql.connector
import hashlib
import os

# -------------------------
# DATABASE CONNECTION
# -------------------------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Sumith@123",
    database="duplication_system"
)
cursor = db.cursor()

# -------------------------
# CREATE TABLES IF NOT EXISTS
# -------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100),
    password VARCHAR(100)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS files (
    id INT AUTO_INCREMENT PRIMARY KEY,
    filename VARCHAR(255),
    filehash VARCHAR(255),
    uploaded_by VARCHAR(100)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS duplicate_files (
    id INT AUTO_INCREMENT PRIMARY KEY,
    filename VARCHAR(255),
    filehash VARCHAR(255),
    original_file VARCHAR(255),
    uploaded_by VARCHAR(100)
)
""")

db.commit()

# -------------------------
#  USER REGISTRATION
# -------------------------
def register():
    username = input("Enter new username: ")
    password = input("Enter new password: ")

    query = "INSERT INTO users (username, password) VALUES (%s, %s)"
    cursor.execute(query, (username, password))
    db.commit()

    print("\nUser registered successfully!\n")

# -------------------------
#  USER LOGIN
# -------------------------
def login():
    username = input("Enter username: ")
    password = input("Enter password: ")

    query = "SELECT * FROM users WHERE username=%s AND password=%s"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()

    if result:
        print("\nLogin Successful! Welcome", username)
        return username
    else:
        print("\nInvalid username or password!")
        return None

# -------------------------
#  FILE HASHING FUNCTION
# -------------------------
def generate_hash(filepath):
    hasher = hashlib.md5()
    with open(filepath, "rb") as file:
        buffer = file.read()
        hasher.update(buffer)
    return hasher.hexdigest()

# -------------------------
#  FILE UPLOAD + DUPLICATE CHECK
# -------------------------
def upload_file(username):
    filepath = input("Enter full file path: ").strip()  # Remove whitespace
    
    # Debug: Show what was entered
    print(f"DEBUG: Looking for file at: {filepath}")
    print(f"DEBUG: Current working directory: {os.getcwd()}")
    
    # Try with raw string to handle backslashes properly
    if not os.path.exists(filepath):
        # Try alternative path formats
        filepath_alt = filepath.replace('\\', '/')
        if os.path.exists(filepath_alt):
            filepath = filepath_alt
        else:
            print(f"File not found at: {filepath}")
            print("Please check:")
            print("1. File exists at that location")
            print("2. Path is copied correctly with no extra spaces")
            print("3. Include file extension (e.g., .wav, .txt)")
            return
    
    filename = os.path.basename(filepath)
    
    # Show that file was found
    print(f"File found: {filename}")
    
    filehash = generate_hash(filepath)
    
    # Check for duplicates
    cursor.execute("SELECT filename FROM files WHERE filehash=%s", (filehash,))
    duplicate = cursor.fetchone()
    
    if duplicate:
        print("\n⚠ DUPLICATE FILE DETECTED! ⚠")
        print("Already uploaded as:", duplicate[0])
        
        # Store in duplicate table
        query = """
        INSERT INTO duplicate_files (filename, filehash, original_file, uploaded_by)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (filename, filehash, duplicate[0], username))
        db.commit()
    
    else:
        # Store in main table
        query = "INSERT INTO files (filename, filehash, uploaded_by) VALUES (%s, %s, %s)"
        cursor.execute(query, (filename, filehash, username))
        db.commit()
        
        print("\nFile uploaded successfully!")

# -------------------------
# VIEW UPLOADED FILES
# -------------------------
def view_files():
    cursor.execute("SELECT * FROM files")
    rows = cursor.fetchall()

    print("\n--- Uploaded Files ---")
    for row in rows:
        print(f"ID: {row[0]}, Name: {row[1]}, Hash: {row[2]}, User: {row[3]}")
    print()


# -------------------------
#UPLOAD FILE FROM BROWSER
#--------------------------
def upload_file_with_browser(username):
    from tkinter import Tk, filedialog
    
    # Hide the root tkinter window
    root = Tk()
    root.withdraw()
    
    # Open file browser
    filepath = filedialog.askopenfilename(title="Select file to upload")
    
    if not filepath:
        print("No file selected!")
        return
    
    filename = os.path.basename(filepath)
    print(f"Selected: {filename}")
    
    filehash = generate_hash(filepath)
    
    # Check for duplicates
    cursor.execute("SELECT filename FROM files WHERE filehash=%s", (filehash,))
    duplicate = cursor.fetchone()
    
    if duplicate:
        print("\n⚠ DUPLICATE FILE DETECTED! ⚠")
        print("Already uploaded as:", duplicate[0])
        
        query = """
        INSERT INTO duplicate_files (filename, filehash, original_file, uploaded_by)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (filename, filehash, duplicate[0], username))
        db.commit()
    else:
        query = "INSERT INTO files (filename, filehash, uploaded_by) VALUES (%s, %s, %s)"
        cursor.execute(query, (filename, filehash, username))
        db.commit()
        print("\nFile uploaded successfully!")


# -------------------------
# VIEW DUPLICATE FILES
# -------------------------
def view_duplicate_files():
    cursor.execute("SELECT * FROM duplicate_files")
    rows = cursor.fetchall()

    print("\n--- Duplicate Files ---")
    for row in rows:
        print(f"Duplicate: {row[1]}, Hash: {row[2]}, Original: {row[3]}, User: {row[4]}")
    print()

# -------------------------
#  MAIN MENU
# -------------------------
def main():
    while True:
        print("\n--- Data Download Duplication Alert System ---")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            register()

        elif choice == "2":
            username = login()
            if username:
                user_menu(username)

        elif choice == "3":
            print("Exiting...")
            break

        else:
            print("Invalid choice!")

# -------------------------
#  USER MENU
# -------------------------
def user_menu(username):
    while True:
        print("\n--- User Menu ---")
        print("1. Upload File")
        print("2. Upload File From Browser")
        print("3. View Uploaded Files")
        print("4. View Duplicate Files")
        print("5. Logout")

        ch = input("Enter choice: ")
        
        if ch=="1":
            upload_file(username)
            
        if ch == "2":
            upload_file_with_browser(username)

        elif ch == "3":
            view_files()

        elif ch == "4":
            view_duplicate_files()

        elif ch == "5":
            print("Logged out!")
            break

        else:
            print("Invalid choice!")

# Run program
main()
