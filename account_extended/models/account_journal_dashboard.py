
from odoo import models, api, _, fields
from odoo.tools.misc import formatLang


class account_journal(models.Model):
    _inherit = "account.journal"

    def get_journal_dashboard_datas(self):
        ret_val = super().get_journal_dashboard_datas()
        currency = self.currency_id or self.company_id.currency_id
        bank_account_balance = nb_lines_bank_account_balance = 0
        outstanding_pay_account_balance = nb_lines_outstanding_pay_account_balance = 0
        if self.type in ('bank', 'cash'):
            bank_account_balance, nb_lines_bank_account_balance = self._get_journal_bank_account_balance(
                domain=[('parent_state', '=', 'posted')])
            outstanding_pay_account_balance, nb_lines_outstanding_pay_account_balance = self._get_journal_outstanding_payments_account_balance(
                domain=[('parent_state', '=', 'posted')])
        general_outstanding_bal = bank_account_balance + outstanding_pay_account_balance
        ret_val.update({
            'general_outstanding_bal': formatLang(self.env, currency.round(general_outstanding_bal), currency_obj=currency),
        })
        return ret_val
