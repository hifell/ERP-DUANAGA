# PLANNING: TELEGRAM BOT INTEGRATION
## PT Dua Naga Kosmetindo

**Tanggal:** 14 September 2026
**Status:** PLANNING

---

## 1. YANG BISA DI TELEGRAM (MOBILE INPUT)

### Scope: Quick Input & Notifications

```
┌─────────────────────────────────────────────────────────┐
│                  TELEGRAM BOT                           │
│                                                         │
│  ✅ CEK / INPUT (Langsung dari HP)                     │
│  ───────────────────────────────────────────────────    │
│                                                         │
│  📦 STOCK                                              │
│  • Cek stock produk                                     │
│  • Low stock alert                                      │
│  • Stock opname (simple)                                 │
│                                                         │
│  📋 SALES                                              │
│  • Buat Sales Order (simple)                            │
│  • Cek status order                                     │
│  • Track delivery                                       │
│                                                         │
│  🏭 QC                                                 │
│  • Input hasil QC (pH, viscosity)                      │
│  • Lihat status QC                                     │
│  • Notifikasi hasil QC                                  │
│                                                         │
│  📥 PURCHASE                                            │
│  • Input receipt (terima barang)                        │
│  • Lihat status PO                                     │
│                                                         │
│  🏭 MANUFACTURING                                       │
│  • Lihat status MO                                      │
│  • Production complete (simple)                         │
│                                                         │
│  📊 NOTIFICATIONS                                       │
│  • Daily summary                                        │
│  • Alert low stock                                      │
│  • Alert QC result                                      │
│  • Alert delivery overdue                               │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 2. YANG TETAP DI ODOO WEB

### Complex Input / Setup (Pakai Browser)

```
┌─────────────────────────────────────────────────────────┐
│                  ODOO WEB UI                            │
│                                                         │
│  ⚙️ SETUP & KONFIGURASI                               │
│  ───────────────────────────────────────────────────    │
│                                                         │
│  🏭 MANUFACTURING                                      │
│  • Buat BoM baru                                       │
│  • Setup routing & workcenter                           │
│  • Konfigurasi bill of materials                        │
│                                                         │
│  📦 PRODUCT                                             │
│  • Setup produk baru (detail)                           │
│  • Konfigurasi price list                               │
│  • Setup attributes & variants                          │
│                                                         │
│  👥 CRM / LEADS                                        │
│  • Manage leads & opportunities                         │
│  • Setup sales pipeline                                 │
│  • Email templates                                     │
│                                                         │
│  📊 ACCOUNTING                                         │
│  • Setup chart of accounts                              │
│  • Journal entries                                      │
│  • Financial reports                                    │
│  • Invoice reconciliation                               │
│                                                         │
│  🔧 SETTINGS                                           │
│  • User management                                      │
│  • Security & access rights                             │
│  • Workflow automation setup                             │
│  • Module installation                                  │
│                                                         │
│  📈 REPORTS (COMPLEX)                                  │
│  • Profit & Loss detailed                               │
│  • Inventory valuation report                           │
│  • Production cost analysis                             │
│  • Custom reports builder                               │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 3. PERBANDINGAN: TELEGRAM vs ODOO

| Task | Telegram | Odoo Web | Alasan |
|------|----------|----------|--------|
| Cek stock | ✅ | ✅ | Telegram lebih cepat |
| Input QC hasil | ✅ | ✅ |QC sering di lab/field |
| Buat SO simple | ✅ | ✅ | Quick sales |
| Buat SO complex (discount bertingkat) | ❌ | ✅ | Need form detail |
| Buat BoM | ❌ | ✅ | Many fields |
| Terima barang | ✅ | ✅ | Gudang staff mobile |
| Buat invoice | ❌ | ✅ | Need tax calculation |
| Cek report | ❌ | ✅ | Complex data |
| Daily alert | ✅ | ❌ | Notifikasi push |

---

## 4. WORKFLOW YANG AKAN DIBUAT

### Total: 10 Workflows

```
┌─────────────────────────────────────────────────────────┐
│  WORKFLOWS TELEGRAM                                    │
└─────────────────────────────────────────────────────────┘

📦 INVENTORY (2)
─────────────────────────────────────────────────────────
1. /stock      - Cek stock produk
2. /lowstock   - Lihat low stock & alerts

📋 SALES (2)
─────────────────────────────────────────────────────────
3. /order      - Buat Sales Order simple
4. /track      - Track status delivery

🧪 QC (2)
─────────────────────────────────────────────────────────
5. /qc         - Input hasil QC (pH, viscosity)
6. /qclist     - Lihat list QC decisions

📥 PURCHASE (2)
─────────────────────────────────────────────────────────
7. /receive    - Input receipt barang
8. /postatus   - Cek status Purchase Order

🏭 MANUFACTURING (1)
─────────────────────────────────────────────────────────
9. /mostatus   - Lihat status Manufacturing Order

📊 NOTIFICATIONS (1)
─────────────────────────────────────────────────────────
10. /summary    - Daily summary notification
```

---

## 5. COMMAND LIST

```
═══════════════════════════════════════════════════════════
📋 DAFTAR COMMAND TELEGRAM BOT
═══════════════════════════════════════════════════════════

📦 INVENTORY
─────────────────────────────────────────────────────────
/stock              - Cek stock produk
/lowstock          - Produk low stock & alert

📋 SALES
─────────────────────────────────────────────────────────
/order              - Buat Sales Order
/track              - Track delivery

🧪 QC
─────────────────────────────────────────────────────────
/qc                 - Input hasil QC lab
/qclist             - Lihat list QC decisions

📥 PURCHASE
─────────────────────────────────────────────────────────
/receive            - Input terima barang
/postatus          - Cek status PO

🏭 MANUFACTURING
─────────────────────────────────────────────────────────
/mostatus           - Cek status MO

📊 INFO
─────────────────────────────────────────────────────────
/start              - Welcome message
/help               - Bantuan
/summary            - Daily summary

═══════════════════════════════════════════════════════════
```

---

## 6. CONTOH FLOW

### 6.1 Cek Stock (/stock)
```
User: /stock
Bot: "Ketik nama product:"

User: "Sabun GlowUp"
Bot: "─────────────────────────────────"
Bot: "📦 Sabun Wajah GlowUp"
Bot: "─────────────────────────────────"
Bot: "Stock: 1.250 pcs"
Bot: "Reserved: 500 pcs"
Bot: "Available: 750 pcs"
Bot: "─────────────────────────────────"
Bot: "[Cek Produk Lain] [🔙 Menu]"
```

### 6.2 Input QC (/qc)
```
User: /qc
Bot: "Batch/LOT Number:"

User: "LOT-2026-0914-001"
Bot: "pH Level (5.5-6.5):"

User: "6.1"
Bot: "Viscosity (1.05-1.10):"

User: "1.07"
Bot: "─────────────────────────────────"
Bot: "✅ QC: PASSED"
Bot: "pH: 6.1 ✅  Viscosity: 1.07 ✅"
Bot: "─────────────────────────────────"
Bot: "MO: Done, Stock: +500 pcs"
```

### 6.3 Buat Order (/order)
```
User: /order
Bot: "Customer:"

User: "Toko Melawai"
Bot: "Product:"

User: "Sabun GlowUp"
Bot: "Qty:"

User: "100"
Bot: "─────────────────────────────────"
Bot: "📋 ORDER"
Bot: "Toko Melawai"
Bot: "Sabun GlowUp x 100pcs"
Bot: "Total: Rp 2.500.000"
Bot: "─────────────────────────────────"
Bot: "[✅ Confirm] [❌ Cancel]"
```

---

## 7. YANG TIDAK PERLU DI TELEGRAM

### Skip untuk Phase 1:

```
❌ NOT PRIORITY / CAN WAIT:

• /invoice    - Invoice complex, tetap di Odoo
• /bo m       - BoM setup, butuh banyak field
• /reports    - Complex reports, di Odoo aja
• /leads      - CRM manage, di Odoo aja
• /users      - User setup, admin only
• /settings   - System config, admin only
• /accounts   - Accounting, complex
• /rfq        - Bisa tapi complex, deferred
• /mo-create  - Deferred, need BoM selection
```

---

## 8. TIMELINE

```
┌─────────────────────────────────────────────────────────┐
│  WEEK 1: Setup & Core                                  │
├─────────────────────────────────────────────────────────┤
│  Day 1: Buat Telegram Bot via @BotFather                 │
│  Day 2: Setup n8n Telegram node                         │
│  Day 3: Base workflow (/start, /help)                   │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  WEEK 2: Inventory & Sales                             │
├─────────────────────────────────────────────────────────┤
│  Day 4: /stock + /lowstock                             │
│  Day 5: /order                                          │
│  Day 6: /track                                          │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  WEEK 3: QC & Purchase                                  │
├─────────────────────────────────────────────────────────┤
│  Day 8:  /qc + /qclist                                 │
│  Day 9:  /receive                                       │
│  Day 10: /postatus                                     │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  WEEK 4: Manufacturing & Polish                        │
├─────────────────────────────────────────────────────────┤
│  Day 11: /mostatus                                     │
│  Day 12: /summary notification                         │
│  Day 13: Testing & bug fixes                            │
│  Day 14: Documentation & Go Live                        │
└─────────────────────────────────────────────────────────┘
```

---

## 9. YANG DIBUTUHKAN UNTUK MULAI

### Pre-Requisites:

```
Yang perlu dari kamu:

1. Telegram Bot Token
   ─────────────────────────────────────────────────────
   a. Buka Telegram
   b. Search: @BotFather
   c. Ketik: /newbot
   d. Beri nama: Duanaga ERP
   e. Beri username: DuanagaERPBOT (unique)
   f. Copy TOKEN yang diberikan
   
2. Konfirmasi proceed
```

---

## 10. ACCEPTANCE CRITERIA

### Done Jika:

```
✅ Bot bisa receive message
✅ /start reply dengan welcome
✅ /stock bisa query stock dari Odoo
✅ /qc bisa create QC decision di Odoo
✅ /order bisa create SO di Odoo
✅ Notifications terkirim via bot
✅ Error handling: user friendly message
```

---

## 11. NEXT STEP

```
Setelah Bot Token dapat:

1. Paste token di .env
2. Aku setup Telegram trigger di n8n
3. Test basic connectivity
4. Develop workflows satu per satu
```

---

## APPROVAL

```
□ Setuju - mulai development (butuh bot token dulu)
□ Revisi - specify perubahan
□ Cancel - tidak jadi
```

