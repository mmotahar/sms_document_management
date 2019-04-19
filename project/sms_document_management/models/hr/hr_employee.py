##############################################################################
#    Copyright (C) Ioppolo and Associates (I&A) 2018 (<http://ioppolo.com.au>).
##############################################################################

from datetime import datetime, timedelta
from odoo import fields, models, api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    document_ids = fields.One2many(
        'ir.attachment', 'employee_id',
        string='Documents',
        help='Related certificates / licenses of employee')
    attachment_number = fields.Integer(
        compute='_compute_attachment_number', string="Number of Attachments")

    availability_ids = fields.One2many(
        'employee.availability', 'employee_id',
        string='Availabilities',
        help='Related availabilities of employee')
    availability_state = fields.Selection(
        [
            ('available', 'Available'),
            ('unavailable', 'Un-Available')
        ],
        compute='_compute_availability_state')

    @api.multi
    def _compute_attachment_number(self):
        attachments = self.env['ir.attachment'].search(
            [('employee_id', 'in', self.ids)])
        for record in self:
            record.attachment_number = len(attachments)

    @api.multi
    def _compute_availability_state(self):
        availability_env = self.env['employee.availability']
        today = datetime.now().date()
        for employee in self:
            availability = availability_env.search([
                ('employee_id', '=', employee.id),
                '|',
                '&',
                ('start_date', '<=', str(today)),
                ('end_date', '>=', str(today)),
                '&',
                ('start_date', '<=', str(today)),
                ('end_date', '=', None)])
            if len(availability) > 0:
                employee.availability_state = 'unavailable'
            else:
                employee.availability_state = 'available'

    @api.multi
    def action_view_certificate_tree_view(self):
        attachment_action = self.env.ref(
            'sms_document_management.action_licenses_and_certificates')
        action = attachment_action.read()[0]
        action['domain'] = str([('employee_id', 'in', self.ids)])
        return action

    @api.multi
    def action_view_employee_availability_tree_view(self):
        availability_action = self.env.ref(
            'sms_document_management.action_employee_availability')
        action = availability_action.read()[0]
        action['domain'] = str([('employee_id', 'in', self.ids)])
        return action

    @api.multi
    def action_availability_state(self):
        return None

    @api.multi
    def send_email_remind_expiry_documents_to_hr_team(self):
        self.ensure_one()
        template = self.env.ref(
            'sms_document_management.email_template_remind_expiry_documents_to_hr_team')
        if not template:
            return True
        context = self.env.context.copy()
        ctx = dict({
            'datas': datas,
        })
        context.update(ctx)
        mail_id = template.with_context(context).send_mail(self.id, True)
        return mail_id

    @api.multi
    def get_expired_documents(self):
        self.ensure_one()
        DAYS_OF_WEEK = 7
        today = datetime.now().date()

        # ============= Get documents need to notify =============
        expire_in_4_week = today + timedelta(DAYS_OF_WEEK * 4)
        expire_in_2_week = today + timedelta(DAYS_OF_WEEK * 2)
        domain = [
            ('active', '=', True),
            ('employee_id', '=', self.id),
            ('expiry_date', '!=', None),
            ('expiry_reminder', '=', True),
            '|',
            ('expiry_date', '=', str(expire_in_4_week)),
            ('expiry_date', '=', str(expire_in_2_week))
        ]
        res = self.document_ids.search(domain)
        return res
