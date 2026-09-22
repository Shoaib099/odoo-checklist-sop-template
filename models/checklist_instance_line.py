# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ChecklistInstanceLine(models.Model):
    _name = 'checklist.instance.line'
    _description = 'Checklist Item'
    _order = 'sequence, id'

    instance_id = fields.Many2one(
        comodel_name='checklist.instance',
        required=True,
        ondelete='cascade',
    )
    sequence = fields.Integer(default=10)
    name = fields.Char(required=True, string='Item')
    is_mandatory = fields.Boolean(default=True)
    responsible_role = fields.Char(string='Suggested Owner')
    is_done = fields.Boolean(string='Done')
    done_by = fields.Many2one(comodel_name='res.users', readonly=True)
    done_date = fields.Datetime(readonly=True)
    note = fields.Text()

    @api.model_create_multi
    def create(self, vals_list):
        lines = super().create(vals_list)
        lines._sync_done_metadata()
        return lines

    def write(self, vals):
        res = super().write(vals)
        if 'is_done' in vals:
            self._sync_done_metadata()
        return res

    def _sync_done_metadata(self):
        """Stamp who ticked an item and when - and clear the stamp if
        someone unticks it, so the audit info never lies."""
        for line in self:
            if line.is_done and not line.done_date:
                line.done_by = self.env.user
                line.done_date = fields.Datetime.now()
            elif not line.is_done and line.done_date:
                line.done_by = False
                line.done_date = False
