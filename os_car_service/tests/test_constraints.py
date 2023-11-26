from datetime import datetime, timedelta

from odoo.tests import tagged
from odoo.exceptions import ValidationError
from .common import TestCommon


@tagged('post_install', '-at_install', 'constraints', 'car_service')
class TestConstraints(TestCommon):

    def test_01_car_service_person(self):
        # Person (Client and Worker) phone number must be unique
        self.env['car.service.client'].create({
            'name': 'Bart',
            'surname': 'Simpson',
            'phone': '+000-000-00-00',
        })
        self.env['car.service.worker'].create({
            'name': 'Bart',
            'surname': 'Simpson',
            'phone': '+000-000-00-00',
            'birth_date': '2001-01-01',
            'address': 'Test str., Apt. 101',
            'passport': 'TEST010101',
        })

        with self.assertRaises(ValidationError):
            self.client_demo.write({
                'phone': '+000-000-00-00',
            })

        with self.assertRaises(ValidationError):
            self.worker_demo.write({
                'phone': '+000-000-00-00',
            })

    def test_02_car_service_worker(self):
        # Worker passport data must be unique
        with self.assertRaises(ValidationError):
            self.env['car.service.worker'].create({
                'name': 'Worker',
                'surname': 'Test',
                'birth_date': '2000-01-01',
                'address': 'Test str., Apt. 100',
                'passport': 'AAA111222',
            })

    def test_03_car_service_client_car_color(self):
        # Car color technical code must be unique
        with self.assertRaises(ValidationError):
            self.env['car.service.client.car.color'].create({
                'name': 'Test color',
                'technical_code': 'Demo code',
            })

    def test_04_car_service_client_car(self):
        # Car number must be unique
        with self.assertRaises(ValidationError):
            self.env['car.service.client.car'].create({
                'client_id': self.client_demo.id,
                'make_id': self.car_make_demo.id,
                'color_id': self.car_color_demo.id,
                'model': 'Test car model',
                'number': 'Demo1111',
            })

    def test_05_car_service_provided_service(self):
        # Unlink invoice to test provided service
        self.invoice_demo.unlink()

        # Service amount must be 1 or bigger
        with self.assertRaises(ValidationError):
            self.provided_service_demo.write({
                'amount': 0,
            })

        # Set date for provided service can not be future date
        with self.assertRaises(ValidationError):
            future_date = (datetime.now() + timedelta(days=5)).date()
            self.provided_service_demo.write({
                'set_date': future_date.strftime('%Y-%m-%d')
            })

        # Provided service car must belong to the chosen client
        test_client = self.env['car.service.client'].create({
            'name': 'Bart',
            'surname': 'Simpson',
        })
        test_client_car = self.env['car.service.client.car'].create({
            'client_id': test_client.id,
            'make_id': self.car_make_demo.id,
            'color_id': self.car_color_demo.id,
            'model': 'Test car model',
            'number': 'TEST1111',
        })
        with self.assertRaises(ValidationError):
            self.provided_service_demo.write({
                'car_id': test_client_car.id,
            })

    def test_06_car_service_invoice(self):
        # Invoice must contain at least one provided service
        with self.assertRaises(ValidationError):
            self.invoice_demo.write({
                'service_ids': [(6, 0, [])]
            })

        # Invoice cannot contain provided services for other clients
        test_client = self.env['car.service.client'].create({
            'name': 'Bart',
            'surname': 'Simpson',
        })
        test_client_car = self.env['car.service.client.car'].create({
            'client_id': test_client.id,
            'make_id': self.car_make_demo.id,
            'color_id': self.car_color_demo.id,
            'model': 'Test car model',
            'number': 'TEST1111',
        })
        test_provided_service = self.env['car.service.provided.service'].create({
            'client_id': test_client.id,
            'car_id': test_client_car.id,
            'service_id': self.service_demo.id,
            'worker_id': self.worker_demo.id,
        })
        with self.assertRaises(ValidationError):
            self.invoice_demo.write({
                'service_ids': [(6, 0, [test_provided_service.id])]
            })

        # Invoice cannot contain already invoiced services
        with self.assertRaises(ValidationError):
            self.env['car.service.invoice'].create({
                'client_id': self.client_demo.id,
                'service_ids': [(6, 0, [self.provided_service_demo.id])],
            })
