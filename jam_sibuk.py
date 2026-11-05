jam_sibuk = {}


def tambah_jam_sibuk(username):
    print("\n TAMBAH JAM SIBUK ")
    hari = input("Hari (contoh: Senin) : ").strip()
    mulai = input("Jam mulai (contoh: 08:00) : ").strip()
    selesai = input("Jam selesai (contoh: 10:00) : ").strip()
    ket = input("Keterangan (kuliah/kerja) : ").strip()

    if hari == "" or mulai == "" or selesai == "":
        print("Hari dan jam tidak boleh kosong!")
        return

    # kalau user belum punya jadwal, buat list kosong dulu
    if username not in jam_sibuk:
        jam_sibuk[username] = []

    data = hari + " " + mulai + "-" + selesai + " " + ket
    jam_sibuk[username].append(data)
    print("Berhasil disimpan!")


def lihat_jam_sibuk(username):
    print("\n JAM SIBUK SAYA ")
    if username not in jam_sibuk or len(jam_sibuk[username]) == 0:
        print("Belum ada jam sibuk.")
        return

    nomor = 1
    for j in jam_sibuk[username]:
        print(nomor, ".", j)
        nomor += 1


def hapus_jam_sibuk(username):
    lihat_jam_sibuk(username)
    if username not in jam_sibuk or len(jam_sibuk[username]) == 0:
        return

    pilih = input("Nomor yang mau dihapus : ").strip()

    if not pilih.isdigit():
        print("Harus berupa angka!")
        return

    pilih = int(pilih)
    if pilih < 1 or pilih > len(jam_sibuk[username]):
        print("Nomor tidak valid!")
        return

    jam_sibuk[username].pop(pilih - 1)
    print("Berhasil dihapus!")


def menu_jam_sibuk(username):
    while True:
        print("\n MENU JAM SIBUK ")
        print("1. Tambah")
        print("2. Lihat")
        print("3. Hapus")
        print("4. Kembali")
        menu = input("Pilih : ").strip()

        if menu == "1":
            tambah_jam_sibuk(username)
        elif menu == "2":
            lihat_jam_sibuk(username)
        elif menu == "3":
            hapus_jam_sibuk(username)
        elif menu == "4":
            break
        else:
            print("Menu tidak ada!")
