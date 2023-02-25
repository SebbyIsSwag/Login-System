import pyotp
import scrypt
import mysql.connector
import re
import ssl
import http.server
import socketserver
import configparser
import os
import hashlib

config = configparser.ConfigParser()
config.read('config.ini')

db_config = config['Database']
db_host = db_config['host']
db_user = db_config['user']
db_password = db_config['password']
db_database = db_config['database']

db = mysql.connector.connect(
  host=db_host,
  user=db_user,
  password=db_password,
  database=db_database
)

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain('server.crt', 'server.key')

cursor = db.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), password_hash VARCHAR(255), password_salt BINARY(16), secret_key_hash VARCHAR(255), secret_key_salt BINARY(16))")

while True:
  username = input("Enter a username: ")
  password = input("Enter a password (must be at least 12 characters long and contain at least one uppercase letter, one lowercase letter, and one digit): ")

  sql = "SELECT * FROM users WHERE username = %s"
  val = (username,)
  cursor.execute(sql, val)
  result = cursor.fetchone()

  if result is not None:
    print("Username already exists. Please choose a different username.")
  else:
    if not re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)[A-Za-z\d]{12,}$', password):
      print("Password does not meet complexity requirements. Please try again.")
    elif len(password) > 64:
      print("Password is too long. Please try again.")
    else:
      salt = os.urandom(16)
      hashed_password = scrypt.hash(password.encode('utf-8'), salt=salt)

      secret_key = pyotp.random_base32()
      secret_key_salt = os.urandom(16)
      hashed_key = scrypt.hash(secret_key.encode('utf-8'), salt=secret_key_salt)

      sql = "INSERT INTO users (username, password_hash, password_salt, secret_key_hash, secret_key_salt) VALUES (%s, %s, %s, %s, %s)"
      val = (username, hashed_password, salt, hashed_key, secret_key_salt)
      cursor.execute(sql, val)
      db.commit()

      print("Account created successfully.")
      break

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello, world!')

httpd = socketserver.TCPServer(("", 443), MyHandler)
httpd.socket = ssl_context.wrap_socket(httpd.socket, server_side=True)
httpd.serve_forever()

while True:
  login_username = input("Enter your username: ")
  login_password = input("Enter your password:")
  # prompt the user for their one-time password
  login_otp = input("Enter your one-time password: ")

  sql = "SELECT password_hash, password_salt, secret_key_salt FROM users WHERE username = %s"
  val = (login_username,)
  cursor.execute(sql, val)
  
  if cursor.rowcount == 0:
    print("Invalid username or password. Please try again.")
  else:
    row = cursor.fetchone()
    hashed_password = row[0]
    password_salt = row[1]

    if scrypt.hash(login_password.encode('utf-8'), salt=password_salt) != hashed_password:
      print("Invalid username or password. Please try again.")
      continue

    secret_key_salt = row[2]

    totp = pyotp.TOTP(pyotp.utils.base32_from_bytes(scrypt.hash(login_otp.encode('utf-8'), salt=secret_key_salt)))
    if not totp.verify(login_otp):
      print("Invalid one-time password. Please try again.")
      continue

    print("Login successful!")
    break
