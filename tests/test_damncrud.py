import pytest
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = os.environ.get("BASE_URL", "http://127.0.0.1:8000")

def test_tc003_add_new_contact(logged_in_driver):
    """TC-012: Pengujian Fungsional Tambah Kontak Baru (Create Contact)"""
    driver = logged_in_driver
    unique_name = f"AutoContact_{int(time.time())}"
    
    # 1. Navigasi ke form tambah kontak
    add_btn = driver.find_element(By.CLASS_NAME, "create-contact")
    add_btn.click()
    time.sleep(1)
    
    assert "Add new contact" in driver.title
    
    # 2. Pengisian data kontak baru
    driver.find_element(By.ID, "name").send_keys(unique_name)
    driver.find_element(By.ID, "email").send_keys("auto.test@example.com")
    driver.find_element(By.ID, "phone").send_keys("081299887766")
    driver.find_element(By.ID, "title").send_keys("Automation Tester")
    
    # 3. Submit form
    driver.find_element(By.XPATH, "//input[@type='submit']").click()
    time.sleep(1)
    
    # 4. Verifikasi kontak muncul di Dashboard via DataTables Search
    assert "Dashboard" in driver.title
    search_input = driver.find_element(By.XPATH, "//input[@type='search']")
    search_input.clear()
    search_input.send_keys(unique_name)
    time.sleep(0.5)
    assert unique_name in driver.page_source

def test_tc004_update_contact(logged_in_driver):
    """TC-032: Pengujian Fungsional Perbarui Data Kontak (Update Contact)"""
    driver = logged_in_driver
    updated_name = f"UpdatedUser_{int(time.time())}"
    
    # 1. Buka form edit kontak ID 2 agar tidak bertabrakan dengan ID 1
    driver.get(f"{BASE_URL.rstrip('/')}/update.php?id=2")
    time.sleep(1)
    
    assert "Change contact" in driver.title
    
    # 2. Ubah nama kontak
    name_field = driver.find_element(By.ID, "name")
    name_field.clear()
    name_field.send_keys(updated_name)
    
    # 3. Submit update
    driver.find_element(By.XPATH, "//input[@type='submit']").click()
    time.sleep(1)
    
    # 4. Verifikasi data berhasil diperbarui via DataTables Search
    assert "Dashboard" in driver.title
    search_input = driver.find_element(By.XPATH, "//input[@type='search']")
    search_input.clear()
    search_input.send_keys(updated_name)
    time.sleep(0.5)
    assert updated_name in driver.page_source

def test_tc005_delete_contact(logged_in_driver):
    """TC-038: Pengujian Fungsional Hapus Kontak (Delete Contact)"""
    driver = logged_in_driver
    target_id = 12
    
    # 1. Akses halaman delete kontak ID 12
    driver.get(f"{BASE_URL.rstrip('/')}/delete.php?id={target_id}")
    time.sleep(1)
    
    # 2. Pastikan di-redirect ke Dashboard setelah penghapusan
    assert "Dashboard" in driver.title
    
    # 3. Verifikasi kontak ID 12 tidak ditemukan di form edit
    driver.get(f"{BASE_URL.rstrip('/')}/update.php?id={target_id}")
    time.sleep(1)
    assert "doesn't exist" in driver.page_source.lower()

def test_tc006_upload_profile_image(logged_in_driver, tmp_path):
    """TC-043: Pengujian Fungsional Upload Foto Profil JPG (Upload Profile)"""
    driver = logged_in_driver
    
    # 1. Navigasi ke halaman Profil
    profil_btn = driver.find_element(By.XPATH, "//a[contains(@href, 'profil.php')]")
    profil_btn.click()
    time.sleep(1)
    
    assert "Profil" in driver.title
    
    # 2. Buat file dummy JPG valid secara dinamis
    sample_jpg = tmp_path / "test_avatar.jpg"
    sample_jpg.write_bytes(b"\xFF\xD8\xFF\xE0\x00\x10JFIF\x00\x01\x01\x01\x00`\x00`\x00\x00\xFF\xD9")
    
    # 3. Upload berkas via form file input
    file_input = driver.find_element(By.ID, "formFile")
    file_input.send_keys(str(sample_jpg))
    
    # 4. Submit Change
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(1)
    
    # 5. Verifikasi pengunggahan sukses
    assert "Profil" in driver.title
    assert "Ekstensi tidak diijinkan" not in driver.page_source

def test_tc007_vpage_functional_submission(logged_in_driver):
    """TC-008: Pengujian Fungsional Form Submission VPage"""
    driver = logged_in_driver
    
    # 1. Navigasi ke VPage
    vpage_btn = driver.find_element(By.XPATH, "//a[contains(@href, 'vpage.php')]")
    vpage_btn.click()
    time.sleep(1)
    
    assert "Dummy Page XSS Detect" in driver.page_source
    
    # 2. Input text biasa
    test_text = "Testing Functional Output"
    thing_input = driver.find_element(By.NAME, "thing")
    thing_input.send_keys(test_text)
    
    # 3. Submit form
    driver.find_element(By.NAME, "submit").click()
    time.sleep(1)
    
    # 4. Verifikasi teks terefleksi di halaman
    assert f"Your thing is {test_text}" in driver.page_source
