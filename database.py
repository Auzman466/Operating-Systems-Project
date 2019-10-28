import sys
import MySQLdb.connector as mc

connection = mc.connect(host='localhost',
                        user='testuser',
                        passwd='testpass',
                        db='bank')

cursor = connection.cursor()
cursor.execute('DROP TABLE IF EXISTS customer')

# create tables
# employee table
sql_command = """
CREATE TABLE employees (
employee_id INT PRIMARY KEY,
fname VARCHAR(20),
lname VARCHAR(30),
address VARCHAR(99),
hire_date DATE
);
"""
cursor.execute(sql_command)

# client table
sql_command = """
CREATE TABLE clients ( 
client_number INT PRIMARY KEY, 
fname VARCHAR(20), 
lname VARCHAR(30), 
gender CHAR(1),
ssn VARCHAR(11),
assigned_employee INT FOREIGN KEY REFERENCES employees(employee_id)
);
"""
cursor.execute(sql_command)

# account table references client keys
sql_command = """
CREATE TABLE accounts (
acc_num INT PRIMARY KEY 
type VARCHAR(15),
balance DECIMAL(10, 2),
client_id INT FOREIGN KEY REFERENCES clients(client_number)
);
"""
cursor.execute(sql_command)

# transactions table references account keys
sql_command = """
CREATE TABLE transactions(
transaction_num INT PRIMARY KEY,
trans_date DATE,
description VARCHAR(99),
amount DECIMAL(10, 2),
account INT FOREIGN KEY REFERENCES accounts(acc_num)
);
"""
cursor.execute(sql_command)

# create data to fill out sql database
employees_data = [('John', 'Freeman', '420 Gordon Road', '2004-11-16'),
                  ('Colin', 'Henson', '4645 Stanton Road', '2019-10-27')]

client_data = [('James', 'Smith', 'm', '721-07-4427'),
               ('John', 'Williams', 'm', '529-56-2164'),
               ('Mary', 'Jones', 'f', '394-78-0036'),
               ('Jennifer', 'Lopez', 'f', '402-32-8027'),
               ]

account_data = [(422501, 'Checking', 4123.00, 1),
                (422502, 'Checking', 8000.50, 2),
                (522501, 'Savings', 1500.33, 2),
                (422503, 'Checking', 10400.00, 3),
                (522502, 'Savings', 0.0, 3),
                (422504, 'Checking', 12440.99, 4)
                ]

transactions_data = [('2019-10-27', 'Spotify', 9.99, 422501),
                     ('2019-09-24', 'RuneScape Membership', 10.99, 422502),
                     ('2019-10-01', 'Transfer from Checking', 1500.33, 522501),
                     ('2019-10-25', 'Transfer from Savings', 400.00, 422503),
                     ('2019-10-25', 'Transfer to Checking', -400.00, 522502),
                     ('2019-09-01', 'Great American Payment', 440.99, 422504)
                     ]
# fill database
# employees
for employee, p in enumerate(employees_data):
    # create sql command string
    format_str = """INSERT INTO employees (employee_id, fname, lname, address, hire_date)
    VALUES ({employee_id} '{first}', '{last}', '{address}', {date});
    """
    sql_command = format_str.format(employee_id=employee, first=p[0], last=p[1], address=p[2], date=p[3])
    print(sql_command)
    # execute
    cursor.execute(sql_command)

# clients are managed by employees
for client, p in enumerate(client_data):
    # create sql command string
    format_str = """INSERT INTO clients (client_number, fname, lname, gender, ssn, assigned_employee)
    VALUES ({client_no}, '{first}', '{last}', '{gender}', '{ssn}', {employee});
    """
    # format string for command
    sql_command = format_str.format(client_no=client, first=p[0], last=p[1], gender=p[2], ssn=p[3], employee=p[4])
    print(sql_command)
    # execute command
    cursor.execute(sql_command)

# accounts have clients
for account, p in enumerate(account_data):
    format_str = """INSERT INTO accounts (acc_num, type, balance, client_id)
    VALUES ({acc_no}, '{acctype}', {bal}, {client});
    """
    sql_command = format_str.format(acc_no=p[0], acctype=p[1], bal=p[2], client=p[3])
    print(sql_command)
    cursor.execute(sql_command)

# transactions are in accounts
for transaction, p in enumerate(transactions_data):
    format_str = """INSERT INTO transactions (transaction_num, trans_date, description, amount, account)
    VALUES ({transaction_num}, {date}, '{description}', {amount}, {account});
    """
    sql_command = format_str.format(transaction_num=transaction, date=p[0], description=p[1], amount=p[2], account=p[3])
    print(sql_command)
    cursor.execute(sql_command)

connection.commit()

cursor.close()
connection.close()
