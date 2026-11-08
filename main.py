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
                print(f"Selamat datang, {username}!")
                return True
    print("Username atau Password salah.")
    return False

anggota = []

def menambahAnggota(group_id):
    print("======== Tambah Anggota ========")

    username = input("Masukkan nama anggota anda: ")
    fileAnggota = "anggota.csv"
    
    if username in anggota:
        print("Hebat anggota sudah terdaftar!")
    else:
        anggota.append(username)
        
        with open(fileAnggota, mode = "a", newline = "") as f:
                writer = csv.writer(f) 
                writer.writerow([group_id, username])
        print(username, "Berhasil ditambahkan sebagai anggota baru!")
        
def tampilankanAnggota(group_id):
    print("======== Daftar Anggota Kelompok ========")

    with open ("anggota.csv", mode = "r", newline = "") as f:
            reader = csv.DictReader(f)
            ditemukan = False

            for data in reader:
                if data["group_id"] == str(group_id):
                    print("-", data["username"])
                    ditemukan = True

            if not ditemukan:
                print("Anggota belum ada.")
    
def mengeluarkanAnggota(group_id):
    print("======== Mengeluarkan Anggota ========")

    username = input("Masukkan nama anggota yang ingin anda keluarkan: ")
    dataBaru = []
    ditemukan = False

    with open ("anggota.csv", mode = "r", newline = "") as f:
        reader = csv.DictReader(f)

        for data in reader:
            if (data["group_id"] == str(group_id) and data["username"].lower() == username.lower()):
                ditemukan = True
            else:
                dataBaru.append(data)

    if ditemukan:
        with open("anggota.csv", mode = "w", newline = "") as f:
            fieldnames = ["group_id", "username"]
            writer = csv.DictWriter(f, fieldnames = fieldnames)
            writer.writeheader()
            writer.writerows(dataBaru)
        print(username, "Anggota sudah berhasil dikeluarkan!")
    else:
        print("Anggota tidak dapat ditemukan")


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
        1. Tambahkan Anggota
        2. Menampilkan Anggota Kelompok
        3. Keluarkan Anggota
        4. Logout
        5. Quit
        ''')
    user_choice = input("Masukkan Input pilihan: ")
    user_choice = user_choice.lower()

    if user_choice == "register" or user_choice == "2" and logged_in == False:
        registerUser()
    elif user_choice == "login" or user_choice == "1" and logged_in == False:
        logged_in = loginUser()
    elif user_choice == "1":
        menambahAnggota(group_id)
    elif user_choice == "2":
        tampilankanAnggota(group_id)
    elif user_choice == "3":
        mengeluarkanAnggota(group_id)
    elif user_choice == "quit" or user_choice == "5" and logged_in == True or user_choice == "4" and logged_in == False:
        active = False
        print("Terimakasih telah menggunakan Common Free Time Finder!")
    elif user_choice == "logout" or user_choice == "4" and logged_in == True:
        logged_in = False
        print("Berhasil logout!")
    else:
        print("Input tidak valid, silahkan coba lagi.") 
