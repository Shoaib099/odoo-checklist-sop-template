# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import UserError


class ChecklistInstance(models.Model):
    """A working checklist someone is actually filling in.

    Generic attachment pattern
    ---------------------------
    Instead of hard-coding a Many2one to project.task (which would force
    every user of this module to have Project installed), we store the
    target as (res_model_id, res_id) - exactly the pattern Odoo itself
    uses for mail.activity. This means ANY other module can create a
    checklist.instance pointed at ANY of its own records with zero
    changes needed here, and with no dependency added to this module.
    A tiny "bridge" module (see checklist_sop_project) can then add a
    convenience smart button on a specific model - that's a separate,
    optional add-on.
    """
    _name = 'checklist.instance'
    _description = 'Checklist'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(required=True, tracking=True)
    template_id = fields.Many2one(
        comodel_name='checklist.template',
        string='Based on Template',
        tracking=True,
    )
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Assigned To',
        default=lambda self: self.env.user,
        tracking=True,
    )
    deadline = fields.Date(tracking=True)
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('in_progress', 'In Progress'),
            ('done', 'Done'),
            ('cancelled', 'Cancelled'),
        ],
        default='draft',
        required=True,
        tracking=True,
    )
    company_id = fields.Many2one(
        comodel_name='res.company',
        default=lambda self: self.env.company,
    )

    # --- generic "attach to any record" reference -------------------
    res_model_id = fields.Many2one(
        comodel_name='ir.model',
        string='Related Document Type',
        ondelete='cascade',
        help='Model of the record this checklist is attached to (optional).',
    )
    res_model = fields.Char(
        string='Related Model',
        related='res_model_id.model',
        store=True,
        readonly=True,
    )
    res_id = fields.Many2oneReference(
        string='Related Record ID',
        model_field='res_model',
    )
    res_name = fields.Char(
        string='Related Record',
        compute='_compute_res_name',
    )

    # --- lines / progress ---------------------------------------------
    line_ids = fields.One2many(
        comodel_name='checklist.instance.line',
        inverse_name='instance_id',
        string='Items',
        copy=True,
    )
    total_lines = fields.Integer(compute='_compute_progress', store=True)
    done_lines = fields.Integer(compute='_compute_progress', store=True)
    progress = fields.Float(
        string='Progress (%)',
        compute='_compute_progress',
        store=True,
        aggregator='avg',
    )

    @api.depends('line_ids.is_done')
    def _compute_progress(self):
        for instance in self:
            total = len(instance.line_ids)
            done = len(instance.line_ids.filtered('is_done'))
            instance.total_lines = total
            instance.done_lines = done
            instance.progress = (done / total * 100.0) if total else 0.0

    @api.depends('res_model', 'res_id')
    def _compute_res_name(self):
        for instance in self:
            name = False
            if instance.res_model and instance.res_id:
                record = self.env[instance.res_model].browse(instance.res_id)
                if record.exists():
                    name = record.display_name
            instance.res_name = name

    # --- onchange -------------------------------------------------------
    @api.onchange('template_id')
    def _onchange_template_id(self):
        """Pre-fill items the moment a template is picked, so the user
        can still tweak them before saving."""
        if self.template_id:
            self.name = self.name or self.template_id.name
            self.line_ids = [(5, 0, 0)] + [
                (0, 0, {
                    'sequence': line.sequence,
                    'name': line.name,
                    'is_mandatory': line.is_mandatory,
                    'responsible_role': line.responsible_role,
                })
                for line in self.template_id.line_ids
            ]

    # --- actions ----------------------------------------------------
    def action_start(self):
        self.write({'state': 'in_progress'})

    def action_done(self):
        for instance in self:
            unfinished_mandatory = instance.line_ids.filtered(
                lambda l: l.is_mandatory and not l.is_done
            )
            if unfinished_mandatory:
                raise UserError(
                    "You can't close this checklist yet - the following "
                    "mandatory items are not done:\n- %s"
                    % '\n- '.join(unfinished_mandatory.mapped('name'))
                )
        self.write({'state': 'done'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def action_reset_to_draft(self):
        self.write({'state': 'draft'})

    def action_open_related_record(self):
        self.ensure_one()
        if not (self.res_model and self.res_id):
            raise UserError('This checklist is not linked to any record.')
        return {
            'type': 'ir.actions.act_window',
            'res_model': self.res_model,
            'res_id': self.res_id,
            'view_mode': 'form',
            'target': 'current',
        }
