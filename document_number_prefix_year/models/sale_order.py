# Copyright 2026 Biricon IT Services GmbH
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
from odoo import api, fields, models

from .numbering import is_new_name, next_number


class SaleOrder(models.Model):
    _inherit = "sale.order"

    quotation_number = fields.Char(
        copy=False, readonly=True, index=True,
        help="Number of the quotation this order was confirmed from.",
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            company = self.env["res.company"].browse(vals.get("company_id")) or self.env.company
            prefix = company.document_number_quotation_prefix
            if prefix and is_new_name(self.env, vals.get("name")):
                vals["name"] = next_number(self.env, company, prefix, "sale_order", "name")
        return super().create(vals_list)

    def action_confirm(self):
        for order in self.filtered(lambda o: o.state in ("draft", "sent")):
            company = order.company_id
            q_prefix, o_prefix = company.document_number_quotation_prefix, company.document_number_order_prefix
            if (
                company.document_number_renumber_on_confirm
                and o_prefix
                and (not q_prefix or (order.name or "").startswith(q_prefix))
                and not (order.name or "").startswith(o_prefix)
            ):
                order.write({
                    "quotation_number": order.name,
                    "name": next_number(self.env, company, o_prefix, "sale_order", "name"),
                })
        return super().action_confirm()
