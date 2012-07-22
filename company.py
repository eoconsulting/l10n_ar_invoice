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

from osv import osv, fields

class company(osv.osv):
    '''
    Campos con datos fiscales de Argentina de la compañia. Se imprimen en la factura.
    El C.U.I.T. se extrae del `company.partner_id.vat`.
    '''

    _inherit = 'res.company'

    _situation = [
            ('responsableinscripto','I.V.A. Responsable Inscripto'),
            ('noresponsableinscripto','I.V.A. Responsable No Inscripto'),
            ('noresponsableiva','No Responsable I.V.A.'),
            ('monotributo','Responsable Monotributo') ]

    def _get_situation_descrip(self, cr, uid, ids, field_name, arg, context=None):
        result = {}
        for company in self.browse(cr, uid, ids, context=context):
            for cond in self._situation:
                if cond[0] == company.situation:
                    result[company.id] = {}
                    result[company.id] = cond[1]
        return result

    _columns = {
        'ing_brutos': fields.char('Ingresos Brutos', size=32, help="ID o descripción de estado en Ingresos Brutos (Argentina solamente)."),
        'startup_activities': fields.date('Startup Activities'),
        'situation': fields.selection(_situation, 'VAT Situation'),
        'situation_descrip': fields.function(_get_situation_descrip, type='char', readonly=True, method=True),
    }

company()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
