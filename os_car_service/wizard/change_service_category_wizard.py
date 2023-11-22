from odoo import models, fields, _


class ChangeServiceCategoryWizard(models.TransientModel):
    _name = 'change.service.category.wizard'
    _description = 'Wizard to change service category'

    category_id = fields.Many2one(
        comodel_name='car.service.service.category',
        required=True,
    )

    # Action methods
    def action_open_wizard(self):
        """Opens wizard form"""

        # if user select only one record
        if len(self._context['active_ids']) == 1:
            service = self.env['car.service.service'].browse(
                self._context['active_ids'][0]
            )
            service.ensure_one()
            category_id = service.category_id.id

        else:
            # set default category id as "Other" category
            category_id = self.env.ref('os_car_service.service_category_other').id

        return {
            'name': _('Change Service Category Wizard'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'change.service.category.wizard',
            'target': 'new',
            'context': {'default_category_id': category_id}
        }

    def action_change_price(self):
        """Change price and/or currency for selected services"""
        self.ensure_one()
        services = self.env['car.service.service'].browse(
            self._context['active_ids']
        )
        for service in services:
            service.write({
                'category_id': self.category_id.id,
            })
