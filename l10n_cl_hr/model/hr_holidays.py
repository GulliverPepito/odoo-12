# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging
import math
from datetime import datetime, timedelta
from odoo import api, fields, models, tools
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF
from odoo.tools import float_compare
from odoo.tools.translate import _


class HRHolidaysStatus(models.Model):
    #_inherit = 'hr.holidays.status'
    _inherit = 'hr.leave.type'
    is_continued = fields.Boolean('Disccount Weekends')



class HRHolidays(models.Model):
    #_inherit = 'hr.holidays'
    _inherit = 'hr.leave'

    def _get_number_of_days(self, date_from, date_to, employee_id):
        from_dt = fields.Datetime.from_string(date_from)
        to_dt = fields.Datetime.from_string(date_to)

        #En el caso de las licencias descontamos dias corridos
        if employee_id and self.holiday_status_id.is_continued:
        #if employee_id and self.leave_type_id.is_continued:
            time_delta = to_dt - from_dt
            return math.ceil(time_delta.days + float(time_delta.seconds) / 86400)
        elif employee_id:
            employee = self.env['hr.employee'].browse(employee_id)
            return employee.get_work_days_count(from_dt, to_dt)
        time_delta = to_dt - from_dt
        return math.ceil(time_delta.days + float(time_delta.seconds) / 86400)


#    @api.onchange('holiday_status_id')
#    def _onchange_holiday_status_id(self):
#        self._check_and_recompute_days()

    @api.onchange('holiday_type')
    def _onchange_type(self):
        if self.holiday_type == 'employee' and not self.employee_id:
            self.employee_id = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
        elif self.holiday_type != 'employee':
            self.employee_id = None


    @api.onchange('date_from','holiday_status_id','employee_id')
    #@api.onchange('date_from','holiday_type','employee_id')
    def _onchange_date_from(self):
        """ If there are no date set for date_to, automatically set one 8 hours later than
            the date_from. Also update the number_of_days.
        """
        date_from = self.date_from
        date_to = self.date_to

        # No date_to set so far: automatically compute one 8 hours later
        if date_from and not date_to:
            date_to_with_delta = fields.Datetime.from_string(date_from) + timedelta(hours=HOURS_PER_DAY)
            self.date_to = str(date_to_with_delta)

        # Compute and update the number of days
        if (date_to and date_from) and (date_from <= date_to):
            self.number_of_days_temp = self._get_number_of_days(date_from, date_to, self.employee_id.id)
        else:
            self.number_of_days_temp = 0

    @api.onchange('date_to','holiday_status_id','employee_id')
    #@api.onchange('date_to','holiday_type','employee_id')
    def _onchange_date_to(self):
        """ Update the number_of_days. """
        date_from = self.date_from
        date_to = self.date_to

        # Compute and update the number of days
        if (date_to and date_from) and (date_from <= date_to):
            self.number_of_days_temp = self._get_number_of_days(date_from, date_to, self.employee_id.id)
        else:
            self.number_of_days_temp = 0
		
			
    ####################################################
    # ORM Overrides methods
    ####################################################

