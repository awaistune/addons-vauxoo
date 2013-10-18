# -*- encoding: utf-8 -*-
###########################################################################
#    Module Writen to OpenERP, Open Source Management Solution
#
#    Copyright (c) 2010 Vauxoo - http://www.vauxoo.com/
#    All Rights Reserved.
#    info Vauxoo (info@vauxoo.com)
############################################################################
#    Coded by: Luis Torres (luis_t@vauxoo.com)
############################################################################
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
from openerp.osv import osv, fields
from openerp.tools.translate import _


class account_account(osv.Model):
    _inherit = 'account.account'

    _columns = {
        'analytic_required': fields.boolean('Analytic Required', help='If '\
        'this field is active, the journal items that used this account '\
        'should have an analytic account'),
    }
    
class account_invoice_line(osv.Model):
    _inherit = 'account.invoice.line'
    
    _columns = {
        'account_analytic_id':  fields.many2one('account.analytic.account', 'Analytic Accounttttt',\
            attrs="{'required': [('account_id.analytic_required', '=', True)]}"),
    }

class account_move(osv.Model):
    _inherit = 'account.move'

    def button_validate(self, cr, uid, ids, context=None):
        moves_without_analytic = ''
        for move in self.browse(cr, uid, ids, context=context):
            for line in move.line_id:
                analytic_st = line.account_id.analytic_required
                if analytic_st:
                    analytic_acc_move = line.analytic_account_id
                    if not analytic_acc_move:
                        moves_without_analytic += '\n' + line.name
            if moves_without_analytic:
                raise osv.except_osv(_('Error'), _('Need add analytic account'\
                    ' in move with name ' + moves_without_analytic + '.'))
        res = super(account_move, self).button_validate(
            cr, uid, ids, context=context)
        return res
