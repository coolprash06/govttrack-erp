from odoo import models, fields, api


class GovttrackConstituency(models.Model):
    _name = "govttrack.constituency"
    _description = "Lok Sabha Constituency"

    name = fields.Char(string="Constituency Name", required=True)
    state = fields.Char(string="State")
    district = fields.Char(string="District")
    population = fields.Integer(string="Population")
    mp_name = fields.Char(string="MP Name")
    mla_name = fields.Char(string="MLA Name")
    contact_info = fields.Char(string="Contact Info")
    mp_party = fields.Char(string="Party")
    term_start_date = fields.Date(string="Term Start Date")
    term_end_date = fields.Date(string="Term End Date")
    districts = fields.Text(string="Covered Districts")
    project_ids = fields.One2many("govttrack.project", "constituency_id", string="Projects")
    project_count = fields.Integer(string="Total Projects", compute="_compute_project_stats", store=True)
    active_project_count = fields.Integer(string="Active Projects", compute="_compute_project_stats", store=True)
    completed_project_count = fields.Integer(string="Completed Projects", compute="_compute_project_stats", store=True)
    total_budget = fields.Float(string="Total Project Budget", compute="_compute_project_stats", store=True)

    @api.depends('project_ids.budget', 'project_ids.status')
    def _compute_project_stats(self):
        for constituency in self:
            constituency.project_count = len(constituency.project_ids)
            constituency.active_project_count = len(constituency.project_ids.filtered(lambda p: p.status in ['submitted', 'under_review', 'approved', 'in_progress']))
            constituency.completed_project_count = len(constituency.project_ids.filtered(lambda p: p.status in ['completed', 'closed']))
            constituency.total_budget = sum(constituency.project_ids.mapped('budget'))
