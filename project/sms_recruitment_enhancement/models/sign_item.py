# -*- coding: utf-8 -*-
from odoo import api, models
from odoo.modules.module import get_module_resource
import csv
import logging
_logger = logging.getLogger(__name__)


class SignItem(models.Model):
    _inherit = "sign.item"

    @api.model
    def _create_sign_item_eoi(self):

        _logger.info("=== START: _create_sign_item_eoi ====")

        csv_path = get_module_resource(
            'sms_recruitment_enhancement', 'static/file_sample',
            'sign_item_eoi.csv')
        csv_datas = csv.DictReader(
            open(csv_path, mode='r', encoding='utf-8-sig'))
        items = []
        for line in csv_datas:
            items.append(line)
        tpl_sign_eoi = self.env.ref(
            'sms_recruitment_enhancement.template_sign_eoi', False)
        tpl_sign_eoi_id = tpl_sign_eoi and tpl_sign_eoi.id or False

        for item in items:
            try:
                item_type = self.env.ref('sign.%s' % item['item_type'], False)
                type_id = item_type and item_type.id or False

                role = self.env.ref('sign.%s' % item['role_name'], False)
                role_id = role and role.id or False
                self.sudo().create({
                    'template_id': tpl_sign_eoi_id,
                    'type_id': type_id,
                    'responsible_id': role_id,
                    'page': item['page'],
                    'posX': item['posX'],
                    'posY': item['posY'],
                    'width': item['width'],
                    'height': item['height'],
                    'required': True if item['required'] == 'true' else False
                })
            except:
                continue
        _logger.info("=== END: _create_sign_item_eoi ====")
        return True

    @api.model
    def _create_sign_item_payroll_info(self):

        _logger.info("=== START: _create_sign_item_payroll_info ====")

        csv_path = get_module_resource(
            'sms_recruitment_enhancement', 'static/file_sample',
            'sign_item_payroll_info.csv')
        csv_datas = csv.DictReader(
            open(csv_path, mode='r', encoding='utf-8-sig'))
        items = []
        for line in csv_datas:
            items.append(line)
        tpl_sign_payroll_info = self.env.ref(
            'sms_recruitment_enhancement.template_sign_payroll_info', False)
        tpl_sign_payroll_info_id = \
            tpl_sign_payroll_info and tpl_sign_payroll_info.id or False

        for item in items:
            try:
                item_type = self.env.ref('sign.%s' % item['item_type'], False)
                type_id = item_type and item_type.id or False

                role = self.env.ref('sign.%s' % item['role_name'], False)
                role_id = role and role.id or False
                self.sudo().create({
                    'template_id': tpl_sign_payroll_info_id,
                    'type_id': type_id,
                    'responsible_id': role_id,
                    'page': item['page'],
                    'posX': item['posX'],
                    'posY': item['posY'],
                    'width': item['width'],
                    'height': item['height'],
                    'required': True if item['required'] == 'true' else False
                })
            except:
                continue
        _logger.info("=== END: _create_sign_item_payroll_info ====")
        return True

    @api.model
    def _create_sign_item_superannuation(self):

        _logger.info("=== START: _create_sign_item_superannuation ====")

        csv_path = get_module_resource(
            'sms_recruitment_enhancement', 'static/file_sample',
            'sign_item_superannuation.csv')
        csv_datas = csv.DictReader(
            open(csv_path, mode='r', encoding='utf-8-sig'))
        items = []
        for line in csv_datas:
            items.append(line)
        tpl_sign_superannuation = self.env.ref(
            'sms_recruitment_enhancement.template_sign_superannuation', False)
        tpl_sign_superannuation_id = \
            tpl_sign_superannuation and tpl_sign_superannuation.id or False

        for item in items:
            try:
                item_type = self.env.ref('sign.%s' % item['item_type'], False)
                type_id = item_type and item_type.id or False

                role = self.env.ref('sign.%s' % item['role_name'], False)
                role_id = role and role.id or False
                self.sudo().create({
                    'template_id': tpl_sign_superannuation_id,
                    'type_id': type_id,
                    'responsible_id': role_id,
                    'page': item['page'],
                    'posX': item['posX'],
                    'posY': item['posY'],
                    'width': item['width'],
                    'height': item['height'],
                    'required': True if item['required'] == 'true' else False
                })
            except:
                continue
        _logger.info("=== END: _create_sign_item_superannuation ====")
        return True

    @api.model
    def _create_sign_item_tax_declaration(self):

        _logger.info("=== START: _create_sign_item_tax_declaration ====")

        csv_path = get_module_resource(
            'sms_recruitment_enhancement', 'static/file_sample',
            'sign_item_tax_declaration.csv')
        csv_datas = csv.DictReader(
            open(csv_path, mode='r', encoding='utf-8-sig'))
        items = []
        for line in csv_datas:
            items.append(line)
        tpl_sign_tax_declaration = self.env.ref(
            'sms_recruitment_enhancement.template_sign_tax_declaration', False)
        tpl_sign_tax_declaration_id = \
            tpl_sign_tax_declaration and tpl_sign_tax_declaration.id or False

        for item in items:
            try:
                item_type = self.env.ref('sign.%s' % item['item_type'], False)
                type_id = item_type and item_type.id or False

                role = self.env.ref('sign.%s' % item['role_name'], False)
                role_id = role and role.id or False
                self.sudo().create({
                    'template_id': tpl_sign_tax_declaration_id,
                    'type_id': type_id,
                    'responsible_id': role_id,
                    'page': item['page'],
                    'posX': item['posX'],
                    'posY': item['posY'],
                    'width': item['width'],
                    'height': item['height'],
                    'required': True if item['required'] == 'true' else False
                })
            except:
                continue
        _logger.info("=== END: _create_sign_item_tax_declaration ====")
        return True

    @api.model
    def _create_sign_item_ppe_size_chart(self):

        _logger.info("=== START: _create_sign_item_ppe_size_chart ====")

        csv_path = get_module_resource(
            'sms_recruitment_enhancement', 'static/file_sample',
            'sign_item_ppe_size_chart.csv')
        csv_datas = csv.DictReader(
            open(csv_path, mode='r', encoding='utf-8-sig'))
        items = []
        for line in csv_datas:
            items.append(line)
        tpl_sign_ppe_size_chart = self.env.ref(
            'sms_recruitment_enhancement.template_sign_ppe_size_chart', False)
        tpl_sign_ppe_size_chart_id = \
            tpl_sign_ppe_size_chart and tpl_sign_ppe_size_chart.id or False

        for item in items:
            try:
                item_type = self.env.ref('sign.%s' % item['item_type'], False)
                type_id = item_type and item_type.id or False

                role = self.env.ref('sign.%s' % item['role_name'], False)
                role_id = role and role.id or False
                self.sudo().create({
                    'template_id': tpl_sign_ppe_size_chart_id,
                    'type_id': type_id,
                    'responsible_id': role_id,
                    'page': item['page'],
                    'posX': item['posX'],
                    'posY': item['posY'],
                    'width': item['width'],
                    'height': item['height'],
                    'required': True if item['required'] == 'true' else False
                })
            except:
                continue
        _logger.info("=== END: _create_sign_item_ppe_size_chart ====")
        return True
