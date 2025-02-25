import streamlit as st
import pymysql
from datetime import datetime

# Adding a logo on the left corner 
st.set_page_config(page_title="Bank Customer Management System", page_icon="https://fiaks.com/wp-content/uploads/2019/04/Suryoday-Final-Logo.jpg")
st.sidebar.image("https://fiaks.com/wp-content/uploads/2019/04/Suryoday-Final-Logo.jpg", width=300)

# MySQL connection configuration
db_config = {
    "host": "database-1.chm6ogy0g0j4.eu-north-1.rds.amazonaws.com",
    "user": "admin",
    "password": "Gaurav#Khole",
    "database": "database-1",
    "cursorclass": pymysql.cursors.DictCursor
}

def get_db_connection():
    return pymysql.connect(**db_config)

def create_customer_table():
    create_table_query = """
    CREATE TABLE IF NOT EXISTS Customer (
        id INT AUTO_INCREMENT PRIMARY KEY,
        full_name VARCHAR(20) NOT NULL,
        date_of_birth DATE NOT NULL,
        gender VARCHAR(20) NOT NULL,
        government_id VARCHAR(15) NOT NULL,
        pan_card VARCHAR(10),
        photograph VARCHAR(50),
        signature VARCHAR(50),
        residential_address VARCHAR(50) NOT NULL,
        mailing_address VARCHAR(50),
        mobile_number VARCHAR(10) NOT NULL UNIQUE,
        email_address VARCHAR(20),
        occupation VARCHAR(15),
        employer_name VARCHAR(20),
        employer_address VARCHAR(50),
        annual_income FLOAT,
        source_of_funds VARCHAR(50),
        account_purpose VARCHAR(50),
        preferred_account_type VARCHAR(20),
        nominee_details VARCHAR(20),
        internet_banking TINYINT(1) DEFAULT 0,
        mobile_banking TINYINT(1) DEFAULT 0,
        initial_deposit FLOAT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(create_table_query)
        conn.commit()
    finally:
        conn.close()

# Create table on startup
create_customer_table()

st.title("Bank Customer Management System")
menu = st.sidebar.selectbox("Menu", ["Create Customer", "Search Customer"])

if menu == "Create Customer":
    st.header("Create Customer Profile")
    with st.form("customer_form"):
        full_name = st.text_input("Full Name")
        date_of_birth = st.date_input("Date of Birth", min_value=datetime(1995, 1, 1))
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        government_id = st.text_input("Government-Issued ID Number",max_chars=15)
        pan_card = st.text_input("PAN Card (Tax ID)")
        photograph = st.text_input("Photograph URL or Path")
        signature = st.text_input("Signature Sample URL or Path")
        residential_address = st.text_area("Residential Address")
        mailing_address = st.text_area("Mailing Address (if different)")
        mobile_number = st.text_input("Mobile Number", max_chars=10)
        email_address = st.text_input("Email Address",)
        occupation = st.text_input("Occupation / Job Title")
        employer_name = st.text_input("Employer Name")
        employer_address = st.text_area("Employer Address")
        annual_income = st.number_input("Annual Income / Salary Details", min_value=0.0, format="%.2f")
        source_of_funds = st.number_input("Source of Funds", min_value=0, step=1)
        account_purpose = st.selectbox("Purpose of Account",["Salary", "Business","Other"])
        preferred_account_type = st.selectbox("Preferred Account Type", ["Savings", "Current", "Fixed Deposit"])
        nominee_details = st.text_input("Nominee Details")
        internet_banking = 1 if st.checkbox("Enable Internet Banking") else 0
        mobile_banking = 1 if st.checkbox("Enable Mobile Banking") else 0
        initial_deposit = st.number_input("Initial Deposit Amount", min_value=0.0, format="%.2f")
        submit = st.form_submit_button("Create Customer")
    
    if submit:
        try:
            dob_str = date_of_birth.strftime("%Y-%m-%d")
            insert_query = """
            INSERT INTO Customer 
            (full_name, date_of_birth, gender, government_id, pan_card, photograph, signature, 
             residential_address, mailing_address, mobile_number, email_address, occupation, 
             employer_name, employer_address, annual_income, source_of_funds, account_purpose, 
             preferred_account_type, nominee_details, internet_banking, mobile_banking, initial_deposit)
            VALUES 
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                full_name, dob_str, gender, government_id, pan_card, photograph, signature,
                residential_address, mailing_address, mobile_number, email_address, occupation,
                employer_name, employer_address, annual_income, source_of_funds, account_purpose,
                preferred_account_type, nominee_details, internet_banking, mobile_banking, initial_deposit
            )
            conn = get_db_connection()
            with conn.cursor() as cursor:
                cursor.execute(insert_query, values)
                conn.commit()
                customer_id = cursor.lastrowid
            conn.close()
            st.success(f"Customer created successfully! Customer ID: {customer_id}")
        except Exception as e:
            st.error(f"Error: {e}")

elif menu == "Search Customer":
    st.header("Search Customer by Mobile Number")
    mobile_number = st.text_input("Enter Mobile Number to search")
    if st.button("Search"):
        if not mobile_number:
            st.error("Please provide a mobile number.")
        else:
            select_query = "SELECT * FROM Customer WHERE mobile_number = %s"
            conn = get_db_connection()
            with conn.cursor() as cursor:
                cursor.execute(select_query, (mobile_number,))
                customer = cursor.fetchone()
            conn.close()
            if customer:
                if customer.get("date_of_birth"):
                    customer["date_of_birth"] = customer["date_of_birth"].strftime('%Y-%m-%d')
                if customer.get("created_at"):
                    customer["created_at"] = customer["created_at"].strftime('%Y-%m-%d %H:%M:%S')
                st.subheader("Customer Details")
                for key, value in customer.items():
                    st.write(f"**{key.replace('_', ' ').title()}:** {value}")
            else:
                st.warning("Customer not found.")
