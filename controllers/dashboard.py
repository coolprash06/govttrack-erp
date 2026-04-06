from odoo import http
from odoo.http import request
from datetime import datetime, timedelta


class GovtTrackDashboard(http.Controller):
    
    @http.route('/govttrack/dashboard', auth='user', type='json')
    def dashboard(self, **kwargs):
        """Render the GovtTrack dashboard with aggregated project data."""
        user = request.env.user
        Project = request.env['govttrack.project']
        Grievance = request.env['govttrack.grievance']
        
        # Get all projects
        projects = Project.search([])
        
        # KPI Calculations
        total_projects = len(projects)
        in_progress_count = len(projects.filtered(lambda p: p.status == 'in_progress'))
        delayed_count = len(projects.filtered(lambda p: p.is_delayed))
        completed_count = len(projects.filtered(lambda p: p.status == 'completed'))
        open_grievance_count = len(Grievance.search([('status', 'in', ['new', 'under_review'])]))
        
        # Delayed projects list (top 5)
        delayed_projects = projects.filtered(lambda p: p.is_delayed).sorted(
            key=lambda x: x.delay_days, reverse=True
        )[:5]
        
        delayed_projects_data = [
            {
                'name': p.name,
                'constituency': p.constituency_id.name if p.constituency_id else 'N/A',
                'delay_days': p.delay_days,
                'status': 'Critical' if p.delay_days > 30 else 'Warning'
            }
            for p in delayed_projects
        ]
        
        # Financial data
        total_budget = sum(projects.mapped('budget'))
        total_spent = sum(projects.mapped('spent_amount'))
        total_remaining = total_budget - total_spent
        budget_utilization = (total_spent / total_budget * 100) if total_budget > 0 else 0
        
        # Format currency for display (in lakhs for Indian rupees)
        def format_currency(amount):
            if amount >= 10000000:  # 1 crore+
                return f"{amount / 10000000:.2f}Cr"
            elif amount >= 100000:  # 1 lakh+
                return f"{amount / 100000:.2f}L"
            else:
                return f"{int(amount):,}"
        
        # Recent grievances (top 5)
        recent_grievances = Grievance.search([], order='date_submitted desc', limit=5)
        grievances_data = [
            {
                'name': g.name,
                'project': g.project_id.name if g.project_id else 'N/A',
                'status': g.status,
                'severity': g.severity
            }
            for g in recent_grievances
        ]
        
        # Status distribution
        status_counts = {}
        for status in ['draft', 'submitted', 'approved', 'in_progress', 'completed', 'rejected', 'closed']:
            status_counts[status] = len(projects.filtered(lambda p: p.status == status))
        
        # Categories
        categories_data = []
        for category in set(projects.mapped('category_id')):
            cat_projects = projects.filtered(lambda p: p.category_id == category)
            categories_data.append({
                'name': category.name,
                'count': len(cat_projects),
                'budget': sum(cat_projects.mapped('budget')),
                'budget_formatted': format_currency(sum(cat_projects.mapped('budget')))
            })
        
        # Prepare data dictionary
        dashboard_data = {
            'total_projects': total_projects,
            'in_progress_count': in_progress_count,
            'delayed_count': delayed_count,
            'completed_count': completed_count,
            'open_grievance_count': open_grievance_count,
            'delayed_projects': delayed_projects_data,
            'total_budget': total_budget,
            'total_budget_formatted': format_currency(total_budget),
            'total_spent': total_spent,
            'total_spent_formatted': format_currency(total_spent),
            'total_remaining': total_remaining,
            'total_remaining_formatted': format_currency(total_remaining),
            'budget_utilization_percent': round(budget_utilization, 1),
            'recent_grievances': grievances_data,
            'status_draft': status_counts.get('draft', 0),
            'status_submitted': status_counts.get('submitted', 0),
            'status_approved': status_counts.get('approved', 0),
            'status_in_progress': status_counts.get('in_progress', 0),
            'status_completed': status_counts.get('completed', 0),
            'categories': categories_data
        }
        
        return dashboard_data
