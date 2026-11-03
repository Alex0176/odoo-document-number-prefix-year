# Odoo Document Numbering by Prefix and Year

Odoo 19.0 addon by **Biricon IT Services GmbH** (LGPL-3).

| Module | Description |
|---|---|
| [document_number_prefix_year](document_number_prefix_year/) | Numbers quotations, sales orders, customer invoices and credit notes, delivery orders, receipts and purchase orders as `<prefix><year><counter>` (e.g. `AN26000001`). |

## What it does

- **Prefix + year + counter** per document type, e.g. `AN26000001` (quotation), `AU26000001` (order), `RE26000001` (invoice), `GU` (credit note), `LI` (delivery), `WE` (receipt), `BE` (purchase order). Prefixes, year format (`26` / `2026`) and counter length are set per company in *Settings → Document Numbering*.
- **Restarts every year** and **continues after imported numbers**: with `AN26119` from an old system in the database, the next quotation is `AN26000120`.
- **Confirmed quotations** can get a new sales order number; the quotation number stays on the order.
- **Invoices and credit notes** are numbered on posting (gapless), the year comes from the invoice date.
- **Safe under concurrency:** assignment under a lock per company, prefix and year, with an additional read for numbers committed meanwhile (Odoo uses `REPEATABLE READ`).
- **Does nothing until configured:** an empty prefix keeps the standard Odoo numbering.

## Requirements

Odoo 19.0 with *Sales*, *Purchase*, *Inventory* and *Invoicing*. No external dependencies.

## Installation

Put `document_number_prefix_year` into the addons path, update the apps list, install the module and enter the prefixes in *Settings → Document Numbering*.

## Tests

```
odoo-bin -d <test database> -i document_number_prefix_year --test-enable --test-tags=/document_number_prefix_year --stop-after-init
```

## Limitations

Quotations are numbered on creation: deleted quotations and e-commerce carts leave gaps (only invoices and credit notes are gapless). Do not switch between two- and four-digit years in a running system. Details in the [module README](document_number_prefix_year/README.rst). German translation included.
