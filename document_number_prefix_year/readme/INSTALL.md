**Requirements**

- Odoo 19.0 with the standard apps *Sales*, *Purchase*, *Inventory* and *Invoicing* (the module depends on
  ``sale``, ``purchase``, ``stock`` and ``account``; they are installed with the module if missing).
- No external Python packages, no network access.

**Installation**

1. Put the folder ``document_number_prefix_year`` into the addons path, update the apps list and install
   *Document Numbering by Prefix and Year*.
2. Installing changes nothing: all prefixes are empty, so Odoo keeps its standard numbering until you enter a
   prefix in *Settings → Document Numbering*.
3. **Production systems:** configure the prefixes at a quiet moment and *before* documents of the new year are
   created. Existing documents keep their names; the counter continues after the highest existing number of the
   same prefix and year.
