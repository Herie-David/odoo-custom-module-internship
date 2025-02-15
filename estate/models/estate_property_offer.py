from odoo import fields, models, api
from datetime import timedelta
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offers"
    _order = "price desc"
    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)', 'The Offer Price must be strictly positive.')
        ]
    price = fields.Float('Price', required=True)
    status = fields.Selection(string='Status',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')]
        )
    partner_id = fields.Many2one(comodel_name='res.partner',
        string='Partner', required=True
        )
    property_id = fields.Many2one(comodel_name='estate.property',
        string='Property', required=True
        )
    validity = fields.Integer("Validity (Days)", default=7)
    date_deadline = fields.Date("Deadline",
        compute ='_compute_date_deadline',
        inverse ='_inverse_date_deadline',
        )
    property_state = fields.Selection(
        related='property_id.state',
        string='Property State',
        store=True
        )
    property_type_id = fields.Many2one(
        comodel_name="estate.property.type",
        string="Property Type",
        related="property_id.property_type_id",
        store=True,
    )

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Date.today()
            record.date_deadline = create_date + timedelta(days=record.validity)
    
    def _inverse_date_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Date.today()
            if record.date_deadline:
                create_date = create_date.date()
                record.validity = (record.date_deadline - create_date).days
    
    def action_refuse(self):
        for record in self:
            record.status = 'refused'

    def action_accept(self):
        for record in self:
            existing_offer = self.env['estate.property.offer'].search([
                ('property_id', '=', record.property_id.id),
                ('status', '=', 'accepted')
            ], limit=1)
            if existing_offer:
                raise UserError("Only one offer can be accepted for this property.")
            
            record.status = 'accepted'
            record.property_id.buyer_id = record.partner_id
            record.property_id.state = 'sold'
            record.property_id.selling_price = record.price 