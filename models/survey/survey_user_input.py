##############################################################################
#    Copyright (C) Ioppolo and Associates (I&A) 2018 (<http://ioppolo.com.au>).
##############################################################################
from odoo import api, models


class SurveyUserInput(models.Model):
    _inherit = 'survey.user_input'

    @api.multi
    def get_data_user_input(self):
        self.ensure_one()
        res = {}
        hrw_class = ''
        driver_class = ''
        for uil in self.user_input_line_ids:
            if uil.question_id:
                # cert_number: only High Risk Work License (HRWL) has
                # license number
                if uil.question_id.question == 'Licence Number':
                    res.update({
                        'cert_number': uil.value_text
                    })
                if uil.answer_type == 'date':
                    if uil.question_id.question == 'Date Completed':
                        # Issued date of Verification of Competency (VOC)
                        res.update({
                            'date_voc': uil.value_date
                        })
                    if uil.question_id.question == 'Date Issued' and \
                            uil.question_id.sequence == 10:
                        # Issued date of High Risk Work License (HRWL)
                        res.update({
                            'date_hrwl': uil.value_date
                        })
                    if uil.question_id.question == 'Date Issued' and \
                            uil.question_id.sequence == 16:
                        # Issued date of Working at Heights (WAH)
                        res.update({
                            'date_wah': uil.value_date
                        })
                    if uil.question_id.question == 'Date Issued' and \
                            uil.question_id.sequence == 20:
                        # Issued date of Enter and Work in Confined Spaces
                        res.update({
                            'date_cse': uil.value_date
                        })
                    if uil.question_id.question == 'Date Issued' and \
                            uil.question_id.sequence == 24:
                        # Issued date of Construction Card
                        res.update({
                            'date_construction': uil.value_date
                        })
                    if uil.question_id.question == 'Date Issued' and \
                            uil.question_id.sequence == 38:
                        # Issued date of Section 44
                        res.update({
                            'date_s44': uil.value_date
                        })
                    if uil.question_id.question == 'Date Issued' and \
                            uil.question_id.sequence == 44:
                        # Issued date of Gas Test
                        res.update({
                            'date_gas': uil.value_date
                        })
                    if uil.question_id.question == 'Date Issued' and \
                            uil.question_id.sequence == 48:
                        # Issued date of Fork Lift
                        res.update({
                            'date_fork_lift': uil.value_date
                        })
                    if uil.question_id.question == 'Expiry Date':
                        # Expiry Date of Drivers License
                        res.update({
                            'date_driver': uil.value_date
                        })
                if uil.question_id.question == 'Classes':
                    if not hrw_class:
                        hrw_class = uil.value_suggested.value
                    else:
                        hrw_class += ', %s' % uil.value_suggested.value
                if uil.question_id.question == 'Class of Licence':
                    if not driver_class:
                        driver_class = uil.value_suggested.value
                    else:
                        driver_class += ', %s' % uil.value_suggested.value
        res.update({
            'hrw_class': hrw_class,
            'driver_class': driver_class
        })
        return res

    @api.multi
    def create_document(self):
        # Create ir_attachment with following vals;
        # vals = {
        #     'employee_id': False,
        #     'res_model': 'hr.applicant',
        #     'res_id': applicant_id,
        #     'name': ,
        #     'datas': ,
        #     'document_type': ,
        #     'cert_number': ,
        #     'date_issue': ,
        #     'expiry_date': ,
        #     'high_risk_work_class': ,
        #     'drivers_license_class': ,
        #     'expiry_reminder':
        # }
        self.ensure_one()
        IrAttachment = self.env['ir.attachment'].sudo()
        applicant = self.env['hr.applicant'].sudo().search(
            [('response_id', '=', self.id)], limit=1)

        # Get some general info
        info = self.get_data_user_input()
        # {
        #     doc_name : [document_type, cert_number, date_issue, expiry_date,
        #                 high_risk_work_class, drivers_license_class,
        #                 expiry_reminder]
        # }
        # Compute HRWL Class

        lst_docs = {
            'Resume': ['resume', None, False, False, None, None, False],
            'Verification of Competency (VOC) Certificate':
            ['voc', None, info.get('date_voc', False),
             False, None, None, True],
            'High Risk Work License (HRWL)': ['hrwl',
                                              info.get('cert_number', False),
                                              info.get('date_hrwl', False),
                                              False,
                                              info.get('hrw_class', False),
                                              None, False],
            'Working at Heights (WAH)': ['wah', None,
                                         info.get('date_wah', False),
                                         False, None, None, True],
            'Enter and Work in Confined Spaces (CSE)': ['cse', None,
                                                        info.get('date_cse',
                                                                 False),
                                                        False, None, None,
                                                        True],
            'Construction Card': ['construction_card', None,
                                  info.get('date_construction', False),
                                  False, None, None, False],
            'Passport or Birth Certificate': ['passport_or_birth_certificate',
                                              None, False, False,
                                              None, None, False],
            'Section 44 Certificate': ['section_44_certificate', None,
                                       info.get('date_s44', False),
                                       False, None, None, False],
            'Official Trade Certificate / Qualification': [
                'official_trade_certificate_qualification', None, False,
                False, None, None, False],
            'Gas Test Certificate': ['gas_test_certificate', None,
                                     info.get('date_gas', False),
                                     False, None, None, False],
            'Fork Lift License': ['fork_lift_license', None,
                                  info.get('date_fork_lift', False),
                                  False, None, None, False],
            'Drivers License': ['drivers_license', None, False,
                                info.get('date_driver', False),
                                None, info.get('driver_class', False), True]

        }
        for uil in self.user_input_line_ids:
            # The first checking: is it a file?
            if uil.answer_type == 'upload_file' and uil.file:
                name = uil.filename and uil.filename.split('.')[0] or ''
                vals = {
                    'res_model': 'hr.applicant',
                    'res_id': applicant and applicant.id or False,
                    'name': name,
                    'datas': uil.file,
                    'datas_fname': uil.filename
                }
                # Get info relate to this document
                doc_name = uil.question_id and uil.question_id.question or ''
                if doc_name in lst_docs.keys():
                    vals.update({
                        'document_type': lst_docs[doc_name][0],
                        'cert_number': lst_docs[doc_name][1],
                        'date_issue': lst_docs[doc_name][2],
                        'expiry_date': lst_docs[doc_name][3],
                        'high_risk_work_class': lst_docs[doc_name][4],
                        'drivers_license_class': lst_docs[doc_name][5],
                        'expiry_reminder': lst_docs[doc_name][6]
                    })
                IrAttachment.create(vals)
        return True

    @api.multi
    def write(self, vals):
        res = super(SurveyUserInput, self).write(vals)
        if vals.get('state', False) == 'done':
            for rec in self:
                rec.create_document()
        return res
