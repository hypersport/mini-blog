import os
import MySQLdb

mysql_user = os.environ.get('MYSQL_USER', 'root')
mysql_password = os.environ.get('MYSQL_PASSWD', 'root')
conn = MySQLdb.connect(host='localhost', user=mysql_user, passwd=mysql_password)
cursor = conn.cursor()
cursor.execute("""CREATE DATABASE if NOT EXISTS flask_dev CHARSET=UTF8""")
cursor.execute("""CREATE DATABASE if NOT EXISTS flask_pro CHARSET=UTF8""")
cursor.close()
conn.close()
