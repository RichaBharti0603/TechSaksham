import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

try:
    # Use environment variables instead of hardcoded values
    con = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

    print(con)
    cur = con.cursor()
    cur.execute('SHOW DATABASES;')
    print(cur.fetchall())

    con.close()

except Exception as e:
    print("Error:", e)


def signup(data):
    try:
        # Connect to database using environment variables
        con = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        
        cur = con.cursor()
        cur.execute('SELECT * FROM student_record WHERE roll = %s', (data[0],))  # Prevent SQL injection
        
        if cur.fetchone():  # Check if user already exists
            con.close()
            return False
        else:
            myquery = '''INSERT INTO student_record(roll, name, password, branch, admin_year, per_10, per_12) 
                         VALUES (%s, %s, %s, %s, %s, %s, %s)'''
            cur.execute(myquery, data)
            con.commit()  # Commit changes to the database
            
            con.close()
            return True
    except Exception as e:
        print("Error:", e)
        return False  # Return False if there's an error
    
def signin(data):
    try:
        # Connect to database using environment variables
        con = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        
        cur = con.cursor()
        cur.execute('SELECT * FROM student_record WHERE roll = %s', (data[0],))  # Prevent SQL injection
        result = cur.fetchone()
        if  result != None and result[0] ==data [0] and result[2]== data[1]:
          # Check if user already exists
            con.close()
            return False
        else:
            con.close()
            return True
    except Exception as e:
        print("Error:", e)
        return False  # Return False if there's an error
    
def search(roll):
    try:
        # Connect to database using environment variables
        con = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        
        cur = con.cursor()
        cur.execute(f"select roll, name, branch, admin_year, per_10, per_12 from student_record where roll = {roll}")
        result = cur.fetchone()
        if result!= None:
            con.close()
            return result
        else:
            con.close()
            return ()
    except Exception as e:
        print(e)

def displayall():
    try:
        # Connect to database using environment variables
        con = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        
        cur = con.cursor()
        cur.execute(f"SELECT *FROM student_record")
        return cur.fetchall()
        
    except Exception as e:
        print(e)


print("*"*20 +"Welcome to My App" + "*"*20)
while True:
    print("1. SignIn \n  2. SignUp \n 3. Search 4. DisplayAll \n 5.Exit ")
    ch= int (input("Enter Your Choice"))


    if ch==1:
        roll = int(input("Enter Your Roll Number"))
        password= int(input("Enter your password"))

        if signin((roll, password)):
            print("You are successfully Login")
        else:
            print("Invalid Login or Password")


    elif ch==2:
        roll = int(input("Enter Your Roll Number:"))
        name = input("Enter Your Name")
        password = input("Enter Your Password")
        branch = input ("Enter Your Branch")
        admin_year = input ("Enter Your Admission Year")
        per_10 = int(input("Enter 10th percentage"))
        per_12 = int (input("Enter 12th percentage"))
        if signup((roll, name, password, branch, admin_year, per_10, per_12)):
            print("Student Registered")
        else:
            print("Student already Registered")


    elif ch==3:
        roll = int(input("Enter roll number to search"))
        info = search(roll)
        print(info)


    elif ch==4:
        allrecord = displayall()
        for record in allrecord:
            print(f"{record[0]} \t {record[1]} \t {record[2]} \t {record[3]} \t {record[4]}")
        print("*"*20)


    elif ch==5:
        break

    else:
        print("Wrong Choice")