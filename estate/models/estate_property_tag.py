from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"
    _order = "name"
    _sql_constraints = [
        ('unique_tag_name', 'UNIQUE(name)', 'The Property Tag must be unique.')
        ]
    name = fields.Char('Tag Name', required=True)
    color = fields.Integer('Color')