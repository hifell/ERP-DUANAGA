# Setup Guide - Duanaga ERP Telegram Bot

## Prerequisites

1. Telegram Bot Token (already obtained: @DuanagaERPBot)
2. n8n running on http://localhost:5678
3. Odoo running on http://localhost:8069

## Setup Steps

### Step 1: Verify n8n Running
```bash
curl http://localhost:5678
# Should return 200
```

### Step 2: Create n8n Credentials

1. Buka http://localhost:5678
2. Login: admin / Duanaga@2024
3. Klik **Settings** → **Credentials**
4. Klik **Add Credential**
5. Search: **Telegram Bot API**
6. Klik **Create New Credential**
7. Name: `telegram-bot-credentials`
8. Bot Token: `8876187198:AAE2SiE33qCzFGSC3-xt5cszkIonO3CKFMY`
9. **Save**

### Step 3: Import Workflow

1. Buka http://localhost:5678
2. Klik **Workflows**
3. Klik **Import from File**
4. Pilih file: `duanaga-telegram-main.json`
5. Workflow akan muncul

### Step 4: Activate Workflow

1. Buka workflow yang baru di-import
2. Klik **Activate** (tombol toggle di pojok kanan atas)
3. Workflow sekarang listening untuk Telegram messages

### Step 5: Set Webhook

Workflow menggunakan polling mode, tidak perlu webhook manual.

---

## Test Bot

1. Buka Telegram
2. Search: **@DuanagaERPBot**
3. Klik **Start**
4. Bot akan reply dengan welcome message

---

## Available Commands

| Command | Description |
|---------|-------------|
| /start | Welcome message |
| /help | Help & usage |
| /stock [product_name] | Cek stock produk |
| /qc | Input QC results (coming soon) |
| /order | Buat Sales Order (coming soon) |
| /summary | Daily summary (coming soon) |

---

## Troubleshooting

### Bot tidak respons?
1. Cek workflow activated
2. Cek credentials correct
3. Cek n8n running

### Error credentials?
1. Settings → Credentials
2. Edit Telegram credentials
3. Verify bot token

---

## File Structure

```
telegram-bot/
├── workflows/
│   ├── telegram-base.json      # Base template
│   └── duanaga-telegram-main.json # Main workflow
├── .env                        # Environment variables
└── README.md                   # This file
```
