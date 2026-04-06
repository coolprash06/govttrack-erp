from datetime import timedelta

from odoo import models, fields, api


class GovttrackGrievance(models.Model):
    _name = "govttrack.grievance"
    _description = "Citizen Grievance"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Subject", required=True)
    project_id = fields.Many2one("govttrack.project", string="Related Project", required=True, tracking=True)
    constituency_id = fields.Many2one("govttrack.constituency", string="Constituency", related="project_id.constituency_id", store=True, readonly=True)
    citizen_name = fields.Char(string="Citizen Name")
    citizen_contact = fields.Char(string="Contact")
    grievance_type = fields.Selection([
        ('safety', 'Safety Issue'),
        ('quality', 'Quality Issue'),
        ('delay', 'Delay Complaint'),
        ('inconvenience', 'Public Inconvenience'),
        ('obstruction', 'Obstruction'),
        ('environmental', 'Environmental Issue')
    ], string="Type")
    description = fields.Text(string="Description")
    severity = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ], string="Severity", default='medium', tracking=True)
    status = fields.Selection([
        ('new', 'New'),
        ('under_review', 'Under Review'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed')
    ], string="Status", default='new', tracking=True)
    assigned_officer_id = fields.Many2one("res.users", string="Assigned Officer", required=True, tracking=True)
    date_submitted = fields.Date(string="Date Submitted", default=fields.Date.today)
    response_deadline = fields.Date(string="Response Deadline", compute="_compute_response_deadline", store=True)
    sla_days = fields.Integer(string="SLA Days", compute="_compute_response_deadline", store=True)
    date_resolved = fields.Date(string="Date Resolved")
    resolution_note = fields.Text(string="Resolution Note")

    @api.depends('date_submitted', 'severity')
    def _compute_response_deadline(self):
        for record in self:
            if not record.date_submitted:
                record.response_deadline = False
                record.sla_days = 0
                continue
            days = 7
            if record.severity == 'high':
                days = 3
            elif record.severity == 'medium':
                days = 5
            record.response_deadline = record.date_submitted + timedelta(days=days)
            record.sla_days = days

    def action_review(self):
        self.status = 'under_review'

    def action_resolve(self):
        self.date_resolved = fields.Date.today()
        self.status = 'resolved'

    def action_close(self):
        self.status = 'closed'
