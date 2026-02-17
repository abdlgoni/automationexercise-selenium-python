# Automation

Sebuah proyek otomasi pengujian menggunakan pytest dan WebDriver.

## Deskripsi

- Struktur untuk pengujian otomatis: halaman (`pages/`), utilitas (`utils/`), dan tes (`tests/`).
- Termasuk konfigurasi `pytest.ini`, `requirements.txt`, dan factory driver.

## Persyaratan

- Python 3.8+
- Paket pada `requirements.txt`

## Instalasi

1. Buat virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Menjalankan Tes

```powershell
pytest -q
```

Untuk membuat laporan HTML (jika tersedia):

```powershell
pytest --html=reports/html_reports/report.html
```

## Struktur Proyek

- `pages/` : Page object classes
- `tests/` : Test cases
- `utils/` : Config, driver factory
- `logs/`, `reports/`, `screenshots/` : Output runtime
