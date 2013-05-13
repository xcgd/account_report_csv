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
    "name" : "Account Report CSV",
    "version" : "0.1",
    "author" : "XCG Consulting",
    "website": "http://www.openerp-experts.com",
    "category": 'Accounting',
    "description": """
    
    Allows you to export a csv file based on accounting balances
    
    - Trial Balance
    - Analytic Balance (based on A codes)
    - Ageing Balance
    
    You can filter by period and disply amounts in currency
    
     
    """,
    "depends" : [
                 'account',
		 'account_streamline',
                 ],
    "data": [
            'wizard/account_report_csv_view.xml',
            'account_report_csv_menu.xml',
                  ],
    'demo_xml': [],
    'test': [],
    'installable': True,
    'active': False,
}

