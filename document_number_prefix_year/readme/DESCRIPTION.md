Numbers sales and purchase documents as **prefix + year + counter**, for example `AN26000001`:

| Document | Example prefix | Example number |
|---|---|---|
| Quotation | AN | AN26000001 |
| Sales order | AU | AU26000001 |
| Customer invoice | RE | RE26000001 |
| Customer credit note | GU | GU26000001 |
| Delivery order | LI | LI26000001 |
| Receipt | WE | WE26000001 |
| Purchase order / RFQ | BE | BE26000001 |

- The counter restarts at 1 every year.
- It always continues after the **highest existing number** of the same prefix and year, whatever its
  length. Numbers migrated or imported from another system (e.g. `AN26119`) are therefore respected and
  the next number is `AN26000120`.
- A confirmed quotation can receive a new sales order number; the quotation number is kept on the order.
- Customer invoices and credit notes are numbered when posted (gapless); their year is the invoice date.
- Everything is configured per company in *Settings → Document Numbering*. An empty prefix keeps the
  standard Odoo numbering for that document type, so the module does nothing until it is configured.
