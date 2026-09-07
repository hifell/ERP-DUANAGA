# N8N + ODOO - COMPLETE AUTOMATION BLUEPRINT
## PT DUA NAGA KOSMETINDO - MAKLON COSMETICS

---

# PART 1: BUSINESS PROCESSES

## 1. PRE-SALES & MARKETING

### 1.1 Website Inquiry Capture
```
Website Form → Lead di Odoo → Assign to Sales → Follow-up Reminder
```
**Trigger:** HTTP POST dari website duanaga.co.id/contact

**Data Masuk:**
```json
{
  "name": "Beauty Glow Indonesia",
  "contact_person": "Budi Santoso",
  "email": "order@beautyglow.id",
  "phone": "+628123456789",
  "company": "PT Beauty Glow Indonesia",
  "product_interest": ["Face Serum", "Body Lotion"],
  "quantity_target": "500-1000 pcs",
  "budget": "Rp 50-100 juta",
  "timeline": "Q4 2026",
  "source": "Website Form"
}
```

**n8n Flow:**
1. Webhook terima data
2. Parse & validate
3. Create Lead di Odoo CRM
4. Assign ke sales team
5. Auto-create follow-up task (3 hari)
6. Notif WA ke marketing

**Odoo Actions:**
- Create `crm.lead`
- Set source: Website
- Set priority: High (jika quantity > 500)
- Assign: Round-robin ke sales team

---

### 1.2 WhatsApp Inquiry to Lead
```
WA Message → n8n → Create Lead di Odoo
```
**Trigger:** WhatsApp webhook (UltraMsg/Fonnte)

**Flow:**
1. Customer kirim WA ke WA Business
2. n8n parse message
3. Extract: nama, no HP, produk interesse
4. Create Lead di Odoo
5. Reply WA: "Terima kasih, tim kami akan segera hubungi Anda"

---

### 1.3 Social Media Lead Capture
```
Instagram DM / Facebook Message → n8n → Lead
```
**Trigger:** Zapier/Make webhook

**Flow:**
1. Social media DM masuk
2. Zapier catch → n8n webhook
3. Parse data (nama, platform, message)
4. Create Lead dengan source = Social Media
5. Notif sales team

---

### 1.4 Trade Show / Event Lead
```
Event Registration → Excel/Form → Bulk Import → Leads
```
**Trigger:** Manual upload atau scheduled email check

**Flow:**
1. Event organizer kirim spreadsheet
2. n8n read email attachment
3. Parse Excel
4. Bulk create Leads di Odoo
5. Tag dengan event name
6. Batch notif ke sales

---

### 1.5 Lead Scoring & Qualification
```
Lead Created → Score Based on Rules → Assign Priority
```
**Scoring Rules:**
| Criteria | Score | Action |
|----------|-------|--------|
| Quantity > 1000 pcs | +20 | Hot Lead |
| Budget > Rp 100 juta | +15 | Hot Lead |
| Has Company Name | +10 | Valid |
| Timeline < 1 bulan | +15 | Immediate |
| Repeat Customer | +25 | VIP |

**Flow:**
1. Lead created/updated
2. n8n calculate score
3. Update lead priority field
4. If score > 50: Hot Lead → Urgent notif
5. If score > 30: Warm Lead → Standard flow
6. If score < 30: Cold Lead → Nurture sequence

---

## 2. QUOTATION & PRICING

### 2.1 Quotation Request from Lead
```
Lead Qualified → Create Quotation → Send to Customer
```
**Trigger:** Sales create quotation di Odoo

**Data:**
```json
{
  "lead_id": 123,
  "customer": "Beauty Glow Indonesia",
  "products": [
    {"product": "Face Serum 30ml", "qty": 1000, "price": 75000},
    {"product": "Custom Bottle", "qty": 1000, "price": 5000},
    {"product": "Custom Box", "qty": 1000, "price": 3500}
  ],
  "total": "Rp 83.500.000",
  "valid_until": "2026-10-05",
  "notes": "Including formulation + packaging"
}
```

**n8n Flow:**
1. Odoo trigger (webhook on SO state=quotation)
2. Format quotation details
3. Create PDF (optional)
4. Send via Email + WA to customer
5. Create follow-up task: 3 hari kemudian

---

### 2.2 Formula Costing Automation
```
BOM Updated → Calculate Cost → Update Product Price
```
**Trigger:** MRP BoM updated

**Flow:**
1. BoM changed (material qty/price update)
2. n8n calculate:
   - Total material cost
   - Labor cost (based on MO time)
   - Overhead (20%)
   - Margin (based on product category)
3. Update product standard price in Odoo
4. Notif sales team: "Harga [Product] updated"

---

### 2.3 Special Pricing Approval
```
SO with Discount > 20% → Request Approval → Notif Manager
```
**Trigger:** SO with discount exceeding threshold

**Flow:**
1. SO submitted with high discount
2. n8n detect: discount > 20%
3. Create approval task in Odoo
4. Notif WA to sales manager
5. Manager approve/reject
6. If approved: proceed with SO
7. If rejected: notify sales rep

---

### 2.4 Quotation Expiry Reminder
```
Quotation > 7 days, no response → Follow-up
```
**Trigger:** Scheduled daily check

**Flow:**
1. Daily at 09:00, search quotations:
   - state = 'sent'
   - create_date < 7 days ago
2. For each quotation:
3. Send WA reminder to customer
4. Log activity in Odoo
5. If no response after 14 days: mark as lost

---

## 3. SALES ORDER MANAGEMENT

### 3.1 Sales Order Confirmed
```
SO Confirmed → Parse Details → Multiple Actions
```
**Trigger:** SO state changed to 'sale'

**Actions:**
1. **Inventory Check:**
   - Verify stock availability
   - If stock < qty: Create backorder alert

2. **Production Trigger:**
   - If make-to-order: Create MO automatically
   - Notif production team

3. **Shipping Planning:**
   - Calculate delivery date based on production + shipping
   - Update SO expected date

4. **Notifications:**
   - WA to Production: New order details
   - WA to Customer: Order confirmed, expected delivery
   - Email to Finance: SO for invoicing

5. **Documentation:**
   - Create project/task for tracking
   - Generate picking list

---

### 3.2 MOQ (Minimum Order Quantity) Alert
```
SO Created → Check against MOQ → Alert if Below
```
**Trigger:** New SO created

**Rules:**
| Product Category | MOQ |
|-----------------|-----|
| Face Care | 300 pcs |
| Body Care | 500 pcs |
| Hair Care | 500 pcs |
| Custom Packaging | 1000 pcs |

**Flow:**
1. SO created
2. n8n check each line against MOQ
3. If below MOQ:
   - Notif WA to customer: "MOQ not met"
   - Request minimum order
4. If OK: proceed with SO

---

### 3.3 Rush Order Handling
```
SO marked Rush → Priority Production → Expedite
```
**Trigger:** SO with rush_order = true

**Flow:**
1. Detect rush order flag
2. Calculate rush fee (10-20%)
3. Update SO with rush fee
4. Notif Production: PRIORITY ORDER
5. Adjust production schedule
6. Update customer: Rush fee + delivery date

---

### 3.4 Order Modification
```
SO Amendment → Track Changes → Notif Stakeholders
```
**Trigger:** SO updated after confirmation

**Changes tracked:**
- Product add/remove
- Quantity change
- Delivery date change
- Price change

**Flow:**
1. SO modified
2. n8n compare before/after
3. Generate change summary
4. If significant (qty > 20% change):
   - Require approval
   - Notif all stakeholders
5. Update Odoo with amendment log

---

### 3.5 Order Cancellation
```
SO Cancelled → Process Refund → Release Stock
```
**Trigger:** SO state = 'cancel'

**Flow:**
1. Detect cancellation
2. Check payment status:
   - If paid: Calculate refund amount
   - Create refund request in Odoo
3. Release reserved stock
4. Cancel related MO (if any)
5. Notif:
   - Customer: Cancellation confirmed
   - Finance: Process refund
   - Production: Cancel MO

---

## 4. PROCUREMENT

### 4.1 Automatic Reordering
```
Stock < Min Level → Create Draft PO → Manager Approval
```
**Trigger:** Scheduled daily check (06:00)

**Flow:**
1. Query Odoo stock levels:
   - Stock < reorder_point
   - Product type = 'consu' (consumable/raw material)
2. For each low-stock item:
3. Get preferred supplier
4. Calculate qty needed (target - current + safety stock)
5. Create draft PO
6. Notif purchasing manager
7. If auto-approve enabled: auto-confirm

---

### 4.2 Purchase Request from Production
```
MO Created → Check Materials → Create PO if Needed
```
**Trigger:** MO confirmed

**Flow:**
1. MO confirmed
2. n8n read BoM components
3. Check current stock of each component
4. Calculate shortfall
5. If shortfall > 0:
   - Create PO for missing materials
   - Set expected delivery = MO scheduled date - 2 days
6. Notif purchasing team

---

### 4.3 Supplier Performance Tracking
```
PO Completed → Track On-Time Delivery → Update Score
```
**Trigger:** PO receipt validated

**Metrics tracked:**
| Metric | Score Impact |
|--------|--------------|
| On-time delivery | +10 |
| Late 1-2 days | 0 |
| Late > 3 days | -5 |
| Quality issues | -10 |
| Wrong items | -15 |

**Flow:**
1. PO receipt completed
2. Compare actual delivery vs promised date
3. Check quality (rejected items?)
4. Update supplier score in Odoo
5. If score drops below threshold:
   - Notif: "Supplier [X] score dropped to [Y]"
   - Create review task

---

### 4.4 Price Comparison
```
Supplier Quote Received → Compare Prices → Recommend Best
```
**Trigger:** Email with quote attachment

**Flow:**
1. n8n check email for attachments
2. Parse quote (PDF/Excel)
3. Extract: supplier, items, prices
4. Compare with:
   - Previous prices
   - Other supplier quotes (same period)
5. Generate comparison report
6. Notif purchasing: "Price comparison ready"
7. Recommend: lowest price / best value

---

### 4.5 Import Material Tracking
```
PO for Import → Track Shipment → Customs Alert
```
**Trigger:** PO with supplier type = 'import'

**Tracking:**
- ETD (Estimated Time of Departure)
- ETA (Estimated Time of Arrival)
- Arrival at port
- Customs clearance
- Delivery to warehouse

**Flow:**
1. PO confirmed with import items
2. Create shipment tracking record
3. Check tracking daily (for major ports)
4. Alert 7 days before ETA
5. Alert on arrival
6. Alert on customs clearance
7. Notif when delivered to warehouse

---

## 5. MANUFACTURING

### 5.1 Production Order Creation
```
SO Confirmed → Create MO → Schedule Production
```
**Trigger:** SO confirmed

**Flow:**
1. SO confirmed
2. n8n read order line products
3. For each product:
   - Check if make-to-order
   - Check BoM exists
   - Calculate qty needed
4. Create MO in Odoo via XML-RPC
5. Set scheduled date = SO delivery date - production_days
6. Assign to production line
7. Notif production manager

---

### 5.2 Production Scheduling
```
MO Created → Schedule Based on Capacity → Adjust Timeline
```
**Trigger:** MO confirmed

**Scheduling Rules:**
| Production Line | Capacity/Day | Changeover Time |
|----------------|--------------|-----------------|
| Line A (Liquid) | 5000 pcs | 2 hours |
| Line B (Cream) | 3000 pcs | 3 hours |
| Line C (Powder) | 2000 pcs | 4 hours |

**Flow:**
1. MO created
2. Calculate production time based on:
   - Product type
   - Qty
   - Line capacity
3. Find available slot
4. If conflict: suggest alternative dates
5. Update MO schedule
6. Notif production team with schedule

---

### 5.3 Material Allocation
```
MO Scheduled → Allocate Materials → Reserve Stock
```
**Trigger:** MO scheduled

**Flow:**
1. MO scheduled
2. n8n read BoM
3. For each component:
   - Check available stock
   - Reserve qty needed
4. If insufficient stock:
   - Create purchase request
   - Alert purchasing
   - Calculate new schedule (based on material arrival)
5. Confirm material allocation in Odoo

---

### 5.4 Production Progress Tracking
```
MO Started → Update Progress → Alert if Delayed
```
**Trigger:** MO state changed to 'progress'

**Tracking:**
- Started time
- Current stage (Mixing/Filling/Packing)
- Expected completion
- Actual vs planned

**Flow:**
1. MO started
2. Start tracking timer
3. Check progress every 2 hours:
   - Query MO state
   - Compare to expected progress
4. If behind schedule:
   - Calculate delay hours
   - Alert production manager
   - Suggest overtime
5. On completion:
   - Calculate actual production time
   - Update efficiency metrics

---

### 5.5 Quality Check Trigger
```
MO Done → Create QC Check → Hold Until Approved
```
**Trigger:** MO state changed to 'done'

**QC Steps:**
1. MO marked done
2. n8n create QC order in Odoo:
   - Sample selection (per batch)
   - Test parameters (pH, viscosity, microbial)
   - Assign to QC team
3. Hold FG in QC location
4. Notif QC team: "New batch ready for inspection"
5. On QC pass: Move to FG stock
6. On QC fail: Alert + create return

---

### 5.6 Batch Traceability
```
Production Complete → Generate Batch Info → Store Data
```
**Data Generated:**
```json
{
  "batch_number": "BN/2026/09/0001",
  "production_date": "2026-09-05",
  "product": "Face Serum Vitamin C 30ml",
  "qty_produced": 1000,
  "batch_size": 1000,
  "line": "Line A",
  "operator": "Operator A",
  "materials_used": [
    {"code": "BB-VITC", "lot": "LOT-2026-08-001", "qty": 5},
    {"code": "BB-GLYC", "lot": "LOT-2026-08-003", "qty": 10}
  ],
  "qc_status": "PASSED",
  "expiry_date": "2027-09-05"
}
```

**Flow:**
1. MO completed
2. n8n generate batch number
3. Capture all tracking data
4. Store in Odoo (custom batch model)
5. Generate QR code with batch info
6. Link to delivery for traceability

---

## 6. INVENTORY & WAREHOUSE

### 6.1 Stock Level Monitoring
```
Scheduled Check → Monitor All Levels → Alert Anomalies
```
**Trigger:** Every 4 hours

**Checks:**
1. Stock levels by category
2. Compare to:
   - Reorder point
   - Safety stock
   - Max stock
3. Detect anomalies:
   - Sudden drop (possible theft/loss)
   - Sudden increase (data error)
   - Negative stock (shouldn't happen)
4. Generate stock report
5. Notif warehouse manager

---

### 6.2 Stock Opname Automation
```
Cycle Count → Compare System vs Physical → Adjust
```
**Trigger:** Scheduled (weekly for ABC items, monthly for all)

**Flow:**
1. Generate cycle count list
2. Send to warehouse team (WA/Email)
3. Receive physical count data
4. Compare with system
5. Calculate variance
6. If variance > threshold:
   - Require investigation
   - Manager approval
7. Post adjustment in Odoo
8. Update inventory valuation

---

### 6.3 Expired Material Alert
```
Check Expiry → Flag Expired → Dispose/Use First
```
**Trigger:** Daily at 07:00

**Flow:**
1. Query materials with:
   - lot_id.expiry_date <= today + 30 days
2. Categorize:
   - Expired: Cannot use
   - Expiring soon: Use first (FEFO)
3. For expired:
   - Move to quarantine location
   - Create disposal request
   - Alert finance for write-off
4. For expiring soon:
   - Flag for production priority
   - Notify production to use first

---

### 6.4 Inter-warehouse Transfer
```
Transfer Request → Approve → Execute → Confirm
```
**Trigger:** Transfer request created

**Flow:**
1. Transfer request submitted
2. Check source stock availability
3. Manager approval (if qty > threshold)
4. Execute transfer
5. Update both locations
6. Notif destination warehouse

---

### 6.5 Scrap/Waste Recording
```
Production Scrap → Record → Report → Analysis
```
**Trigger:** Manual entry or MO close

**Data:**
- Product
- Qty scrapped
- Reason (damaged, expired, rejected, overflow)
- Cost impact

**Flow:**
1. Scrap recorded in Odoo
2. n8n capture event
3. Calculate cost impact
4. Update production cost
5. Weekly scrap report
6. Trend analysis (identify issues)

---

## 7. LOGISTICS & DELIVERY

### 7.1 Delivery Scheduling
```
SO Ready → Schedule Delivery → Assign Driver/Vehicle
```
**Trigger:** FG ready for delivery

**Flow:**
1. FG available in stock
2. Group deliveries by:
   - Location (same city/region)
   - Delivery date
3. Create delivery route
4. Assign vehicle + driver
5. Update SO with delivery schedule
6. Notif customer: Delivery scheduled

---

### 7.2 Delivery Tracking
```
Delivery Out for Delivery → Track → Update Customer
```
**Trigger:** DO state = 'out_for_delivery'

**Updates:**
- Driver location (GPS if available)
- ETA updates
- Delivery confirmation

**Flow:**
1. DO dispatched
2. n8n receive tracking update
3. Update ETA
4. Notif customer: "Driver en route, ETA [time]"
5. On completion: Confirm delivery
6. Notif: "Delivery completed"

---

### 7.3 Failed Delivery Handling
```
Delivery Attempt Failed → Re-attempt → Notif Customer
```
**Trigger:** DO state = 'failed_delivery'

**Reasons:**
- Customer not available
- Wrong address
- Refused delivery

**Flow:**
1. Delivery failed
2. n8n capture failure reason
3. Schedule re-attempt
4. Notif customer: "Delivery attempt failed, we will try again on [date]"
5. If 3 failures: Escalate to sales team
6. Update DO with attempt log

---

### 7.4 Return/Reverse Logistics
```
Return Request → Process → Credit/Replace
```
**Trigger:** Customer complaint or return request

**Flow:**
1. Return request received
2. Create return order in Odoo
3. Send return label to customer
4. Track return shipment
5. On receipt: QC check
6. If valid return:
   - Refund or replacement
   - Update inventory
7. Notif customer: Resolution
8. Update customer satisfaction score

---

### 7.5 Delivery Performance Report
```
Weekly → Generate Report → Analyze Performance
```
**Trigger:** Every Monday 08:00

**Metrics:**
- Total deliveries
- On-time rate
- First-attempt success rate
- Average delivery time
- Failed deliveries
- Customer feedback

**Flow:**
1. Aggregate delivery data
2. Calculate metrics
3. Generate report
4. Compare with previous weeks
5. Identify issues
6. Notif logistics manager
7. Create improvement tasks

---

## 8. FINANCE & ACCOUNTING

### 8.1 Invoice Generation
```
Delivery Completed → Generate Invoice → Send to Customer
```
**Trigger:** DO state = 'delivered'

**Flow:**
1. Delivery confirmed
2. n8n read DO details
3. Generate invoice:
   - Based on SO terms
   - Include delivery reference
4. Post invoice in Odoo
5. Send to customer (Email + WA)
6. Set payment due date (Net 30/60)
7. Add to accounts receivable

---

### 8.2 Payment Tracking
```
Invoice Due → Track → Send Reminder → Follow-up
```
**Trigger:** Scheduled daily

**Reminders:**
| Days Overdue | Action |
|--------------|--------|
| 0 | Invoice due today |
| 3 | Gentle reminder |
| 7 | Payment reminder |
| 14 | Urgent reminder |
| 30 | Escalate to manager |

**Flow:**
1. Check all open invoices
2. Calculate days overdue
3. For each overdue:
   - Send appropriate reminder
   - Log in Odoo
4. If > 30 days: Escalate
5. Update aging report

---

### 8.3 Payment Received
```
Payment Received → Reconcile → Update Records
```
**Trigger:** Bank statement import or manual entry

**Flow:**
1. Payment received
2. Match to invoice:
   - By amount
   - By reference
   - By customer
3. Reconcile in Odoo
4. Update AR aging
5. Notif customer: Payment received, thank you
6. Update customer payment history

---

### 8.4 Supplier Payment
```
PO Receipt → Generate Bill → Pay Supplier
```
**Trigger:** PO receipt validated

**Flow:**
1. Materials received
2. Generate vendor bill:
   - Based on PO price
   - Adjust for qty variance
3. Post bill in Odoo
4. Track payment terms
5. On due date: Create payment
6. Execute payment
7. Reconcile in Odoo

---

### 8.5 Cost Center Reporting
```
Monthly → Generate Cost Report → Analyze Profitability
```
**Trigger:** End of month

**Reports:**
- Cost by product
- Cost by customer
- Cost by sales channel
- Margin analysis
- Variance report

**Flow:**
1. Close month
2. Generate reports from Odoo
3. Calculate actual vs standard cost
4. Analyze profitability:
   - By product
   - By customer
   - By project (for private label)
5. Generate PDF report
6. Notif management
7. Create action items for negative variance

---

### 8.6 Tax Compliance
```
Transactions → Calculate Tax → Prepare Reports
```
**Trigger:** Scheduled (monthly for reports, real-time for recording)

**Tax Types:**
- PPN (VAT 11%)
- PPh 23 (Withholding tax)
- PPh 21 (Employee tax)

**Flow:**
1. Record all taxable transactions
2. Calculate tax amounts
3. Generate tax report
4. Prepare SPT (tax return)
5. Notif finance for review
6. On approval: Submit tax

---

## 9. QUALITY CONTROL

### 9.1 Incoming QC (Raw Materials)
```
PO Received → QC Check → Accept/Reject
```
**Trigger:** Receipt in warehouse

**QC Parameters:**
| Material Type | Tests |
|--------------|-------|
| Powder (Vitamin C, Niacinamide) | Identity, Purity, Moisture |
| Liquid (Glycerin, Aloe Vera) | pH, Specific Gravity, Micro |
| Packaging (Bottle, Box) | Dimension, Appearance, Strength |

**Flow:**
1. Materials received
2. Generate QC order
3. Assign to QC technician
4. Record test results
5. If PASS: Move to stock
6. If FAIL: Reject + return to supplier
7. Update supplier score

---

### 9.2 In-Process QC (Production)
```
During Production → Spot Check → Adjust if Needed
```
**Trigger:** Production at specific stage

**Checks:**
- Mixing: Uniformity, pH
- Filling: Weight check, seal integrity
- Packaging: Label accuracy, appearance

**Flow:**
1. Production at check point
2. QC technician performs check
3. Record results
4. If out of spec:
   - Alert production
   - Investigate cause
   - Adjust if possible
5. Log all checks

---

### 9.3 Final Product QC
```
Production Complete → Final QC → Release to Stock
```
**Trigger:** MO completed

**Final Tests:**
- Appearance
- Weight
- pH
- Micro test (sample)
- Packaging integrity

**Flow:**
1. MO marked complete
2. Create final QC order
3. Random sample selection (per batch size)
4. Perform all tests
5. Record in Odoo
6. If PASS: Release to FG stock
7. If FAIL: Hold for investigation

---

### 9.4 Customer Complaint Handling
```
Complaint Received → Investigate → Resolve → Prevent
```
**Trigger:** Complaint ticket created

**Flow:**
1. Complaint received (WA, Email, Phone)
2. Create ticket in Odoo
3. Assign to QC team
4. Investigate:
   - Check batch records
   - Contact production
   - Request sample return
5. Determine root cause
6. Take corrective action
7. Respond to customer
8. If systemic: Update SOP

---

### 9.5 QC Metrics Dashboard
```
Weekly → Generate QC Metrics → Track Trends
```
**Metrics:**
- First pass rate
- Rejection rate by type
- Complaint rate
- Supplier quality score
- In-process defect rate

**Flow:**
1. Aggregate QC data
2. Calculate metrics
3. Compare to targets
4. Identify trends
5. Generate dashboard
6. Notif QC manager
7. Create improvement tasks

---

## 10. CUSTOMER SERVICE

### 10.1 Customer Onboarding
```
New Customer → Welcome → Introduce Services
```
**Trigger:** New customer created in Odoo

**Flow:**
1. Customer record created
2. n8n welcome sequence:
   - Welcome email
   - Introduction to services
   - Request for requirements form
   - Share catalog
3. Create onboarding task list
4. Assign to account manager
5. Schedule introduction call

---

### 10.2 Account Review
```
Quarterly → Review Account → Identify Opportunities
```
**Trigger:** Every quarter

**Review Points:**
- Order frequency
- Order value
- Product mix
- Payment history
- Satisfaction score

**Flow:**
1. Generate account summary
2. Calculate metrics
3. Identify upsell opportunities
4. Review contract terms
5. Schedule review meeting
6. Create action items

---

### 10.3 Customer Feedback Collection
```
Post-Delivery → Request Feedback → Collect NPS
```
**Trigger:** 7 days after delivery

**Flow:**
1. Delivery confirmed
2. Wait 7 days
3. Send feedback request:
   - Survey link
   - WA follow-up
4. Collect NPS (0-10)
5. Record in Odoo
6. If NPS < 7: Escalate to manager
7. Aggregate for quarterly report

---

### 10.4 Loyalty Program
```
Track Orders → Calculate Points → Reward
```
**Trigger:** Order completed

**Program Rules:**
- 1 point per Rp 10,000 spent
- Redeem: 100 points = Rp 10,000 discount
- Birthday bonus: 2x points

**Flow:**
1. Order completed
2. Calculate points earned
3. Update customer loyalty record
4. If milestone reached (1000 pts):
   - Send reward notification
5. On redemption:
   - Apply discount to new order
   - Deduct points

---

### 10.5 Churn Prevention
```
No Order > 90 Days → Investigate → Reactivate
```
**Trigger:** Scheduled weekly

**Flow:**
1. Find customers with last order > 90 days
2. Segment:
   - High value, inactive
   - Medium value, inactive
   - Low value, inactive
3. For high value:
   - Personal outreach from sales
   - Special offer
4. For medium value:
   - Send promotions
   - Share new products
5. For low value:
   - Email campaign
6. Track reactivation rate

---

## 11. REPORTING & ANALYTICS

### 11.1 Daily Sales Report
```
Every Day 08:00 → Generate Report → Send to Team
```
**Report Content:**
```json
{
  "date": "2026-09-05",
  "new_leads": 5,
  "leads_converted": 2,
  "quotations_sent": 3,
  "orders_confirmed": 2,
  "order_value": 85000000,
  "deliveries_completed": 3,
  "revenue": 65000000,
  "top_products": ["Face Serum", "Body Lotion"],
  "pending_quotations": 8,
  "overdue_invoices": 2
}
```

---

### 11.2 Weekly Operations Report
```
Every Monday 08:00 → Generate Report → Management
```
**Report Content:**
- Production output vs target
- MO completion rate
- QC pass rate
- Inventory turnover
- Delivery performance
- Customer complaints

---

### 11.3 Monthly Financial Report
```
End of Month → Generate Report → Management Review
```
**Report Content:**
- Revenue by product category
- Gross margin by product
- Top customers by revenue
- Expenses breakdown
- Profitability by segment
- Cash flow
- AR aging

---

### 11.4 Custom Analytics Dashboard
```
On-Demand → Query Data → Display Dashboard
```
**Dashboard Views:**
- Sales Pipeline
- Production Status
- Inventory Heatmap
- Customer Health Score
- Supplier Performance

---

## 12. INTEGRATIONS

### 12.1 E-Commerce Integration (Shopee/Tokopedia)
```
Marketplace Order → n8n → Odoo SO → Update Stock
```
**Trigger:** Webhook from marketplace

**Flow:**
1. Order placed on marketplace
2. Marketplace webhook sent to n8n
3. Parse order data
4. Create SO in Odoo
5. Reserve inventory
6. Update marketplace stock (if sync enabled)
7. Notif customer (via marketplace)
8. Update Odoo on shipment

---

### 12.2 Accounting Software Integration
```
Odoo Transactions → Sync to Accounting Software
```
**Sync Data:**
- Customer invoices
- Vendor bills
- Payments
- Journal entries

**Flow:**
1. Transaction recorded in Odoo
2. n8n trigger on create/update
3. Transform data format
4. Push to accounting software
5. Handle sync errors

---

### 12.3 Shipping Integration (JNE/SiCepat)
```
DO Created → Request Pickup → Get Tracking
```
**Trigger:** DO confirmed, ready for shipping

**Flow:**
1. DO ready for shipment
2. n8n create shipment request to API
3. Get tracking number
4. Update DO with tracking
5. Send tracking to customer

---

### 12.4 Payment Gateway Integration
```
Online Payment → Confirm → Process Order
```
**Trigger:** Payment notification webhook

**Flow:**
1. Payment received
2. Verify with payment gateway
3. Update invoice status
4. Trigger fulfillment
5. Send confirmation to customer

---

# PART 2: N8N NODE CONFIGURATIONS

## ODOO XML-RPC COMMANDS

### Authentication
```
URL: http://erp_duanaga_odoo:8069/xmlrpc/2/common
Method: authenticate
Params: [db, login, password, {}]
Returns: uid (integer)
```

### Create Record
```
Model: crm.lead
Method: create
Params: [{name, contact_name, email_from, phone, description, type}]
```

### Search Records
```
Model: sale.order
Method: search_read
Params: [domain, {fields: [...], limit: 50}]
Domain examples:
- [['state', '=', 'sale']]
- [['date_order', '>=', '2026-09-01']]
- [['partner_id', '=', partner_id]]
```

### Update Record
```
Model: sale.order
Method: write
Params: [[id], {state: 'sale'}]
```

### Call Method
```
Model: sale.order
Method: action_confirm
Params: [[id]]
```

---

## WHATSAPP API (UltraMsg)

### Send Message
```
POST https://api.ultramsg.com/{instance_id}/messages/chat
Body:
{
  "token": "your_token",
  "to": "+628123456789",
  "body": "Message text"
}
```

### Send Template
```
POST https://api.ultramsg.com/{instance_id}/messages
Body:
{
  "token": "your_token",
  "to": "+628123456789",
  "template": "your_template_id",
  "vars": ["John", "September 15"]
}
```

---

## TELEGRAM CONFIGURATION

### Bot Setup
1. Message @BotFather
2. Create bot: /newbot
3. Get bot token: 123456789:ABCdef...
4. Add bot to group
5. Get group ID via @userinfobot

### Send Message
```
POST https://api.telegram.org/bot{TOKEN}/sendMessage
Body:
{
  "chat_id": "-1001234567890",
  "text": "Message text",
  "parse_mode": "HTML"
}
```

---

# PART 3: IMPLEMENTATION PRIORITY

## Phase 1: Critical (Week 1)
1. Lead Capture from Website
2. SO Confirmation Notifications
3. Daily Report
4. Low Stock Alert

## Phase 2: Important (Week 2-3)
5. Quotation Follow-up
6. Production Progress Tracking
7. Delivery Notifications
8. Invoice Reminders

## Phase 3: Enhancement (Week 4+)
9. Customer Feedback Collection
10. E-commerce Integration
11. Advanced Analytics
12. Loyalty Program

## Phase 4: Optimization (Month 2+)
13. AI-based Lead Scoring
14. Predictive Demand Planning
15. Cost Optimization Suggestions
16. Custom Dashboards

---

# PART 4: ERROR HANDLING

## Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| Odoo connection timeout | Container not ready | Add retry with exponential backoff |
| Duplicate leads | Multiple form submissions | Add deduplication logic |
| Invalid phone format | Country code missing | Validate & auto-add +62 |
| Workflow stuck | Node error | Add error handling + alert |
| Data sync failure | Schema mismatch | Log error + manual review |

## Monitoring

- Enable n8n execution logging
- Set up error alerts (Telegram)
- Monitor Odoo XML-RPC response time
- Track failed webhook deliveries

---

# APPENDIX: WORKFLOW TEMPLATES

Each workflow JSON file includes:
- Workflow name
- Trigger configuration
- Node connections
- Error handling
- Test data

Files:
- `wf-lead-capture.json`
- `wf-daily-report.json`
- `wf-low-stock-alert.json`
- `wf-so-confirmed.json`
- `wf-delivery-done.json`
- `wf-invoice-reminder.json`
- `wf-production-tracking.json`
- `wf-customer-feedback.json`

---

*Document Version: 1.0*
*Last Updated: 2026-09-05*
*Author: Claude AI for PT Dua Naga Kosmetindo*
