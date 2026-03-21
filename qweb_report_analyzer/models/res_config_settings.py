# -*- coding: utf-8 -*-
"""
QWeb Report Analyzer - Settings
Free & Open Source - No license required.
"""

from odoo import models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    # No license fields needed — the addon is completely free.
    # The settings view still shows usage instructions (see XML view).
