# Copyright 2026 Biricon IT Services GmbH
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
from odoo import api, models

from .numbering import is_new_name, next_number


class StockPicking(models.Model):
    _inherit = "stock.picking"

    @api.model_create_multi
    def create(self, vals_list):
        PickingType = self.env["stock.picking.type"]
        for vals in vals_list:
            ptype = PickingType.browse(vals.get("picking_type_id") or self.env.context.get("default_picking_type_id"))
            if not ptype or not is_new_name(self.env, vals.get("name")):
                continue
            company = ptype.company_id or self.env.company
            prefix = {
                "outgoing": company.document_number_delivery_prefix,
                "incoming": company.document_number_receipt_prefix,
            }.get(ptype.code)
            if prefix:
                vals["name"] = next_number(self.env, company, prefix, "stock_picking", "name")
        return super().create(vals_list)
