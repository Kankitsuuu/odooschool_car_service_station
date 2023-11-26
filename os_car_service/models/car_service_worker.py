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
        translate=True,
    )
    passport = fields.Char(
        string='Passport(Details)',
        required=True,
    )
    age = fields.Integer(
        compute='_compute_age',
    )
    service_ids = fields.One2many(
        comodel_name='car.service.provided.service',
        inverse_name='worker_id',
    )
    service_total = fields.Integer(
        compute='_compute_service_total',
    )

    # Compute methods
    @api.depends('birth_date')
    def _compute_age(self):
        """Compute age field"""
        today = fields.Date.today()
        for worker in self:
            birthday = worker.birth_date
            if birthday:
                current = (today.month, today.day) < (birthday.month, birthday.day)
                worker.age = today.year - birthday.year - current
            else:
                worker.age = None

    @api.depends('service_ids')
    def _compute_service_total(self):
        """Compute service_total field"""
        for worker in self:
            worker.service_total = len(worker.service_ids)

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

    # Action methods
    def action_open_services(self):
        """Open tree,form view of provided services by worker"""
        self.ensure_one()
        return {
            'name': _('Provided Services'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'car.service.provided.service',
            'domain': [('id', 'in', self.service_ids.ids)],
            'target': 'current',
        }
