from odoo import models, fields, api, _


class CarServiceClient(models.Model):
    _name = 'car.service.client'
    _description = 'Car Service Client'
    _inherit = 'car.service.person'

    car_ids = fields.One2many(
        comodel_name='car.service.client.car',
        inverse_name='client_id',
        readonly=True,
    )
    car_total = fields.Integer(
        compute='_compute_car_total',
    )
    service_ids = fields.One2many(
        comodel_name='car.service.provided.service',
        inverse_name='client_id',
    )
    service_total = fields.Integer(
        compute='_compute_service_total',
    )
    invoice_ids = fields.One2many(
        comodel_name='car.service.invoice',
        inverse_name='client_id',
    )
    invoice_total = fields.Integer(
        compute='_compute_invoice_total'
    )

    # Compute methods
    @api.depends('car_ids')
    def _compute_car_total(self):
        """Compute car_total field"""
        for client in self:
            client.car_total = len(client.car_ids)

    @api.depends('service_ids')
    def _compute_service_total(self):
        """Compute service_total field"""
        for client in self:
            client.service_total = len(client.service_ids)

    @api.depends('invoice_ids')
    def _compute_invoice_total(self):
        """Compute invoice_total field"""
        for client in self:
            client.invoice_total = len(client.invoice_ids)

    # Action methods
    def action_open_cars(self):
        """Open tree,form view of client cars"""
        self.ensure_one()
        return {
            'name': _('Cars'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'car.service.client.car',
            'domain': [('id', 'in', self.car_ids.ids)],
            'target': 'current',
        }

    def action_open_services(self):
        """Open tree,form view of provided services for client"""
        self.ensure_one()
        return {
            'name': _('Provided Services'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'car.service.provided.service',
            'domain': [('id', 'in', self.service_ids.ids)],
            'target': 'current',
        }

    def action_open_invoices(self):
        """Open tree,form view of client invoices"""
        self.ensure_one()
        return {
            'name': _('Invoices'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'car.service.invoice',
            'domain': [('id', 'in', self.invoice_ids.ids)],
            'target': 'current',
        }
