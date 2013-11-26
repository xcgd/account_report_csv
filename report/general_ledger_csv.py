from openerp.addons.account_report_webkit.report.general_ledger import (
    GeneralLedgerWebkit
)
from openerp.addons.account_report_webkit.report.webkit_parser_header_fix import (
    HeaderFooterTextWebKitParser
)


class GeneralLedgerCsv(GeneralLedgerWebkit):

    def __init__(self, cursor, uid, context):
        super(GeneralLedgerCsv, self).__init__(
            cursor, uid, '', context=context)

    def get_objects(self, data, ids):
        """Simulate a Webkit report to gather objects to be extracted as CSV,
        then return them."""

        self.set_context([], data, ids)

        return self.localcontext['objects']

HeaderFooterTextWebKitParser(
    'report.account.account_report_general_ledger_csv',
    'account.account',
    '',
    parser=GeneralLedgerCsv
)
