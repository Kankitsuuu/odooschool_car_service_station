from odoo import models, fields


class CarServiceClient(models.Model):
    _name = 'car.service.client'
    _description = 'Car Service Client'
    _inherit = 'car.service.person'

    car_ids = fields.One2many(
        comodel_name='car.service.client.car',
        inverse_name='client_id',
    )
