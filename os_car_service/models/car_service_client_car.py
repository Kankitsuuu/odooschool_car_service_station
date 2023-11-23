from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class CarServiceClientCar(models.Model):
    _name = 'car.service.client.car'
    _description = 'Car Service Client`s Car'

    name = fields.Char(
        compute='_compute_name',
        store=True,
    )
    client_id = fields.Many2one(
        comodel_name='car.service.client',
        required=True,
    )
    make_id = fields.Many2one(
        comodel_name='car.service.client.car.make',
        required=True,
    )
    color_id = fields.Many2one(
        comodel_name='car.service.client.car.color',
        required=True,
    )
    number = fields.Char(
        required=True,
    )
    model = fields.Char(
        required=True,
    )
    photo = fields.Image(
        max_width=1920,
        max_height=1080,
    )
    year = fields.Integer()
    body = fields.Selection(
        selection=[('sedan', 'Sedan'),
                   ('coupe', 'Coupe'),
                   ('minivan', 'Minivan'),
                   ('van', 'Van'),
                   ('muscle', 'Muscle'),
                   ('hatchback', 'Hatchback'),
                   ('convertible', 'Convertible'),
                   ('crossover', 'Crossover'),
                   ('pickup', 'Pickup'),
                   ('suv', 'SUV'),
                   ('station-wagon', 'Station Wagon'),
                   ('sport', 'Sport'),
                   ('roadster', 'Roadster'),
                   ('other', 'Other')],
        default='sedan',
    )
    service_ids = fields.One2many(
        comodel_name='car.service.provided.service',
        inverse_name='car_id',
    )
    service_total = fields.Integer(
        compute='_compute_service_total',
    )

    # Compute methods
    @api.depends('make_id', 'color_id', 'model', 'number')
    def _compute_name(self):
        """Compute name method"""
        for car in self:
            make = car.make_id.name
            color = car.color_id.name
            car.name = f'{make} {car.model} {color} {car.number}'

    @api.depends('service_ids')
    def _compute_service_total(self):
        """Compute service_total field"""
        for car in self:
            car.service_total = len(car.service_ids)

    # Constraint methods
    @api.constrains('number')
    def _check_number(self):
        """Checking the uniqueness of the car number"""
        for car in self:
            cars_count = self.search_count([('number', '=', car.number)])
            if cars_count > 1:
                raise ValidationError(_(
                    'Car number must be unique.'
                ))

    # Action methods
    def action_open_services(self):
        """Open tree,form view of provided services for car"""
        self.ensure_one()
        return {
            'name': _('Provided Services'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'car.service.provided.service',
            'domain': [('id', 'in', self.service_ids.ids)],
            'target': 'current',
        }
