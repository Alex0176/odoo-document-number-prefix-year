# Copyright 2026 Biricon IT Services GmbH
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
from odoo import api, models

from .numbering import is_new_name, next_number


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            company = self.env["res.company"].browse(vals.get("company_id")) or self.env.company
            prefix = company.document_number_purchase_prefix
            if prefix and is_new_name(self.env, vals.get("name")):
                vals["name"] = next_number(self.env, company, prefix, "purchase_order", "name")
        return super().create(vals_list)
