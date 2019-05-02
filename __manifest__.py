##############################################################################
#    Copyright (C) Ioppolo and Associates (I&A) 2018 (<http://ioppolo.com.au>).
##############################################################################
{
    "name": "SMS Document Management",
    "version": "12.0.0.1.0",
    "description": """
This module aims to manage employee's documents
Odoo.sh
    """,
    "website": "http://ioppolo.com.au",
    "author": "Ioppolo & Associates",
    "category": "Ioppolo & Associates",
    "depends": [
        "sms_recruitment_enhancement",
        "documents",
        "portal",
    ],
    "data": [
        # ============================================================
        # SECURITY SETTING - GROUP - PROFILE
        # ============================================================
        # "security/",
        "security/ir.model.access.csv",

        # ============================================================
        # DATA
        # ============================================================
        # "data/",
        "data/email_template_data.xml",
        "data/ir_cron_data.xml",


        # ============================================================
        # VIEWS
        # ============================================================
        # "views/",
        "views/base/ir_attachment_view.xml",
        "views/hr/hr_employee_view.xml",
        "views/hr/employee_availability_view.xml",

        "views/gantt/web_gantt_templates.xml",

        "wizards/hr/employee_register_wizard_view.xml",
        "wizards/portal/portal_template.xml",

        # ============================================================
        # MENU
        # ============================================================
        # "menu/",
        "menu/sms_hr_menu.xml",
        "menu/hr_employee_menu.xml",

        # ============================================================
        # FUNCTION USED TO UPDATE DATA LIKE POST OBJECT
        # ============================================================
        # "data/sms_update_functions_data.xml",
    ],

    "test": [],
    "demo": [],
    "installable": True,
    "active": False,
    "application": False,
}
