import os
import pymysql

mysql_user = os.environ.get('MYSQL_USER', 'root')
mysql_password = os.environ.get('MYSQL_PASSWD', '123456')
conn = pymysql.connect(host='localhost',
                       user=mysql_user,
                       passwd=mysql_password)
cursor = conn.cursor()
cursor.execute("""CREATE DATABASE if NOT EXISTS flask_dev CHARSET=UTF8MB4""")
cursor.execute("""CREATE DATABASE if NOT EXISTS flask_pro CHARSET=UTF8MB4""")
cursor.close()
conn.close()
