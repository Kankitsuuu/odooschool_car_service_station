from odoo import models, fields


class CarServiceServiceCategory(models.Model):
    _name = 'car.service.service.category'
    _description = 'Car Service Categories'

    name = fields.Char(
        required=True,
    )
