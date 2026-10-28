from odoo import models, fields

class ProjectProject(models.Model):
    _inherit = 'project.project'
    
    regulatory_type = fields.Selection([
        ('bpom', 'BPOM Registration'),
        ('halal', 'Halal Certification'),
    ], string='Regulatory Type', index=True)
    
    regulatory_state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string='Status', default='draft', index=True)
    
    submission_date = fields.Date(string='Submission Date')
    estimated_approval_date = fields.Date(string='Estimated Approval Date')
    approval_date = fields.Date(string='Approval Date')
