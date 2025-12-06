import random
import string # Digunakan untuk menghasilkan karakter acak

# =======================================================
# DATA AWAL
# =======================================================
pengguna = {}

# Struktur Data Utama: 
# kelas_data: {kode_kelas: {nama, pengajar, murid[], tugas{kode_tugas: {nama, deskripsi, nilai{murid: nilai}, jawaban{murid: jawaban}}}}}
kelas_data = {}


# =======================================================
# UTILITY FUNCTIONS (ANTI-TYPO & MULTI-BARIS)
# =======================================================
def garis():
    print("=" * 40)


def input_non_kosong(text):
    """Memastikan input string tidak kosong."""
    isi = ""
    while not isi.strip():
        isi = input(text)
        if not isi.strip():
            print("Input tidak boleh kosong. Silakan masukkan lagi.")
    return isi

def input_angka_aman(text, min_val=0, max_val=100):
    """
    Meminta input angka (float) dan menangani ValueError (typo non-angka)
    serta memastikan rentang.
    """
    while True:
        isi_str = input(text)
        try:
            nilai = float(isi_str)
            if min_val <= nilai <= max_val:
                return nilai
            else:
                print(f"Nilai harus dalam rentang {min_val} hingga {max_val}. Silakan masukkan lagi.")
        except ValueError:
            print("Input harus berupa angka (misal: 85 atau 90.5). Silakan masukkan lagi.")
            
def input_pilihan_menu(max_pilihan):
    """
    Meminta input angka untuk pilihan menu (0 sampai max_pilihan) 
    dan menangani typo (input non-angka atau di luar rentang).
    """
    while True:
        pilih_str = input("Pilih: ")
        try:
            pilih = int(pilih_str)
            if 0 <= pilih <= max_pilihan:
                return str(pilih)
            else:
                print(f"Pilihan harus antara 0 sampai {max_pilihan}. Silakan coba lagi.")
        except ValueError:
            print("Input harus berupa angka pilihan menu. Silakan coba lagi.")

def navigasi_kembali_atau_logout():
    """
    Menampilkan menu pilihan Kembali atau Logout dengan tampilan tombol dan konfirmasi.
    Mengembalikan 'LOGOUT', 'KEMBALI', atau 'BATAL'.
    """
    garis()
    print("NAVIGASI: Pilih Tujuan Anda")
    garis()
    
    # TAMPILAN SEPERTI TOMBOL
    print("[1.Kembali]     [0.Logout]")
    
    max_pilihan = 1
    pilih = input_pilihan_menu(max_pilihan)

    if pilih == "0":
        konf_logout = input("Yakin ingin Logout dari akun? (Y/T): ").upper()
        if konf_logout == 'Y':
            print("Anda telah logout dari akun.")
            return 'LOGOUT' 
        else:
            print("Logout dibatalkan. Kembali ke Menu Pilihan Saat Ini.")
            return 'BATAL'
    else: # pilih == "1"
        return 'KEMBALI'

def input_multibaris(prompt_awal):
    """
    Memungkinkan pengguna memasukkan teks multibaris. Input diakhiri dengan baris 'SELESAI'.
    Baris kosong (hanya Enter) akan dimasukkan sebagai bagian dari input.
    """
    print(prompt_awal)
    print(" (Ketik **SELESAI** di baris baru dan tekan Enter untuk mengakhiri input. Baris kosong akan dimasukkan.):")
    
    lines = []
    while True:
        try:
            # Menggunakan input() tanpa prompt untuk mode multibaris
            line = input() 
            
            # KONDISI PENGAKHIRAN: Hanya jika baris adalah 'SELESAI' (tanpa spasi di awal/akhir)
            if line.strip().upper() == 'SELESAI': 
                break
            
            # Tambahkan baris, termasuk baris kosong
            lines.append(line) 

        except EOFError:
            break
            
    return '\n'.join(lines)


def generate_unique_class_code(data):
    """Menghasilkan kode alfanumerik acak 6 karakter yang unik."""
    characters = string.ascii_uppercase + string.digits
    while True:
        code = ''.join(random.choices(characters, k=6))
        if code not in data:
            return code


# =======================================================
# UTAMA: LOGIN & DAFTAR
# =======================================================
def masuk():
    garis()
    print("LOGIN")
    garis()
    email = input_non_kosong("Email: ")
    
    if email not in pengguna:
        print("Email tidak terdaftar.")
        return None
        
    password = input_non_kosong("Password: ")
    
    if pengguna[email]["password"] == password:
        # Notifikasi Peran (Semi-Login)
        peran = pengguna[email]['peran']
        print(f"\n[✔] Berhasil login sebagai {pengguna[email]['nama']} (Peran: {peran.upper()}).")
        return email
    else:
        print("Password salah.")
        return None

def daftar_murid():
    garis()
    print("DAFTAR MURID BARU")
    garis()
    email = input_non_kosong("Email baru: ")
    if email in pengguna:
        print("Email sudah digunakan.")
        return
    nama = input_non_kosong("Nama lengkap: ")
    password = input_non_kosong("Password: ")
    pengguna[email] = {
        "nama": nama,
        "password": password,
        "peran": "murid"
    }
    print("Pendaftaran murid berhasil! Silakan Login.")

def daftar_pengajar():
    garis()
    print("DAFTAR PENGAJAR BARU")
    garis()
    email = input_non_kosong("Email baru: ")
    if email in pengguna:
        print("Email sudah digunakan.")
        return
    nama = input_non_kosong("Nama lengkap: ")
    password = input_non_kosong("Password: ")
    pengguna[email] = {
        "nama": nama,
        "password": password,
        "peran": "pengajar"
    }
    print("Pendaftaran pengajar berhasil! Silakan Login.")


# =======================================================
# FUNGSI PENGAJAR (CRUD KELAS & TUGAS)
# =======================================================
def buat_kelas(email):
    garis()
    print("BUAT KELAS (Random Code)")
    garis()
    
    # --- PERUBAHAN UTAMA: MENGGUNAKAN RANDOM CODE ---
    kode = generate_unique_class_code(kelas_data)
    
    nama = input_non_kosong("Nama kelas: ")
    
    kelas_data[kode] = {
        "nama": nama,
        "pengajar": email,
        "murid": [],
        "tugas": {}
    }
    print(f"\nKelas '{nama}' berhasil dibuat.")
    print(f"Bagikan kode unik ini kepada murid: {kode}")
    # ------------------------------------------------

def hapus_kelas(email):
    garis()
    print("HAPUS KELAS")
    garis()
    lihat_kelas_pengajar(email)
    kode = input_non_kosong("Masukkan kode kelas yang akan dihapus: ")
    if kode not in kelas_data or kelas_data[kode]["pengajar"] != email:
        print("Kelas tidak ditemukan atau Anda bukan pengajar kelas ini.")
        return
    konfirmasi = input(f"Yakin hapus kelas '{kelas_data[kode]['nama']}'? (Y/T): ").upper()
    if konfirmasi == 'Y':
        del kelas_data[kode]
        print("Kelas berhasil dihapus.")
    else:
        print("Penghapusan dibatalkan.")

def lihat_kelas_pengajar(email):
    garis()
    print("KELAS YANG DIKELOLA")
    garis()
    ada = False
    for kode, info in kelas_data.items():
        if info["pengajar"] == email:
            ada = True
            print(f"- {kode} | {info['nama']} ({len(info['murid'])} murid)")
    if not ada:
        print("Belum ada kelas yang Anda kelola.")

def update_nama_kelas(email):
    garis()
    print("UBAH NAMA KELAS")
    garis()
    lihat_kelas_pengajar(email)
    kode = input_non_kosong("Masukkan kode kelas yang akan diubah: ")
    if kode not in kelas_data or kelas_data[kode]["pengajar"] != email:
        print("Kelas tidak ditemukan atau Anda bukan pengajarnya.")
        return
    nama_lama = kelas_data[kode]['nama']
    nama_baru = input_non_kosong(f"Nama baru untuk '{nama_lama}': ")
    kelas_data[kode]['nama'] = nama_baru
    print(f"Nama kelas berhasil diubah dari '{nama_lama}' menjadi '{nama_baru}'.")

def tambah_tugas(kode):
    garis()
    print("TAMBAH TUGAS")
    garis()
    nama_tugas = input_non_kosong("Nama tugas (misal: Makalah Akhir): ")
    kode_tugas = input_non_kosong("Kode tugas (misal: T01): ")
    if kode_tugas in kelas_data[kode]["tugas"]:
        print("Kode tugas sudah ada.")
        return
        
    print("\n--- Deskripsi Tugas ---")
    deskripsi = input_multibaris("Masukkan Deskripsi/Isi Tugas:") 
    
    # Jika deskripsi terlalu pendek, kita pastikan ada isi
    if not deskripsi.strip():
        print("Deskripsi tidak boleh kosong. Pembatalan penambahan tugas.")
        return
        
    kelas_data[kode]["tugas"][kode_tugas] = {
        "nama": nama_tugas,
        "deskripsi": deskripsi, 
        "nilai": {},
        "jawaban": {} 
    }
    print(f"Tugas '{nama_tugas}' berhasil ditambahkan.")

def hapus_tugas(kode):
    garis()
    print("HAPUS TUGAS")
    garis()
    if not kelas_data[kode]["tugas"]:
        print("Belum ada tugas dalam kelas ini.")
        return
    print("Daftar Tugas:")
    for kt, info in kelas_data[kode]["tugas"].items():
        print(f"- {kt}: {info['nama']}")
    kode_tugas = input_non_kosong("Masukkan kode tugas yang akan dihapus: ")
    if kode_tugas not in kelas_data[kode]["tugas"]:
        print("Tugas tidak ditemukan.")
        return
    nama_tugas = kelas_data[kode]["tugas"][kode_tugas]['nama']
    konfirmasi = input(f"Yakin hapus tugas '{nama_tugas}' beserta nilainya? (Y/T): ").upper()
    if konfirmasi == 'Y':
        del kelas_data[kode]["tugas"][kode_tugas]
        print("Tugas berhasil dihapus.")
    else:
        print("Penghapusan dibatalkan.")

def beri_nilai(kode):
    garis()
    print("BERI NILAI")
    garis()
    if not kelas_data[kode]["tugas"]:
        print("Belum ada tugas untuk dinilai.")
        return
    
    print("Daftar Tugas:")
    for kt, info in kelas_data[kode]["tugas"].items():
        print(f"- {kt}: {info['nama']}")
    kode_tugas = input_non_kosong("Kode tugas yang dinilai: ")
    
    if kode_tugas not in kelas_data[kode]["tugas"]:
        print("Tugas tidak ditemukan.")
        return
    
    murid = input_non_kosong("Email murid: ")
    
    if murid not in kelas_data[kode]["murid"]:
        print("Murid tidak ada dalam kelas.")
        return
    
    # --- Tampilkan Jawaban Murid ---
    jawaban_murid = kelas_data[kode]["tugas"][kode_tugas]["jawaban"].get(murid)
    
    if jawaban_murid is None:
        print(f"\n[!] Murid {pengguna[murid]['nama']} BELUM MENYERAHKAN tugas ini.")
        if murid in kelas_data[kode]["tugas"][kode_tugas]["nilai"]:
             print(f"     (Nilai sebelumnya: {kelas_data[kode]['tugas'][kode_tugas]['nilai'][murid]})")
        lanjut = input("Tetap ingin memberi nilai? (Y/T): ").upper()
        if lanjut != 'Y':
            print("Pemberian nilai dibatalkan.")
            return
    else:
        print(f"\n--- Jawaban dari {pengguna[murid]['nama']} ---")
        print(f"\n{jawaban_murid}\n")
        print("---------------------------------")

    nilai = input_angka_aman("Nilai (0-100): ")
    kelas_data[kode]["tugas"][kode_tugas]["nilai"][murid] = nilai
    print(f"Nilai {nilai} berhasil diberikan untuk {pengguna[murid]['nama']} pada tugas {kelas_data[kode]['tugas'][kode_tugas]['nama']}.")

def lihat_nilai_semua(kode):
    garis()
    print(f"NILAI SEMUA MURID KELAS {kode}")
    garis()
    murid_di_kelas = kelas_data[kode]["murid"]
    tugas_all = kelas_data[kode]["tugas"]
    if not murid_di_kelas:
        print("Belum ada murid yang bergabung.")
        return
    if not tugas_all:
        print("Belum ada tugas.")
        return
    header = ["Nama Murid"]
    kode_tugas_list = list(tugas_all.keys())
    for kt in kode_tugas_list:
        header.append(tugas_all[kt]['nama'][:10].strip() + '...')
    
    # Penyesuaian lebar untuk tabel
    col_width = 15
    print("| " + " | ".join([h.ljust(col_width) for h in header]) + " |")
    print("-" * (len("| " + " | ".join([h.ljust(col_width) for h in header]) + " |") + 2))
    
    for email_murid in murid_di_kelas:
        baris = [pengguna[email_murid]['nama'][:col_width].ljust(col_width)]
        for kt in kode_tugas_list:
            nilai = tugas_all[kt]['nilai'].get(email_murid, "-")
            baris.append(str(nilai).center(col_width))
        print("| " + " | ".join(baris) + " |")

def lihat_murid_dalam_kelas(kode):
    garis()
    print(f"DAFTAR MURID KELAS {kode}")
    garis()
    daftar = kelas_data[kode]["murid"]
    if daftar:
        for i, m in enumerate(daftar, 1):
            print(f"{i}. {pengguna[m]['nama']} ({m})")
    else:
        print("Belum ada murid.")
        
# =======================================================
# FUNGSI MURID
# =======================================================
def lihat_kelas_murid(email):
    garis()
    print("KELAS SAYA")
    garis()
    ada = False
    for kode, info in kelas_data.items():
        if email in info["murid"]:
            ada = True
            print(f"- {kode} | {info['nama']} (Pengajar: {pengguna[info['pengajar']]['nama']})")
    if not ada:
        print("Belum bergabung kelas.")

def gabung_kelas(email):
    garis()
    print("GABUNG KELAS")
    garis()
    kode = input_non_kosong("Masukkan kode kelas: ")

    if kode not in kelas_data:
        print("Kode kelas tidak ditemukan.")
        return

    if email in kelas_data[kode]["murid"]:
        print("Anda sudah terdaftar di kelas ini.")
        return

    kelas_data[kode]["murid"].append(email)
    print(f"Berhasil bergabung ke kelas '{kelas_data[kode]['nama']}'.")


def keluar_kelas(email):
    garis()
    print("KELUAR KELAS")
    garis()
    lihat_kelas_murid(email)
    kode = input_non_kosong("Masukkan kode kelas yang akan ditinggalkan: ")
    if kode not in kelas_data or email not in kelas_data[kode]["murid"]:
        print("Kelas tidak ditemukan atau Anda tidak di dalamnya.")
        return
    nama_kelas = kelas_data[kode]['nama']
    konfirmasi = input(f"Yakin keluar dari kelas '{nama_kelas}'? (Y/T): ").upper()
    if konfirmasi == 'Y':
        kelas_data[kode]["murid"].remove(email)
        print(f"Berhasil keluar dari kelas '{nama_kelas}'.")
    else:
        print("Pembatalan keluar kelas.")

def lihat_detail_kelas_murid(email):
    kode = input_non_kosong("Masukkan kode kelas untuk melihat detail: ")
    if kode not in kelas_data or email not in kelas_data[kode]["murid"]:
        print("Kelas tidak ditemukan atau Anda belum bergabung.")
        return
    info = kelas_data[kode]
    pengajar_nama = pengguna[info['pengajar']]['nama']
    garis()
    print(f"DETAIL KELAS {info['nama']} ({kode})")
    garis()
    print(f"Pengajar: {pengajar_nama}")
    print(f"Jumlah Murid: {len(info['murid'])}")
    print("\nDaftar Tugas:")
    if info['tugas']:
        for kt, tugas_info in info['tugas'].items():
            nilai_saya = tugas_info['nilai'].get(email, "Belum Dinilai")
            status_jawaban = "SUDAH" if email in tugas_info['jawaban'] else "BELUM"
            
            print(f"- Tugas: {tugas_info['nama']} ({kt})")
            # Tampilkan deskripsi dengan batasan baris untuk ringkasan
            desc_lines = tugas_info['deskripsi'].split('\n')
            desc_preview = desc_lines[0] + (' ...' if len(desc_lines) > 1 or len(desc_lines[0]) > 50 else '')
            print(f"  Deskripsi: {desc_preview}") 
            
            print(f"  Status Jawaban: {status_jawaban}")
            print(f"  Nilai Anda: {nilai_saya}")
            print("-" * 15)
    else:
        print("- Belum ada tugas.")
    garis()

def lihat_nilai_murid(email, kode):
    garis()
    print(f"NILAI TUGAS KELAS {kelas_data[kode]['nama']}")
    garis()
    tugas_all = kelas_data[kode]["tugas"]
    if not tugas_all:
        print("Belum ada tugas.")
        return
    print(f"| {'Nama Tugas'.ljust(25)} | {'Status/Nilai'.center(15)} |")
    print("-" * 45)
    for kt, tugas_info in tugas_all.items():
        nilai = tugas_info['nilai'].get(email, "Belum Dinilai")
        status = "Sudah Dinilai" if nilai != "Belum Dinilai" else ("Tersimpan" if email in tugas_info['jawaban'] else "Belum Diserahkan")
        print(f"| {tugas_info['nama'].ljust(25)} | {str(nilai).center(15)} ({status}) |")

def mengerjakan_tugas(email, kode):
    garis()
    print("MENGERJAKAN TUGAS")
    garis()
    tugas_all = kelas_data[kode]["tugas"]
    if not tugas_all:
        print("Belum ada tugas.")
        return
    
    print("Daftar Tugas yang Tersedia:")
    tugas_untuk_dikerjakan = []
    
    for kt, info in tugas_all.items():
        # Tugas ditampilkan meskipun sudah dinilai, agar bisa diakses untuk melihat deskripsi
        status = "Sudah Dinilai" if email in info["nilai"] else ("Sudah Diserahkan" if email in info["jawaban"] else "Belum Dikerjakan")
        tugas_untuk_dikerjakan.append(kt) # Semua tugas ditambahkan
        print(f"- {kt} | {info['nama']} (Status: {status})")

    if not tugas_untuk_dikerjakan:
        print("Belum ada tugas.")
        return

    kode_tugas = input_non_kosong("Masukkan kode tugas yang akan dikerjakan/diserahkan: ")

    if kode_tugas not in tugas_all:
        print("Kode tugas tidak valid.")
        return
    
    # --- PENGGUNAAN FUNGSI MULTI-BARIS ---
    tugas_info = tugas_all[kode_tugas]
    
    # Tampilkan Deskripsi Tugas
    garis()
    print(f"--- Mengerjakan Tugas: {tugas_info['nama']} ---")
    print(f"Deskripsi Tugas:")
    print(f"\n{tugas_info['deskripsi']}\n")
    print("-" * 40)
    
    # Tampilkan Jawaban Sebelumnya (jika ada)
    jawaban_sebelumnya = tugas_info["jawaban"].get(email, "Belum ada jawaban tersimpan.")
    print(f"Jawaban Tersimpan Sebelumnya:\n{jawaban_sebelumnya}\n")
    
    # Konfirmasi untuk input baru
    konfirmasi = input("Apakah Anda ingin memasukkan jawaban baru/merevisi? (Y/T): ").upper()
    if konfirmasi != 'Y':
        print("Pembatalan pengerjaan tugas.")
        return
        
    # Memanggil fungsi baru untuk input multibaris
    jawaban = input_multibaris("Tulis jawaban Anda di bawah ini:") 
    
    # Simpan jawaban
    if jawaban.strip():
        kelas_data[kode]["tugas"][kode_tugas]["jawaban"][email] = jawaban
        # Hapus nilai jika murid merevisi jawaban (opsional, tapi disarankan)
        if email in kelas_data[kode]["tugas"][kode_tugas]["nilai"]:
             del kelas_data[kode]["tugas"][kode_tugas]["nilai"][email]
             print("\n[!] Jawaban direvisi. Nilai sebelumnya dihapus. Menunggu penilaian baru.")
        
        print("\n[✔] Jawaban berhasil disimpan dan diserahkan.")
        print("Menunggu penilaian dari pengajar.")
    else:
        print("\n[!] Penyerahan dibatalkan. Jawaban kosong.")
    # ----------------------------------------

# =======================================================
# MENU CLASSES
# =======================================================
def masuk_kelas_pengajar(email):
    lihat_kelas_pengajar(email)
    kode = input_non_kosong("Masukkan kode kelas untuk dikelola: ")
    if kode not in kelas_data or kelas_data[kode]["pengajar"] != email:
        print("Kelas tidak ditemukan atau Anda bukan pengajar kelas ini.")
        return None
    return menu_kelas_pengajar(email, kode)

def menu_kelas_pengajar(email, kode):
    while True:
        garis()
        print(f"KELOLA KELAS {kelas_data[kode]['nama']} ({kode})")
        garis()
        print("1. Lihat Daftar Murid")
        print("2. Kelola Tugas (Tambah/Hapus/Deskripsi)")
        print("3. Beri Nilai Tugas (Lihat Jawaban Murid)")
        print("4. Lihat Nilai Semua Murid (Tabel)")
        print("0. Kembali/ Logout")
        max_pilihan = 4
        pilih = input_pilihan_menu(max_pilihan)
        
        if pilih == "1":
            lihat_murid_dalam_kelas(kode)
        elif pilih == "2":
            if sub_menu_tugas_pengajar(kode) == 'LOGOUT':
                return 'LOGOUT'
        elif pilih == "3":
            beri_nilai(kode)
        elif pilih == "4":
            lihat_nilai_semua(kode)
        elif pilih == "0":
            aksi = navigasi_kembali_atau_logout()
            if aksi == 'LOGOUT':
                return 'LOGOUT'
            elif aksi == 'KEMBALI':
                break

def sub_menu_tugas_pengajar(kode):
    while True:
        garis()
        print(f"MENU TUGAS KELAS {kode}")
        garis()
        print("1. Tambah Tugas Baru (CREATE + Deskripsi)")
        print("2. Hapus Tugas (DELETE)")
        print("0. Kembali/ Logout")
        max_pilihan = 2
        pilih = input_pilihan_menu(max_pilihan)
        
        if pilih == "1":
            tambah_tugas(kode)
        elif pilih == "2":
            hapus_tugas(kode)
        elif pilih == "0":
            aksi = navigasi_kembali_atau_logout()
            if aksi == 'LOGOUT':
                return 'LOGOUT'
            elif aksi == 'KEMBALI':
                break
    return None

def masuk_kelas_murid(email):
    lihat_kelas_murid(email)
    kode = input_non_kosong("Masukkan kode kelas yang ingin dimasuki: ")
    if kode not in kelas_data or email not in kelas_data[kode]["murid"]:
        print("Kelas tidak ditemukan atau Anda belum bergabung kelas ini.")
        return None
    return menu_kelas_murid(email, kode)

def menu_kelas_murid(email, kode):
    while True:
        garis()
        print(f"MENU KELAS MURID {kelas_data[kode]['nama']} ({kode})")
        garis()
        print("1. Lihat Detail Kelas (Tugas & Deskripsi)")
        print("2. Lihat Tugas & Nilai Saya")
        print("3. Kerjakan Tugas (Input Jawaban)")
        print("0. Kembali/ Logout")
        max_pilihan = 3
        pilih = input_pilihan_menu(max_pilihan)
        if pilih == "1":
            lihat_detail_kelas_murid(email)
        elif pilih == "2":
            lihat_nilai_murid(email, kode)
        elif pilih == "3":
            mengerjakan_tugas(email, kode)
        elif pilih == "0":
            aksi = navigasi_kembali_atau_logout()
            if aksi == 'LOGOUT':
                return 'LOGOUT'
            elif aksi == 'KEMBALI':
                break

# =======================================================
# MENU UTAMA (ROLES)
# =======================================================
def menu_pengajar(email):
    while True:
        garis()
        print(f"MENU PENGAJAR | {pengguna[email]['nama']}")
        garis()
        print("1. Buat Kelas Baru (CREATE)")
        print("2. Lihat Kelas Dikelola (READ)")
        print("3. Kelola Kelas (Masuk/UPDATE/DELETE)")
        print("0. Logout")
        max_pilihan = 3
        pilih = input_pilihan_menu(max_pilihan)
        if pilih == "1":
            buat_kelas(email)
        elif pilih == "2":
            lihat_kelas_pengajar(email)
        elif pilih == "3":
            if sub_menu_kelola_kelas_pengajar(email) == 'LOGOUT':
                break
        elif pilih == "0":
            konfirmasi = input("Anda Yakin ingin Logout? (Y/T): ").upper()
            if konfirmasi == 'Y':
                break

def sub_menu_kelola_kelas_pengajar(email):
    while True:
        garis()
        print("KELOLA KELAS")
        garis()
        print("1. Masuk Kelas (Untuk Kelola Tugas/Nilai)")
        print("2. Ubah Nama Kelas (UPDATE)")
        print("3. Hapus Kelas (DELETE)")
        print("0. Kembali/ Logout") 
        max_pilihan = 3
        pilih = input_pilihan_menu(max_pilihan)
        if pilih == "1":
            if masuk_kelas_pengajar(email) == 'LOGOUT':
                return 'LOGOUT'
        elif pilih == "2":
            update_nama_kelas(email)
        elif pilih == "3":
            hapus_kelas(email)
        elif pilih == "0":
            aksi = navigasi_kembali_atau_logout()
            if aksi == 'LOGOUT':
                return 'LOGOUT'
            elif aksi == 'KEMBALI':
                break
    return None

def menu_murid(email):
    while True:
        garis()
        print(f"MENU MURID | {pengguna[email]['nama']}")
        garis()
        print("1. Lihat Kelas Saya")
        print("2. Gabung Kelas")
        print("3. Keluar Kelas")
        print("4. Masuk Kelas (Lihat Detail/Kerjakan Tugas)")
        print("0. Logout")
        max_pilihan = 4
        pilih = input_pilihan_menu(max_pilihan)
        if pilih == "1":
            lihat_kelas_murid(email)
        elif pilih == "2":
            gabung_kelas(email)
        elif pilih == "3":
            keluar_kelas(email)
        elif pilih == "4":
            if masuk_kelas_murid(email) == 'LOGOUT':
                break
        elif pilih == "0":
            konfirmasi = input("Anda Yakin ingin Logout? (Y/T): ").upper()
            if konfirmasi == 'Y':
                break

# =======================================================
# MAIN EXECUTION
# =======================================================
def jalankan():
    while True:
        garis()
        print("SISTEM PENDIDIKAN GCR")
        garis()
        print("1. Masuk")
        print("2. Daftar murid baru")
        print("3. Daftar pengajar baru")
        print("0. Keluar")
        max_pilihan = 3
        pilih = input_pilihan_menu(max_pilihan)
        if pilih == "1":
            email = masuk()
            if not email:
                continue
            peran = pengguna[email]["peran"]
            if peran == "pengajar":
                menu_pengajar(email)
            else:
                menu_murid(email)
        elif pilih == "2":
            daftar_murid()
        elif pilih == "3":
            daftar_pengajar()
        elif pilih == "0":
            print("Terima kasih. Sistem dimatikan.")
            break

if __name__ == "__main__":
    jalankan()