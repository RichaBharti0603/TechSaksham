import streamlit as st
import sqlite3
from streamlit_option_menu import option_menu

# Database connection
def connect_db():
    conn = sqlite3.connect("mydb.db")
    return conn

# Create table if not exists
def create_Table():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS student (
            name TEXT, 
            password TEXT, 
            roll INTEGER PRIMARY KEY, 
            branch TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Insert record
def addRecord(data):
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute('INSERT INTO student(name, password, roll, branch) VALUES (?, ?, ?, ?)', data)
        conn.commit()
        conn.close()
    except sqlite3.IntegrityError:
        st.error ("User already registered")
        conn.close()

# View records
def view_record():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM student')
    result = cur.fetchall()
    conn.close()
    return result

# Display records
def display():
    data = view_record()
    st.markdown("<table>", unsafe_allow_html= True)
    for row in data:
        st.markdown(f"<row><td style >{row[1]}</td>", unsafe_allow_html=True)
    st.markdown("</table>", unsafe_allow_html= True)
       

# SignUp Function
def signup():
    st.title("Sign Up")

    username = st.text_input("Enter Your Username")
    name = st.text_input("Enter Your Name")
    roll = st.number_input("Enter Your Roll No.", min_value=1, step=1)
    branch = st.text_input("Enter Your Branch")
    password = st.text_input("Enter Your Password", type="password")
    confirmPassword = st.text_input("Confirm Your Password", type="password")

    if st.button("Click to SignUp"):
        if password != confirmPassword:
            st.error("Your Passwords don't match")
        elif not name or not password or not roll or not branch:
            st.error("All fields are required!")
        else:
            addRecord((name, password, roll, branch))
            st.success("Signup successful!")

# Initialize database
create_Table()

# Sidebar Menu
with st.sidebar:
    selected = option_menu("Select From Here", ["SignUp", "Display All Records"])

if selected == "SignUp":
    signup()
elif selected == "Display All Records":
    display()
