=====================================
Document Numbering by Prefix and Year
=====================================

Numbers quotations, sales orders, customer invoices and credit notes, delivery orders, receipts and
purchase orders as **prefix + year + counter**, e.g. ``AN26000001``.

**License:** LGPL-3 · **Author:** Biricon IT Services GmbH · **Odoo:** 19.0

========================  ==============  ================
Document                  Example prefix  Example number
========================  ==============  ================
Quotation                 AN              AN26000001
Sales order               AU              AU26000001
Customer invoice          RE              RE26000001
Customer credit note      GU              GU26000001
Delivery order            LI              LI26000001
Receipt                   WE              WE26000001
Purchase order / RFQ      BE              BE26000001
========================  ==============  ================

Features
========

* The counter restarts at 1 every year (per company and prefix).
* It continues after the highest existing number of the same prefix and year, whatever its length, so
  numbers imported from another system (e.g. ``AN26119``) are respected: the next one is ``AN26000120``.
* A confirmed quotation can get a new sales order number; the quotation number is kept on the order.
* Customer invoices and credit notes are numbered on posting (gapless); the year is taken from the
  invoice date.
* Numbers are assigned under a lock per company, prefix and year; the highest number is also read with a
  second cursor so that numbers committed by a concurrent transaction are not missed (Odoo uses
  ``REPEATABLE READ``).
* Does nothing until a prefix is entered: an empty prefix keeps the standard Odoo numbering.

Installation
============

Requirements
------------

- Odoo 19.0 with the standard apps *Sales*, *Purchase*, *Inventory* and *Invoicing* (installed with the module
  if missing). No external Python packages, no network access.

Installation
------------

1. Put the folder ``document_number_prefix_year`` into the addons path, update the apps list and install
   *Document Numbering by Prefix and Year*.
2. Installing changes nothing: all prefixes are empty, so Odoo keeps its standard numbering until you enter a
   prefix in *Settings → Document Numbering*.
3. **Production systems:** configure the prefixes at a quiet moment and *before* documents of the new year are
   created. Existing documents keep their names; the counter continues after the highest existing number of the
   same prefix and year.

Configuration
=============

*Settings → Document Numbering* (per company):

* prefixes for quotation, sales order, invoice, credit note, delivery order, receipt and purchase order
  (leave empty to keep the standard Odoo numbering for that document type); a prefix must not contain spaces
  or end with a digit
* year format (``26`` or ``2026``)
* number of counter digits (default 6)
* new number on confirmation of a quotation

Usage
=====

Quotation and order
-------------------

A quotation gets the next number of the quotation series (``AN26000001``). When it is confirmed, the order gets
the next number of the sales order series (``AU26000001``) and the quotation number stays in the field
*Quotation Number*. If the order prefix is empty or the name does not start with the quotation prefix, the order
keeps its name.

Invoices and credit notes
-------------------------

Numbered when posted, so deleted drafts leave no gap. The year comes from the *invoice date*: an invoice dated
2025-12-30 and posted on 2026-01-02 is ``RE25...``. All sales journals of a company share one counter per prefix.
Vendor bills and miscellaneous entries are not touched.

Deliveries, receipts, purchase orders
-------------------------------------

Pickings of type *Delivery* and *Receipt* and purchase orders are numbered when they are created.

Importing numbers from another system
--------------------------------------

Import the old documents with their original names. The next new document continues after the highest number
of the same prefix and year: with ``AN26119`` in the database the next quotation is ``AN26000120``.

Switching it off
----------------

Empty a prefix and that document type is numbered by Odoo again. Existing names are never changed.

Known issues
============

* **Quotations are numbered on creation.** Deleted or cancelled quotations leave gaps, and so does every sales
  order created by another module: carts of the e-commerce shop (*website_sale*) are sales orders in the
  state *Quotation* and use up a number each. Only customer invoices and credit notes are gapless.
* **Changing the year format** (two ↔ four digits) in a running system confuses the counter: with the stem
  ``AN26`` an existing ``AN2026000001`` is read as counter ``26000001``. Decide on the format before the first
  document.
* Counters have at most 15 digits; longer digit strings are ignored when looking for the highest number.
* No separate series per journal or warehouse: the counter is per company, prefix and year.
* Vendor bills, payments, journal entries, manufacturing orders etc. keep the standard Odoo sequences.
* The behaviour with two users numbering at the same time was verified by hand against a copy of a production
  database but is not part of the automatic tests.

Technical notes
===============

====================================  ===============================================================
Document                              Hook
====================================  ===============================================================
Quotation                             ``sale.order.create`` (name empty, ``/`` or *New*)
Sales order                           ``sale.order.action_confirm`` (before the standard confirmation)
Customer invoice / credit note        ``account.move._set_next_sequence`` (called when posting)
Delivery / receipt                    ``stock.picking.create`` by operation type
Purchase order                        ``purchase.order.create``
====================================  ===============================================================

The highest counter is found with a regular expression on the stored name (``^<stem>([0-9]{1,15})$``, the stem
is escaped), per company. A transaction-level advisory lock (``pg_advisory_xact_lock``) per company and stem
serialises the assignment. Because the snapshot of a transaction that waited for the lock predates the commit of
the transaction that held it, the highest number is read a second time with a short-lived cursor
(``registry.cursor()``); the larger value wins. Without that second read, two orders created at the same moment
got the same number in a test (neither ``sale.order`` nor ``purchase.order`` has a unique constraint on the name).

Tests
-----

::

    odoo-bin -d <test database> -i document_number_prefix_year --test-enable \
        --test-tags=/document_number_prefix_year --stop-after-init

Changelog
=========

**19.0.1.0.0 (2026-11-03)** - first version.

Credits
=======

Authors: Biricon IT Services GmbH
