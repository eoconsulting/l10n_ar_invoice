# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Mariano Ruiz <mrsarm@gmail.com>,
#            Enterprise Objects Consulting (<http://www.eoconsulting.com.ar>)
#    Created: 2012-07-18
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

import time
from report import report_sxw

class ar_account_invoice(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(ar_account_invoice, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'use_header': False,
        })
report_sxw.report_sxw(
    'report.ar.account.invoice',
    'account.invoice',
    'addons/l10n_ar_invoice/report/invoice.rml',
    parser=ar_account_invoice
)

class ar_account_invoice_with_header(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(ar_account_invoice_with_header, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'use_header': True,
        })
report_sxw.report_sxw(
    'report.ar.account.invoice.with.header',
    'account.invoice',
    'addons/l10n_ar_invoice/report/invoice.rml',
    parser=ar_account_invoice_with_header
)
