##############################################################################
#    Copyright (C) Ioppolo and Associates (I&A) 2018 (<http://ioppolo.com.au>).
##############################################################################
from odoo import api, models
from odoo.tools import email_split
from odoo.exceptions import ValidationError


def extract_email(email):
    """ extract the email address from a user-friendly email address """
    addresses = email_split(email)
    return addresses[0] if addresses else ''


class PortalWizardUser(models.TransientModel):
    """
        A model to configure users in the portal wizard.
    """

    _inherit = 'portal.wizard.user'

    @api.multi
    def _create_user(self):
        """
            override native function for adding related hr.employee
        """
        company_id = self.env.context.get('company_id')
        employee_id = self.env['hr.employee'].search(
            [('address_home_id', '=', self.partner_id.id)])
        if not employee_id:
            raise ValidationError(
                "The related employee of this contact is not exist!")

        return self.env['res.users'].with_context(
            no_reset_password=True)._create_user_from_template({
                'email': extract_email(self.email),
                'login': extract_email(self.email),
                'partner_id': self.partner_id.id,
                'employee_ids': [(6, 0, [employee_id.id])],
                'company_id': company_id,
                'company_ids': [(6, 0, [company_id])],
            })
