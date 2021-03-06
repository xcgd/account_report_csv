import base64
import StringIO

from openerp.osv import fields, orm
from openerp.tools.translate import _

from openerp.addons.account_report_csv.report import general_ledger_csv
from openerp.addons.account_report_csv.unicode_csv import UnicodeWriter


class AccountGeneralLedgerCsvWizard(orm.TransientModel):
    _name = 'general.ledger.csv'
    _inherit = 'general.ledger.webkit'

    _columns = {
        'csv_delimiter': fields.char(
            'CSV delimiter',
            size=1,
            required=True
        ),
        'csv_quotechar': fields.char(
            'CSV quote character',
            size=1,
            required=True
        ),
        'name': fields.char('Export name', readonly=True),
        'data': fields.binary('Export', readonly=True),
    }

    _defaults = {
        'csv_delimiter': lambda *a: ',',
        'csv_quotechar': lambda *a: '"',
        'name': lambda *a: 'export_general_ledger.csv',
    }

    def check_report(self, cr, uid, ids, context=None):
        res = super(AccountGeneralLedgerCsvWizard, self).check_report(
            cr, uid, ids, context=context)

        this = self.browse(cr, uid, ids)[0]

        # Get analytic code names.
        a_code_obj = self.pool.get('analytic.code')
        a_codes = a_code_obj.search(cr, uid, [], context=context)
        a_codes = a_code_obj.read(cr, uid, a_codes, ['name'], context=context)
        a_codes = {
            a_code['id']: a_code['name']
            for a_code in a_codes
        }
        a_codes[0] = ''

        # Initialize the report class manually and get desired values.
        objects = general_ledger_csv.GeneralLedgerCsv(
            cr, uid, context=context
        ).get_objects(res['datas'], ids)

        # Generate the CSV data.
        csv_data = StringIO.StringIO()
        csv_writer = UnicodeWriter(
            csv_data,
            delimiter=str(this.csv_delimiter),
            quotechar=str(this.csv_quotechar)
        )

        # Write the first line (field names).
        csv_writer.writerows([[
            'state',
            'account_code',
            'account_name',
            'partner',
            'period',
            'transaction_date',
            'currency',
            'base_debit',
            'base_credit',
            'other_debit',
            'other_credit',
            'internal_number',
            'reference',
            'name',
            'number',
            'due_date',
            'allocation_date',
            'allocation_ref',
            # TODO manage analytic fields better (take their name, allow an
            # infinity of fields...)
            'line_analytic_1',
            'line_analytic_2',
            'line_analytic_3',
            'line_analytic_4',
            'line_analytic_5',
        ]])

        # Write the actual data.
        for account in objects:
            csv_writer.writerows([[
                line.get('state') or u'',
                account.code or u'',
                account.name or u'',
                line.get('partner_name') or u'',
                line.get('period_code') or u'',
                line.get('date') or u'',
                (
                    line.get('currency_code') or
                    account.company_id.currency_id.name or
                    u''
                ),
                str(line.get('debit')),
                str(line.get('credit')),
                str(line.get('debit_curr')),
                str(line.get('credit_curr')),
                line.get('internal_sequence_number') or u'',
                line.get('lref') or u'',
                line.get('lname') or u'',
                line.get('move_name') or u'',
                line.get('date_maturity') or u'',
                line.get('date_reconcile') or u'',
                line.get('rec_name') or u'',
                a_codes[line.get('a1_id') or 0],
                a_codes[line.get('a2_id') or 0],
                a_codes[line.get('a3_id') or 0],
                a_codes[line.get('a4_id') or 0],
                a_codes[line.get('a5_id') or 0],
            ] for line in account.ledger_lines])

        # Save the CSV data in a field so the user can then download it.
        self.write(cr, uid, ids, {
            'data': base64.encodestring(csv_data.getvalue() or u'\n'),
        }, context=context)

        view_obj = self.pool.get('ir.ui.view')
        view_id = view_obj.search(cr, uid,
            [('name', '=', 'account_general_ledger_view_csv_done')])

        return {
            'name': _('General Ledger Export'),
            'res_id': this.id,
            'res_model': 'general.ledger.csv',
            'target': 'new',
            'type': 'ir.actions.act_window',
            'view_id': view_id,
            'view_mode': 'form',
            'view_type': 'form',
        }

AccountGeneralLedgerCsvWizard()
