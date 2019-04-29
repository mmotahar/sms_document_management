##############################################################################
#    Copyright (C) Ioppolo and Associates (I&A) 2018 (<http://ioppolo.com.au>).
##############################################################################

from odoo import fields, models, api, _
from odoo.exceptions import Warning


class EmployeeAvailability(models.Model):
    _name = 'employee.availability'
    _rec_name = 'employee_id'

    employee_id = fields.Many2one(
        'hr.employee', string='Employee', required=True)
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    number_of_days = fields.Integer(
        'Day(s)', compute='compute_number_of_days', store=False)
    status = fields.Selection(
        [
            ('contracted', 'Contracted'),
            ('leave', 'Leave'),
        ],
        string='Status',
        default='contracted')
    color = fields.Integer(
        'Gantt Color', compute='compute_gantt_color', store=False)
    description = fields.Text(string='Description')
    customer_id = fields.Many2one(
        'res.partner', string='Customer',
        domain=[('customer', '=', True)])

    @api.depends('start_date', 'end_date')
    def compute_number_of_days(self):
        for rec in self:
            if not all([rec.start_date, rec.end_date]):
                continue
            start_date = fields.Date.from_string(rec.start_date)
            end_date = fields.Date.from_string(rec.end_date)
            rec.number_of_days = (end_date - start_date).days + 1

    @api.depends('status')
    @api.multi
    def compute_gantt_color(self):
        for rec in self:
            if rec.status == 'contracted':
                rec.color = 11
            elif rec.status == 'leave':
                rec.color = 12

    @api.model
    def search_read(
            self, domain=None, fields=None, offset=0, limit=None, order=None):
        """
        Inherit to read color of gantt chart
        """
        if fields:
            fields.append('color')
        res = super(EmployeeAvailability, self).search_read(
            domain, fields, offset, limit, order)
        return res

    @api.constrains('start_date', 'end_date')
    def constrains_start_end_date(self):
        """
        End Date must be after or equal to Start Date
        """
        for rec in self:
            if not all([rec.start_date, rec.end_date]):
                continue
            if rec.start_date > rec.end_date:
                raise Warning(_(
                    'End Date must be after or equal to Start Date'))
