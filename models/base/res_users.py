##############################################################################
#    Copyright (C) Ioppolo and Associates (I&A) 2018 (<http://ioppolo.com.au>).
##############################################################################

from odoo import models, api


class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.multi
    def get_portal_url(self):
        self.ensure_one()
        base_url = self.env[
            'ir.config_parameter'].sudo().get_param('web.base.url')
        return base_url + '/my'
