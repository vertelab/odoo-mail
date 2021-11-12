from odoo import models, fields, _

class ResPartner(models.Model):
    _inherit = 'res.partner'

    ssyk_codes = fields.Text(compute='_compute_ssyk', sting='SSYK Codes')

    def _compute_ssyk(self):
        for partner in self:
            ssyk = []
            for job in partner.job_ids:
                ssyk.append(job.ssyk_code)
            partner.ssyk_codes = ','.join(ssyk)
