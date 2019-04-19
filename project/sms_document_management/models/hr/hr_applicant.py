##############################################################################
#    Copyright (C) Ioppolo and Associates (I&A) 2018 (<http://ioppolo.com.au>).
##############################################################################
from odoo import models, api, _
from odoo.exceptions import UserError


class Applicant(models.Model):
    _inherit = "hr.applicant"

    @api.multi
    def create_employee_from_applicant(self):
        """
        Create an hr.employee from the hr.applicants
        Override to:
            - Update employee on attachment from applicants
            - Grant Portal Access
        """
        employee = False
        for applicant in self:
            contact_name = False
            if applicant.partner_id:
                address_id = applicant.partner_id.address_get(
                    ['contact'])['contact']
                contact_name = applicant.partner_id.name_get()[0][1]
            else:
                new_partner_id = self.env['res.partner'].create({
                    'is_company': False,
                    'name': applicant.partner_name,
                    'email': applicant.email_from,
                    'phone': applicant.partner_phone,
                    'mobile': applicant.partner_mobile
                })
                # Customized by Trobz
                applicant.write({'partner_id': new_partner_id.id})
                # =================
                address_id = new_partner_id.address_get(['contact'])['contact']
            if applicant.job_id and (applicant.partner_name or contact_name):
                applicant.job_id.write({
                    'no_of_hired_employee':
                    applicant.job_id.no_of_hired_employee + 1})
                employee = self.env['hr.employee'].create({
                    'name': applicant.partner_name or contact_name,
                    'job_id': applicant.job_id.id,
                    'address_home_id': address_id,
                    'department_id': applicant.department_id.id or False,
                    'address_id':
                    applicant.company_id and
                    applicant.company_id.partner_id and
                    applicant.company_id.partner_id.id or False,
                    'work_email':
                    applicant.department_id and
                    applicant.department_id.company_id and
                    applicant.department_id.company_id.email or False,
                    'work_phone':
                    applicant.department_id and
                    applicant.department_id.company_id and
                    applicant.department_id.company_id.phone or False})
                applicant.write({'emp_id': employee.id})
                applicant.job_id.message_post(
                    body=_('New Employee %s Hired') %
                    applicant.partner_name
                    if applicant.partner_name else applicant.name,
                    subtype="hr_recruitment.mt_job_applicant_hired")
            else:
                raise UserError(_('You must define an Applied Job and a '
                                  'Contact Name for this applicant.'))
            # Customized by Trobz ##################################
            if not applicant.emp_id:
                continue
            applicant.attachment_ids.write(
                {'employee_id': applicant.emp_id.id})
            # create new portal wizard
            if applicant.partner_id:
                wizard = self.env['portal.wizard'].sudo().with_context(
                    active_ids=[applicant.partner_id.id]).create({})
                wizard.user_ids.write({'in_portal': True})
                wizard.action_apply()
            # ######################################################
        employee_action = self.env.ref('hr.open_view_employee_list')
        dict_act_window = employee_action.read([])[0]
        dict_act_window['context'] = {'form_view_initial_mode': 'edit'}
        dict_act_window['res_id'] = employee.id
        return dict_act_window

    @api.multi
    def action_get_attachment_tree_view(self):
        action = super(Applicant, self).action_get_attachment_tree_view()
        action['search_view_id'] = (self.env.ref(
            'sms_document_management.view_ir_attachment_search').id, )
        return action
