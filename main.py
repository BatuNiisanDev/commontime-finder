import csv
import random
from IPython.display import clear_output

#Sistem Registrasi dan Login user, Shootout to Bryan Randle (@BryanJR) on Medium! -BatuNiisanDev 2026

def registerUser():
    with open ("users.csv", mode = 'a', newline = "") as f:
        writer = csv.writer(f, delimiter = ',')

        print("=========== Registrasi Pengguna Baru ===========")

        username = input("Masukkan Username: ")
        user_email = input("Masukkan Email: ")
        password_hash = input("Masukkan Password: ")
        user_id = random.randint(1000, 9999)

        clear_output()

        print("=========== Registrasi Pengguna Baru ===========")
        print("Berhasil registrasi pengguna baru!")
        writer.writerow([user_id, username, user_email, password_hash])

def loginUser():

    print("=========== Login Pengguna ===========")
    username = input("Masukkan Username: ")
    password_hash = input("Masukkan Password: ")

    clear_output()

    with open ("users.csv", mode="r") as f:
        reader = csv.reader(f, delimiter = ',')
        for row in reader:
            if row [1] == username and row [3] == password_hash:
                print(f"Selmat datang, {username}!")
                return True
    print("Username atau Password salah.")
    return False

print("=========== Common Time Finder ===========")

#main loop user
active = True
logged_in = False

while active:
    if logged_in == False:
        print('''
        1. Login
        2. Register
        3. Quit
        ''')
    else:
        print('''
        1. Logout
        2. Quit
        ''')
    user_choice = input("Masukkan Input pilihan: ")
    user_choice = user_choice.lower()

    if user_choice == "register" or user_choice == "2" and logged_in == False:
        registerUser()
    elif user_choice == "login" or user_choice == "1" and logged_in == False:
        logged_in = loginUser()
    elif user_choice == "quit" or user_choice == "2" and logged_in == True or user_choice == "3" and logged_in == False:
        active = False
        print("Terimakasih telah menggunakan Common Time Finder!")
    elif user_choice == "logout" or user_choice == "1" and logged_in == True:
        logged_in = False
        print("Berhasil logout!")
    else:
        print("Input tidak valid, silahkan coba lagi.") 