# PLANNING: TELEGRAM BOT + ODOO ERP INTEGRATION
## PT Dua Naga Kosmetindo

**Versi:** 1.0
**Tanggal:** 14 September 2026
**Status:** PLANNING (Belum Dieksekusi)

---

## 1. OVERVIEW

### 1.1 Tujuan
```
Integrasikan Telegram Bot sebagai input channel ke Odoo ERP
untuk kemudahan staff dalam input data dari mobile.
```

### 1.2 Arsitektur
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Telegram   │ ──► │    n8n      │ ──► │   Odoo      │
│    Bot      │     │ Workflows   │     │  Database   │
└─────────────┘     └─────────────┘     └─────────────┘
   Input             Logic               Storage
   Channel           Hub                 Core
```

### 1.3 Scope

**Included:**
- Semua modul Odoo yang sudah terinstall (8 addons)
- Staff di lapangan, gudang, lab, sales
- Real-time data sync

**Excluded (v1):**
- WhatsApp integration (fase 2)
- Advanced reporting dashboard via bot
- Voice input
- Multi-language

---

## 2. TELEGRAM BOT SETUP

### 2.1 Bot Creation Steps

```
Step 1: Buat Bot via @BotFather
├── Bot Name: Duanaga ERP Bot
├── Username: @DuanagaERPBOT
└── Token: Simpan aman (.env)

Step 2: Configure Bot
├── Enable Inline Mode
├── Enable Group Mode
├── Set Privacy: Disabled (untuk admin)
└── Set Commands Menu

Step 3: Create Channel/Group
├── Channel: Duanaga Notifications
│   ├── #alerts-stock
│   ├── #alerts-qc
│   └── #alerts-delivery
└── Group: Duanaga Team
```

### 2.2 Bot Configuration

```yaml
BOT_CONFIG:
  name: "Duanaga ERP Bot"
  username: "@DuanagaERPBOT"
  token: "${TELEGRAM_BOT_TOKEN}"
  
PERMISSIONS:
  groups_allowed: true
  privacy_mode: false  # Admin only
```

---

## 3. MODULE-WISE WORKFLOW PLANNING

### 3.1 SALES MODULE

#### Command: `/order` - Buat Sales Order

**Flow:**
```
User: /order
Bot: "🏪 Buat Order Baru"
Bot: "Pilih atau ketik customer:"

User: [Ketik "Toko Melawai"] atau [Klik dari list]
Bot: "Customer: Toko Kosmetik Melawai"
Bot: "Pilih product:"

User: [Ketik nama] atau [Klik dari list dengan pagination]
Bot: "Product: Sabun Wajah GlowUp"
Bot: "Qty (pcs):"

User: [Ketik "500"]
Bot: "─────────────────────────────────"
Bot: "Product: Sabun Wajah GlowUp"
Bot: "Qty: 500 pcs"
Bot: "Harga: Rp 25.000"
Bot: "Subtotal: Rp 12.500.000"
Bot: "─────────────────────────────────"
Bot: "[Tambah Product] [Selesai]"

User: [Klik Selesai]
Bot: "Delivery Date:"

User: [Ketik "25/09/2026"] atau [/tomorrow]
Bot: "─────────────────────────────────"
Bot: "📋 RINGKASAN ORDER"
Bot: "Customer: Toko Kosmetik Melawai"
Bot: "Product: Sabun GlowUp x 500pcs"
Bot: "Total: Rp 12.500.000"
Bot: "Delivery: 25/09/2026"
Bot: "─────────────────────────────────"
Bot: "[✅ Confirm] [❌ Cancel]"

User: [Klik ✅ Confirm]
Bot: "✅ ORDER BERHASIL!"
Bot: "SO Number: SOO/2026/0145"
Bot: "Status: Quotation"
```

**Odoo Create:**
```python
sale_order = {
    'partner_id': partner_id,
    'date_order': datetime.now(),
    'commitment_date': delivery_date,
    'order_line': [
        (0, 0, {
            'product_id': product_id,
            'product_uom_qty': qty,
            'price_unit': price,
        })
    ]
}
```

---

#### Command: `/quotation` - Buat Quotation

**Flow:**
```
User: /quotation
Bot: "📄 Buat Quotation"
[Same flow as /order, tapi status = draft]
Bot: "Quotation SOO/2026/0146 created"
```

---

#### Command: `/myorders` - Lihat Orders Saya

**Flow:**
```
User: /myorders
Bot: "📋 Order Saya"
Bot: "Filter:"
Bot: "[All] [Quotation] [Sales Order] [Done]"

User: [Klik All]
Bot: "─────────────────────────────────"
Bot: "1. SOO/2026/0140 - Toko X"
Bot: "   Rp 8.500.000 - Delivered ✅"
Bot: ""
Bot: "2. SOO/2026/0141 - Toko Y"
Bot: "   Rp 5.000.000 - Ready"
Bot: ""
Bot: "3. SOO/2026/0142 - Toko Z"
Bot: "   Rp 12.000.000 - Quotation"
Bot: "─────────────────────────────────"
Bot: "Klik untuk detail"
```

---

#### Command: `/track` - Track Delivery

**Flow:**
```
User: /track
Bot: "🔍 Track Delivery"
Bot: "Masukkan SO Number:"

User: "SOO/2026/0140"
Bot: "─────────────────────────────────"
Bot: "📦 SOO/2026/0140"
Bot: "Customer: Toko Kosmetik Melawai"
Bot: "─────────────────────────────────"
Bot: "📍 Timeline:"
Bot: "✅ 12/09 - Order Received"
Bot: "✅ 13/09 - Confirmed"
Bot: "✅ 14/09 - In Production"
Bot: "✅ 15/09 - QC Passed"
Bot: "⏳ 16/09 - Ready to Ship"
Bot: "📋 Estimated Delivery: 18/09/2026"
Bot: "─────────────────────────────────"
Bot: "No. Resi: JNE1234567890"
Bot: "Track: jne.co.id/JNE1234567890"
```

---

### 3.2 PURCHASE MODULE

#### Command: `/po` - Buat Purchase Order

**Flow:**
```
User: /po
Bot: "📥 Buat Purchase Order"
Bot: "Pilih Vendor:"

User: [Ketik atau pilih dari list]
Bot: "Vendor: PT Chemindo Maju"
Bot: "Tambah Product:"

User: "Glycerin 99%"
Bot: "─────────────────────────────────"
Bot: "Glycerin 99% (Pharmaceutical Grade)"
Bot: "Qty (kg):"

User: "500"
Bot: "Harga Vendor (Rp/kg):"

User: "45000"
Bot: "─────────────────────────────────"
Bot: "Product: Glycerin 99%"
Bot: "Qty: 500 kg"
Bot: "Harga: Rp 45.000/kg"
Bot: "Subtotal: Rp 22.500.000"
Bot: "─────────────────────────────────"
Bot: "[Tambah Vendor] [Selesai]"

User: [Selesai]
Bot: "Expected Delivery Date:"

User: "30/09/2026"
Bot: "─────────────────────────────────"
Bot: "📋 RINGKASAN PO"
Bot: "Vendor: PT Chemindo Maju"
Bot: "Product: Glycerin 99% x 500kg"
Bot: "Total: Rp 22.500.000"
Bot: "Delivery: 30/09/2026"
Bot: "─────────────────────────────────"
Bot: "[✅ Confirm PO]"

User: [✅]
Bot: "✅ PO BERHASIL!"
Bot: "PO Number: POO/2026/0089"
Bot: "Vendor notified via email"
```

---

#### Command: `/receive` - Terima Barang

**Flow:**
```
User: /receive
Bot: "📥 Terima Barang"
Bot: "PO Number:"

User: "POO/2026/0089"
Bot: "─────────────────────────────────"
Bot: "PO: POO/2026/0089"
Bot: "Vendor: PT Chemindo Maju"
Bot: "─────────────────────────────────"
Bot: "Items to Receive:"
Bot: "1. Glycerin 99% - 500 kg"
Bot: "2. Kojic Acid - 50 kg"
Bot: "3. Niacinamide - 30 kg"
Bot: "─────────────────────────────────"
Bot: "Receive Item 1:"
Bot: "Glycerin 99%"
Bot: "Qty Ordered: 500 kg"
Bot: "Qty Received:" 

User: "500"
Bot: "Condition:"
Bot: "[✅ Good] [⚠️ Damaged]"

User: [✅ Good]
Bot: "LOT/Serial Number:"

User: "LOT-GLY-2026-0915"
Bot: "─────────────────────────────────"
Bot: "✅ Glycerin 99% - 500 kg received"
Bot: "LOT: LOT-GLY-2026-0915"
Bot: ""
Bot: "Remaining to receive:"
Bot: "1. Kojic Acid - 50 kg"
Bot: "2. Niacinamide - 30 kg"
Bot: "─────────────────────────────────"
Bot: "[Continue] [✅ Complete All]"
```

---

#### Command: `/rfq` - Request for Quotation

**Flow:**
```
User: /rfq
Bot: "📋 Request for Quotation"
[Same flow as /po, tapi status = RFQ]
Bot: "RFQ sent to vendor"
```

---

### 3.3 INVENTORY MODULE

#### Command: `/stock` - Cek Stock

**Flow:**
```
User: /stock
Bot: "📦 Cek Stock"
Bot: "Ketik nama product atau SKU:"

User: "Sabun GlowUp"
Bot: "─────────────────────────────────"
Bot: "📦 Sabun Wajah GlowUp"
Bot: "SKU: SKU-SABUN-GLOWUP"
Bot: "─────────────────────────────────"
Bot: "📍 Locations:"
Bot: "├── WH/Stock: 1.250 pcs"
Bot: "├── Reserved: 500 pcs"
Bot: "└── Available: 750 pcs"
Bot: ""
Bot: "📊 Forecast:"
Bot: "├── Incoming: 0 pcs"
Bot: "├── Outgoing: 300 pcs"
Bot: "└── Forecasted: 950 pcs"
Bot: ""
Bot: "⚠️ Alert: Below reorder point (1000 pcs)"
Bot: "─────────────────────────────────"
Bot: "[Cek Product Lain] [📊 Low Stock Report]"
```

---

#### Command: `/lowstock` - Low Stock Alert

**Flow:**
```
User: /lowstock
Bot: "⚠️ LOW STOCK REPORT"
Bot: "Generated: 14/09/2026 09:00"
Bot: "─────────────────────────────────"
Bot: "🔴 CRITICAL (Stock = 0):"
Bot: "1. Retinol 2.5% - 0 pcs"
Bot: "   Action: STOP PRODUCTION"
Bot: ""
Bot: "🟡 WARNING (Below Safety):"
Bot: "1. Glycerin 99% - 50 kg"
Bot: "   Safety: 100 kg | Current: 50 kg"
Bot: "   Action: Purchase Request triggered"
Bot: ""
Bot: "2. Niacinamide - 15 kg"
Bot: "   Safety: 30 kg | Current: 15 kg"
Bot: "   Action: Purchase Request triggered"
Bot: ""
Bot: "─────────────────────────────────"
Bot: "[Create PO] [📞 Contact Vendor] [Dismiss]"
```

---

### 3.4 MANUFACTURING MODULE

#### Command: `/mo` - Buat Manufacturing Order

**Flow:**
```
User: /mo
Bot: "🏭 Buat Manufacturing Order"
Bot: "Product:"

User: "Sabun Wajah GlowUp"
Bot: "─────────────────────────────────"
Bot: "Product: Sabun Wajah GlowUp"
Bot: "Bill of Materials: Sabun GlowUp - Default"
Bot: "─────────────────────────────────"
Bot: "Components Available:"
Bot: "├── Glycerin: 75 kg ✅"
Bot: "├── Kojic Acid: 25 kg ✅"
Bot: "├── Niacinamide: 15 kg ✅"
Bot: "└── Aqua: 300 kg ✅"
Bot: "─────────────────────────────────"
Bot: "Qty to Produce:"

User: "500"
Bot: "─────────────────────────────────"
Bot: "📋 RINGKASAN MO"
Bot: "Product: Sabun Wajah GlowUp"
Bot: "Qty: 500 pcs"
Bot: "Batch Size: 100 kg"
Bot: "─────────────────────────────────"
Bot: "Schedule:"
Bot: "├── Start: 18/09/2026"
Bot: "└── Deadline: 22/09/2026"
Bot: "─────────────────────────────────"
Bot: "[✅ Create MO]"

User: [✅]
Bot: "✅ MO BERHASIL!"
Bot: "MO Number: MO/2026/09/0026"
Bot: "Product: Sabun Wajah GlowUp"
Bot: "Qty: 500 pcs"
Bot: "─────────────────────────────────"
Bot: "📍 Production Schedule:"
Bot: "1. Mixing - 18/09 08:00"
Bot: "2. Heating - 18/09 08:30"
Bot: "3. Filling - 18/09 09:15"
Bot: "4. QC Check - 18/09 10:15"
Bot: "─────────────────────────────────"
Bot: "⚠️ Stock reserved"
Bot: "📞 Production team notified"
```

---

#### Command: `/mostatus` - Cek Status MO

**Flow:**
```
User: /mostatus
Bot: "🏭 Manufacturing Status"
Bot: "Filter:"
Bot: "[All] [In Progress] [Pending] [Done]"

User: [Klik In Progress]
Bot: "─────────────────────────────────"
Bot: "📍 IN PROGRESS (3 Orders)"
Bot: ""
Bot: "1. MO/2026/09/0025"
Bot: "   Product: Sabun Wajah GlowUp"
Bot: "   Progress: ████████░░ 80%"
Bot: "   Status: Filling"
Bot: "   ETA: 18/09 14:00"
Bot: ""
Bot: "2. MO/2026/09/0026"
Bot: "   Product: Serum Vit C"
Bot: "   Progress: ████░░░░░░ 40%"
Bot: "   Status: Mixing"
Bot: "   ETA: 19/09 10:00"
Bot: ""
Bot: "3. MO/2026/09/0027"
Bot: "   Product: Lip Cream Matte"
Bot: "   Progress: ██░░░░░░░░ 20%"
Bot: "   Status: Waiting Materials"
Bot: "   ETA: 20/09 16:00"
Bot: "─────────────────────────────────"
```

---

### 3.5 QC MODULE

#### Command: `/qc` - Input QC Results

**Flow:**
```
User: /qc
Bot: "🔬 QC Input"
Bot: "Batch/LOT Number:"

User: "LOT-2026-0914-001"
Bot: "─────────────────────────────────"
Bot: "Batch: LOT-2026-0914-001"
Bot: "Product: Sabun Wajah GlowUp"
Bot: "MO: MO/2026/09/0025"
Bot: "Qty: 500 pcs"
Bot: "─────────────────────────────────"
Bot: "📊 QC Parameters:"
Bot: ""
Bot: "pH Level:"
Bot: "Range: 5.5 - 6.5"

User: "6.1"
Bot: "✅ pH: 6.1 (IN RANGE)"
Bot: ""
Bot: "Viscosity (Pa.s):"
Bot: "Range: 1.05 - 1.10"

User: "1.07"
Bot: "✅ Viscosity: 1.07 (IN RANGE)"
Bot: ""
Bot: "Visual Check:"
Bot: "[✅ Pass] [❌ Fail]"

User: [✅ Pass]
Bot: "─────────────────────────────────"
Bot: "📊 QC SUMMARY"
Bot: "Batch: LOT-2026-0914-001"
Bot: "─────────────────────────────────"
Bot: "pH: 6.1 ✅ (5.5-6.5)"
Bot: "Viscosity: 1.07 ✅ (1.05-1.10)"
Bot: "Visual: Pass ✅"
Bot: "─────────────────────────────────"
Bot: "[🔬 Submit to KBR Engine]"
Bot: "[❌ Cancel]"

User: [🔬 Submit]
Bot: "⏳ Processing KBR Engine..."
Bot: "─────────────────────────────────"
Bot: "✅ QC DECISION: APPROVED"
Bot: "─────────────────────────────────"
Bot: "Engine: Knowledge-Based Reasoning"
Bot: "Confidence: 98.5%"
Bot: ""
Bot: "Recommendation:"
Bot: "Batch memenuhi spesifikasi."
Bot: "Releasable untuk distribusi."
Bot: ""
Bot: "📦 Qty Approved: 500 pcs"
Bot: "📍 Location: WH/Stock"
Bot: "─────────────────────────────────"
Bot: "MO MO/2026/09/0025: DONE ✅"
Bot: "Stock Updated: +500 pcs"
```

---

#### Command: `/qcfail` - QC Failed

**Flow:**
```
User: /qcfail
Bot: "🔬 QC Input - FAIL"
Bot: "Batch/LOT Number:"

User: "LOT-2026-0914-002"
Bot: [Same initial flow]
Bot: "pH Level:"

User: "6.8"
Bot: "❌ pH: 6.8 (OUT OF RANGE)"
Bot: "   Required: 5.5 - 6.5"
Bot: ""
Bot: "Viscosity:"

User: "1.07"
Bot: "✅ Viscosity: 1.07 (IN RANGE)"
Bot: [Submit to KBR]
Bot: "─────────────────────────────────"
Bot: "⚠️ QC DECISION: REWORK REQUIRED"
Bot: "─────────────────────────────────"
Bot: "Issue: pH terlalu tinggi"
Bot: ""
Bot: "Recommendation:"
Bot: "1. Kembalikan ke Mixing"
Bot: "2. Tambah Asam Sitrat 0.5%"
Bot: "3. Re-test pH"
Bot: "4. Resubmit QC"
Bot: ""
Bot: "MO Status: In Progress (Rework)"
Bot: "─────────────────────────────────"
Bot: "📞 Production notified"
```

---

### 3.6 REGULATORY MODULE

#### Command: `/bpom` - BPOM Status

**Flow:**
```
User: /bpom
Bot: "🏛️ BPOM REGISTRATION STATUS"
Bot: "─────────────────────────────────"
Bot: "📍 PRODUCT REGISTRATIONS"
Bot: ""
Bot: "1. Sabun GlowUp Plus"
Bot: "   NIE: Pending Submission"
Bot: "   Status: 🔴 DRAFT"
Bot: ""
Bot: "2. Serum Vit C Premium"
Bot: "   NIE: ML12345678901AB"
Bot: "   Status: ✅ APPROVED"
Bot: "   Expires: 15/12/2026 (92 days)"
Bot: ""
Bot: "3. Night Cream Classic"
Bot: "   NIE: ML55555555555YY"
Bot: "   Status: ❌ EXPIRED"
Bot: "   Action: STOP DISTRIBUTION"
Bot: "─────────────────────────────────"
Bot: "⚠️ ACTION REQUIRED:"
Bot: "• Submit renewal: 1 product"
Bot: "• Stop distribution: 1 product"
Bot: "─────────────────────────────────"
Bot: "[📝 Submit Renewal] [📞 Contact BPOM]"
```

---

#### Command: `/niecheck` - Check NIE Product

**Flow:**
```
User: /niecheck
Bot: "🔍 Check NIE Product"
Bot: "Masukkan NIE Number:"

User: "ML12345678901AB"
Bot: "─────────────────────────────────"
Bot: "NIE: ML12345678901AB"
Bot: "─────────────────────────────────"
Bot: "Product: Serum Vit C Premium"
Bot: "Brand: Duanaga"
Bot: "Category: MLS (Make Up Lip Stain)"
Bot: "Net Weight: 50 ml"
Bot: "─────────────────────────────────"
Bot: "Status: ✅ ACTIVE"
Bot: "Valid Until: 15/12/2026"
Bot: "Days Remaining: 92 days"
Bot: "─────────────────────────────────"
Bot: "⚠️ RENEWAL RECOMMENDED"
Bot: "Submit renewal 90 days before expiry"
```

---

### 3.7 CONSIGNMENT MODULE

#### Command: `/consign` - Consignment Operations

**Flow:**
```
User: /consign
Bot: "📦 CONSIGNMENT MENU"
Bot: "[📥 Receive] [📤 Send] [📊 Report]"
```

**Receive Consignment:**
```
User: [📥 Receive]
Bot: "Vendor:"

User: "PT Chemindo Maju"
Bot: "Product:"

User: "Glycerin 99%"
Bot: "Qty:"

User: "100"
Bot: "─────────────────────────────────"
Bot: "Consignment Details:"
Bot: "Vendor: PT Chemindo Maju"
Bot: "Product: Glycerin 99%"
Bot: "Qty: 100 kg"
Bot: "─────────────────────────────────"
Bot: "[✅ Confirm]"
```

---

### 3.8 UTILITY COMMANDS

#### Command: `/start` - Welcome
```
Bot: "👋 Selamat datang di Duanaga ERP Bot!"
Bot: "PT Dua Naga Kosmetindo"
Bot: "─────────────────────────────────"
Bot: "Command yang tersedia:"
Bot: ""
Bot: "📦 Sales:"
Bot: "/order - Buat Sales Order"
Bot: "/quotation - Buat Quotation"
Bot: "/myorders - Lihat orders"
Bot: "/track - Track delivery"
Bot: ""
Bot: "📥 Purchase:"
Bot: "/po - Buat Purchase Order"
Bot: "/receive - Terima barang"
Bot: "/rfq - Request for Quotation"
Bot: ""
Bot: "🏭 Manufacturing:"
Bot: "/mo - Buat MO"
Bot: "/mostatus - Status MO"
Bot: ""
Bot: "🔬 QC:"
Bot: "/qc - Input QC results"
Bot: ""
Bot: "📦 Inventory:"
Bot: "/stock - Cek stock"
Bot: "/lowstock - Low stock alert"
Bot: ""
Bot: "🏛️ Regulatory:"
Bot: "/bpom - Status BPOM"
Bot: ""
Bot: "📊 Reports:"
Bot: "/report - Daily summary"
Bot: ""
Bot: "Ketik /help untuk bantuan"
```

---

#### Command: `/help` - Help
```
Bot: "📖 BANTUAN"
Bot: "─────────────────────────────────"
Bot: "Cara penggunaan:"
Bot: ""
Bot: "1. Ketik command (misal: /order)"
Bot: "2. Ikuti instruksi bot"
Bot: "3. Jawab pertanyaan dengan:"
Bot: "   - Ketik jawaban"
Bot: "   - Klik tombol (inline keyboard)"
Bot: ""
Bot: "Tips:"
Bot: "• Ketik /cancel untuk batalkan"
Bot: "• Ketik /back untuk kembali"
Bot: "• Ketik /status untuk lihat status"
Bot: ""
Bot: "─────────────────────────────────"
Bot: "Kontak Admin:"
Bot: "📞 021-1234-5678"
Bot: "📧 admin@duanaga.com"
```

---

#### Command: `/report` - Daily Summary

**Flow:**
```
User: /report
Bot: "📊 LAPORAN HARIAN"
Bot: "Tanggal: 14 September 2026"
Bot: "─────────────────────────────────"
Bot: "📈 SALES"
Bot: "• SO Baru: 5 orders"
Bot: "• Total Value: Rp 45.000.000"
Bot: "• Conversion: 68%"
Bot: ""
Bot: "🏭 PRODUCTION"
Bot: "• MO Completed: 3 batches"
Bot: "• MO In Progress: 5 orders"
Bot: "• QC Passed: 3 (100%)"
Bot: ""
Bot: "📦 INVENTORY"
Bot: "• Low Stock Items: 5"
Bot: "• Goods Received: 2 PO"
Bot: "• Delivered: 8 orders"
Bot: ""
Bot: "⚠️ ALERTS"
Bot: "• Retinol: STOCK OUT"
Bot: "• Niacinamide: LOW STOCK (15kg)"
Bot: "• Night Cream: NIE EXPIRED"
Bot: "─────────────────────────────────"
```

---

## 4. IMPLEMENTATION TIMELINE

### Phase 1: Core Setup (Day 1-2)
```
Day 1:
├── Setup Telegram Bot via @BotFather
├── Configure bot permissions
├── Create .env file with tokens
├── Test bot connectivity
└── Setup n8n Telegram node

Day 2:
├── Create base conversation workflow
├── Implement /start and /help
├── Setup error handling
└── Test basic message flow
```

### Phase 2: Sales & Purchase (Day 3-5)
```
Day 3: Sales Module
├── /order - Create SO
├── /quotation - Create Quote
├── /myorders - List orders
└── /track - Track delivery

Day 4: Purchase Module
├── /po - Create PO
├── /receive - Goods receipt
└── /rfq - Request for quotation

Day 5: Integration Testing
├── Full sales flow test
├── Full purchase flow test
└── Error handling test
```

### Phase 3: Inventory & Manufacturing (Day 6-8)
```
Day 6: Inventory Module
├── /stock - Check inventory
├── /lowstock - Low stock alerts
└── /transfer - Internal transfer

Day 7: Manufacturing Module
├── /mo - Create MO
├── /mostatus - MO status
└── /produce - Production complete

Day 8: Integration Testing
└── Full production flow test
```

### Phase 4: QC & Regulatory (Day 9-11)
```
Day 9: QC Module
├── /qc - QC input
├── /qcfail - QC failed flow
└── KBR engine integration

Day 10: Regulatory Module
├── /bpom - BPOM status
├── /niecheck - NIE check
└── Expiry alerts setup

Day 11: Integration Testing
└── Full QC flow test
```

### Phase 5: Polish & Deploy (Day 12-14)
```
Day 12-13: Testing & Bug Fixes
├── User acceptance testing
├── Error handling
├── Performance optimization
└── Security audit

Day 14: Go Live
├── Deploy to production
├── Train staff
├── Documentation
└── Support handover
```

---

## 5. TECHNICAL REQUIREMENTS

### 5.1 External Services

```yaml
SERVICES:
  telegram:
    provider: Telegram Bot API
    token: ${TELEGRAM_BOT_TOKEN}
    webhook_mode: true
    
  odoo:
    url: http://localhost:8069
    db: duanaga
    user: admin
    api: XML-RPC / JSON-RPC
    
  n8n:
    url: http://localhost:5678
    webhook_base: http://localhost:5678/webhook
```

### 5.2 n8n Nodes Required

```yaml
NODES:
  - Telegram Bot Trigger
  - Telegram Bot Action (Send Message)
  - Telegram Bot Action (Reply Keyboard)
  
  - HTTP Request (Odoo API)
  - XML-RPC (Odoo legacy API)
  
  - Switch
  - IF
  - Code (Data transformation)
  
  - Telegram Bot Setup (Webhook)
```

### 5.3 Database Schema Additions

```sql
-- Table untuk conversation state
CREATE TABLE telegram_conversation_state (
    id SERIAL PRIMARY KEY,
    telegram_user_id BIGINT,
    telegram_chat_id BIGINT,
    command VARCHAR(50),
    step VARCHAR(50),
    data JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Table untuk bot users
CREATE TABLE telegram_users (
    id SERIAL PRIMARY KEY,
    telegram_id BIGINT UNIQUE,
    telegram_username VARCHAR(100),
    odoo_user_id INTEGER,
    role VARCHAR(50),
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 6. ERROR HANDLING

### 6.1 Error Types

| Error | Handling | User Message |
|-------|----------|---------------|
| Odoo Connection Failed | Retry 3x | "Server busy, coba lagi" |
| Invalid Input | Ask again | "Format salah, coba lagi" |
| Product Not Found | Search suggestion | "Produk tidak ada, coba lagi" |
| Stock Insufficient | Show available | "Stock 50 pcs, kurang 450 pcs" |
| Auth Failed | Re-login | "Session expired, login ulang" |
| Timeout | Retry once | "Koneksi timeout" |

### 6.2 Fallback Flow

```
User Input → Parse → Validate
                      ↓
              [Valid] → Process → Respond
                      ↓
              [Invalid] → Error Message → Ask Again
```

---

## 7. SECURITY

### 7.1 User Authentication

```yaml
AUTHENTICATION:
  method: Telegram User ID mapping
  
  # Only authorized users can use bot
  allowed_users:
    - telegram_id: "123456789"  # Admin
      role: "admin"
    - telegram_id: "987654321"  # Sales Manager
      role: "sales"
    - telegram_id: "555666777"  # QC Staff
      role: "qc"
    - telegram_id: "888999000"  # Warehouse
      role: "warehouse"
```

### 7.2 Permission Matrix

| Command | Admin | Sales | QC | Warehouse | Viewer |
|---------|-------|-------|-----|-----------|--------|
| /order | ✅ | ✅ | ❌ | ❌ | ❌ |
| /qc | ✅ | ❌ | ✅ | ❌ | ❌ |
| /receive | ✅ | ❌ | ❌ | ✅ | ❌ |
| /stock | ✅ | ✅ | ✅ | ✅ | ✅ |
| /report | ✅ | ✅ | ❌ | ❌ | ✅ |

---

## 8. DELIVERABLES

### 8.1 Files to Create

```
telegram-bot/
├── README.md                          # Setup guide
├── .env.example                      # Environment template
├── workflows/
│   ├── telegram-base.json             # Base workflow
│   ├── sales/
│   │   ├── order.json
│   │   ├── quotation.json
│   │   └── track.json
│   ├── purchase/
│   │   ├── po.json
│   │   ├── receive.json
│   │   └── rfq.json
│   ├── inventory/
│   │   ├── stock.json
│   │   └── lowstock.json
│   ├── manufacturing/
│   │   ├── mo.json
│   │   └── mostatus.json
│   ├── qc/
│   │   └── qc-input.json
│   └── utility/
│       ├── start.json
│       ├── help.json
│       └── report.json
├── database/
│   └── init.sql                       # Schema init
└── config/
    └── allowed_users.yaml              # User permissions
```

### 8.2 n8n Workflows (Total: 14)

```yaml
WORKFLOWS:
  BASE:
    - telegram-base (1)
  
  SALES:
    - create-order (2)
    - create-quotation (3)
    - track-delivery (4)
  
  PURCHASE:
    - create-po (5)
    - receive-goods (6)
    - create-rfq (7)
  
  INVENTORY:
    - check-stock (8)
    - low-stock-alert (9)
  
  MANUFACTURING:
    - create-mo (10)
    - mo-status (11)
  
  QC:
    - qc-input (12)
  
  UTILITY:
    - daily-report (13)
    - notification-broadcast (14)
```

---

## 9. ACCEPTANCE CRITERIA

### 9.1 Functional Requirements

- [ ] Bot respond to /start with welcome message
- [ ] All 14 commands work as documented
- [ ] Data correctly created in Odoo
- [ ] Real-time stock query works
- [ ] QC input triggers KBR engine
- [ ] Error messages are user-friendly
- [ ] Only authorized users can execute commands

### 9.2 Non-Functional Requirements

- [ ] Response time < 3 seconds
- [ ] 99% uptime
- [ ] Backup workflow exists
- [ ] Documentation complete
- [ ] Staff trained

### 9.3 Test Scenarios

| Scenario | Expected Result |
|----------|-----------------|
| User: /order → create SO | SO created in Odoo |
| User: /qc with valid pH | QC approved, stock updated |
| User: /qc with invalid pH | QC rework, MO status updated |
| User: /stock Sabun | Show current stock levels |
| User: Unauthorized command | "Access denied" message |

---

## 10. BUDGET & COST

### 10.1 Direct Costs

| Item | Cost | Notes |
|------|------|-------|
| Telegram Bot | FREE | No cost |
| n8n | FREE (self-hosted) | Already running |
| Odoo | Already installed | No additional cost |
| Domain (optional) | Rp 150.000/year | For HTTPS |
| SSL Certificate | FREE (Let's Encrypt) | If using domain |

### 10.2 Development Time

| Phase | Hours | Notes |
|-------|-------|-------|
| Setup & Config | 4 hours | Bot creation, n8n setup |
| Sales + Purchase | 8 hours | 4 workflows |
| Inventory + MFG | 8 hours | 4 workflows |
| QC + Regulatory | 6 hours | 2 workflows |
| Testing + Polish | 8 hours | UAT, fixes |
| Documentation | 4 hours | User guide |
| **TOTAL** | **38 hours** | ~1 week dev |

---

## 11. NEXT STEPS

### After Approval:

1. **Create Telegram Bot** via @BotFather
2. **Get Bot Token**
3. **Deploy base workflow to n8n**
4. **Test connectivity**
5. **Proceed with Phase 1**

### Pre-Requisites from User:

- [ ] BotFather token
- [ ]确认要开始

---

## 12. APPROVAL

```
Planning ini sudah lengkap dan siap dieksekusi.

Silakan review dan berikan konfirmasi untuk proceed.

Persetujuan:
□ Setuju - mulai development
□ Perlu revisi - specify bagian yang perlu diubah
□ Tidak jadi - cancel
```

