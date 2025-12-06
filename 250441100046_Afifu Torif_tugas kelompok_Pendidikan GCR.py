# SISTEM PENDIDIKAN GCR - Versi perbaikan (login guru/murid ada)
pengguna = {
    "guru1@gmail.com": {"nama": "Guru Satu", "password": "111", "peran": "pengajar"},
    "guru2@gmail.com": {"nama": "Guru Dua", "password": "222", "peran": "pengajar"},
    "mhs1@gmail.com": {"nama": "Murid Satu", "password": "333", "peran": "murid"},
}

kelas_data = {}

counter_kelas = 1
def buat_kode_random():
    global counter_kelas
    kode = f"KLS{counter_kelas:03d}"
    counter_kelas += 1
    return kode

def garis():
    print("=" * 40)

def input_non_kosong(text):
    isi = ""
    while not isi.strip():
        isi = input(text)
    return isi

# ---------------- LOGIN GURU & MURID ----------------
def login_guru():
    garis()
    print("LOGIN GURU")
    garis()
    email = input_non_kosong("Email Guru: ")
    pwd = input_non_kosong("Password: ")
    if email in pengguna and pengguna[email]["password"] == pwd and pengguna[email]["peran"] == "pengajar":
        print("Login Guru berhasil.")
        return email
    else:
        print("Login gagal. Pastikan akun guru tersedia dan password benar.")
        return None

def login_murid():
    garis()
    print("LOGIN MAHASISWA")
    garis()
    email = input_non_kosong("Email Mahasiswa: ")
    pwd = input_non_kosong("Password: ")
    if email in pengguna and pengguna[email]["password"] == pwd and pengguna[email]["peran"] == "murid":
        print("Login Mahasiswa berhasil.")
        return email
    else:
        print("Login gagal. Pastikan akun mahasiswa tersedia dan password benar.")
        return None

# ---------------- PENDAFTARAN MURID ----------------
def daftar_murid():
    garis()
    print("DAFTAR MAHASISWA BARU")
    garis()
    email = input_non_kosong("Email baru: ")
    if email in pengguna:
        print("Email sudah digunakan.")
        return
    nama = input_non_kosong("Nama lengkap: ")
    password = input_non_kosong("Password: ")
    pengguna[email] = {"nama": nama, "password": password, "peran": "murid"}
    print("Pendaftaran berhasil!")

# ---------------- FUNGSI KELAS ----------------
def buat_kelas(email):
    garis()
    print("BUAT KELAS")
    garis()
    kode = buat_kode_random()
    print(f"Kode kelas otomatis: {kode}")
    nama = input_non_kosong("Nama kelas: ")
    kelas_data[kode] = {"nama": nama, "pengajar": email, "murid": [], "tugas": {}}
    print(f"Kelas '{nama}' berhasil dibuat!")

def lihat_kelas_pengajar(email):
    garis()
    print("KELAS DIKELOLA")
    garis()
    ada = False
    for kode, info in kelas_data.items():
        if info["pengajar"] == email:
            ada = True
            print(f"- {kode} | {info['nama']}")
    if not ada:
        print("Tidak ada kelas.")

def ubah_kelas(email):
    kode = input_non_kosong("Masukkan kode kelas: ")
    if kode not in kelas_data or kelas_data[kode]["pengajar"] != email:
        print("Kelas tidak ditemukan atau bukan milik Anda.")
        return
    nama_baru = input_non_kosong("Nama kelas baru: ")
    kelas_data[kode]["nama"] = nama_baru
    print("Nama kelas berhasil diubah.")

def hapus_kelas(email):
    kode = input_non_kosong("Masukkan kode kelas: ")
    if kode not in kelas_data or kelas_data[kode]["pengajar"] != email:
        print("Kelas tidak ditemukan atau bukan milik Anda.")
        return
    del kelas_data[kode]
    print("Kelas berhasil dihapus.")

# ---------------- FUNGSI MURID KELAS ----------------
def lihat_murid_dalam_kelas(kode):
    garis()
    print("DAFTAR MURID")
    garis()
    daftar = kelas_data.get(kode, {}).get("murid", [])
    if daftar:
        for m in daftar:
            nama = pengguna.get(m, {}).get("nama", m)
            print("- " + nama)
    else:
        print("Belum ada murid.")

def hapus_murid_dari_kelas(kode):
    murid = input_non_kosong("Email murid yang ingin dihapus dari kelas: ")
    if kode not in kelas_data:
        print("Kode kelas tidak ditemukan.")
        return
    if murid in kelas_data[kode]["murid"]:
        kelas_data[kode]["murid"].remove(murid)
        for t in kelas_data[kode]["tugas"].values():
            if murid in t:
                del t[murid]
        print("Murid berhasil dikeluarkan dari kelas.")
    else:
        print("Murid tidak ada di kelas.")

# ---------------- FUNGSI TUGAS ----------------
def tambah_tugas(kode):
    tugas = input_non_kosong("Nama tugas baru: ")
    if tugas in kelas_data[kode]["tugas"]:
        print("Tugas sudah ada.")
        return
    kelas_data[kode]["tugas"][tugas] = {}
    print("Tugas berhasil ditambahkan.")

def lihat_semua_tugas(kode):
    garis()
    print("DAFTAR TUGAS")
    garis()
    tugas_all = kelas_data[kode]["tugas"]
    if not tugas_all:
        print("Belum ada tugas.")
        return
    for t in tugas_all:
        print("- " + t)

def ubah_tugas(kode):
    tugas = input_non_kosong("Nama tugas yang ingin diubah: ")
    if tugas not in kelas_data[kode]["tugas"]:
        print("Tugas tidak ditemukan.")
        return
    tugas_baru = input_non_kosong("Nama tugas baru: ")
    kelas_data[kode]["tugas"][tugas_baru] = kelas_data[kode]["tugas"].pop(tugas)
    print("Nama tugas diubah.")

def hapus_tugas(kode):
    tugas = input_non_kosong("Nama tugas yang dihapus: ")
    if tugas not in kelas_data[kode]["tugas"]:
        print("Tugas tidak ditemukan.")
        return
    del kelas_data[kode]["tugas"][tugas]
    print("Tugas dihapus.")

# ---------------- FUNGSI NILAI ----------------
def beri_nilai(kode):
    tugas = input_non_kosong("Nama tugas: ")
    if tugas not in kelas_data[kode]["tugas"]:
        print("Tugas tidak ditemukan.")
        return
    murid = input_non_kosong("Email murid: ")
    if murid not in kelas_data[kode]["murid"]:
        print("Murid tidak ada di kelas.")
        return
    s = input_non_kosong("Nilai: ")
    try:
        nilai = float(s)
    except:
        print("Nilai harus berupa angka.")
        return
    kelas_data[kode]["tugas"][tugas][murid] = nilai
    print("Nilai berhasil diberikan.")

def ubah_nilai(kode):
    tugas = input_non_kosong("Nama tugas: ")
    if tugas not in kelas_data[kode]["tugas"]:
        print("Tugas tidak ditemukan.")
        return
    murid = input_non_kosong("Email murid: ")
    if murid not in kelas_data[kode]["tugas"][tugas]:
        print("Belum ada nilai untuk murid ini.")
        return
    s = input_non_kosong("Nilai baru: ")
    try:
        nilai = float(s)
    except:
        print("Nilai harus berupa angka.")
        return
    kelas_data[kode]["tugas"][tugas][murid] = nilai
    print("Nilai berhasil diubah.")

def hapus_nilai(kode):
    tugas = input_non_kosong("Nama tugas: ")
    if tugas not in kelas_data[kode]["tugas"]:
        print("Tugas tidak ditemukan.")
        return
    murid = input_non_kosong("Email murid: ")
    if murid not in kelas_data[kode]["tugas"][tugas]:
        print("Tidak ada nilai untuk murid ini.")
        return
    del kelas_data[kode]["tugas"][tugas][murid]
    print("Nilai dihapus.")

def lihat_nilai_semua(kode):
    garis()
    print("NILAI SEMUA MURID")
    garis()
    tugas_all = kelas_data[kode]["tugas"]
    if not tugas_all:
        print("Belum ada tugas.")
        return
    for tugas, nilai_murid in tugas_all.items():
        print(f"\nTugas: {tugas}")
        if not nilai_murid:
            print("  (Belum ada nilai)")
        for murid, nilai in nilai_murid.items():
            nama = pengguna.get(murid, {}).get("nama", murid)
            print(f"- {nama}: {nilai}")

# ---------------- MENU KELAS PENGAJAR ----------------
def menu_kelas_pengajar(email, kode):
    if kode not in kelas_data or kelas_data[kode]["pengajar"] != email:
        print("Kelas tidak ditemukan atau bukan milik Anda.")
        return
    while True:
        garis()
        print(f"MENU KELAS PENGAJAR ({kode})")
        garis()
        print("1. Lihat murid")
        print("2. Kelola tugas")
        print("3. Kelola nilai")
        print("4. Lihat nilai semua murid")
        print("5. Hapus murid dari kelas")
        print("0. Kembali")
        pilih = input("Pilih: ")

        if pilih == "1":
            lihat_murid_dalam_kelas(kode)

        elif pilih == "2":
            # submenu tugas
            while True:
                garis()
                print("MENU TUGAS")
                garis()
                print("1. Tambah tugas")
                print("2. Lihat tugas")
                print("3. Ubah tugas")
                print("4. Hapus tugas")
                print("0. Kembali")
                p = input("Pilih: ")
                if p == "1": tambah_tugas(kode)
                elif p == "2": lihat_semua_tugas(kode)
                elif p == "3": ubah_tugas(kode)
                elif p == "4": hapus_tugas(kode)
                elif p == "0": break
                else: print("Pilihan salah.")

        elif pilih == "3":
            # submenu nilai
            while True:
                garis()
                print("MENU NILAI")
                garis()
                print("1. Beri nilai")
                print("2. Ubah nilai")
                print("3. Hapus nilai")
                print("0. Kembali")
                p = input("Pilih: ")
                if p == "1": beri_nilai(kode)
                elif p == "2": ubah_nilai(kode)
                elif p == "3": hapus_nilai(kode)
                elif p == "0": break
                else: print("Pilihan salah.")

        elif pilih == "4":
            lihat_nilai_semua(kode)

        elif pilih == "5":
            hapus_murid_dari_kelas(kode)

        elif pilih == "0":
            break
        else:
            print("Pilihan tidak valid.")

# ---------------- MENU PENGAJAR ----------------
def menu_pengajar(email):
    while True:
        garis()
        print("MENU GURU")
        garis()
        print("1. Buat kelas")
        print("2. Lihat kelas")
        print("3. Ubah kelas")
        print("4. Hapus kelas")
        print("5. Masuk ke kelas")
        print("0. Keluar")
        pilih = input("Pilih: ")
        if pilih == "1": buat_kelas(email)
        elif pilih == "2": lihat_kelas_pengajar(email)
        elif pilih == "3": ubah_kelas(email)
        elif pilih == "4": hapus_kelas(email)
        elif pilih == "5":
            kode = input_non_kosong("Masukkan kode kelas: ")
            if kode in kelas_data and kelas_data[kode]["pengajar"] == email:
                menu_kelas_pengajar(email, kode)
            else:
                print("Kelas tidak ditemukan atau bukan milik Anda.")
        elif pilih == "0":
            break
        else:
            print("Pilihan tidak valid.")

# ---------------- MENU MURID ----------------
def lihat_kelas_murid(email):
    garis()
    print("KELAS SAYA")
    garis()
    ada = False
    for kode, info in kelas_data.items():
        if email in info["murid"]:
            ada = True
            print(f"- {kode} | {info['nama']}")
    if not ada:
        print("Belum bergabung kelas.")

def gabung_kelas(email):
    kode = input_non_kosong("Masukkan kode kelas: ")
    if kode not in kelas_data:
        print("Kelas tidak ditemukan.")
        return
    if email in kelas_data[kode]["murid"]:
        print("Sudah bergabung.")
        return
    kelas_data[kode]["murid"].append(email)
    print("Berhasil bergabung!")

def lihat_nilai_murid(email, kode):
    garis()
    print("NILAI TUGAS")
    garis()
    tugas_all = kelas_data[kode]["tugas"]
    if not tugas_all:
        print("Belum ada tugas.")
        return
    for tugas, nilai_murid in tugas_all.items():
        nilai = nilai_murid.get(email, "-")
        print(f"- {tugas}: {nilai}")

def menu_kelas_murid(email, kode):
    while True:
        garis()
        print(f"MENU KELAS MURID ({kode})")
        garis()
        print("1. Lihat tugas & nilai")
        print("0. Kembali")
        pilih = input("Pilih: ")
        if pilih == "1": lihat_nilai_murid(email, kode)
        elif pilih == "0": break
        else: print("Pilihan tidak valid.")

def menu_murid(email):
    while True:
        garis()
        print("MENU MAHASISWA")
        garis()
        print("1. Lihat kelas saya")
        print("2. Gabung kelas")
        print("3. Masuk kelas")
        print("0. Keluar")
        pilih = input("Pilih: ")
        if pilih == "1": lihat_kelas_murid(email)
        elif pilih == "2": gabung_kelas(email)
        elif pilih == "3":
            kode = input_non_kosong("Masukkan kode kelas: ")
            if kode in kelas_data and email in kelas_data[kode]["murid"]:
                menu_kelas_murid(email, kode)
            else:
                print("Kelas tidak ditemukan atau belum bergabung.")
        elif pilih == "0": break
        else: print("Pilihan tidak valid.")

# ---------------- PROGRAM UTAMA ----------------
def jalankan():
    while True:
        garis()
        print("SISTEM PENDIDIKAN GCR")
        garis()
        print("1. Login sebagai Guru")
        print("2. Login sebagai Mahasiswa")
        print("3. Daftar Mahasiswa Baru")
        print("0. Keluar")
        pilih = input("Pilih: ")
        if pilih == "1":
            email = login_guru()
            if email:
                menu_pengajar(email)
        elif pilih == "2":
            email = login_murid()
            if email:
                menu_murid(email)
        elif pilih == "3":
            daftar_murid()
        elif pilih == "0":
            print("Terima kasih telah menggunakan sistem.")
            break
        else:
            print("Pilihan tidak valid.")

jalankan()