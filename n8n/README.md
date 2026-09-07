# N8N WORKFLOWS - PT DUA NAGA KOSMETINDO

## CARA IMPORT

1. Buka `http://localhost:5678`
2. Login: `admin@duanaga.co.id` / `Duanaga@2024`
3. Klik **"+ New Workflow"**
4. Klik **menu (3 dots)** di workflow
5. Pilih **"Import from JSON"**
6. Copy-paste content dari file `.json`
7. Atau klik **"Import from URL"** (kalau ada)

---

## WORKFLOWS YANG TERSEDIA

| File | Nama | Trigger | Fungsi |
|------|------|---------|--------|
| wf1-lead-capture.json | Lead Capture | HTTP POST /webhook/lead | Terima lead dari website |
| wf2-daily-report.json | Daily Report | Schedule 08:00 | Report harian ke WA |
| wf3-low-stock-alert.json | Low Stock Alert | Schedule 09:00 | Alert stok rendah |
| wf4-so-confirmed.json | SO Confirmed | HTTP POST /webhook/so-confirmed | Alert Production |
| wf5-delivery-done.json | Delivery Done | HTTP POST /webhook/delivery-done | Notify Customer |

---

## SETUP SEBELUM PAKAI

### 1. Setup Telegram Bot

1. Buka `@BotFather` di Telegram
2. Ketik `/newbot`
3. Ikuti instruksi, dapat **BOT TOKEN**
4. Buat group, add bot, get **GROUP ID**

**Get Group ID:**
- Add `@userinfobot` ke group
- Kirim pesan di group
- Bot akan show GROUP ID

### 2. Update Workflow

Ganti `chatId` dengan ID group kamu:
```
chatId: "=-1001234567890"
         ^^^^^^^^^^^^^^^^^
         Ganti dengan ID group kamu
```

### 3. Setup Odoo Connection

Pastikan endpoint Odoo accessible dari container:
```
http://erp_duanaga_odoo:8069/xmlrpc/2/object
```

---

## TEST WORKFLOW

1. Klik workflow
2. Klik **"Test workflow"**
3. Kirim test data (POST request)
4. Cek apakah berhasil

**Test Lead Capture:**
```bash
curl -X POST http://localhost:5678/webhook/lead \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Client",
    "email": "test@email.com",
    "phone": "+628123456789",
    "product": "Private Label Serum",
    "quantity": "500 pcs"
  }'
```

---

## ACTIVATE WORKFLOW

1. Buka workflow
2. Toggle switch di **kanan atas** → hijau
3. Workflow akan jalan otomatis sesuai trigger

---

## LOGS

**Lihat logs:**
1. Buka workflow
2. Klik **"Executions"** tab
3. Lihat history & error

---

## TROUBLESHOOTING

### Workflow tidak jalan?
- Check toggle switch → harus ON (hijau)
- Check logs di "Executions" tab
- Test manual dengan "Test workflow"

### Odoo connection error?
- Pastikan container `erp_duanaga_odoo` running
- Check network: `docker network ls`

### Telegram tidak kirim?
- Check BOT TOKEN
- Check GROUP ID
- Bot harus jadi member group

---

## CUSTOMIZE

### Ganti WA dengan WhatsApp API

Replace node Telegram dengan:
- **UltraMsg node**
- **Twilio node**
- **Fonnte API node**

### Ganti schedule

Edit cron expression:
```
0 8 * * * = Every day 08:00
0 9 * * 1 = Every Monday 09:00
*/15 * * * * = Every 15 minutes
```

---

## FILE STRUCTURE

```
n8n/
├── wf1-lead-capture.json
├── wf2-daily-report.json
├── wf3-low-stock-alert.json
├── wf4-so-confirmed.json
├── wf5-delivery-done.json
└── README.md (this file)
```

---

*Last Updated: 2026-09-05*
