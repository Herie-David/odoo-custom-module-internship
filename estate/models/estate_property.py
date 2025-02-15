from odoo import fields, models, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'The expected price must be strictly positive.'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'The selling price must be positive.')
        ]
    name = fields.Char('Title', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Availability Date', 
            default=lambda self: fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True)
    bedrooms = fields.Integer('Bedrooms', default= 2)
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area (sqm)', default=0)
    garden_orientation = fields.Selection(string='Garden Orientation', default='north',
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')]
        )
    tag_ids = fields.Many2many(comodel_name='estate.property.tag', string='Tags')
    color = fields.Integer('Color')
    
    active = fields.Boolean('Active', default=True)
    state = fields.Selection(string='Status',
        required=True,
        default='new',
        selection=[
            ('new', 'New'),
            ('offer received', 'Offer Received'),
            ('offer accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')]
        )
    offer_ids = fields.One2many(string='Offers',
        comodel_name ='estate.property.offer',
        inverse_name ='property_id'
        )
    best_price = fields.Float(string="Best Offer", compute="_compute_best_price")
    total_area = fields.Float(string="Total Area (sqm)", compute="_compute_total_area")
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    seller_id = fields.Many2one("res.users", string="Salesman")
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    
    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        default = dict(default or {})
        default['date_availability'] = None
        default['selling_price'] = None
        default['state'] = 'new'
        return super(EstateProperty, self).copy(default)
    
    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = None
    
    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0.00
    
    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price > 0 and record.selling_price < (0.9 * record.expected_price):
                raise ValidationError(
                    "The selling price cannot be lower than 90% of the expected price."
                )
    
    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("A sold property cannot be cancelled.")
            record.state = 'cancelled'

    def action_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError("A cancelled property cannot be set as sold.")
            record.state = 'sold'