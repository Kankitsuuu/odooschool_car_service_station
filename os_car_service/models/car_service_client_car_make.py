from odoo import models, fields


class CarServiceClientCarMake(models.Model):
    _name = 'car.service.client.car.make'
    _description = 'Car Service Client`s Car Make'

    name = fields.Char()
