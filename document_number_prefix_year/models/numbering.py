# Copyright 2026 Biricon IT Services GmbH
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
"""Shared numbering logic: <prefix><year><counter> (vendor bills: <prefix><year><month><counter>).

* The counter restarts at 1 every year (per prefix and company).
* It always continues after the highest existing number with the same prefix and year, whatever its
  length, so numbers imported from another system (e.g. "AN26119") are taken into account.
* A transaction-level advisory lock per company/prefix/year serialises number assignment. Because Odoo works
  with REPEATABLE READ, the highest number is read twice: in the current transaction (own, uncommitted numbers)
  and with a second cursor (numbers committed by other transactions while we waited for the lock).
"""
import re
import zlib

from odoo import fields

NEW_NAMES = ("/", "New")


def is_new_name(env, name):
    return not name or name in NEW_NAMES or name == env._("New")


def next_number(env, company, prefix, table, column, date=None, with_month=False, digits=None):
    """Return the next number for ``prefix`` in ``table.column`` for ``company``.

    ``with_month``: number = prefix + year + month + counter (the counter restarts every month).
    ``digits``: counter length, default the company setting.
    """
    date = date or fields.Date.context_today(env.user)
    year = date.strftime("%Y" if company.document_number_year_digits == "4" else "%y")
    month = date.strftime("%m") if with_month else ""
    stem = "%s%s%s" % (prefix, year, month)
    pattern = re.sub(r"([^A-Za-z0-9])", r"\\\1", stem)
    key = "document_number_prefix_year:%s:%s" % (company.id, stem)
    env.cr.execute("SELECT pg_advisory_xact_lock(%s)", (zlib.crc32(key.encode()) & 0x7FFFFFFF,))
    query = (
        "SELECT max(substring({col} FROM %s)::bigint) FROM {tbl} "
        "WHERE {col} ~ %s AND (company_id = %s OR company_id IS NULL)".format(col=column, tbl=table)
    )
    params = ("^%s([0-9]{1,15})$" % pattern, "^%s[0-9]{1,15}$" % pattern, company.id)
    env.cr.execute(query, params)
    last = env.cr.fetchone()[0] or 0
    # Odoo runs REPEATABLE READ: the snapshot of this transaction predates the lock, so a number that another
    # transaction committed while we were waiting is invisible here. A second, short-lived cursor sees it.
    with env.registry.cursor() as cr2:
        cr2.execute(query, params)
        last = max(last, cr2.fetchone()[0] or 0)
    return "%s%0*d" % (stem, max(digits or company.document_number_digits or 1, 1), last + 1)
