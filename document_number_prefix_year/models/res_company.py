# Copyright 2026 Biricon IT Services GmbH
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
from odoo import api, fields, models
from odoo.exceptions import ValidationError

PREFIX_FIELDS = (
    "document_number_quotation_prefix",
    "document_number_order_prefix",
    "document_number_invoice_prefix",
    "document_number_refund_prefix",
    "document_number_delivery_prefix",
    "document_number_receipt_prefix",
    "document_number_purchase_prefix",
    "document_number_bill_prefix",
)


class ResCompany(models.Model):
    _inherit = "res.company"

    document_number_quotation_prefix = fields.Char("Quotation Prefix")
    document_number_order_prefix = fields.Char("Sales Order Prefix")
    document_number_invoice_prefix = fields.Char("Invoice Prefix")
    document_number_refund_prefix = fields.Char("Credit Note Prefix")
    document_number_delivery_prefix = fields.Char("Delivery Order Prefix")
    document_number_receipt_prefix = fields.Char("Receipt Prefix")
    document_number_purchase_prefix = fields.Char("Purchase Order Prefix")
    document_number_bill_prefix = fields.Char(
        "Vendor Bill Prefix",
        help="Vendor bills are numbered <prefix><year><month><counter> (e.g. WE26110001) when set; empty keeps "
        "the standard Odoo numbering.",
    )
    document_number_bill_period = fields.Selection(
        [("month", "Year and month"), ("year", "Year only")], string="Vendor Bill Period", default="month", required=True
    )
    document_number_bill_digits = fields.Integer("Vendor Bill Counter Digits", default=4)
    document_number_digits = fields.Integer("Counter Digits", default=6)
    document_number_year_digits = fields.Selection(
        [("2", "Two digits (26)"), ("4", "Four digits (2026)")], string="Year Format", default="2", required=True
    )
    document_number_renumber_on_confirm = fields.Boolean(
        "New Number on Confirmation",
        default=True,
        help="When a quotation is confirmed it gets a number with the sales order prefix; "
        "the quotation number is kept on the order.",
    )

    @api.constrains(*PREFIX_FIELDS, "document_number_digits", "document_number_bill_digits")
    def _check_document_number_config(self):
        for company in self:
            if not 1 <= company.document_number_digits <= 12:
                raise ValidationError(self.env._("The counter must have between 1 and 12 digits."))
            if not 1 <= company.document_number_bill_digits <= 12:
                raise ValidationError(self.env._("The vendor bill counter must have between 1 and 12 digits."))
            for fname in PREFIX_FIELDS:
                prefix = company[fname]
                if prefix and (not prefix.strip() or prefix[-1].isdigit() or any(c.isspace() for c in prefix)):
                    raise ValidationError(
                        self.env._("Prefix “%(prefix)s” must not contain spaces or end with a digit.", prefix=prefix)
                    )
