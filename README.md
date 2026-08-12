# DamnCRUD - UAS Pengujian Perangkat Lunak (III RPLK)

Repositori ini merupakan hasil pengerjaan **Ujian Akhir Semester (UAS) Mata Kuliah Pengujian Perangkat Lunak**, yang disusun oleh **Taruna Madya Satria Alba Pramasha (III RPLK)**, Program Studi Rekayasa Perangkat Lunak Kripto, Politeknik Siber dan Sandi Negara (T.A. 2025/2026).

**URL Repositori GitHub Submission**: [https://github.com/ecotank/UAS-DamnCRUD-Alba](https://github.com/ecotank/UAS-DamnCRUD-Alba)

---

## 1. Perbedaan Proyek Original vs Repositori Baru

Berikut adalah perbandingan komprehensif antara repositori asal (`hermanka/DamnCRUD`) dengan repositori pengujian baru (`ecotank/UAS-DamnCRUD-Alba`):

| Komponen / Aspek | Repositori Original (`hermanka/DamnCRUD`) | Repositori Baru (`ecotank/UAS-DamnCRUD-Alba`) |
| :--- | :--- | :--- |
| **Arsitektur Pengujian** | Tidak memiliki skrip pengujian otomatis (0% Test Coverage). | Mengimplementasikan **50 Pure Functional Test Cases Matrix** + **Pytest + Selenium Automated E2E Suite**. |
| **Integrasi Pipeline CI/CD** | Belum ada integrasi pipeline CI/CD (Pengujian manual). | Dilengkapi **GitHub Actions Workflow** (`.github/workflows/ci.yml`) dengan eksekusi paralel `pytest -n 2 --dist=loadfile`. |
| **Bug `create.php`** | Memiliki bug `Undefined variable $id` pada baris 17 (pemicu error runtime PHP). | **Fixed**: Menggunakan *explicit column naming* `INSERT INTO contacts (name, email, phone, title, created)`. |
| **Bug `update.php`** | **1.** Tidak ada proteksi sesi login.<br>**2.** Field Phone `value=""` (kosong, data lama hilang). | **1. Fixed**: Menambahkan `session_start()` & proteksi login.<br>**2. Fixed**: Memuat data lama `value="<?= $contact['phone'] ?>"`. |
| **Redirect Logic** | `header("location: ...")` tanpa `exit()`, menyebabkan skrip PHP tetap dieksekusi di belakang layar. | **Fixed**: Menambahkan fungsi `exit()` setelah setiap *location header redirect*. |
| **Koneksi Database PDO** | Host DB terkunci pada `'localhost'` (gagal terkoneksi Unix Socket di Linux Docker Runner). | **Fixed**: Membaca host TCP `127.0.0.1` (`getenv('DB_HOST') ?: '127.0.0.1'`). |

---

## 2. Rincian Pengujian yang Telah Dilakukan

Pengujian perangkat lunak dilakukan secara bertahap menggunakan pendekatan **Shift-Left Testing** dan **Functional QA Specification**:

### A. Manual Functional & Boundary Value Testing (50 Test Cases)
Dilakukan pengujian fungsional komprehensif yang mencakup 5 modul utama:
1. **Autentikasi & Proteksi Sesi (TC-001 - TC-011)**: Login valid/invalid, required form validation, logout session destruction, dan verifikasi proteksi direct URL tanpa sesi login.
2. **Manajemen Kontak / CRUD Operations (TC-012 - TC-041)**:
   * Pengujian alur positif Create, Read, Update, Delete.
   * **Boundary Value Analysis**: Input string Nama > 255 karakter, parameter ID bernilai negatif (`-5`), float desimal (`1.5`), dan non-numeric (`abc`).
   * **Input Validation Flaws**: Identifikasi kelemahan validasi format email (tanpa `@`), nomor telepon (dapat diisi abjad), dan nama spasi kosong (*whitespace*).
3. **DataTables Filtering & Pagination (TC-024 - TC-028)**: Testing pencarian *real-time*, navigasi halaman pagination, pengurutan kolom, dan penanganan karakter wildcard (`%`, `*`).
4. **Pengelolaan Profil & Upload Berkas (TC-042 - TC-050)**: Testing pengunggahan berkas `.jpg`/`.jpeg` valid, penolakan format `.png`/`.pdf`, penanganan double extension (`.jpg.png`), validasi file 0-byte, dan penolakan ekstensi *uppercase* (`.JPG`).

### B. Automated End-to-End Testing (Selenium WebDriver + Pytest)
Diotomatisasi menggunakan Python 3.11 dan Selenium WebDriver (Chrome Headless):
* **`tests/conftest.py`**: Fixture Selenium WebDriver + Remote Grid Fallback & automatic login session handling.
* **`tests/test_damncrud.py`**: 5 skrip otomasi pengujian fungsional utama:
  1. `test_tc012_add_new_contact`: Otomasi penambahan kontak & verifikasi pencarian DataTables.
  2. `test_tc032_update_contact`: Otomasi pengubahan nama kontak & verifikasi update.
  3. `test_tc038_delete_contact`: Otomasi penghapusan kontak & konfirmasi JavaScript alert.
  4. `test_tc043_upload_profile_image`: Otomasi pengunggahan berkas profil JPG dinamis.
  5. `test_tc008_vpage_functional_submission`: Otomasi form submission & verifikasi perolehan output.
 
     <img width="923" height="312" alt="Screenshot 2026-08-12 095857" src="https://github.com/user-attachments/assets/f6195dae-675e-400a-83c7-d24418056249" />

### C. Continuous Integration Pipeline (GitHub Actions)
Dikembangkan workflow `.github/workflows/ci.yml`:
* Menjalankan Service Container **MySQL 8.0** terisolasi di GitHub Runner.
* Menjalankan **PHP Built-in Server** pada `http://127.0.0.1:8000`.
* Menjalankan eksekusi pengujian secara **paralel** (`pytest -n 2 --dist=loadfile`) menggunakan modul `pytest-xdist`.

---

## 3. Matriks Lengkap 50 Pure Functional Test Cases

Berikut adalah rincian lengkap **50 Pure Functional Test Cases** pada aplikasi DamnCRUD beserta hasil dan temuannya:

| ID | TEST CASE OBJECTIVE | TEST CASE DESCRIPTION | EXPECTED RESULT | ACTUAL RESULT | PASS/FAIL |
| :---: | :--- | :--- | :--- | :--- | :---: |
| **TC-001** | Autentikasi User Valid | Input username `admin` dan password `nimda666!` pada form login. | Sistem mengautentikasi pengguna dan mengarahkan ke Dashboard (`index.php`). | Pengguna masuk ke `index.php` dan tampil pesan *Howdy, damn admin!*. | **PASS** |
| **TC-002** | Autentikasi Password Invalid | Input username `admin` dan password salah `wrong123`. | Sistem menolak autentikasi dan menampilkan notifikasi kesalahan kredensial. | Tampil notifikasi `Damn, wrong credentials!!`. | **PASS** |
| **TC-003** | Autentikasi Username Invalid | Input username `user_palsu` dan password `nimda666!`. | Sistem menolak login dan menampilkan notifikasi kesalahan kredensial. | Tampil notifikasi `Damn, wrong credentials!!`. | **PASS** |
| **TC-004** | Validasi Required Form Login | Menekan tombol login tanpa mengisi field username atau password. | Browser/Sistem memicu atribut validasi HTML `required` dan menahan submit form. | Form menahan submit dengan notifikasi browser `Please fill out this field`. | **PASS** |
| **TC-005** | Fungsi Logout Sesi Pengguna | Menekan tombol *Sign out* pada header/menu navigasi. | Sesi pengaksesan dihancurkan (`session_destroy()`) dan di-redirect ke `login.php`. | Pengguna ter-logout dan di-redirect ke `login.php`. | **PASS** |
| **TC-006** | Proteksi Sesi Dashboard (`index.php`) | Mengakses langsung `index.php` tanpa memiliki cookie/session login. | Sistem menolak akses dan mengarahkan pengguna ke `login.php`. | Pengguna otomatis di-redirect ke `login.php`. | **PASS** |
| **TC-007** | Proteksi Sesi Profil (`profil.php`) | Mengakses langsung `profil.php` tanpa sesi login aktif. | Sistem menolak akses dan mengarahkan pengguna ke `login.php`. | Pengguna otomatis di-redirect ke `login.php`. | **PASS** |
| **TC-008** | Proteksi Sesi VPage (`vpage.php`) | Mengakses langsung `vpage.php` tanpa sesi login aktif. | Sistem menolak akses dan mengarahkan pengguna ke `login.php`. | Pengguna otomatis di-redirect ke `login.php`. | **PASS** |
| **TC-009** | Proteksi Sesi Create (`create.php`) | Mengakses langsung `create.php` tanpa sesi login aktif. | Sistem menolak akses dan mengarahkan pengguna ke `login.php`. | Pengguna otomatis di-redirect ke `login.php`. | **PASS** |
| **TC-010** | Proteksi Sesi Update (`update.php`) | Mengakses langsung `update.php?id=1` tanpa sesi login aktif. | Sistem menolak akses dan mengarahkan pengguna ke `login.php`. | Pengguna otomatis di-redirect ke `login.php`. | **PASS** |
| **TC-011** | Proteksi Sesi Delete (`delete.php`) | Mengakses langsung `delete.php?id=1` tanpa sesi login aktif. | Sistem menolak tindakan hapus dan mengarahkan pengguna ke `login.php`. | Pengguna otomatis di-redirect ke `login.php`. | **PASS** |
| **TC-012** | Tambah Kontak Baru Valid | Mengisi form `create.php` dengan data valid (Nama, Email, Phone, Title) dan tekan Save. | Record kontak baru tersimpan ke database `badcrud` dan tampil pada Dashboard. | Kontak baru tersimpan dan tampil pada daftar tabel kontak. | **PASS** |
| **TC-013** | Tambah Kontak Nama Kosong | Mengosongkan field Name pada form `create.php` dan menekan Save. | Browser/Form memblokir submit karena atribut `required` pada field Name. | Tooltip validasi browser muncul menolak pengiriman form. | **PASS** |
| **TC-014** | Tambah Kontak Email Kosong | Mengosongkan field Email pada form `create.php` dan menekan Save. | Browser/Form memblokir submit karena atribut `required` pada field Email. | Tooltip validasi browser muncul menolak pengiriman form. | **PASS** |
| **TC-015** | Tambah Kontak No HP Kosong | Mengosongkan field Phone pada form `create.php` dan menekan Save. | Browser/Form memblokir submit karena atribut `required` pada field Phone. | Tooltip validasi browser muncul menolak pengiriman form. | **PASS** |
| **TC-016** | Tambah Kontak Title Kosong | Mengosongkan field Title pada form `create.php` dan menekan Save. | Browser/Form memblokir submit karena atribut `required` pada field Title. | Tooltip validasi browser muncul menolak pengiriman form. | **PASS** |
| **TC-017** | Navigation Cancel pada Form Create | Menekan tombol *Cancel* pada form `create.php`. | Formulir dibatalkan dan sistem mengarahkan kembali ke `index.php`. | Pengguna di-redirect kembali ke Dashboard `index.php`. | **PASS** |
| **TC-018** | Penanganan Variabel `$id` pada Create | Mengirimkan form `create.php` pada kode asli tanpa penanganan `$id`. | Menghasilkan error PHP `Undefined variable $id` pada mode error reporting tinggi. | Terdeteksi bug PHP `$id` undefined variable. *(Fixed)*. | **PASS** *(Bug Identified)* |
| **TC-019** | Syntax Email Tanpa Simbol `@` | Input format email `budi.example.com` tanpa karakter `@` pada `create.php`. | Browser/Form menolak submit karena format syntax email tidak valid. | Form ter-submit karena HTML menggunakan `type="text"`. | **FAIL** *(Validation Flaw)* |
| **TC-020** | Validasi Phone Karakter Abjad | Input string abjad `ABCD-EFGH` pada field Phone number di `create.php`. | Aplikasi memvalidasi hanya format angka yang diizinkan untuk nomor telepon. | Form menerima string abjad karena `type="text"`. | **FAIL** *(Validation Flaw)* |
| **TC-021** | Input Whitespace String Nama | Input string berupa spasi saja `   ` pada field Name saat tambah kontak. | Sistem memotong whitespace (`trim()`) atau menolak penambahan nama kosong. | Kontak tersimpan dengan nama spasi kosong. | **FAIL** *(Sanitization Flaw)* |
| **TC-022** | Boundary String Input Nama | Input string Nama sepanjang 300 karakter (melebihi kolom `varchar(255)`). | Database memotong string secara otomatis tanpa menyebabkan aplikasi crash. | MariaDB memotong string menjadi 255 karakter dan menyimpan data. | **PASS** |
| **TC-023** | Special Characters & Emoji | Input nama mengandung simbol khusus & unicode `Budi @#$% 😃` pada form create. | Sistem dapat menyimpan dan merender karakter UTF-8 / utf8mb4 tanpa corrupt. | Database `utf8mb4` menyimpan dan menampilkan karakter presisi. | **PASS** |
| **TC-024** | Tampilan Tabel Daftar Kontak | Menavigasi ke Dashboard `index.php` setelah login. | Menampilkan daftar kontak dari database lengkap dengan kolom Name, Email, Phone, Title, Created. | Seluruh kolom data kontak ditampilkan secara terstruktur. | **PASS** |
| **TC-025** | Fitur Pencarian DataTables | Ketik kata kunci nama (misal `John`) pada input search DataTables. | Tabel secara dinamis memfilter dan hanya menampilkan baris kontak yang cocok. | DataTabel menyaring hasil secara *real-time*. | **PASS** |
| **TC-026** | Fitur Navigasi Pagination DataTables | Menekan tombol halaman `2` atau `Next` pada bagian bawah tabel. | Tabel berpindah halaman dan menampilkan baris data kontak selanjutnya (11-15). | Halaman tabel berpindah dan menampilkan data kontak urutan 11 ke atas. | **PASS** |
| **TC-027** | Fitur Pengurutan Kolom (Sorting) | Menekan header kolom *Name* atau *Created* pada tabel `index.php`. | Baris data terurut secara Ascending (A-Z) atau Descending (Z-A). | Urutan baris tabel berubah sesuai kriteria pengurutan kolom. | **PASS** |
| **TC-028** | Filter Wildcards Search Table | Input karakter wildcard `%` atau `*` pada pencarian DataTables. | DataTables menangani string pencarian secara literal tanpa memicu query error. | DataTables menyaring string pencarian secara literal. | **PASS** |
| **TC-029** | Membuka Form Update ID Valid | Menekan tombol *edit* pada baris kontak dengan ID 1. | Menampilkan halaman `update.php?id=1` dengan data kontak terisi di form. | Form update terbuka dan menampilkan data terisi dari ID kontak terkait. | **PASS** |
| **TC-030** | Membuka Form Update ID Tidak Ada | Mengakses URL `update.php?id=99999` yang tidak terdaftar di database. | Sistem menghentikan eksekusi dan menampilkan pesan `Contact doesn't exist!`. | Tampil pesan `Contact doesn't exist!`. | **PASS** |
| **TC-031** | Membuka Form Update Tanpa ID | Mengakses URL `update.php` tanpa menyertakan parameter `?id=`. | Sistem menghentikan eksekusi dan menampilkan pesan `No ID specified!`. | Tampil pesan `No ID specified!`. | **PASS** |
| **TC-032** | Simpan Perubahan Update Kontak | Mengubah Nama dan Title pada `update.php?id=1` lalu menekan tombol Update. | Perubahan data ter-update di database dan pengguna di-redirect ke Dashboard. | Data kontak terbarui dan pengguna di-redirect ke `index.php`. | **PASS** |
| **TC-033** | Verifikasi Value Field Phone Update | Membuka halaman form `update.php?id=1` pada versi kode asli. | Value awal field Phone terisi dengan nomor telepon lama kontak. | Terdeteksi bug `value=""` (kosong). *(Fixed)*. | **PASS** *(Bug Identified)* |
| **TC-034** | Navigation Cancel pada Form Update | Menekan tombol *Cancel* pada form `update.php?id=1`. | Perubahan dibatalkan dan sistem mengarahkan kembali ke `index.php`. | Pengguna di-redirect kembali ke Dashboard tanpa mengubah data. | **PASS** |
| **TC-035** | Parameter ID Non-Numeric | Mengakses URL `update.php?id=abc` dengan parameter string abjad. | PDO prepared statement menangani cast ID secara aman dan menampilkan error tidak ada data. | Tampil `Contact doesn't exist!` tanpa pemicu MySQL PDO Syntax Error. | **PASS** |
| **TC-036** | Parameter ID Nilai Negatif | Mengakses URL `update.php?id=-5` dengan ID bilangan bulat negatif. | Query SQL tidak menemukan record dengan ID < 0 dan menampilkan penanganan pesan aman. | Tampil `Contact doesn't exist!`. | **PASS** |
| **TC-037** | Parameter ID Nilai Desimal Float | Mengakses URL `update.php?id=1.5` dengan bilangan desimal float. | Query PDO memproses atau mengonversi ID menjadi integer 1 secara aman. | Data ID 1 berhasil ditampilkan tanpa pemicu MySQL PDO Syntax Exception. | **PASS** |
| **TC-038** | Hapus Kontak Konfirmasi OK | Menekan tombol *delete* pada kontak dan memilih **OK** pada dialog konfirmasi JS. | Record kontak terhapus dari DB dan baris kontak hilang dari tabel `index.php`. | Dialog alert terkonfirmasi dan data kontak terhapus dari tabel. | **PASS** |
| **TC-039** | Hapus Kontak Konfirmasi Cancel | Menekan tombol *delete* pada kontak dan memilih **Cancel** pada dialog konfirmasi JS. | Tindakan hapus dibatalkan dan data kontak tetap berada di tabel. | Dialog alert dibatalkan dan data kontak tidak terhapus. | **PASS** |
| **TC-040** | Direct Delete Non-Existent ID | Mengakses URL `delete.php?id=99999` untuk menghapus record ID yang tidak ada. | Query `DELETE` mengeksekusi 0 baris terpengaruh dan mengarahkan kembali ke `index.php`. | Redirect ke `index.php` secara sukses tanpa error PHP. | **PASS** |
| **TC-041** | Direct Delete Tanpa Parameter ID | Mengakses langsung URL `delete.php` tanpa parameter `?id=`. | Sistem menghentikan eksekusi dan menampilkan pesan `No ID specified!`. | Tampil pesan `No ID specified!`. | **PASS** |
| **TC-042** | Tampilan Halaman Profil User | Menavigasi ke halaman `profil.php` melalui menu navigasi. | Menampilkan foto profil saat ini, form upload foto baru, serta info Username & Password. | Halaman profil terbuka dan menampilkan seluruh informasi akun pengguna. | **PASS** |
| **TC-043** | Upload Foto Profil Format JPG | Memilih berkas foto bermformat `.jpg` di `profil.php` dan menekan Change. | Berkas diunggah ke `image/profile.jpg` dan halaman ter-refresh menampilkan foto baru. | Berkas terunggah sukses tanpa notifikasi error. | **PASS** |
| **TC-044** | Upload Foto Profil Format JPEG | Memilih berkas foto bermformat `.jpeg` di `profil.php` dan menekan Change. | Berkas diunggah ke `image/profile.jpg` dan halaman ter-refresh menampilkan foto baru. | Berkas terunggah sukses tanpa notifikasi error. | **PASS** |
| **TC-045** | Upload Foto Profil Format PNG | Memilih berkas foto bermformat `.png` di `profil.php` dan menekan Change. | Sistem menolak berkas dan menampilkan pesan error pembatasan ekstensi file. | Tampil pesan error *Ekstensi tidak diijinkan. Hanya menerima file JPG/JPEG*. | **PASS** |
| **TC-046** | Upload Foto Profil Berkas PDF | Memilih dokumen bermformat `.pdf` di `profil.php` dan menekan Change. | Sistem menolak berkas dan menampilkan pesan error pembatasan ekstensi file. | Tampil pesan error *Ekstensi tidak diijinkan. Hanya menerima file JPG/JPEG*. | **PASS** |
| **TC-047** | Upload Ekstensi Huruf Besar | Upload berkas gambar bermformat `AVATAR.JPG` / `AVATAR.JPEG` di `profil.php`. | Sistem melakukan konversi `strtolower()` dan mengizinkan pengunggahan foto profil. | Penanganan ekstensi `end(explode())` peka huruf (*case-sensitive*), file `.JPG` ditolak. | **FAIL** *(Extension Logic Bug)* |
| **TC-048** | Upload Double Extension | Upload berkas `avatar.jpg.png` dengan ekstensi ganda di `profil.php`. | Sistem memeriksa ekstensi paling akhir (`.png`) dan memblokir pengunggahan. | Ekstensi `.png` di bagian akhir terdeteksi dan sistem menolak upload file. | **PASS** |
| **TC-049** | Upload Berkas Kosong (0-Byte) | Upload berkas kosong 0-byte ber-ekstensi `.jpg` di `profil.php`. | Sistem memeriksa ukuran berkas `filesize > 0` dan menolak berkas kosong. | Berkas terunggah tetapi berukuran 0-byte. Terdeteksi tidak ada validasi minimal ukuran file. | **FAIL** *(Validation Flaw)* |
| **TC-050** | Submit Upload Profil Tanpa File | Menekan tombol *Change* tanpa memilih berkas file pada form `profil.php`. | Sistem tidak melakukan tindakan upload dan tetap pada halaman profil. | Halaman Profil di-reload tanpa perubahan file foto. | **PASS** |

---

## 4. Cara Menjalankan Otomasi Pengujian

### Prasyarat:
* PHP 8.2+
* Python 3.11+
* MySQL / MariaDB Server

### Langkah-langkah:
1. **Clone Repositori**:
   ```bash
   git clone https://github.com/ecotank/UAS-DamnCRUD-Alba.git
   cd UAS-DamnCRUD-Alba
   ```
2. **Install Dependensi Python**:
   ```bash
   pip install pytest pytest-xdist selenium webdriver-manager
   ```
3. **Jalankan PHP Web Server & Import Database**:
   ```bash
   # Jalankan MySQL Service (Port 3306) & Import db/damncrud.sql ke database badcrud
   php -S 127.0.0.1:8000
   ```
4. **Eksekusi Pengujian Pytest**:
   ```bash
   python -m pytest tests/test_damncrud.py -v -n 2
   ```

---
*Dikembangkan oleh Taruna Madya Satria Alba Pramasha (III RPLK) - Politeknik Siber dan Sandi Negara.*
