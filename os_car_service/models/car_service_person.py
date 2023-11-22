from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class CarServicePerson(models.AbstractModel):
    _name = 'car.service.person'
    _description = 'Car Service Person Abstract Model'

    name = fields.Char(
        required=True,
    )
    surname = fields.Char(
        required=True,
    )
    phone = fields.Char()
    email = fields.Char()
    photo = fields.Image(
        max_width=1920,
        max_height=1080,
    )
    gender = fields.Selection(
        selection=[('male', 'Male'),
                   ('female', 'Female'),
                   ('other', 'Other')],
        default='male',
    )

    def name_get(self):
        return [(rec.id, f'{rec.name} {rec.surname}') for rec in self]

    # Constraint methods
    @api.constrains('phone')
    def _check_phone(self):
        """Checking the uniqueness of the phone number if phone exists"""
        for person in self:
            if person.phone:
                person_count = self.search_count([('phone', '=', person.phone)])
                if person_count > 1:
                    raise ValidationError(_(
                        'Person with the same phone number already exists.'
                    ))
