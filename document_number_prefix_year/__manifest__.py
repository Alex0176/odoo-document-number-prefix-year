# Copyright 2026 Biricon IT Services GmbH
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
{
    "name": "Document Numbering by Prefix and Year",
    "summary": "Number quotations, orders, invoices, credit notes, deliveries, receipts and purchase orders as "
    "<prefix><year><counter> (e.g. AN26000001), restarting every year and continuing after imported numbers",
    "version": "19.0.1.1.0",
    "category": "Accounting",
    "author": "Biricon IT Services GmbH",
    "website": "https://github.com/Alex0176/odoo-document-number-prefix-year",
    "license": "LGPL-3",
    "depends": ["sale", "purchase", "stock", "account"],
    "data": [
        "views/res_config_settings_views.xml",
        "views/sale_order_views.xml",
    ],
    "installable": True,
}
