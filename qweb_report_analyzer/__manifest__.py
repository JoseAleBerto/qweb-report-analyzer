# -*- coding: utf-8 -*-
{
    'name': 'QWeb Report Analyzer - View Dependency Tree',
    'version': '17.0.1.0.0',
    'category': 'Technical',
    'summary': 'Analyze QWeb report views: dependency tree, t-calls, XPaths, inherited views — free & open source',
    'description': """
QWeb Report Analyzer
====================

The essential tool for Odoo developers and consultants to understand,
debug and document QWeb reports. Free and open source. No license required.

Key Features
------------
* Dependency Tree: Full visual hierarchy of all view relationships
* Inherited Views: All modifications with XPath expressions per module
* T-Call Detection: Every template referenced via t-call
* Module Tracking: Know exactly which module owns each view
* One-Click Export: Download the full analysis as a .txt file
* Fully Local: Runs entirely inside Odoo — no internet or server needed

How to use
----------
1. Go to Settings -> Technical -> Reporting -> Reports
2. Select any report from the list
3. Click Action -> Analyze Report Views
4. A .txt file downloads automatically with the complete analysis

Compatible with Odoo 17, 18, and 19.

Source code: https://github.com/JoseAleBerto/qweb-report-analyzer
Author: Jose Bertorelli — josealebertorelli@gmail.com
    """,
    'author': 'Jose Bertorelli',
    'website': 'https://github.com/JoseAleBerto/qweb-report-analyzer',
    'license': 'LGPL-3',
    'price': 0.00,
    'currency': 'EUR',
    'depends': [
        'base',
        'web',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/res_config_settings_views.xml',
        'data/server_action.xml',
    ],
    'images': [
        'static/description/icon.png',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'support': 'josealebertorelli@gmail.com',
}
