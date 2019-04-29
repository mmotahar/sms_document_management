##############################################################################
#    Copyright (C) Ioppolo and Associates (I&A) 2018 (<http://ioppolo.com.au>).
##############################################################################
from datetime import datetime, timedelta
from odoo import fields, models, api

DAYS_OF_WEEK = 7


class IrAttachment(models.Model):
    _name = "ir.attachment"
    _inherit = ['ir.attachment', 'portal.mixin']

    employee_id = fields.Many2one(
        'hr.employee', string='Employee', track_visibility="onchange")
    document_type = fields.Selection(
        [
            ('voc', 'Verification of Competency (VOC) Certificate'),
            ('hrwl', 'High Risk Work License (HRWL)'),
            ('wah', 'Working at Heights (WAH)'),
            ('cse', 'Enter and Work in Confined Spaces (CSE)'),
            ('construction_card', 'Construction Card'),
            ('passport_or_birth_certificate', 'Passport or Birth Certificate'),
            ('resume', 'Resume'),
            ('section_44_certificate', 'Section 44 Certificate'),
            (
                'official_trade_certificate_qualification',
                'Official Trade Certificate / Qualification'),
            ('gas_test_certificate', 'Gas Test Certificate'),
            ('fork_lift_license', 'Fork Lift License'),
            ('drivers_license', 'Drivers License'),
        ],
        string='Document Type', track_visibility="onchange")

    cert_number = fields.Char(
        string='License / Cert Number', track_visibility="onchange")
    date_issue = fields.Date(
        string='Date Issue / Completed', track_visibility="onchange")
    expiry_date = fields.Date(
        string='Expiry Date', track_visibility="onchange")
    expiry_week = fields.Integer(
        string='Expiry Week', compute='compute_expiry_week',
        help='Technical fields to send expery notice email')
    high_risk_work_class = fields.Char(
        string='High Risk Work Class', track_visibility="onchange")
    drivers_license_class = fields.Char(
        string='Drivers License Class', track_visibility="onchange")
    expiry_reminder = fields.Boolean(
        stringk='Expiry Reminder', track_visibility="onchange")
    active = fields.Boolean(
        string='Active', track_visibility="onchange")

    def _compute_access_url(self):
        super(IrAttachment, self)._compute_access_url()
        for attachment in self:
            attachment.access_url = '/my/certificates/%s' % (attachment.id)

    @api.multi
    def compute_expiry_week(self):
        for rec in self:
            if not rec.expiry_date:
                continue
            today = datetime.now().date()
            expiry_date = fields.Date.from_string(rec.expiry_date)
            rec.expiry_week = int((expiry_date - today).days / DAYS_OF_WEEK)

    @api.multi
    def send_email_remind_expiry_documents_to_employee(self):
        self.ensure_one()
        template = self.env.ref(
            'sms_document_management.email_template_remind_expiry_documents_to_employee')
        if not template:
            return True
        mail_id = template.send_mail(self.id, True)
        return mail_id

    @api.model
    def scheduler_remind_expiry_documents(self):
        today = datetime.now().date()

        # ============= Get documents need to notify =============
        expire_in_4_week = today + timedelta(DAYS_OF_WEEK * 4)
        expire_in_2_week = today + timedelta(DAYS_OF_WEEK * 2)
        domain = [
            ('active', '=', True),
            ('employee_id', '!=', None),
            ('expiry_date', '!=', None),
            ('expiry_reminder', '=', True),
            '|',
            ('expiry_date', '=', str(expire_in_4_week)),
            '|',
            ('expiry_date', '=', str(expire_in_2_week)),
            ('expiry_date', '=', str(today)),
        ]

        remind_docs = self.search(
            domain,
            order='employee_id, expiry_date')
        if not remind_docs:
            return
        # Remind to Hr Admin
        employees = remind_docs.mapped('employee_id')
        for employee in employees:
            employee.send_email_remind_expiry_documents_to_hr_team()
        # Remind to employee
        for doc in remind_docs:
            doc.send_email_remind_expiry_documents_to_employee()
