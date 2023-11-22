from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class CarServiceWorker(models.Model):
    _name = 'car.service.worker'
    _description = 'Car Service Station Worker'
    _inherit = 'car.service.person'

    birth_date = fields.Date(
        required=True,
    )
    address = fields.Char(
        required=True,
    )
    passport = fields.Char(
        string='Passport(Details)',
        required=True,
    )
    age = fields.Integer(
        compute='_compute_age',
    )

    # Compute methods
    @api.depends('birth_date')
    def _compute_age(self):
        today = fields.Date.today()
        for worker in self:
            birthday = worker.birth_date
            if birthday:
                current = (today.month, today.day) < (birthday.month, birthday.day)
                worker.age = today.year - birthday.year - current
            else:
                worker.age = None

    # Constraint methods
    @api.constrains('passport')
    def _check_passport(self):
        """Checking the uniqueness of the passport details"""
        for worker in self:
            worker_count = self.search_count(
                [('passport', '=', worker.passport)]
            )
            if worker_count > 1:
                raise ValidationError(_(
                    'Passport code must be unique.'
                ))
