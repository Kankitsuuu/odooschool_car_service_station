from datetime import datetime, timedelta

from odoo.tests import tagged
from odoo.exceptions import UserError
from .common import TestCommon


@tagged('post_install', '-at_install', 'crud', 'car_service')
class TestCRUD(TestCommon):

    def test_01_car_service_provided_service_crud(self):
        # User cannot change invoiced service
        with self.assertRaises(UserError):
            self.provided_service_demo.write({
                'amount': 5,
            })
        # User cannot delete invoiced service
        with self.assertRaises(UserError):
            self.provided_service_demo.unlink()

    def test_02_car_service_invoice_crud(self):
        set_date = (datetime.now() - timedelta(days=2))
        self.invoice_demo.write({
            'is_paid': True
        })

        # User cannot change paid invoices (except is_paid field)
        with self.assertRaises(UserError):
            self.invoice_demo.write({
                'set_date': set_date.strftime('%Y-%m-%d %H:%M')
            })

        # User cannot delete paid invoices
        with self.assertRaises(UserError):
            self.invoice_demo.unlink()

        self.invoice_demo.write({
            'is_paid': False
        })
        self.invoice_demo.write({
            'set_date': set_date.strftime('%Y-%m-%d %H:%M')
        })
        self.invoice_demo.unlink()
