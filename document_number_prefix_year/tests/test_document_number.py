# Copyright 2026 Biricon IT Services GmbH
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
from datetime import date

from odoo import fields
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestDocumentNumber(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.company = cls.env.company
        cls.company.write({
            "document_number_quotation_prefix": "AN",
            "document_number_order_prefix": "AU",
            "document_number_invoice_prefix": "RE",
            "document_number_refund_prefix": "GU",
            "document_number_delivery_prefix": "LI",
            "document_number_receipt_prefix": "WE",
            "document_number_purchase_prefix": "BE",
            "document_number_digits": 6,
            "document_number_year_digits": "2",
            "document_number_renumber_on_confirm": True,
        })
        cls.yy = fields.Date.context_today(cls.env.user).strftime("%y")
        cls.partner = cls.env["res.partner"].create({"name": "Numbering customer"})
        cls.service = cls.env["product.product"].create(
            {"name": "Service", "type": "service", "invoice_policy": "order", "list_price": 100}
        )
        cls.goods = cls.env["product.product"].create({"name": "Goods", "type": "consu", "list_price": 10})

    def _order(self, **vals):
        return self.env["sale.order"].create(dict(
            {"partner_id": self.partner.id, "order_line": [(0, 0, {"product_id": self.service.id})]}, **vals))

    def _num(self, name):
        return int(name[4:])

    def test_quotation_and_confirmation(self):
        so = self._order()
        self.assertRegex(so.name, r"^AN%s\d{6}$" % self.yy)
        quotation = so.name
        so.action_confirm()
        self.assertRegex(so.name, r"^AU%s\d{6}$" % self.yy)
        self.assertEqual(so.quotation_number, quotation)

    def test_continues_after_imported_number(self):
        self._order(name="AN%s9119" % self.yy)          # e.g. imported from a previous system (other length)
        so = self._order()
        self.assertEqual(so.name, "AN%s%06d" % (self.yy, 9120))

    def test_no_renumber(self):
        self.company.document_number_renumber_on_confirm = False
        so = self._order()
        name = so.name
        so.action_confirm()
        self.assertEqual(so.name, name)
        self.assertFalse(so.quotation_number)

    def test_invoice_refund_and_new_year(self):
        so = self._order()
        so.action_confirm()
        inv = so._create_invoices()
        inv.invoice_date = date(2026, 6, 1)
        inv.action_post()
        self.assertRegex(inv.name, r"^RE26\d{6}$")
        refund = inv._reverse_moves([{"invoice_date": date(2026, 6, 2)}])
        refund.action_post()
        self.assertRegex(refund.name, r"^GU26\d{6}$")
        inv_next_year = self.env["account.move"].create({
            "move_type": "out_invoice", "partner_id": self.partner.id, "invoice_date": date(2099, 1, 5),
            "invoice_line_ids": [(0, 0, {"product_id": self.service.id, "quantity": 1, "price_unit": 5})],
        })
        inv_next_year.action_post()
        self.assertEqual(inv_next_year.name, "RE99000001")

    def test_purchase_and_pickings(self):
        po = self.env["purchase.order"].create(
            {"partner_id": self.partner.id, "order_line": [(0, 0, {"product_id": self.goods.id, "product_qty": 1})]})
        self.assertRegex(po.name, r"^BE%s\d{6}$" % self.yy)
        wh = self.env["stock.warehouse"].search([("company_id", "=", self.company.id)], limit=1)
        out = self.env["stock.picking"].create({"picking_type_id": wh.out_type_id.id, "partner_id": self.partner.id})
        self.assertRegex(out.name, r"^LI%s\d{6}$" % self.yy)
        rec = self.env["stock.picking"].create({"picking_type_id": wh.in_type_id.id, "partner_id": self.partner.id})
        self.assertRegex(rec.name, r"^WE%s\d{6}$" % self.yy)

    def test_empty_prefix_keeps_standard(self):
        self.company.document_number_quotation_prefix = False
        so = self._order()
        self.assertFalse(so.name.startswith("AN"))

    def test_four_digit_year(self):
        self.company.document_number_year_digits = "4"
        so = self._order()
        self.assertRegex(so.name, r"^AN%s\d{6}$" % fields.Date.context_today(self.env.user).strftime("%Y"))

    def test_prefix_with_special_characters(self):
        self.company.document_number_quotation_prefix = "A.(N"
        self._order(name="AXXN%s000500" % self.yy)      # must not match as a regular expression
        so = self._order()
        self.assertEqual(so.name, "A.(N%s000001" % self.yy)

    def test_consecutive_numbers_in_one_transaction(self):
        first, second = self._order(), self._order()
        self.assertEqual(self._num(second.name), self._num(first.name) + 1)

    def test_very_long_digit_strings_are_ignored(self):
        self._order(name="AN%s%s" % (self.yy, "9" * 25))
        so = self._order()
        self.assertRegex(so.name, r"^AN%s\d{6}$" % self.yy)

    def _bill(self, bill_date, price=10):
        return self.env["account.move"].create({
            "move_type": "in_invoice", "partner_id": self.partner.id, "invoice_date": bill_date,
            "invoice_line_ids": [(0, 0, {"product_id": self.goods.id, "quantity": 1, "price_unit": price})],
        })

    def test_vendor_bill_numbers_by_month(self):
        self.company.document_number_bill_prefix = "WE"
        self.company.document_number_bill_digits = 4
        # an old number from another system (counter in the year/month slot) must not disturb the new scheme
        old = self._bill(date(2018, 4, 3))
        old.name = "WE18040019"
        first = self._bill(date(2026, 11, 5))
        first.action_post()
        self.assertEqual(first.name, "WE26110001")
        second = self._bill(date(2026, 11, 20))
        second.action_post()
        self.assertEqual(second.name, "WE26110002")
        december = self._bill(date(2026, 12, 1))
        december.action_post()
        self.assertEqual(december.name, "WE26120001", "the counter restarts every month")
        credit = first._reverse_moves([{"invoice_date": date(2026, 11, 25)}])
        credit.action_post()
        self.assertRegex(credit.name, r"^WE2611\d{4}$")

    def test_vendor_bill_year_only(self):
        self.company.write({"document_number_bill_prefix": "WE", "document_number_bill_period": "year",
                            "document_number_bill_digits": 5})
        bill = self._bill(date(2026, 3, 2))
        bill.action_post()
        self.assertEqual(bill.name, "WE2600001")

    def test_vendor_bill_without_prefix_keeps_standard(self):
        self.company.document_number_bill_prefix = False
        bill = self._bill(date(2026, 3, 2))
        bill.action_post()
        self.assertNotRegex(bill.name, r"^WE")
