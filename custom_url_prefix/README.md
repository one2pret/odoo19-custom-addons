$readme = @'
# Custom URL Prefix Odoo 19

**Module Name:** `custom_url_prefix`
**Version:** 19.0.1.0.0
**Author:** (Custom/Internal)

---

## 1. Pendahuluan

Modul ini bertujuan untuk menyederhanakan dan merapikan struktur URL utama pada Odoo 19. Secara *default*, *web client* Odoo menggunakan awalan (`prefix`) `/odoo/` untuk hampir semua aplikasinya (contoh: `http://localhost:8069/odoo/discuss`). 

Dengan modul `custom_url_prefix`, URL disederhanakan dengan menghapus kata `/odoo` sehingga menjadi lebih ramah pengguna (contoh: `http://localhost:8069/discuss`).

## 2. Penjelasan Teknis & Arsitektur

Karena sejak Odoo 17 (termasuk Odoo 19) sistem navigasi *frontend* sudah dialihkan sepenuhnya ke *client-side router* berbasis **Owl** (bukan sekadar navigasi halaman statis klasik), trik *redirect* server 301/302 biasa di Python tidak lagi cukup. Mengganti URL server saja akan ditimpa ulang oleh *router JavaScript* di peramban yang melakukan *hardcode* `/odoo`.

Oleh karena itu, modul ini menggunakan dua pendekatan secara paralel:

### A. Server-Side Controller (Python)
File: `controllers/home.py`

Modul ini menimpa (`override`) kelas `Home` bawaan Odoo. Kita mendefinisikan *route* statis untuk aplikasi-aplikasi yang sering digunakan (contoh: `/discuss`, `/inventory`, `/calendar`, dll) dengan metode `@http.route`.
Alih-alih melakukan *redirect* (yang membuat URL berganti), metode ini langsung me-*render* keseluruhan `web_client`. 
- **Tujuan:** Agar saat pengguna mengetik URL bersih langsung dari luar, server Odoo tidak mengembalikan *Error 404 Not Found*. Server langsung mengirim kerangka aplikasi web.

### B. Client-Side Router Patch (JavaScript)
File: `static/src/js/custom_router.js`

Modul ini melakukan *monkey-patch* (menimpa fungsi inti secara dinamis pada saat *runtime*) terhadap layanan *router* Owl bawaan Odoo (`@web/core/browser/router`). Ada dua fungsi utama yang diubah:
1.  **`router.stateToUrl(state)`**: Ini adalah fungsi yang dipanggil Odoo ketika kamu mengklik menu. Odoo menghasilkan URL seperti `/odoo/discuss`. *Patch* kita mencegat URL hasil *generate* ini dan menghapus teks `/odoo` sebelum menampilkannya ke *Address Bar* peramban.
2.  **`router.urlToState(urlObj)`**: Ini adalah kebalikannya; dipanggil saat kamu me-*refresh* halaman atau menempel URL bersih (misal `/discuss`) dan router perlu memahami kamu sedang membuka aplikasi apa. *Patch* ini akan mengelabui Odoo dengan menambahkan kembali `/odoo` secara gaib (`/odoo/discuss`) sebelum URL tersebut diurai, karena mesin internal router tidak tahu apa itu `/discuss`.

---

## 3. Rencana Kerja (Roadmap) & Rencana Pemeliharaan

Karena pendekatan modul ini cukup "agresif" (*monkey-patching core function*), ada beberapa langkah lanjutan dan rencana pemeliharaan yang perlu diperhatikan:

### Fase 1: Identifikasi Menu/Aplikasi
- **Status:** Selesai (Versi Awal).
- **Kendala saat ini:** Modul ini baru memuat *route* statis untuk beberapa aplikasi dasar (`/discuss`, `/inventory`, `/calendar`, `/contacts`, `/sales`).
- **Tindakan:** Jika ada aplikasi baru yang dipasang, pengembang **wajib** mendaftarkan aplikasinya di `controllers/home.py`. Jika tidak, mengetik `/purchase` secara manual dari *address bar* akan mengembalikan 404.

### Fase 2: Dynamic Route Handling (Eksplorasi)
- **Tujuan:** Menghindari *hardcoding* jalur satu-per-satu di `controllers/home.py`.
- **Rencana:** Menyelidiki apakah memungkinkan membuat *catch-all route* atau mendeteksi daftar aplikasi secara dinamis berdasarkan modul yang terinstal.
- **Risiko:** Pendekatan *catch-all route* (`/<path:path>`) sangat berisiko di Odoo karena akan menabrak rute bawaan (`/web`, rute-rute *Website* (`website`), *eCommerce*, dll).
- **Langkah Kerja:** Mencoba membuat rute dinamis yang divalidasi terhadap modul (`ir.module.module`) dan izin baca model.

### Fase 3: Kompatibilitas dengan Progressive Web App (PWA)
- **Tujuan:** Memastikan PWA/Offline mode berjalan.
- **Rencana:** *Service Worker* Odoo dan `manifest.webmanifest` secara bawaan menargetkan *scope* `/odoo`.
- **Langkah Kerja:** Memeriksa apakah `webmanifest.py` dan `service_worker.js` perlu di-*patch* agar mendeteksi struktur URL *root* (`/`) dan memuat aset *offline* dengan benar.

## 4. Kelemahan dan Peringatan (Risks)

Sebelum menggunakan modul ini dalam mode **Produksi**, pahami risiko berikut:
1.  **Tabrakan Rute Rute Kustom:** Pastikan nama aplikasi di Odoo (misal `/shop`) tidak bentrok dengan modul *website_sale*. Jika website Odoo aktif, rute Odoo *backend* dan rute *frontend* (portal) bisa beririsan.
2.  **Pembaruan Versi Odoo Minor/Major:** Karena kita melakukan *monkey-patching* pada file JavaScript inti `router.js`, jika struktur kode asli Odoo di-update pada rilis minor (misal dari 19.0.1 ke 19.0.2), ada kemungkinan *patch* JavaScript ini akan rusak dan aplikasi macet (layar kosong/putih). Selalu uji modul ini di sistem percobaan (*Staging/Test Environment*) sebelum memperbarui Odoo.
3.  **Ketergantungan Rute Manual:** Harus menambah URL di controller python setiap pasang App baru.

---

**Terakhir Diperbarui:** 29 April 2026
**Lingkungan Odoo:** Odoo v19.0
'@
Set-Content -Path "D:\2026\Project\odoo\odoo19\odoo19-custom-addons\custom_url_prefix\README.md" -Value $readme -Encoding UTF8
