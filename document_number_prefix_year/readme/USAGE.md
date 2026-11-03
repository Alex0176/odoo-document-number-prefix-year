**Numbering a quotation and its order**

1. Create a quotation: it gets the next number of the quotation series, e.g. ``AN26000001``.
2. Confirm it: with *New number on confirmation* switched on (default) the order gets the next number of the
   sales order series, e.g. ``AU26000001``. The quotation number stays on the order in the field
   *Quotation Number* (form, list, search).
3. If the order prefix is empty, or the name does not start with the quotation prefix (e.g. the number was typed
   by hand), the order keeps its name.

**Invoices and credit notes**

Customer invoices and credit notes get their number **when they are posted**, not when they are created, so drafts
that are deleted never leave a gap. The year is taken from the *invoice date*, not from today: an invoice dated
2025-12-30 that is posted on 2026-01-02 is numbered ``RE25...``. Invoices and credit notes of all sales journals of
a company share one counter per prefix. Vendor bills and miscellaneous entries are not touched.

**Deliveries, receipts and purchase orders**

Pickings of type *Delivery* and *Receipt* and purchase orders / requests for quotation are numbered when they are
created.

**Importing numbers from another system**

Import the old documents with their original names. The next new document continues after the highest number of
the same prefix and year, whatever its length: with ``AN26119`` in the database the next quotation is
``AN26000120``.

**Switching it off**

Empty a prefix and that document type is numbered by Odoo again. Existing names are never changed.
