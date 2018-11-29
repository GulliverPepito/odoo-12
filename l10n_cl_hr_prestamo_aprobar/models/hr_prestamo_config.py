# -*- coding: utf-8 -*-
###################################################################################
#
#    Intellego-BI.com
#    Copyright (C) 2017-TODAY Intellego Business Intelligence S.A.(<http://www.intellego-bi.com>).
#    Author: Rodolfo Bermúdez Neubauer(<https://www.intellego-bi.com>)
#
#    This program is free software: you can modify
#    it under the terms of the GNU Affero General Public License (AGPL) as
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
###################################################################################
from odoo import models, fields, api, _

class AccConfig(models.TransientModel):
    _inherit = 'res.config.settings'

    prestamo_approve = fields.Boolean(default=False, string="Approval from Accounting Department",
                                  help="Loan Approval from account manager")

    @api.model
    def get_values(self):
        res = super(AccConfig, self).get_values()
        res.update(
            prestamo_approve=self.env['ir.config_parameter'].sudo().get_param('account.prestamo_approve')
        )
        return res

    @api.multi
    def set_values(self):
        super(AccConfig, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('account.prestamo_approve', self.prestamo_approve)

