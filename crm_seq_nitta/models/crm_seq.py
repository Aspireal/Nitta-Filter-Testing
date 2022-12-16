from odoo import api, fields, models, _


class CrmLead(models.Model):
    _inherit = "crm.lead"

    reference_no = fields.Char(string='Lead Reference', required=True, readonly=True, default=lambda self: _('New'),
                               track_visibility='onchange')
    reference_no1 = fields.Char(string='Opportunity Reference', required=True, readonly=True,
                                default=lambda self: _('New'), track_visibility='onchange')
    lead_ref = fields.Char(string="Lead Reference", compute='_compute_reference')

    @api.depends('reference_no')
    def _compute_reference(self):
        for rec in self:
            if rec.type == 'opportunity':
                rec.lead_ref = rec.reference_no
            else:
                rec.lead_ref = rec.reference_no

    # Lead Sequence
    @api.model
    def create(self, vals):
        if vals.get('reference_no', _('New')) == _('New'):
            vals['reference_no'] = self.env['ir.sequence'].next_by_code('crm.lead') or _('New')

        if vals.get('reference_no1', _('New')) == _('New'):
            vals['reference_no1'] = self.env['ir.sequence'].next_by_code('crm.lead.opportunity') or _('New')
        res = super(CrmLead, self).create(vals)
        return res
