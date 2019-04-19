##############################################################################
#    Copyright (C) Ioppolo and Associates (I&A) 2018 (<http://ioppolo.com.au>).
##############################################################################

from odoo import fields, models, api, _
from odoo.exceptions import Warning


class EmployeeRegisterWizard(models.TransientModel):
    _name = 'employee.register.wizard'

    certificate = fields.Selection(
        [
            ('voc', 'Verification of Competency (VOC) Certificate'),
            ('wah', 'Working at Heights'),
            ('cse', 'Enter and Work in Confined Spaces'),
            ('drivers_license', 'Drivers License')
        ],
        string='Required Certificate / License', required=False)
    date_from = fields.Date(string='Date From', required=True)
    date_to = fields.Date(string='Date To', required=True)

    @api.constrains('date_from', 'date_to')
    def constrains_start_end_date(self):
        """
        End Date must be after or equal to Start Date
        """
        for rec in self:
            if not all([rec.date_from, rec.date_to]):
                continue
            if rec.date_from > rec.date_to:
                raise Warning(_(
                    'Date From must be after or equal to Date To'))

    @api.multi
    def filter_employee_register(self):
        self.ensure_one()
        attach_env = self.env['ir.attachment']
        avail_env = self.env['employee.availability']

        required_certificate = self.certificate
        date_from = self.date_from
        date_to = self.date_to

        availability = avail_env.search([
            ('start_date', '!=', None),
            ('end_date', '!=', None),
            ('start_date', '<=', str(date_to)),
            ('end_date', '>=', str(date_from))])
        endless_availability = avail_env.search([
            ('end_date', '=', None),
            ('start_date', '<=', str(date_to))])
        unavailable_employee_ids = availability and availability.mapped(
            'employee_id').ids or []
        unavailable_employee_ids.extend(
            endless_availability and endless_availability.mapped(
                'employee_id').ids or [])

        certificates = attach_env.search([
            ('employee_id', '!=', None),
            ('employee_id', 'not in', unavailable_employee_ids),
            ('document_type', '=', required_certificate)])
        employee_ids = certificates.mapped('employee_id').ids or []

        availability_action = self.env.ref(
            'sms_document_management.action_licenses_and_certificates')
        action = availability_action.read()[0]
        action['domain'] = str([('employee_id', 'in', employee_ids)])
        action['context'] = str({'search_default_group_employee': True})
        return action
