import base64
import StringIO

from openerp.osv import fields, orm
from openerp.tools.translate import _

from openerp.addons.account_report_csv.report import trial_balance_csv
from openerp.addons.account_report_csv.unicode_csv import UnicodeWriter


class AccountTrialBalanceCsvWizard(orm.TransientModel):
    _name = 'trial.balance.csv'
    _inherit = 'trial.balance.webkit'

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
        'name': lambda *a: 'export_trial_balance.csv',
    }

    def check_report(self, cr, uid, ids, context=None):
        res = super(AccountTrialBalanceCsvWizard, self).check_report(
            cr, uid, ids, context=context)

        this = self.browse(cr, uid, ids)[0]

        # Initialize the report class manually and get desired values.
        objects = trial_balance_csv.TrialBalanceCsv(
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
            'code',
            'description',
            'currency',
            'other_debit',
            'other_credit',
            'other_balance',
        ]])

        # Write the actual data.
        csv_writer.writerows([[
            account.code or u'',
            account.name or u'',
            this.currency_id.name if this.currency_id else u'',
            str(account.debit),
            str(account.credit),
            str(account.balance),
        ] for account in objects
        if account.to_display and account.type != 'view'
        ])

        # Save the CSV data in a field so the user can then download it.
        self.write(cr, uid, ids, {
            'data': base64.encodestring(csv_data.getvalue() or u'\n'),
        }, context=context)

        view_obj = self.pool.get('ir.ui.view')
        view_id = view_obj.search(cr, uid,
            [('name', '=', 'account_trial_balance_view_csv_done')])

        return {
            'name': _('Trial Balance Export'),
            'res_id': this.id,
            'res_model': 'trial.balance.csv',
            'target': 'new',
            'type': 'ir.actions.act_window',
            'view_id': view_id,
            'view_mode': 'form',
            'view_type': 'form',
        }

AccountTrialBalanceCsvWizard()
