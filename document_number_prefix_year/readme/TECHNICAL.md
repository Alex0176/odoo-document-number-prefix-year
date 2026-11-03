**Where the numbers are assigned**

| Document | Hook | Series |
|---|---|---|
| Quotation | ``sale.order.create`` when ``name`` is empty, ``/`` or *New* | quotation prefix |
| Sales order | ``sale.order.action_confirm`` (before the standard confirmation) | order prefix |
| Customer invoice / credit note | ``account.move._set_next_sequence`` (called when posting) | invoice / credit note prefix |
| Delivery / receipt | ``stock.picking.create`` by operation type (*outgoing* / *incoming*) | delivery / receipt prefix |
| Purchase order | ``purchase.order.create`` | purchase prefix |

The company fields (``document_number_*``) are mirrored on ``res.config.settings``.

**Counter logic** (``models/numbering.py``)

- Number = prefix + year (``%y`` or ``%Y``) + counter padded to the configured number of digits.
- The highest counter is found with a regular expression on the stored name
  (``^<stem>([0-9]{1,15})$``, the stem is escaped), per company; names without a company are included.
- A transaction-level advisory lock (``pg_advisory_xact_lock``) per company and stem serialises the assignment.
- Odoo works with ``REPEATABLE READ``: the snapshot of a transaction that waited for the lock predates the
  commit of the transaction that held it, so the first read can miss that number. Therefore the highest number is
  read a second time with a short-lived cursor (``registry.cursor()``) that sees all committed rows; the larger
  value wins. The first read still covers numbers assigned earlier *in the same transaction*, which the second
  cursor cannot see. Without the second read, two orders created at the same moment got the same number in a
  test (neither ``sale.order`` nor ``purchase.order`` has a unique constraint on the name).

**Invoices:** ``_set_next_sequence`` writes the name and calls ``_compute_split_sequence`` so that Odoo's sequence
mixin (prefix, number, year detection for the next invoice of the same journal) stays consistent.
