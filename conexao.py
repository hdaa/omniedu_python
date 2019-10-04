import mysql.connector

mydb = mysql.connector.connect(
	host="localhost",
	user="root",
	passwd="root",
	database="omni_dev"
	)