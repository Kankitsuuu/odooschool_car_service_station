from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class CarServiceClientCarColor(models.Model):
    _name = 'car.service.client.car.color'
    _description = 'Car Service Client`s Car color'

    name = fields.Char(
        required=True,
        translate=True,
    )
    technical_code = fields.Char(
        required=True,
    )
    description = fields.Char(
        translate=True,
    )
    is_metallic = fields.Boolean(
        default=True,
    )

    # Constraint methods
    @api.constrains('technical_code')
    def _check_technical_code(self):
        """Checking the uniqueness of the color technical code"""
        for color in self:
            color_count = self.search_count(
                [('technical_code', '=', color.technical_code)]
            )
            if color_count > 1:
                raise ValidationError(_(
                    'Technical code must be unique.'
                ))
