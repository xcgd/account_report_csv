# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013 XCG Consulting (www.xcg-consulting.fr)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    "name": "Account Report CSV",
    "version": "1.2",
    "author": "XCG Consulting",
    "website": "http://www.openerp-experts.com",
    "category": 'Accounting',
    "description": """
Export reports as CSV:
 - General Ledger
 - Trial Balance

Provides the usual filters (by account, period, currency, etc).
    """,
    "depends": [
        'account_report_webkit',
        'analytic_structure',
    ],
    "data": [
        'wizard/general_ledger_csv_wizard_view.xml',
        'wizard/trial_balance_csv_wizard_view.xml',
        'csv_menu.xml',
    ],
    'demo_xml': [],
    'test': [],
    'installable': True,
    'active': False,
}
