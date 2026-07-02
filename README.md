# AutomationExercise Selenium Python

[![CI](https://github.com/abdlgoni/automationexercise-selenium-python/actions/workflows/test.yml/badge.svg)](https://github.com/abdlgoni/automationexercise-selenium-python/actions/workflows/test.yml)

Framework otomasi UI untuk [AutomationExercise](https://www.automationexercise.com/) menggunakan Selenium dan Pytest, dibangun dengan pendekatan yang dekat dengan praktik industri: pemisahan logika test dari halaman aplikasi, manajemen browser yang konsisten, dan pelaporan yang memudahkan debugging.

---

## Cakupan Testing

| File | Skenario | Status |
|---|---|---|
| `tests/test_authentication.py` | Registrasi, login valid/invalid, logout, duplicate email | Passed |
| `tests/test_add_product_to_cart.py` | Tambah produk ke keranjang, verifikasi isi keranjang | Passed |
| `tests/test_contact_form.py` | Submit form kontak dengan file upload | Passed |
| `tests/test_place_order.py` | Checkout dengan registrasi saat proses order | Passed |
| `tests/test_product.py` | Verifikasi daftar produk dan detail produk | Passed |
| `tests/test_product_quantity.py` | Validasi perubahan kuantitas di keranjang | Passed |
| `tests/test_search_product.py` | Pencarian produk berdasarkan kata kunci | Passed |
| `tests/test_testcasepage.py` | Akses dan verifikasi halaman Test Cases | Passed |
| `tests/test_verify_subscription.py` | Subscription dari homepage, cart, dan product page | Passed |

**15 test**, semua passed pada run CI terbaru.

---

## Tech Stack

- Python 3.9+
- Selenium WebDriver + WebDriver Manager
- Pytest + pytest-html
- Faker — generate data akun unik per test run
- python-dotenv — konfigurasi environment

---

## Arsitektur

```
automationexercise-selenium-python/
├── pages/               # Page Object per halaman aplikasi
├── tests/               # Test case dan fixtures pytest
│   └── conftest.py      # WebDriver lifecycle dan registered_account fixture
├── utils/
│   ├── config.py        # Baca env var, konstanta timeout dan path
│   ├── driver_factory.py
│   └── data_generator.py
├── reports/             # HTML report, screenshot on failure, JUnit XML
├── logs/
└── .github/workflows/
    └── test.yml
```

### Keputusan Desain

**Page Object Model** — locator dan interaksi halaman dipisahkan dari logika test. Perubahan selector UI hanya perlu diperbaiki di satu kelas, bukan di setiap test yang menggunakannya.

**Driver lifecycle di conftest.py** — WebDriver dibuat dan ditutup per test melalui fixture `scope="function"`. Ini menjaga isolasi antar test dan memastikan tidak ada state browser yang bocor ke test berikutnya.

**`registered_account` fixture** — test yang membutuhkan akun valid menggunakan fixture ini, bukan hardcoded credential. Fixture register akun baru dengan data random sebelum test, dan melakukan fallback delete di teardown. Ini menghilangkan ketergantungan pada akun manual yang bisa terhapus kapan saja.

**Persistent account via env var** — `test_logout_user` dan `test_signup_existing_email` menggunakan `TEST_EMAIL` dan `TEST_PASSWORD` dari environment. Akun ini tidak pernah didelete oleh test manapun — test yang membutuhkan akun yang sudah terdaftar bergantung pada keberadaan akun ini.

**Faker untuk test data** — email dan data registrasi digenerate dinamis untuk menghindari konflik duplicate email saat test dijalankan berulang kali.

**Config terpusat** — timeout, path, dan konfigurasi browser dibaca dari `Config` class. Nilai default tersedia sehingga test bisa jalan tanpa `.env`, kecuali untuk skenario yang membutuhkan persistent account.

---

## Setup

### Prasyarat

- Python 3.9+
- Google Chrome (versi terbaru)

### Instalasi

```bash
git clone https://github.com/abdlgoni/automationexercise-selenium-python.git
cd automationexercise-selenium-python

python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### Konfigurasi

Salin template environment dan isi nilainya:

```bash
# Windows
copy .env.example .env

# Mac/Linux
cp .env.example .env
```

Isi `.env` dengan nilai yang sesuai — lihat tabel Environment Variables di bawah.

---

## Menjalankan Test

```bash
# Suite lengkap dengan HTML report
pytest -v --html=reports/html_reports/report.html --self-contained-html

# Headless mode
pytest -v --headless --html=reports/html_reports/report.html --self-contained-html

# Modul tertentu
pytest tests/test_authentication.py -v

# Output ringkas untuk CI
pytest -q --junitxml=reports/pytest-results.xml
```

---

## Environment Variables

| Variable | Deskripsi | Required | Lokal | CI |
|---|---|---|---|---|
| `BROWSER` | Browser yang dipakai (`chrome`, `firefox`) | Optional | `.env` | Hardcode di workflow |
| `HEADLESS` | Jalankan browser headless (`true`/`false`) | Optional | `.env` | `true` di workflow |
| `TEST_EMAIL` | Email persistent account untuk skenario auth | Required* | `.env` | GitHub Secret |
| `TEST_PASSWORD` | Password persistent account | Required* | `.env` | GitHub Secret |

*Required untuk `test_logout_user` dan `test_signup_existing_email`. Test lain tidak bergantung pada variabel ini.

> **Catatan:** `TEST_EMAIL` dan `TEST_PASSWORD` merujuk ke akun yang dibuat manual dan tidak boleh didelete oleh test manapun. Akun ini dipakai sebagai persistent fixture — bukan sebagai akun yang dirotasi per run.

---

## Known Issues

**Encoding log di Windows** — output console dapat menampilkan karakter tidak terbaca ketika log berisi simbol non-ASCII. Fungsi test tidak terpengaruh. Perbaikan direncanakan dengan mengubah format log ke ASCII-safe.

---

## Roadmap

- [ ] Parallel test execution untuk mengurangi waktu eksekusi
- [ ] Assertion lebih spesifik pada skenario cart dan checkout
- [ ] Dukungan multi-environment (staging vs production)

---

## Proyek Terkait

- [Playwright TypeScript Framework](https://github.com/abdlgoni/automationplaywright) — framework E2E dengan CI/CD, storage state, dan custom fixtures
- [Manual QA Portfolio](https://github.com/abdlgoni/qa-portfolio-sauce-demo) — 18 test case manual dengan bug report dan UX improvement report
