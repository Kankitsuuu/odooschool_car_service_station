from odoo import models, fields, _


class CreateInvoiceWizard(models.TransientModel):
    _name = 'create.invoice.wizard'
    _description = 'Wizard to create invoice'

    client_id = fields.Many2one(
        comodel_name='car.service.client',

    )
    service_ids = fields.Many2many(
        comodel_name='car.service.provided.service',
        required=True,
    )

    # Action methods
    def action_open_wizard(self):
        """Opens wizard form"""
        client_id = None
        service_ids = []
        # if user open wizard with provided service action
        if self._context.get('active_ids'):
            # search all selected services
            services = self.env['car.service.provided.service'].browse(
                self._context['active_ids']
            )
            # add services with the same client
            for service in services:
                if not client_id:
                    client_id = service.client_id.id
                    service_ids.append(service.id)
                    continue
                elif client_id == service.client_id.id:
                    service_ids.append(service.id)
        # open wizard form with default data
        return {
            'name': _('Create Invoice Wizard'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'create.invoice.wizard',
            'target': 'new',
            'context': {
                'default_client_id': client_id,
                'default_service_ids': service_ids,
            }
        }

    def action_create_invoice(self):
        """Creates invoice and opens form view"""
        self.ensure_one()
        invoice = self.env['car.service.invoice'].create({
            'client_id': self.client_id.id,
            'service_ids': self.service_ids.ids,
        })
        # Open tree,form views with new invoice
        return {
            'name': _(f'Invoice {invoice.name}'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'car.service.invoice',
            'target': 'current',
            'domain': [('id', '=', invoice.id)],
        }
