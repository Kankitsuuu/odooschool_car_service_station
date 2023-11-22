from odoo import models, fields, _


class ChangeServicePriceWizard(models.TransientModel):
    _name = 'change.service.price.wizard'
    _description = 'Wizard to change service price'

    price = fields.Float(
        required=True,
        string='New price',
        digits=(12, 2),
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        required=True,
    )

    # Action methods

    def action_open_wizard(self):
        """Opens wizard form"""
        service = self.env['car.service.service'].browse(
            self._context['active_ids'][0]
        )
        service.ensure_one()
        price = service.price
        currency_id = service.currency_id.id
        return {
            'name': _('Change Service Price Wizard'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'change.service.price.wizard',
            'target': 'new',
            'context': {
                'default_price': price,
                'default_currency_id': currency_id,
            }
        }

    def action_change_price(self):
        """Change price and/or currency for selected services"""
        self.ensure_one()
        services = self.env['car.service.service'].browse(
            self._context['active_ids']
        )
        for service in services:
            service.write({
                'price': self.price,
                'currency_id': self.currency_id.id,
            })

