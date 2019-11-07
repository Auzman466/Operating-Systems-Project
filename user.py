import MySQLdb as mc

connection = mc.connect(host='localhost',
                        user='testuser',
                        passwd='testpass',
                        db='bank')

cursor = connection.cursor()


def add_client():
    fname = input('Enter client first name: ')
    lname = input('Enter client last name: ')
    gender = input('Enter client gender (m or f): ')
    ssn = input('Enter client social security number (separated by hyphens): ')
    employee = input('Enter employee ID to assign client to: ')
    format_str = """INSERT INTO clients (fname, lname, gender, ssn, assigned_employee)
        VALUES ('{first}', '{last}', '{gender}', '{ssn}', {employee});
        """
    sql_command = format_str.format(first=fname, last=lname, gender=gender, ssn=ssn, employee=employee)
    cursor.execute(sql_command)
    connection.commit()
    menu()


def assign_client():
    cursor.execute('SELECT * FROM clients')
    result = cursor.fetchall()
    for r in result:
        print(r)
    client = int(input('Which client do you want to reassign? '))
    cursor.execute('SELECT employee_id, lname, fname FROM employees')
    result = cursor.fetchall()
    for r in result:
        print(r)
    employee = int(input('Assign client to which employee? '))
    statement = 'UPDATE clients SET assigned_employee = %s WHERE client_number = %s'
    val = (employee, client)
    cursor.execute(statement, val)
    connection.commit()
    menu()


def create_account():
    acc_num = int(input('Input new account number: '))
    acc_type = input('Input account type (checking, savings): ')
    client = int(input('Input client ID of account holder: '))
    statement = """INSERT INTO accounts (acc_num, type, balance, client_id)
        VALUES (%s, %s, %s, %s);
        """
    vals = (acc_num, acc_type, 0, client)
    cursor.execute(statement, vals)
    connection.commit()
    menu()


def delete_account():
    acc_num = int(input('Which account will be deleted? '))
    stmt = 'SELECT * FROM accounts WHERE acc_num = %s'
    cursor.execute(stmt, acc_num)
    result = cursor.fetchall()
    print(result)
    bal = float(result[2])
    if bal != 0.00:
        print('Cannot delete account with a balance.')
        menu()
    else:
        confirm = input('Delete this account? y/n')
        if confirm == 'y':
            stmt = 'DELETE FROM accounts WHERE acc_num = %s'
            vals = acc_num
            cursor.execute(stmt, vals)
            connection.commit()
            menu()
        else:
            menu()


def add_transaction():
    account = int(input('Enter account to add transaction to: '))
    trans_date = input('Enter date of transaction (format YYYY-MM-DD): ')
    trans_desc = input('Enter transaction description: ')
    amount = float(input('Enter transaction amount: '))
    stmt = """INSERT INTO transactions (trans_date, description, amount, account)
    VALUES (%s, %s, %s, %s);
    """
    vals = (trans_date, trans_desc, amount, account)
    cursor.execute(stmt, vals)
    stmt = 'SELECT * FROM accounts WHERE acc_num = %s'
    vals = account
    cursor.execute(stmt, vals)
    result = cursor.fetchall()
    bal = float(result[2])
    bal = bal - amount
    stmt = 'UPDATE accounts SET balance = %s WHERE acc_num = %s'
    vals = (bal, account)
    cursor.execute(stmt, vals)
    connection.commit()
    menu()


def quit_bank():
    cursor.close()
    connection.close()
    print('Connection closed.')


def menu():
    print('Welcome to the Online Banking Management System.')
    print('1. Add New Client')
    print('2. Assign Clients')
    print('3. Create New Bank Account')
    print('4. Remove Bank Account')
    print('5. Add Transactions')
    print('6. Quit')
    selection = int(input('Select a command.'))
    if selection == 1:
        add_client()
    elif selection == 2:
        assign_client()
    elif selection == 3:
        create_account()
    elif selection == 4:
        delete_account()
    elif selection == 5:
        add_transaction()
    elif selection == 6:
        quit_bank()
    else:
        print('Invalid selection.')
        menu()
