from odoo import api, fields, models

class GovttrackCategory(models.Model):
    _name = "govttrack.category"
    _description = "Project Category"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    project_ids = fields.One2many("govttrack.project", "category_id", string="Projects")
    project_count = fields.Integer(string="Total Projects", compute="_compute_project_stats", store=True)
    active_project_count = fields.Integer(string="Active Projects", compute="_compute_project_stats", store=True)
    completed_project_count = fields.Integer(string="Completed Projects", compute="_compute_project_stats", store=True)
    total_budget = fields.Float(string="Total Project Budget", compute="_compute_project_stats", store=True)

    @api.depends("project_ids.budget", "project_ids.status")
    def _compute_project_stats(self):
        for category in self:
            projects = category.project_ids
            category.project_count = len(projects)
            category.active_project_count = len(projects.filtered(lambda p: p.status in ['submitted', 'under_review', 'approved', 'in_progress']))
            category.completed_project_count = len(projects.filtered(lambda p: p.status in ['completed', 'closed']))
            category.total_budget = sum(projects.mapped('budget'))