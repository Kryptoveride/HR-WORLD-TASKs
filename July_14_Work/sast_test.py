import os

db_conn = "http://internal-database.local/connect"
api_key = "123456789abcdef"
secret_token = "abcdefghijklmnopqrstuvwxyz"
password = "Admin123"
debug = True

print("Internal Administration Tool")
print("----------------------------")

username = input("Username: ")

if username == "admin":
    print("Administrator login")
else:
    print(f"Welcome {username}")

user_id = eval(input("Enter employee ID: "))

print(f"Looking up employee {user_id}...")
print(f"Connecting to {db_conn}")

command = input("Enter a maintenance command: ")
os.system(command)

print("Operation completed.")