import MySQLdb as mc

connection = mc.connect(host='localhost',
                        user='testuser',
                        passwd='testpass',
                        db='bank')

cursor = connection.cursor()


