import pymysql

# Open database connection
db = pymysql.connect("localhost","root","Parath0du","EVHoops")

# prepare a cursor object using cursor() method
cursor = db.cursor()

# Prepare SQL query to INSERT a record into the database.
sql = """INSERT INTO player_info(idnew_table,
   first_name, last_name, age, height, email, favorite_position, create_date, update_date)
   VALUES (3, 'Shine', 'Abraham', 48, 63, 'tomtiffanie@gmail.com', 'SG', '2019-08-28', '2019-08-28')"""
try:
   # Execute the SQL command
   cursor.execute(sql)
   # Commit your changes in the database
   db.commit()
except:
   # Rollback in case there is any error
   db.rollback()

# disconnect from server
db.close()