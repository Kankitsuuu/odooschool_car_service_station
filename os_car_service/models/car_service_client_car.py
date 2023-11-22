from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class CarServiceClientCar(models.Model):
    _name = 'car.service.client.car'
    _description = 'Car Service Client`s Car'

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
    model = fields.Char()
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

    # Default methods
    def name_get(self):
        """Default name get method."""
        names = []
        selection = self.fields_get(allfields=['body'])['body']['selection']
        bodies = dict(selection)
        for car in self:
            make = car.make_id.name
            color = car.color_id.name
            body = bodies[car.body]
            name = f'{make} {color} {body} {car.number}'
            names.append((car.id, name))
        return names

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
