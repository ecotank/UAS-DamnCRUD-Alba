# DamnCRUD - UAS Pengujian Perangkat Lunak (4 RPLK)

Repositori ini merupakan hasil pengerjaan **Ujian Akhir Semester (UAS) Mata Kuliah Pengujian Perangkat Lunak**, Program Studi Rekayasa Perangkat Lunak Kripto (4 RPLK), Politeknik Siber dan Sandi Negara (T.A. 2025/2026).

**URL Repositori GitHub Submission**: [https://github.com/ecotank/UAS-DamnCRUD-Alba](https://github.com/ecotank/UAS-DamnCRUD-Alba)

---

## 1. Perbedaan Proyek Original vs Repositori Baru

Berikut adalah perbandingan komprehensif antara repositori asal (`hermanka/DamnCRUD`) dengan repositori pengujian baru (`ecotank/UAS-DamnCRUD-Alba`):

| Komponen / Aspek | Repositori Original (`hermanka/DamnCRUD`) | Repositori Baru (`ecotank/UAS-DamnCRUD-Alba`) |
| :--- | :--- | :--- |
| **Arsitektur Pengujian** | Tidak memiliki skrip pengujian otomatis (0% Test Coverage). | Mengimplementasikan **50 Pure Functional Test Cases Matrix** + **Pytest + Selenium Automated E2E Suite**. |
| **Integrasi Pipeline CI/CD** | Belum ada integrasi pipeline CI/CD (Pengujian manual). | Dilengkapi **GitHub Actions Workflow** (`.github/workflows/ci.yml`) dengan eksekusi paralel `pytest -n auto`. |
| **Bug `create.php`** | Memiliki bug `Undefined variable $id` pada baris 17 (pemicu error runtime PHP). | **Fixed**: Menggunakan *explicit column naming* `INSERT INTO contacts (name, email, phone, title, created)`. |
| **Bug `update.php`** | **1.** Tidak ada proteksi sesi login.<br>**2.** Field Phone `value=""` (kosong, data lama hilang). | **1. Fixed**: Menambahkan `session_start()` & proteksi login.<br>**2. Fixed**: Memuat data lama `value="<?= $contact['phone'] ?>"`. |
| **Redirect Logic** | `header("location: ...")` tanpa `exit()`, menyebabkan skrip PHP tetap dieksekusi di belakang layar. | **Fixed**: Menambahkan fungsi `exit()` setelah setiap *location header redirect*. |
| **Dokumentasi & Laporan** | Berkas `README.md` minimalis (hanya kredensial login default). | Dilengkapi berkas lapor `.docx` otomatis (`build_docx.py`), dokumen lembar jawaban, dan `README.md` komprehensif. |

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
  1. `test_tc003_add_new_contact`: Otomasi penambahan kontak & verifikasi pencarian DataTables.
  2. `test_tc004_update_contact`: Otomasi pengubahan nama kontak & verifikasi update.
  3. `test_tc005_delete_contact`: Otomasi penghapusan kontak & konfirmasi JavaScript alert.
  4. `test_tc006_upload_profile_image`: Otomasi pengunggahan berkas profil JPG dinamis.
  5. `test_tc007_vpage_functional_submission`: Otomasi form submission & verifikasi perolehan output.

### C. Continuous Integration Pipeline (GitHub Actions)
Dikembangkan workflow `.github/workflows/ci.yml`:
* Menjalankan Service Container **MySQL 8.0** terisolasi di GitHub Runner.
* Menjalankan **PHP Built-in Server** pada `http://127.0.0.1:8000`.
* Menjalankan eksekusi pengujian secara **paralel** (`pytest -n auto`) menggunakan modul `pytest-xdist`.

---

## 3. Matriks Hasil Pengujian & Temuan Bug Fungsional

Berikut adalah ringkasan temuan pengujian fungsional pada aplikasi kode asli:

| ID Uji | Skenario Pengujian | Hasil yang Diharapkan | Hasil Aktual (Kode Asli) | Status Pengujian |
| :---: | :--- | :--- | :--- | :---: |
| **TC-018** | Penanganan Variabel `$id` pada `create.php` | Data tersimpan tanpa memicu error PHP runtime. | Error `Undefined variable $id` pada PHP 8. | **FAIL** *(Fixed)* |
| **TC-019** | Validasi Email Tanpa Simbol `@` | Form menolak format email `budi.example.com`. | Form ter-submit karena HTML menggunakan `type="text"`. | **FAIL** *(Validation Flaw)* |
| **TC-020** | Validasi Nomor Telepon Berisi Abjad | Form menolak string `ABCD-EFGH` pada field Phone. | Form menerima string abjad tanpa validasi numerik. | **FAIL** *(Validation Flaw)* |
| **TC-021** | Input Nama Berisi Spasi Kosong | Sistem menolak atau memotong spasi `'   '`. | Nama spasi tersimpan tanpa sanitasi `trim()`. | **FAIL** *(Sanitization Flaw)* |
| **TC-027** | Populasi Field Phone pada `update.php` | Form edit menampilkan nomor telepon lama. | Field Phone terisi `value=""` (kosong). | **FAIL** *(Fixed)* |
| **TC-047** | Upload File Ekstensi Huruf Besar (`.JPG`) | Sistem mengizinkan berkas `AVATAR.JPG`. | Ditolak karena check extension case-sensitive. | **FAIL** *(Logic Bug)* |
| **TC-049** | Upload File Gambar 0-Byte | Sistem menolak berkas 0-byte (`filesize > 0`). | File 0-byte terunggah tanpa validasi ukuran file. | **FAIL** *(Validation Flaw)* |

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
   pip install pytest pytest-xdist selenium webdriver-manager python-docx
   ```
3. **Jalankan PHP Web Server & Import Database**:
   ```bash
   # Jalankan MySQL Service (Port 3306) & Import db/damncrud.sql ke database badcrud
   php -S 127.0.0.1:8000
   ```
4. **Eksekusi Pengujian Paralel Pytest**:
   ```bash
   pytest tests/test_damncrud.py -v -n auto
   ```

---
*Dikembangkan oleh Mahasiswa Rekayasa Perangkat Lunak Kripto (4 RPLK) - Politeknik Siber dan Sandi Negara.*
