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
#---------------------------------------Step-1 Validation
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
    
def validate_province(province):
    '''
    Validates that the name of the provionce is in upper case
    '''
    valid_province = ['BC','AL','MB','ON','YT','QC','NF','NB','NS']
    return province.upper() in validate_province
#---------------------------------------Step-2 Search for the next available account number and pin for new users
def get_next_available_account_and_pin(cursor):
    '''
    It will fetch for the available account number and pin
    '''
    connection = sql_connecter
    if connection :
        cursor = connection.cursor
        try:
            cursor.execute('''SELECT Account_Number, Pin 
            FROM Accounts 
            WHERE Activated = 0 
            ORDER BY Account_Number ASC 
            LIMIT 1''')
            result = cursor.fetchone()
            if result:
                return result[0] , result[1]
            else:
                return None, None
        except Exception as e:
            print(f"Error: {e}")
            return None, None
#---------------------------------------Step-3 Verify user login

def verfy_account(cursor,account_number,pin):
    '''
    Verifies the account number and the pin if teh account exists in the databse or not 
    and if yes then the pin is coprrect or not\.
    '''
    try:
        cursor.execute('''
        SELECT * From Accounts
        WHERE Account_Number = %s and Pin = %s and Activated = 1
        ''',(account_number,pin))

        return cursor.fetchone is not None #True if account exists
    except Exception as e:
        print(f"Error verifying this account please check your details and try again:{e}")
        return False
    
#---------------------------------------Step-4 Add a new user or activate the account of the existing user

def insert_customer(cursor,connection,first_name,last_name,dob,phone,province,account_number,pin):
    try: 
        # First, check if the account number already exists

        cursor.execute('''
        SELECT * FROM Accounts
        WHERE Account_Number = %s,
        ''',(account_number))
        existing_customer = cursor.fetchone()
        
        if existing_account :
            cursor.execute('''
            SELECT Customer_ID FROM Accounts
            WHERE Account_Number = %s             
            ''',(account_number))
            account_info = cursor.fetchone()

            if account_info:
                #If we find the customer id then we will just activate that account
                customer_id = account_info[0]
                cursor.execute('''
                UPDATE Accounts 
                SET Activated = 1 , Customer_ID = %s
                WHERE Account_Number = %s
                ''',(customer_id,account_number))
        else:
            #If the account does not exists make a new one by assigning the account number and pin
            cursor.execute('''
            INSERT INTO Customers (First_Name,Last_Name,DOB,Phone,Province)
            Values (%s,%s,%s,%s,%s)
            ''',(first_name, last_name, dob, phone, province))

            #Insert the fetched account number and pin with initial balance 0 in the accounts table
            cursor.execute('''
            INSERT INTO Accounts (Account_Number, Pin, Activated, Balance, Customer_ID)
            Values(%s,%s,1,0,%s)
            ''',(account_number, pin, customer_id))
            print(f"The account has been successfully created for {first_name}{last_name} , \n The account number is {account_number}")
        
        # Commit the changes to the database after all the changes
        connection.commit()

    except Exception as e:
        print("Error inserting a customer")
        connection.rollback()

#---------------------------------------Step-5 Inserting a transaction 
def insert_transaction(cursor,connection,account_number,transaction_type,amount):
    try:
        cursor.execute('''
        INSERT INTO Transactions (Account_Number,Transaction_Type,Amount,Transaction_date_time) 
        VALUES (%s,%s,%s,Now())
        ''',(account_number,transaction_type,amount))

        # Commit the changes to the database after all the changes
        connection.commit()
    except mysql.connector.Error as e:
        print(f"SQL Error :{e}")
    except Exception as e:
        print(f"Error while inserting an transaction :{e}")

#---------------------------------------Step-6 We will calculate the total balance 
def calculate_balance(cursor,account_number):
    try:
        cursor.execute('''
        ''')







    






    


    

