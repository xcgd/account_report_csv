from openerp.addons.account_report_webkit.report.trial_balance import (
    TrialBalanceWebkit
)
from openerp.addons.account_report_webkit.report.webkit_parser_header_fix import (
    HeaderFooterTextWebKitParser
)


class TrialBalanceCsv(TrialBalanceWebkit):

    def __init__(self, cursor, uid, context):
        super(TrialBalanceCsv, self).__init__(
            cursor, uid, '', context=context)

    def get_objects(self, data, ids):
        """Simulate a Webkit report to gather objects to be extracted as CSV,
        then return them."""

        objects, new_ids, context_report_values = (
            self.compute_balance_data(data))

        self.localcontext.update(context_report_values)

        self.set_context(objects, data, new_ids)

        return self.localcontext['objects']

HeaderFooterTextWebKitParser(
    'report.account.account_report_trial_balance_csv',
    'account.account',
    '',
    parser=TrialBalanceCsv
)
