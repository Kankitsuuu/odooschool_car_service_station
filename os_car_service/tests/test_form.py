import hashlib
from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo.tests import tagged
from odoo.tests.common import Form
from .common import TestCommon


@tagged('post_install', '-at_install', 'form', 'car_service')
class TestForm(TestCommon):

    def test_01_car_service_client(self):
        client_form = Form(self.client_demo)
        self.assertEqual(client_form.service_total, 1)
        self.assertEqual(client_form.invoice_total, 1)

    def test_02_car_service_worker(self):
        worker_form = Form(self.worker_demo)
        self.assertEqual(worker_form.service_total, 1)
        birth_date = datetime.now() - relativedelta(years=22) + relativedelta(days=5)
        worker_form.birth_date = birth_date.date()
        worker_form.save()
        self.assertEqual(self.worker_demo.age, 21)

    def test_03_car_service_car_color(self):
        test_color = self.env['car.service.client.car.color'].create({
            'name': 'Test color',
            'technical_code': 'Test code111',
        })
        color_form = Form(test_color)
        self.assertEqual(color_form.is_metallic, True)

    def test_04_car_service_client_car(self):
        car_form = Form(self.client_car_demo)
        self.assertEqual(car_form.service_total, 1)
        car_form.model = 'TEST'
        car_form.number = 'TEST1111'
        car_form.save()
        self.assertEqual(
            self.client_car_demo.name,
            'Demo make TEST Demo color TEST1111'
        )

    def test_05_car_service_service(self):
        test_service = self.env['car.service.service'].create({
            'name': 'Test service',
            'price': 1500,
        })
        service_form = Form(test_service)
        self.assertEqual(
            service_form.category_id.id,
            self.env.ref('os_car_service.service_category_other').id,
        )

    def test_06_car_service_provided_service(self):
        provided_service = self.env['car.service.provided.service'].create({
            'client_id': self.client_demo.id,
            'car_id': self.client_car_demo.id,
            'service_id': self.service_demo.id,
            'worker_id': self.worker_demo.id,
            'set_date': datetime(2000, 1, 1).strftime('%Y-%m-%d'),
        })
        provided_service_form = Form(provided_service)
        provided_service_form.amount = 5
        provided_service_form.save()
        predicted_name_data = f'2000-01-01{self.client_demo.id}'
        predicted_name = hashlib.sha512(
            predicted_name_data.encode()
        ).hexdigest()
        self.assertEqual(provided_service.name, predicted_name[:8].upper())
        self.assertEqual(provided_service.price_total, 500)
        self.assertFalse(provided_service.is_paid)

    def test_07_car_service_invoice(self):
        invoice_form = Form(self.invoice_demo)
        self.assertEqual(invoice_form.price, 100)
