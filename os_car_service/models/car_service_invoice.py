import hashlib
from typing import Optional, NoReturn

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class CarServiceInvoice(models.Model):
    _name = 'car.service.invoice'
    _description = 'Car Service Invoice'

    name = fields.Char(
        compute='_compute_name',
        store=True,
    )
    client_id = fields.Many2one(
        comodel_name='car.service.client',
        required=True,
    )
    set_date = fields.Datetime(
        default=fields.Datetime.now,
        readonly=True,
    )
    service_ids = fields.Many2many(
        comodel_name='car.service.provided.service',
    )
    price = fields.Float(
        compute='_compute_price',
        digits=(12, 2),
    )
    is_paid = fields.Boolean(
        default=False,
    )

    # Compute methods
    @api.depends('set_date', 'client_id')
    def _compute_name(self):
        """
        Compute name field
        as hash string from set_date and client_id
        """
        for invoice in self:
            name_data = f"{invoice.set_date.strftime('%Y-%m-%d %H:%M:%s')}{invoice.client_id.id}"
            name = hashlib.sha512(name_data.encode()).hexdigest()
            invoice.name = name[:10].upper()

    @api.depends('service_ids')
    def _compute_price(self):
        """
        Compute invoice price
        as total price of provided services
        """
        for invoice in self:
            if invoice.service_ids:
                invoice.price = sum(
                    [service.price_total for service in invoice.service_ids]
                )
            else:
                invoice.price = 0

    # Constraint methods
    @api.constrains('client_id', 'service_ids')
    def _check_client_services(self):
        """
        Checks client id in provided service ids
        If the entries don't match it will raise ValidationError
        """
        for invoice in self:
            # check if invoice has provided services
            if not invoice.service_ids:
                raise ValidationError(_(
                    'At least one service must be listed on the invoice.'
                ))
            for service in invoice.service_ids:
                # check if services have the same client
                if invoice.client_id.id != service.client_id.id:
                    raise ValidationError(_(
                        "You cannot specify other clients' services."
                    ))
                # check if services already invoiced
                elif service.invoice_id:
                    raise ValidationError(_(
                        'You cannot add services from other invoices.'
                    ))
                service.invoice_id = invoice

    # Onchange methods

    @api.onchange('client_id')
    def _onchange_client_id(self):
        self.service_ids = False

    # CRUD methods
    def write(self, vals):
        """
        Write method
        (Can change if only invoice is not paid)
        """
        res = super(CarServiceInvoice, self).write(vals)
        if vals.get('is_paid'):
            if vals['is_paid']:
                return res
        self.check_is_paid()
        if vals.get('service_ids'):
            # set invoice_id as False for current services
            for invoice in self:
                for service in invoice.service_ids:
                    service.invoice_id = False
        return res

    def unlink(self):
        """
        Unlink method
        (Can unlink if only invoice is not paid)
        """
        self.check_is_paid()
        return super(CarServiceInvoice, self).unlink()

    # Other methods
    def check_is_paid(self) -> Optional[NoReturn]:
        """
        Checks whether the invoice has paid status
        If not it will raise UserError
        """
        for invoice in self:
            if invoice.is_paid:
                raise UserError(_(
                    'You cannot change paid invoices.'
                ))
