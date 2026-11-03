- **Quotations are numbered on creation.** Quotations that are deleted or cancelled leave gaps in the quotation
  series, and so does every sales order created by another module: carts of the e-commerce shop (*website_sale*)
  are sales orders in the state *Quotation* and use up a number each. Only customer invoices and credit notes are
  gapless (numbered on posting).
- **Changing the year format** (two digits ↔ four digits) in a running system confuses the counter: with ``AN26``
  as stem, an existing ``AN2026000001`` is read as counter ``26000001``. Decide on the format before the first
  document.
- **Counters have at most 15 digits.** Longer digit strings after the stem are ignored when looking for the
  highest number.
- **No separate series per journal or warehouse.** The counter is per company, prefix and year. Several sales
  journals share the invoice counter.
- **Prefixes** must not contain spaces and must not end with a digit (otherwise prefix, year and counter cannot be
  told apart); the settings reject such prefixes.
- Only the numbers of the document types listed in the description are handled. Vendor bills, payments, journal
  entries, manufacturing orders and similar documents keep the standard Odoo sequences.
- The tests cover the numbering rules with ordinary transactions. The behaviour with two users numbering at the
  same time was verified by hand against a copy of a production database (two transactions, the second waiting
  for the first) but is not part of the automatic tests.
