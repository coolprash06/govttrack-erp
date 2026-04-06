from datetime import date

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class GovttrackProject(models.Model):
    _name = "govttrack.project"
    _description = "Public Work Project"

    name = fields.Char(string="Project Title", required=True)
    project_code = fields.Char(string="Project Code", readonly=True, copy=False)
    description = fields.Text(string="Description")
    constituency_id = fields.Many2one("govttrack.constituency", string="Constituency")
    district = fields.Char(string="District")
    location = fields.Char(string="Location/Area")
    category_id = fields.Many2one("govttrack.category", string="Category")
    mp_name = fields.Char(string="Recommending MP", related="constituency_id.mp_name", readonly=True)
    estimated_cost = fields.Float(string="Estimated Cost")
    recommended_date = fields.Date(string="Recommended Date", default=fields.Date.today)
    approval_date = fields.Date(string="Approval Date")
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    actual_completion_date = fields.Date(string="Actual Completion Date")
    term_end_date = fields.Date(string="Term End Date", related="constituency_id.term_end_date", readonly=True)
    priority = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ], string="Priority", default='medium')
    status = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
        ('closed', 'Closed')
    ], string="Status", default='draft')
    assigned_officer_id = fields.Many2one("res.users", string="Assigned Officer")
    grievance_ids = fields.One2many("govttrack.grievance", "project_id", string="Grievances")
    grievance_count = fields.Integer(string="Grievance Count", compute="_compute_grievance_count", store=True)
    open_grievance_count = fields.Integer(string="Open Grievance Count", compute="_compute_grievance_count", store=True)
    is_delayed = fields.Boolean(string="Is Delayed", compute="_compute_delay_status", store=True)
    completed_within_term = fields.Boolean(string="Completed Within Term", compute="_compute_term_completion", store=True)
    days_left_in_term = fields.Integer(string="Days Left in Term", compute="_compute_term_completion", store=True)
    notes = fields.Text(string="Notes")
    budget = fields.Float(string="Budget")
    allocated_amount = fields.Float(string="Allocated Amount")
    spent_amount = fields.Float(string="Spent Amount")
    budget_short = fields.Char(string="Budget (Short)", compute="_compute_financial_short")
    spent_amount_short = fields.Char(string="Spent (Short)", compute="_compute_financial_short")
    currency_id = fields.Many2one('res.currency', string="Currency", default=lambda self: self.env.company.currency_id)
    completion_percentage = fields.Float(string="Completion %", compute="_compute_completion_percentage", store=True)
    delay_days = fields.Integer(string="Delay Days", compute="_compute_delay_days", store=True)
    progress_notes = fields.Text(string="Progress Notes")

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for record in self:
            if record.start_date and record.end_date and record.start_date > record.end_date:
                raise ValidationError("Start Date cannot be after the End Date.")

    @api.depends("budget", "spent_amount")
    def _compute_financial_short(self):
        def format_short(amount):
            if not amount:
                return "0.00"
            if amount >= 10000000:
                return f"{amount / 10000000:.2f} Cr"
            elif amount >= 100000:
                return f"{amount / 100000:.2f} L"
            elif amount >= 1000:
                return f"{amount / 1000:.2f} K"
            else:
                return f"{amount:.2f}"

        for record in self:
            record.budget_short = format_short(record.budget)
            record.spent_amount_short = format_short(record.spent_amount)

    @api.depends("grievance_ids.status")
    def _compute_grievance_count(self):
        for record in self:
            record.grievance_count = len(record.grievance_ids)
            record.open_grievance_count = len(record.grievance_ids.filtered(lambda g: g.status in ['new', 'under_review']))

    @api.depends("end_date", "status")
    def _compute_delay_status(self):
        today = date.today()
        for record in self:
            if record.end_date and record.status not in ['completed', 'closed']:
                record.is_delayed = today > record.end_date
            else:
                record.is_delayed = False

    @api.depends("end_date", "status")
    def _compute_delay_days(self):
        today = date.today()
        for record in self:
            if record.end_date and record.status not in ['completed', 'closed']:
                record.delay_days = max(0, (today - record.end_date).days) if today > record.end_date else 0
            else:
                record.delay_days = 0

    @api.depends("actual_completion_date", "term_end_date")
    def _compute_term_completion(self):
        for record in self:
            if record.actual_completion_date and record.term_end_date:
                record.completed_within_term = record.actual_completion_date <= record.term_end_date
                record.days_left_in_term = max(0, (record.term_end_date - record.actual_completion_date).days) if record.completed_within_term else 0
            else:
                record.completed_within_term = False
                record.days_left_in_term = 0

    @api.depends("allocated_amount", "spent_amount")
    def _compute_completion_percentage(self):
        for record in self:
            if record.allocated_amount:
                record.completion_percentage = min(100.0, (record.spent_amount / record.allocated_amount) * 100)
            else:
                record.completion_percentage = 0.0

    def action_draft(self):
        self.status = 'draft'

    def action_review(self):
        self.status = 'under_review'

    def action_submit(self):
        self.status = 'submitted'

    def action_approve(self):
        self.approval_date = fields.Date.today()
        self.status = 'approved'

    def action_reject(self):
        self.status = 'rejected'

    def action_start(self):
        self.start_date = fields.Date.today()
        self.status = 'in_progress'

    def action_complete(self):
        self.actual_completion_date = fields.Date.today()
        self.status = 'completed'

    def action_close(self):
        self.status = 'closed'

print('LOADING PROJECT.PY!!!!!')
