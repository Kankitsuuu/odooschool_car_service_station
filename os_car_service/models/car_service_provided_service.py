import hashlib
from typing import Optional, NoReturn

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class CarServiceProvidedService(models.Model):
    _name = 'car.service.provided.service'
    _description = 'Car Service Invoice'

    name = fields.Char(
        compute='_compute_name',
        store=True,
    )
    set_date = fields.Date(
        default=fields.Date.today,
        required=True,
    )
    client_id = fields.Many2one(
        comodel_name='car.service.client',
        required=True,
    )
    car_id = fields.Many2one(
        comodel_name='car.service.client.car',
        required=True,
    )
    possible_car_ids = fields.One2many(
        related='client_id.car_ids',
    )
    worker_id = fields.Many2one(
        comodel_name='car.service.worker',
        string='Responsible worker',
        required=True,
    )
    service_id = fields.Many2one(
        comodel_name='car.service.service',
        required=True,
    )
    amount = fields.Integer(
        required=True,
        default=1,
    )
    price_total = fields.Float(
        compute='_compute_price_total',
        digits=(12, 2),
    )
    invoice_id = fields.Many2one(
        comodel_name='car.service.invoice',
        readonly=True,
    )
    is_invoiced = fields.Boolean(
        compute='_compute_is_invoiced',
    )
    is_paid = fields.Boolean(
        related='invoice_id.is_paid',
        store=True,
    )

    # Compute methods
    @api.depends('set_date', 'client_id')
    def _compute_name(self):
        """
        Compute name field
        as hash string from set_date and client_id
        """
        for service in self:
            name_data = (f"{service.set_date.strftime('%Y-%m-%d')}"
                         f"{service.client_id.id}")
            name = hashlib.sha512(name_data.encode()).hexdigest()
            service.name = name[:8].upper()

    @api.depends('service_id', 'amount')
    def _compute_price_total(self):
        """Compute price_total field"""
        for service in self:
            service.price_total = service.service_id.price * service.amount

    @api.depends('invoice_id')
    def _compute_is_invoiced(self):
        """Compute is invoiced field"""
        for service in self:
            service.is_invoiced = bool(service.invoice_id)

    # Constraint methods
    @api.constrains('amount')
    def _check_amount(self):
        """Validation of amount field (can not be less than 1)"""
        for service in self:
            if service.amount < 1:
                raise ValidationError(_(
                    'Service amount should be 1 or bigger.'
                ))

    @api.constrains('set_date')
    def _check_set_date(self):
        """Validation of set_date field (can not be future date)"""
        for service in self:
            if service.set_date > fields.Date.today():
                raise ValidationError(_(
                    'You can not set a future date.'
                ))

    @api.constrains('car_id', 'client_id')
    def _check_car_id(self):
        """
        Validation of car_id field
        (The car can only belong to the selected client)
        """
        for service in self:
            if service.car_id.id not in service.possible_car_ids.ids:
                raise ValidationError(_(
                    'The car should belong to the selected client.'
                ))

    # Onchange methods
    @api.onchange('car_id')
    def _onchange_car_id(self):
        """Automatically set the owner of the car as client_id"""
        self.client_id = self.car_id.client_id

    # CRUD methods
    def write(self, vals, from_invoice: bool = False):
        """
        Write method
        Change allowed from invoice write method
        (User can change only uninvoiced services)
        """
        if not from_invoice:
            self.check_is_invoiced()
        return super(CarServiceProvidedService, self).write(vals)

    def unlink(self):
        """
        Unlink method
        (User can delete only uninvoiced services)
        """
        self.check_is_invoiced()
        return super(CarServiceProvidedService, self).unlink()

    # Other methods
    def check_is_invoiced(self) -> Optional[NoReturn]:
        """
        Checks whether the service has paid status
        If not it will raise UserError
        """
        for service in self:
            if service.is_invoiced:
                raise UserError(_(
                    'You cannot change invoiced services.'
                ))
