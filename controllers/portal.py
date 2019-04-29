##############################################################################
#    Copyright (C) Ioppolo and Associates (I&A) 2018 (<http://ioppolo.com.au>).
##############################################################################
from odoo.http import request, route
from odoo.exceptions import AccessError, MissingError
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo import http, _


class CustomerPortal(CustomerPortal):
    def _prepare_portal_layout_values(self):
        res = super(CustomerPortal, self)._prepare_portal_layout_values()
        user = request.env.user
        employee = request.env['hr.employee'].sudo().search(
            [('user_id', '=', user.id)])
        documents = employee.sudo().document_ids
        certificate_license_count = len(documents)
        res.update({
            'certificate_license_count': certificate_license_count
        })
        return res

    @http.route(['/my/certificates', '/my/certificates/page/<int:page>'],
                type='http', auth="user", website=True)
    def portal_my_certificates(
            self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        user = request.env.user
        values = self._prepare_portal_layout_values()
        IrAttachment = request.env['ir.attachment']

        employee = request.env['hr.employee'].sudo().search(
            [('user_id', '=', user.id)])
        domain = [
            ('employee_id', '=', employee.id),
            ('active', '=', True)
        ]

        searchbar_sortings = {
            'name': {'label': _('Name'), 'order': 'name'},
        }
        # default sortby order
        if not sortby:
            sortby = 'name'
        sort_order = searchbar_sortings[sortby]['order']

        archive_groups = self._get_archive_groups('ir.attachment', domain)
        if date_begin and date_end:
            domain += [('create_date', '>', date_begin),
                       ('create_date', '<=', date_end)]

        # count for pager
        order_count = IrAttachment.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/certificates",
            total=order_count,
            page=page,
            step=self._items_per_page
        )
        # content according to pager and archive selected
        certificates = IrAttachment.sudo().search(
            domain, order=sort_order, limit=self._items_per_page,
            offset=pager['offset'])
        request.session['my_certificates_history'] = certificates.ids[:100]

        values.update({
            'certificates': certificates,
            'page_name': 'my_certificates',
            'pager': pager,
            'archive_groups': archive_groups,
            'default_url': '/my/certificates',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
        })
        return request.render("sms_document_management.portal_my_certificates",
                              values)

    @route(['/my/certificates/<int:doc_id>'], type='http',
           auth='public', website=True)
    def portal_document_page(self, doc_id, report_type=None, access_token=None,
                             message=False, download=False, **kw):
        values = self._prepare_portal_layout_values()
        document = request.env['ir.attachment'].sudo().browse(doc_id)
        try:
            self._document_check_access(
                'ir.attachment', doc_id, access_token=access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        vals_document_type = request.env['ir.attachment'].fields_get(
            allfields=['document_type'])
        document_type_dict = {}
        if 'document_type' in vals_document_type and\
                'selection' in vals_document_type['document_type']:
            document_type_dict = dict(
                vals_document_type['document_type']['selection'])

        vals_driver_license = request.env['ir.attachment'].fields_get(
            allfields=['drivers_license_class'])
        license_class_dict = {}
        if 'drivers_license_class' in vals_driver_license and\
                'selection' in vals_driver_license['drivers_license_class']:
            license_class_dict = dict(
                vals_driver_license['drivers_license_class']['selection'])

        vals_high_risk = request.env['ir.attachment'].fields_get(
            allfields=['high_risk_work_class'])
        risk_class_dict = {}
        if 'high_risk_work_class' in vals_high_risk and\
                'selection' in vals_high_risk['high_risk_work_class']:
            risk_class_dict = dict(
                vals_high_risk['high_risk_work_class']['selection'])

        values.update({
            'risk_class_dict': risk_class_dict,
            'document_type_dict': document_type_dict,
            'license_class_dict': license_class_dict,
            'document': document,
            # 'redirect': redirect,
            'page_name': 'my_certificates',
        })

        response = request.render(
            "sms_document_management.portal_certificate_detail", values)

        response.headers['X-Frame-Options'] = 'DENY'
        return response
