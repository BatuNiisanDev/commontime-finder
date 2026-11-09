import csv
import random
from IPython.display import clear_output
from jam_sibuk import menu_jam_sibuk
import os
import uuid
from datetime import datetime

# ==================================================
# DATABASE / FILE CSV
# ==================================================

def buat_file_csv(nama_file, header):
    if not os.path.exists(nama_file):
        with open(nama_file, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(header)


buat_file_csv("users.csv", ["user_id", "username", "email", "password"])
buat_file_csv("groups.csv", ["group_id", "group_name", "owner"])
buat_file_csv("group_members.csv", ["group_id", "username"])
buat_file_csv("busy_times.csv", ["group_id", "username", "day", "start", "end"])


# ==================================================
# FITUR ANGGOTA LAIN 1
# REGISTRASI DAN LOGIN USER
# ==================================================

def registerUser():
    print("\n========== REGISTRASI USER ==========")

    username = input("Username: ")
    email = input("Email: ")
    password = input("Password: ")

    with open("users.csv", "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row["username"] == username:
                print("Username sudah digunakan!")
                return

    user_id = str(uuid.uuid4())[:8]

    with open("users.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([user_id, username, email, password])

    print("Registrasi berhasil!")


def loginUser():
    print("\n========== LOGIN USER ==========")

    username = input("Username: ")
    password = input("Password: ")

    with open("users.csv", "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row["username"] == username and row["password"] == password:
                print(f"Selamat datang, {username}!")
                return username

    print("Username atau password salah!")
    return None


# ==================================================
# FITUR SAYA 2
# MEMBUAT KELOMPOK
# ==================================================

def createGroup(username):
    print("\n========== BUAT KELOMPOK ==========")

    group_name = input("Masukkan nama kelompok: ").strip()

    if not group_name:
        print("Nama kelompok tidak boleh kosong!")
        return

    group_id = str(uuid.uuid4())[:8]

    with open("groups.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([group_id, group_name, username])

    # Pembuat kelompok otomatis menjadi anggota
    with open("group_members.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([group_id, username])

    print("Kelompok berhasil dibuat!")
    print(f"Nama kelompok : {group_name}")
    print(f"ID kelompok   : {group_id}")


# ==================================================
# FITUR SAYA 2
# MENAMPILKAN KELOMPOK
# ==================================================

def showGroups(username):
    print("\n========== DAFTAR KELOMPOK ==========")

    found = False

    with open("group_members.csv", "r", newline="") as file:
        members = csv.DictReader(file)

        for member in members:
            if member["username"] == username:
                with open("groups.csv", "r", newline="") as group_file:
                    groups = csv.DictReader(group_file)

                    for group in groups:
                        if group["group_id"] == member["group_id"]:
                            print(
                                f"ID: {group['group_id']} | "
                                f"Nama: {group['group_name']} | "
                                f"Pemilik: {group['owner']}"
                            )
                            found = True
                            break

    if not found:
        print("Kamu belum tergabung dalam kelompok.")


# ==================================================
# FITUR SAYA 2
# MENGHAPUS KELOMPOK
# ==================================================

def deleteGroup(username):
    print("\n========== HAPUS KELOMPOK ==========")

    # Hanya pemilik kelompok yang dapat menghapus
    with open("groups.csv", "r", newline="") as file:
        groups = list(csv.DictReader(file))

    owned_groups = [
        group for group in groups
        if group["owner"] == username
    ]

    if not owned_groups:
        print("Kamu tidak memiliki kelompok untuk dihapus.")
        return

    for group in owned_groups:
        print(
            f"ID: {group['group_id']} | "
            f"Nama: {group['group_name']}"
        )

    group_id = input("\nMasukkan ID kelompok yang ingin dihapus: ")

    target = None

    for group in owned_groups:
        if group["group_id"] == group_id:
            target = group
            break

    if target is None:
        print("Kelompok tidak ditemukan!")
        return

    konfirmasi = input(
        f"Yakin menghapus {target['group_name']}? (y/n): "
    ).lower()

    if konfirmasi != "y":
        print("Penghapusan dibatalkan.")
        return

    # Hapus kelompok dari groups.csv
    groups = [
        group for group in groups
        if group["group_id"] != group_id
    ]

    with open("groups.csv", "w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["group_id", "group_name", "owner"]
        )
        writer.writeheader()
        writer.writerows(groups)

    # Hapus seluruh anggota kelompok
    with open("group_members.csv", "r", newline="") as file:
        members = list(csv.DictReader(file))

    members = [
        member for member in members
        if member["group_id"] != group_id
    ]

    with open("group_members.csv", "w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["group_id", "username"]
        )
        writer.writeheader()
        writer.writerows(members)

    # Hapus seluruh jadwal kelompok
    with open("busy_times.csv", "r", newline="") as file:
        schedules = list(csv.DictReader(file))

    schedules = [
        schedule for schedule in schedules
        if schedule["group_id"] != group_id
    ]

    with open("busy_times.csv", "w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "group_id", "username", "day", "start", "end"
            ]
        )
        writer.writeheader()
        writer.writerows(schedules)

    print("Kelompok berhasil dihapus!")


# ==================================================
# FITUR ANGGOTA LAIN 3
# MEMASUKKAN ANGGOTA KE KELOMPOK
# ==================================================

def addMember(username):
    print("\n========== TAMBAH ANGGOTA ==========")

    showGroups(username)

    group_id = input("\nMasukkan ID kelompok: ")
    new_member = input("Username anggota yang ingin ditambahkan: ")

    # Periksa kepemilikan kelompok
    with open("groups.csv", "r", newline="") as file:
        groups = list(csv.DictReader(file))

    group = next(
        (
            g for g in groups
            if g["group_id"] == group_id
            and g["owner"] == username
        ),
        None
    )

    if group is None:
        print("Kelompok tidak ditemukan atau bukan milikmu!")
        return

    # Periksa akun anggota
    with open("users.csv", "r", newline="") as file:
        users = list(csv.DictReader(file))

    if not any(u["username"] == new_member for u in users):
        print("Username belum terdaftar!")
        return

    # Periksa anggota yang sudah bergabung
    with open("group_members.csv", "r", newline="") as file:
        members = list(csv.DictReader(file))

    if any(
        m["group_id"] == group_id
        and m["username"] == new_member
        for m in members
    ):
        print("Anggota sudah berada di kelompok!")
        return

    with open("group_members.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([group_id, new_member])

    print("Anggota berhasil ditambahkan!")


# ==================================================
# FITUR ANGGOTA LAIN 3
# MENGELUARKAN ANGGOTA DARI KELOMPOK
# ==================================================

def removeMember(username):
    print("\n========== KELUARKAN ANGGOTA ==========")

    showGroups(username)

    group_id = input("\nMasukkan ID kelompok: ")

    with open("groups.csv", "r", newline="") as file:
        groups = list(csv.DictReader(file))

    group = next(
        (
            g for g in groups
            if g["group_id"] == group_id
            and g["owner"] == username
        ),
        None
    )

    if group is None:
        print("Kelompok tidak ditemukan atau bukan milikmu!")
        return

    with open("group_members.csv", "r", newline="") as file:
        members = list(csv.DictReader(file))

    group_members = [
        m for m in members
        if m["group_id"] == group_id
    ]

    print("\nAnggota kelompok:")

    for member in group_members:
        print("-", member["username"])

    target = input("\nUsername yang ingin dikeluarkan: ")

    if target == username:
        print("Pemilik kelompok tidak dapat dikeluarkan!")
        return

    if not any(m["username"] == target for m in group_members):
        print("Anggota tidak ditemukan!")
        return

    members = [
        m for m in members
        if not (
            m["group_id"] == group_id
            and m["username"] == target
        )
    ]

    with open("group_members.csv", "w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["group_id", "username"]
        )
        writer.writeheader()
        writer.writerows(members)

    print("Anggota berhasil dikeluarkan!")


# ==================================================
# FITUR ANGGOTA LAIN 4
# INPUT JAM SIBUK ANGGOTA
# ==================================================

def inputBusyTime(username):
    print("\n========== INPUT JAM SIBUK ==========")

    showGroups(username)

    group_id = input("\nMasukkan ID kelompok: ")

    with open("group_members.csv", "r", newline="") as file:
        members = list(csv.DictReader(file))

    is_member = any(
        m["group_id"] == group_id
        and m["username"] == username
        for m in members
    )

    if not is_member:
        print("Kamu bukan anggota kelompok tersebut!")
        return

    day = input("Hari (Senin/Minggu): ").strip().lower()

    days = [
        "senin", "selasa", "rabu", "kamis",
        "jumat", "sabtu", "minggu"
    ]

    if day not in days:
        print("Nama hari tidak valid!")
        return

    start = input("Jam mulai (HH:MM): ")
    end = input("Jam selesai (HH:MM): ")

    try:
        start_time = datetime.strptime(start, "%H:%M")
        end_time = datetime.strptime(end, "%H:%M")
    except ValueError:
        print("Format jam harus HH:MM!")
        return

    if start_time >= end_time:
        print("Jam selesai harus lebih besar dari jam mulai!")
        return

    with open("busy_times.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            group_id, username, day, start, end
        ])

    print("Jam sibuk berhasil disimpan!")


# ==================================================
# FITUR SAYA 5
# MENGAMBIL SELURUH JADWAL SIBUK
# ==================================================

def getBusyTimes(group_id, day):

    busy_times = []

    with open("busy_times.csv", "r", newline="") as file:
        schedules = csv.DictReader(file)

        for schedule in schedules:
            if (
                schedule["group_id"] == group_id
                and schedule["day"].lower() == day.lower()
            ):
                start = datetime.strptime(
                    schedule["start"], "%H:%M"
                )

                end = datetime.strptime(
                    schedule["end"], "%H:%M"
                )

                busy_times.append((start, end))

    return busy_times


# ==================================================
# FITUR SAYA 5
# MENGHITUNG WAKTU KOSONG BERSAMA
# ==================================================

def findFreeTime(group_id, day):

    busy_times = getBusyTimes(group_id, day)

    # Jam operasional pencarian: 08.00 sampai 22.00
    batas_awal = datetime.strptime("08:00", "%H:%M")
    batas_akhir = datetime.strptime("22:00", "%H:%M")

    # Urutkan jadwal berdasarkan jam mulai
    busy_times.sort(key=lambda waktu: waktu[0])

    # Gabungkan jadwal yang bertabrakan atau berdekatan
    merged = []

    for start, end in busy_times:

        start = max(start, batas_awal)
        end = min(end, batas_akhir)

        if start >= end:
            continue

        if not merged or start > merged[-1][1]:
            merged.append([start, end])

        else:
            merged[-1][1] = max(
                merged[-1][1], end
            )

    # Cari celah di antara jadwal sibuk
    free_times = []
    current_time = batas_awal

    for start, end in merged:

        if current_time < start:
            free_times.append((current_time, start))

        current_time = max(current_time, end)

    # Periksa waktu kosong setelah jadwal terakhir
    if current_time < batas_akhir:
        free_times.append((current_time, batas_akhir))

    return free_times


# ==================================================
# FITUR SAYA 5
# MENAMPILKAN HASIL FREE TIME
# ==================================================

def showFreeTime(username):

    print("\n========== CARI FREE TIME ==========")

    showGroups(username)

    group_id = input("\nMasukkan ID kelompok: ")

    # Pastikan pengguna merupakan anggota kelompok
    with open("group_members.csv", "r", newline="") as file:
        members = list(csv.DictReader(file))

    is_member = any(
        m["group_id"] == group_id
        and m["username"] == username
        for m in members
    )

    if not is_member:
        print("Kamu bukan anggota kelompok tersebut!")
        return

    day = input("Masukkan hari pencarian: ").strip().lower()

    days = [
        "senin", "selasa", "rabu", "kamis",
        "jumat", "sabtu", "minggu"
    ]

    if day not in days:
        print("Nama hari tidak valid!")
        return

    free_times = findFreeTime(group_id, day)

    print(f"\nHasil pencarian free time hari {day.capitalize()}:")
    print("------------------------------------")

    if not free_times:
        print("Tidak ditemukan waktu kosong bersama.")
    else:
        for i, (start, end) in enumerate(free_times, 1):
            print(
                f"{i}. {start.strftime('%H:%M')} - "
                f"{end.strftime('%H:%M')}"
            )

    print("------------------------------------")


# ==================================================
# MENU KELOMPOK
# ==================================================

def groupMenu(username):

    while True:

        print("\n========== MENU KELOMPOK ==========")
        print("1. Buat kelompok")
        print("2. Tampilkan kelompok")
        print("3. Hapus kelompok")
        print("4. Tambah anggota")
        print("5. Keluarkan anggota")
        print("6. Input jam sibuk")
        print("7. Cari free time")
        print("8. Kembali")

        choice = input("Pilih menu: ")

        if choice == "1":
            createGroup(username)

        elif choice == "2":
            showGroups(username)

        elif choice == "3":
            deleteGroup(username)

        elif choice == "4":
            addMember(username)

        elif choice == "5":
            removeMember(username)

        elif choice == "6":
            inputBusyTime(username)

        elif choice == "7":
            showFreeTime(username)

        elif choice == "8":
            break

        else:
            print("Pilihan tidak valid!")


# ==================================================
# MENU UTAMA
# ==================================================

def main():

    print("====================================")
    print("       COMMON TIME FINDER")
    print("====================================")

    while True:

        print("\n========== MENU UTAMA ==========")
        print("1. Login")
        print("2. Register")
        print("3. Keluar")

        choice = input("Pilih menu: ")

        if choice == "1":

            username = loginUser()

            if username is not None:
                groupMenu(username)

        elif choice == "2":
            registerUser()

        elif choice == "3":
            print("Terima kasih telah menggunakan Common Time Finder!")
            break

        else:
            print("Pilihan tidak valid!")


# ==================================================
# MENJALANKAN PROGRAM
# ==================================================

if __name__ == "__main__":
    main()