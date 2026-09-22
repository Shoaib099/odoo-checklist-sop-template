# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ChecklistTemplate(models.Model):
    """A reusable checklist / SOP definition.

    Think of this as the *blueprint*. It never gets "completed" itself -
    it just holds an ordered list of items that will be copied onto a
    checklist.instance every time someone uses this template.
    """
    _name = 'checklist.template'
    _description = 'Checklist / SOP Template'
    _order = 'name'

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    category = fields.Selection(
        selection=[
            ('onboarding', 'Onboarding'),
            ('quality', 'Quality Check'),
            ('safety', 'Safety'),
            ('approval', 'Approval / Sign-off'),
            ('other', 'Other'),
        ],
        default='other',
        required=True,
    )
    description = fields.Text(help='Explain when this checklist should be used.')
    line_ids = fields.One2many(
        comodel_name='checklist.template.line',
        inverse_name='template_id',
        string='Checklist Items',
        copy=True,
    )
    line_count = fields.Integer(compute='_compute_line_count')
    instance_count = fields.Integer(compute='_compute_instance_count')
    company_id = fields.Many2one(
        comodel_name='res.company',
        default=lambda self: self.env.company,
    )

    @api.depends('line_ids')
    def _compute_line_count(self):
        for template in self:
            template.line_count = len(template.line_ids)

    def _compute_instance_count(self):
        # avoid a search per record: one grouped read_group for the whole recordset
        counts = dict(
            self.env['checklist.instance']._read_group(
                domain=[('template_id', 'in', self.ids)],
                groupby=['template_id'],
                aggregates=['__count'],
            )
        )
        for template in self:
            template.instance_count = counts.get(template, 0)

    def action_view_instances(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Checklists from %s' % self.name,
            'res_model': 'checklist.instance',
            'view_mode': 'list,form',
            'domain': [('template_id', '=', self.id)],
            'context': {'default_template_id': self.id},
        }

    def action_create_instance(self):
        """Smart-button/menu shortcut: create one instance from this
        template and jump straight into its form so the user can pick
        who it's for."""
        self.ensure_one()
        instance = self.env['checklist.instance'].create({
            'template_id': self.id,
            'name': self.name,
        })
        return {
            'type': 'ir.actions.act_window',
            'name': 'New Checklist',
            'res_model': 'checklist.instance',
            'view_mode': 'form',
            'res_id': instance.id,
        }
