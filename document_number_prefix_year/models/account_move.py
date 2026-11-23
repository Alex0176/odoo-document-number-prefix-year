# Copyright 2026 Biricon IT Services GmbH
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
from odoo import models

from .numbering import next_number


class AccountMove(models.Model):
    _inherit = "account.move"

    def _document_number_prefix(self):
        self.ensure_one()
        company = self.company_id
        if self.journal_id.type == "purchase":
            if self.move_type in ("in_invoice", "in_refund"):
                return company.document_number_bill_prefix
            return False
        if self.journal_id.type != "sale":
            return False
        return {
            "out_invoice": company.document_number_invoice_prefix,
            "out_refund": company.document_number_refund_prefix,
        }.get(self.move_type)

    def _set_next_sequence(self):
        """Customer invoices and credit notes: number on posting (gapless), year from the invoice date.

        Vendor bills (only if a bill prefix is set): prefix + year + month + counter, e.g. WE26110001; the period
        is taken from the bill date."""
        self.ensure_one()
        prefix = self._document_number_prefix()
        if not prefix:
            return super()._set_next_sequence()
        company = self.company_id
        bill = self.journal_id.type == "purchase"
        name = next_number(
            self.env, company, prefix, "account_move", "name", self.invoice_date or self.date,
            with_month=bill and company.document_number_bill_period == "month",
            digits=company.document_number_bill_digits if bill else None,
        )
        self.with_context(clear_sequence_mixin_cache=False)[self._sequence_field] = name
        self._compute_split_sequence()
