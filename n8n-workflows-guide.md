# N8N WORKFLOW GUIDE - PT DUA NAGA KOSMETINDO
## Maklon Cosmetics Automation

---

## WORKFLOW 1: Lead Capture dari Website
### Trigger: HTTP Request (POST)

```
Website Form → n8n Webhook → Create Lead di Odoo → Notif WA ke Marketing
```

**Webhook URL:** `http://localhost:5678/webhook/lead`

**Data yang diterima:**
```json
{
  "name": "Nama Client",
  "email": "email@client.com",
  "phone": "+628123456789",
  "company": "PT Contoh Indonesia",
  "product": "Private Label Face Serum",
  "quantity": "500 pcs",
  "message": "Ingin bikin produk skincare..."
}
```

**Steps:**
1. **Webhook** - Terima data dari website
2. **Code** - Parse & validate data
3. **Odoo Create Lead** - XML-RPC ke Odoo
4. **Telegram/WA** - Notif ke Marketing

---

## WORKFLOW 2: Follow-up Reminder (3 Hari)
### Trigger: Schedule (Every day 08:00)

```
Schedule → Search Leads (created > 3 days, no activity) → Notif Reminder
```

**Steps:**
1. **Schedule** - Every day at 08:00
2. **Odoo - Search** - Find leads with `date_open` > 3 days, `stage_id` = New
3. **IF** - Leads found > 0
4. **Telegram/WA** - "Reminder: {{count}} leads belum di-follow up!"
5. **Email** - Send to sales manager

---

## WORKFLOW 3: SO Confirmed → Alert Production
### Trigger: Odoo Webhook (Manual trigger dari Odoo)

```
SO Confirmed → Parse SO Data → Notif WA ke Production Team
```

**Trigger Data:**
```json
{
  "so_number": "SO/2026/00027",
  "customer": "Beauty Glow Indonesia",
  "products": ["Face Serum 500 pcs", "Body Lotion 300 pcs"],
  "expected_date": "2026-09-15"
}
```

**Steps:**
1. **Webhook** - Terima trigger dari Odoo
2. **Odoo - Read** - Get SO details
3. **Telegram/WA** - Notif ke Production:
   ```
   📦 NEW ORDER!
   
   SO: {{so_number}}
   Customer: {{customer}}
   Products: {{products}}
   Due Date: {{expected_date}}
   ```

---

## WORKFLOW 4: MO Completed → Alert QC & Sales
### Trigger: Odoo Webhook

```
MO Done → Parse Data → Notif QC → Notif Customer
```

**Steps:**
1. **Webhook** - MO completed
2. **Odoo - Read** - Get MO & linked SO
3. **Telegram/WA QC** - "MO {{mo_number}} completed, ready for QC"
4. **IF QC Passed** - Notif Sales: "Product ready for delivery"

---

## WORKFLOW 5: Delivery Completed → Notif Customer
### Trigger: Odoo Webhook

```
Delivery Validated → Get Delivery Details → Send WA to Customer
```

**Steps:**
1. **Webhook** - Delivery done
2. **Odoo - Read** - Get delivery + SO info
3. **Telegram/WA Customer** - 
   ```
   ✅ Delivery Confirmed
   
   Hi {{customer_name}}!
   
   Pesanan Anda telah kami kirim:
   {{products}}
   Jumlah: {{qty}}
   Resi: {{tracking_number}}
   
   Terima kasih atas kepercayaan Anda!
   - PT Dua Naga Kosmetindo
   ```

---

## WORKFLOW 6: Daily Report (Jam 8 pagi)
### Trigger: Schedule (Every day 08:00)

```
Schedule → Query Odoo → Summary Report → WA Group Management
```

**Steps:**
1. **Schedule** - Every day 08:00
2. **Odoo - Search** - SO created yesterday
3. **Odoo - Search** - MO completed yesterday
4. **Odoo - Search** - Delivery done yesterday
5. **Odoo - Search** - New leads yesterday
6. **Telegram/WA Group** -
   ```
   📊 DAILY REPORT - {{date}}
   
   📥 New Leads: {{leads_count}}
   📦 Sales Orders: {{so_count}}
   🏭 MO Completed: {{mo_count}}
   🚚 Deliveries: {{delivery_count}}
   
   Total Revenue (Est): Rp {{revenue}}
   
   #DuaNagaDailyReport
   ```

---

## WORKFLOW 7: Stok Alert (Low Stock)
### Trigger: Schedule (Every day 09:00)

```
Schedule → Check Stock Levels → IF < Min → Create PO + Alert
```

**Steps:**
1. **Schedule** - Every day 09:00
2. **Odoo - Read** - Get stock levels for BB (Vitamin C, Shea Butter, dll)
3. **IF** - Stock < minimum threshold
4. **Telegram/WA** - Alert Purchasing:
   ```
   ⚠️ LOW STOCK ALERT!
   
   {{material_name}}: {{current_stock}} {{uom}}
   Minimum: {{min_stock}}
   
   Silakan buat PO ke supplier!
   ```
5. **IF** - Critical (stock = 0)
6. **Odoo - Create PO** - Auto-generate PO

---

## WORKFLOW 8: Payment Reminder
### Trigger: Schedule (Every Monday 09:00)

```
Schedule → Find Overdue Invoices → Notif Customer
```

**Steps:**
1. **Schedule** - Every Monday 09:00
2. **Odoo - Search** - Invoices with `invoice_date_due` < today, `state` = open
3. **IF** - Overdue invoices found
4. **Telegram/WA** - 
   ```
   💰 PAYMENT REMINDER
   
   Hi {{customer_name}},
   
   Berikut invoice yang belum dibayar:
   
   Invoice: {{invoice_number}}
   Amount: Rp {{amount_due}}
   Due Date: {{due_date}}
   Days Overdue: {{days_overdue}}
   
   Mohon segera melakukan pembayaran.
   
   Terima kasih!
   ```

---

## WORKFLOW 9: Customer Feedback Request
### Trigger: Manual / After Delivery

```
Delivery Done → Wait 7 Days → Send Feedback Request
```

**Steps:**
1. **Webhook** - Delivery completed
2. **Odoo - Read** - Get customer info
3. **Wait** - 7 days
4. **Telegram/WA** -
   ```
   Hi {{customer_name}}!
   
   Sudah seminggu produk {{product_name}} sampai ya.
   
   Bagaimana hasilnya? Silakan share feedback Anda:
   - Email: feedback@duanaga.co.id
   - WA: +62 811-2127-464
   
   Masukan Anda sangat berarti untuk kami!
   
   Salam,
   Tim Dua Naga Kosmetindo
   ```

---

## WORKFLOW 10: E-commerce Integration (Shopee/Tokopedia)
### Trigger: HTTP Request

```
E-commerce Order → Parse Data → Create SO in Odoo → Update Stock
```

**Steps:**
1. **Webhook** - E-commerce API callback
2. **Code** - Parse order data
3. **Odoo - Create SO** - Create sales order
4. **Odoo - Update Stock** - Reserve inventory
5. **Telegram/WA** - Notif Sales: "New E-commerce order: {{order_id}}"

---

## SETUP DI N8N

### Node: Odoo (XML-RPC)

**Configuration:**
```
URL: http://erp_duanaga_odoo:8069/xmlrpc/2/object
Database: duanaga
User ID: 2
Password: admin
```

**Create Lead:**
```
Model: crm.lead
Method: create
Arguments: [{name, contact_name, email_from, phone, description, type: 'lead'}]
```

**Search Records:**
```
Model: crm.lead
Domain: [['create_date', '>=', '{{ $today }}'], ['stage_id', '=', 1]]
Fields: [name, contact_name, email_from, phone]
```

### Node: Telegram

**Send Message:**
```
Chat ID: -1001234567890 (Group ID)
Message: {{ $json.message }}
```

### Node: WA (Twilio/UltraMsg)

**Send Message:**
```
From: whatsapp:+14155238886
To: {{ $json.phone }}
Body: {{ $json.message }}
```

---

## INTEGRASI WHATSAPP

### Option 1: UltraMsg (Recommended)
```
API Key: [your-api-key]
Instance: duanaga_instance
```

### Option 2: Fonnte
```
API Key: [your-api-key]
```

### Option 3: WAPI (Unofficial)
```
Not recommended for production
```

---

## FLOW DIAGRAM

```
┌─────────────────────────────────────────────────────────────┐
│                     WEBSITE duanaga.co.id                   │
└─────────────────────┬───────────────────────────────────────┘
                      │ POST /webhook/lead
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                         N8N                                  │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────┐ │
│  │  Workflow 1 │    │  Workflow 2 │    │   Workflow 3+   │ │
│  │ Lead Capture│    │   Reminder  │    │  (see above)   │ │
│  └──────┬──────┘    └─────────────┘    └─────────────────┘ │
│         │                                                    │
│         ├─► ODOO (CRM Lead)                                │
│         │                                                    │
│         └─► WhatsApp (Marketing Team)                       │
│                                                              │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    ODOO ERP                                  │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────────────┐   │
│  │   CRM   │ │  Sales  │ │   MRP   │ │   Inventory     │   │
│  └────┬────┘ └────┬────┘ └────┬────┘ └────────┬────────┘   │
│       │            │           │               │             │
│       └────────────┴───────────┴───────────────┘             │
│                            │                                 │
│                            ▼                                 │
│                   ┌────────────────┐                         │
│                   │  Webhook to n8n│                         │
│                   │  (on actions)  │                         │
│                   └────────┬───────┘                         │
└────────────────────────────┼─────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                    WhatsApp Groups                            │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────────┐    │
│  │  Marketing   │ │  Production  │ │  Management      │    │
│  └──────────────┘ └──────────────┘ └──────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

---

## QUICK START

1. **Buka n8n:** `http://localhost:5678`
2. **Login:** admin@duanaga.co.id / Duanaga@2024
3. **Create Workflow Baru**
4. **Pilih Trigger:** HTTP Request / Schedule / Webhook
5. **Tambah Nodes:** Odoo, Telegram, WA, Code, etc
6. **Test:** Klik "Test workflow"
7. **Activate:** Toggle switch di kanan atas

---

*Document Version: 1.0*
*Last Updated: 2026-09-05*
