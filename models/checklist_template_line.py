# -*- coding: utf-8 -*-
from odoo import fields, models


class ChecklistTemplateLine(models.Model):
    _name = 'checklist.template.line'
    _description = 'Checklist Template Item'
    _order = 'sequence, id'

    template_id = fields.Many2one(
        comodel_name='checklist.template',
        required=True,
        ondelete='cascade',
    )
    sequence = fields.Integer(default=10)
    name = fields.Char(required=True, string='Item')
    is_mandatory = fields.Boolean(
        default=True,
        help='If checked, this item MUST be completed before the checklist '
             'generated from this template can be marked as Done.',
    )
    responsible_role = fields.Char(
        string='Suggested Owner',
        help='Free-text hint, e.g. "HR", "IT", "Team Lead". Not enforced, '
             'just a hint shown on the generated checklist item.',
    )
    note = fields.Text()
