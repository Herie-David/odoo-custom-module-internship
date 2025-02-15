from odoo import fields, models, api

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Types"
    _order = "sequence, name"
    _sql_constraints = [
        ('unique_type_name', 'UNIQUE(name)', 'The Property Type must be unique.')
        ]
    name = fields.Char(required=True)
    sequence = fields.Integer(string="Sequence", default=1)
    description = fields.Text()
    property_ids = fields.One2many(comodel_name="estate.property", 
        inverse_name="property_type_id", 
        string="Properties")
    offer_ids = fields.One2many(
        comodel_name="estate.property.offer",
        inverse_name="property_type_id",
        string="Offers",
    )
    offer_count = fields.Integer(
        string="Offer Count",
        compute="_compute_offer_count",
    )

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)