from odoo import models, fields, api
from odoo.exceptions import UserError


class ReportAnalyzerWizard(models.TransientModel):
    _name = 'report.analyzer.wizard'
    _description = 'QWeb Report Analyzer — Run Analysis'

    report_id = fields.Many2one(
        'ir.actions.report',
        string='Report',
        readonly=True,
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        active_id = self._context.get('active_id')
        if active_id:
            res['report_id'] = active_id
        return res

    def action_run(self):
        if not self.report_id:
            raise UserError(
                "No report selected.\n\n"
                "Go to: Settings \u2192 Technical \u2192 Reporting \u2192 Reports, "
                "select a report, then use the gear menu."
            )
        return self.env['report.analyzer'].analyze_report(self.report_id.id)
