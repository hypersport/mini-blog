import os
import MySQLdb

mysql_user = os.environ.get('MYSQL_USER', 'root')
mysql_password = os.environ.get('MYSQL_PASSWD', 'root')
conn = MySQLdb.connect(host='localhost', user=mysql_user, passwd=mysql_password)
cursor = conn.cursor()
cursor.execute("""create database if not exists flask_dev""")
cursor.execute("""create database if not exists flask_pro""")
cursor.close()
conn.close()
