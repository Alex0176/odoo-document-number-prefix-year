# Copyright 2026 Biricon IT Services GmbH
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    document_number_quotation_prefix = fields.Char(related="company_id.document_number_quotation_prefix", readonly=False)
    document_number_order_prefix = fields.Char(related="company_id.document_number_order_prefix", readonly=False)
    document_number_invoice_prefix = fields.Char(related="company_id.document_number_invoice_prefix", readonly=False)
    document_number_refund_prefix = fields.Char(related="company_id.document_number_refund_prefix", readonly=False)
    document_number_delivery_prefix = fields.Char(related="company_id.document_number_delivery_prefix", readonly=False)
    document_number_receipt_prefix = fields.Char(related="company_id.document_number_receipt_prefix", readonly=False)
    document_number_purchase_prefix = fields.Char(related="company_id.document_number_purchase_prefix", readonly=False)
    document_number_digits = fields.Integer(related="company_id.document_number_digits", readonly=False)
    document_number_year_digits = fields.Selection(related="company_id.document_number_year_digits", readonly=False)
    document_number_renumber_on_confirm = fields.Boolean(
        related="company_id.document_number_renumber_on_confirm", readonly=False
    )
