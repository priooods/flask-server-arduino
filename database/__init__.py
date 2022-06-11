import mysql.connector
from mysql.connector import errorcode
import os # ini untuk mendapatkan environment variable
from dotenv import load_dotenv # ini supaya file .env bisa dibaca
load_dotenv() # func untuk membaca .env file

# buat try & except biar kita bisa dapet balikan kalau mysql connection error
try:
  # buat connection dengan mysql server
  connect = mysql.connector.connect(host=os.getenv('DB_HOST'),database=os.getenv('DB_NAME'),port=os.getenv('DB_PORT'),user=os.getenv('DB_USER'),password=os.getenv('DB_PASS'))
except mysql.connector.Error as err:
  # check kalau access ke mysql gagal
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your username or password")
  # check kalau database yang di tuju salah / ga ada
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  # keluarin semua error selain diatas
  else:
    print(err)
else: # kalau semua oke, keluarin var connect 
  # kita buat var db baru dengan tujuan untuk menambahkan perintah cursor()
  # cursor disini adalah perintah yg akan digunakan untuk melakukan pemanggilan query
  # pemanggilan query perlu ditambahkan perintah execute('Query masukin disini')
  # example : db.execute('Query masukin disini')
  connect_to_db = connect.cursor(buffered=True , dictionary=True)
    
  