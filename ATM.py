#python3 /workspaces/Githubtest/ATM.py -- to run the code
# ATM.py

import mysql.connector
import datetime
import matplotlib.pyplot as plt

def sql_connecter():
    try:
        connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Cruel1430@',
                database='ATM')
        return connection
    except mysql.connector.Error as Err:
        print(f"Error: {Err}")
        return None
    
def validate_name(name):
    """
    Validate if the name contains only alphabetic characters.
    """
    return name.isalpha()

def validate_ph_number(phone_number):
    """
    Validate if the phone number contains only digits and is 10 characters long.
    """
    return phone_number.isdigit() and len(phone_number) == 10

def validate_dob(dob):
    """
    Validate if the date of birth is in the format YYYY-MM-DD.
    """
    try:
        datetime.datetime.strptime(dob, '%Y-%m-%d')
        return True
    except ValueError:
        return False
    

