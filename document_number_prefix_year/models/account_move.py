# Copyright 2026 Biricon IT Services GmbH
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
from odoo import models

from .numbering import next_number


class AccountMove(models.Model):
    _inherit = "account.move"

    def _document_number_prefix(self):
        self.ensure_one()
        if self.journal_id.type != "sale":
            return False
        company = self.company_id
        return {
            "out_invoice": company.document_number_invoice_prefix,
            "out_refund": company.document_number_refund_prefix,
        }.get(self.move_type)

    def _set_next_sequence(self):
        """Customer invoices and credit notes: number on posting (gapless), year from the invoice date."""
        self.ensure_one()
        prefix = self._document_number_prefix()
        if not prefix:
            return super()._set_next_sequence()
        name = next_number(self.env, self.company_id, prefix, "account_move", "name", self.invoice_date or self.date)
        self.with_context(clear_sequence_mixin_cache=False)[self._sequence_field] = name
        self._compute_split_sequence()
