from odoo import models, fields


class CarServiceService(models.Model):
    _name = 'car.service.service'
    _description = 'Car Service Services'

    name = fields.Char(
        required=True,
        translate=True,
    )
    description = fields.Text(
        translate=True,
    )
    price = fields.Float(
        digits=(12, 2),
        required=True,
    )
    category_id = fields.Many2one(
        comodel_name='car.service.service.category',
        required=True,
        default=lambda self: self.env.ref(
            'os_car_service.service_category_other'
        ),
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
    )
