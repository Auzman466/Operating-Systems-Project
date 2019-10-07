import sys
import MySQLdb.connector as mc

connection = mc.connect(host='localhost',
                        user='testuser',
                        passwd='testpass',
                        db='bank')

cursor = connection.cursor()
cursor.execute('DROP TABLE IF EXISTS customer')

sql_command = """
CREATE TABLE clients ( 
client_number INT PRIMARY KEY, 
fname VARCHAR(20), 
lname VARCHAR(30), 
gender CHAR(1),
ssn VARCHAR(11));
"""
cursor.execute(sql_command)

sql_command = """
CREATE TABLE accounts (
acc_num INT PRIMARY KEY 
type VARCHAR(15),
balance INT,
client_id INT FOREIGN KEY REFERENCES clients(client_number));
"""
cursor.execute(sql_command)

client_data = [('James', 'Smith', 'm', '721-07-4427'),
               ('John', 'Williams', 'm', '529-56-2164'),
               ('Mary', 'Jones', 'f', '394-78-0036'),
               ('Jennifer', 'Lopez', 'f', '402-32-8027'),
               ]

account_data = [(422501, 'Checking', 4123, 1),
                (422502, 'Checking', 8000, 2),
                (522501, 'Savings', 1500, 2),
                (422503, 'Checking', 10400, 3),
                (522502, 'Savings', 0, 3),
                (422504, 'Checking', 12440, 4)
                ]

for client, p in enumerate(client_data):
    format_str = """INSERT INTO clients (client_number, fname, lname, gender, birth_date)
    VALUES ({client_no}, '{first}', '{last}', '{gender}', '{birthdate}');
    """
    sql_command = format_str.format(client_no=client, first=p[0], last=p[1], gender=p[2], ssn=p[3])
    print(sql_command)
    cursor.execute(sql_command)

for client, p in enumerate(account_data):
    format_str = """INSERT INTO accounts (acc_num, type, balance, client_id)
    VALUES ({acc_no}, '{acctype}', {bal}, {client});
    """
    sql_command = format_str.format(acc_no=p[0], acctype=p[1], bal=p[2], client=p[3])
    print(sql_command)
    cursor.execute(sql_command)

connection.commit()

cursor.close()
connection.close()
