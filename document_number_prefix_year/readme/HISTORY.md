**19.0.1.0.0 (2026-11-03)**

- First version: prefix + year + counter for quotations, sales orders, customer invoices and credit notes,
  delivery orders, receipts and purchase orders; new number on confirmation with the quotation number kept;
  continues after imported numbers; per-company settings; German translation.

## 19.0.1.1.0

- Vendor bills and vendor credit notes (purchase journals) can be numbered as prefix + year + month + counter,
  e.g. ``WE26110001``, with the counter restarting every month (setting *Vendor Bills*: prefix, period month or
  year, counter digits). The bill date decides the period. Empty prefix keeps the standard Odoo numbering; existing
  numbers are never changed and the counter only moves forward.

