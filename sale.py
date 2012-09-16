# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Mariano Ruiz <mrsarm@gmail.com>,
#            Enterprise Objects Consulting (<http://www.eoconsulting.com.ar>)
#    Created: 2012-09-13
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

from osv import fields, osv
import decimal_precision as dp

_all_taxes = lambda x: True
_all_except_vat = lambda x: 'IVA' not in x.name

class sale_order_line(osv.osv):
    """
    En argentina como no se diferencian los impuestos en las facturas, excepto el IVA
    agrego funciones que ignoran el iva solamenta a la hora de imprimir los valores.
    """
    def _amount_calc_taxes(self, cr, uid, ids, tax_filter, default_quantity):
        res = {}
        tax_obj = self.pool.get('account.tax')
        for line in self.browse(cr, uid, ids):
            tax_ids = filter(tax_filter, line.tax_id)
            price_unit = line.price_unit
            for tax in line.tax_id:
                if tax.price_include and tax not in tax_ids:
                    price_unit = line.price_subtotal
                    break
            price = price_unit * (1-(line.discount or 0.0)/100.0)
            quantity = default_quantity if default_quantity is not None else line.product_uom_qty
            taxes = tax_obj.compute_all(cr, uid,
                                        tax_ids, price, quantity,
                                        product=line.product_id,
                                        address_id=line.order_id.partner_invoice_id,
                                        partner=line.order_id.partner_id)
            res[line.id] = taxes['total_included']
        return res

    def _amount_unit_vat_included(self, cr, uid, ids, prop, unknow_none, unknow_dict):
        return self._amount_calc_taxes(cr, uid, ids, _all_taxes, 1)

    def _amount_subtotal_vat_included(self, cr, uid, ids, prop, unknow_none, unknow_dict):
        return self._amount_calc_taxes(cr, uid, ids, _all_taxes, None)

    def _amount_unit_not_vat_included(self, cr, uid, ids, prop, unknow_none, unknow_dict):
        return self._amount_calc_taxes(cr, uid, ids, _all_except_vat, 1)

    def _amount_subtotal_not_vat_included(self, cr, uid, ids, prop, unknow_none, unknow_dict):
        return self._amount_calc_taxes(cr, uid, ids, _all_except_vat, None)

    _inherit = 'sale.order.line'
    _columns = {
        'price_unit_vat_included': fields.function(_amount_unit_vat_included, method=True,
                                               string='Unit Price with VAT', type="float",
                                               digits_compute= dp.get_precision('Account'), store=False),
        'price_subtotal_vat_included': fields.function(_amount_subtotal_vat_included, method=True,
                                               string='Subtotal with VAT', type="float",
                                               digits_compute= dp.get_precision('Account'), store=False),
        'price_unit_not_vat_included': fields.function(_amount_unit_not_vat_included, method=True,
                                               string='Unit Price without VAT', type="float",
                                               digits_compute= dp.get_precision('Account'), store=False),
        'price_subtotal_not_vat_included': fields.function(_amount_subtotal_not_vat_included, method=True,
                                               string='Subtotal without VAT', type="float",
                                               digits_compute= dp.get_precision('Account'), store=False),
    }

sale_order_line()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
