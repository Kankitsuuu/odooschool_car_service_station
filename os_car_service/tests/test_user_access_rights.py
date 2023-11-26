from odoo.tests import tagged
from odoo.exceptions import AccessError
from .common import TestCommon


@tagged('post_install', '-at_install', 'access', 'user_access', 'car_service')
class TestUserAccessRights(TestCommon):

    def test_01_car_service_user_models_read(self):
        self.client_demo.with_user(self.car_service_user).read()
        self.worker_demo.with_user(self.car_service_user).read()
        self.car_make_demo.with_user(self.car_service_user).read()
        self.car_color_demo.with_user(self.car_service_user).read()
        self.client_car_demo.with_user(self.car_service_user).read()
        self.service_category_demo.with_user(self.car_service_user).read()
        self.service_demo.with_user(self.car_service_user).read()
        self.provided_service_demo.with_user(self.car_service_user).read()
        self.invoice_demo.with_user(self.car_service_user).read()

    def test_02_car_service_user_client_access_rights(self):
        # Create
        with self.assertRaises(AccessError):
            self.env['car.service.client'].with_user(self.car_service_user).create({
                'name': 'Bart',
                'surname': 'Simpson',
            })
        # Write
        with self.assertRaises(AccessError):
            self.client_demo.with_user(self.car_service_user).write({
                'name': 'Bart',
                'surname': 'Simpson',
            })
        # Unlink
        with self.assertRaises(AccessError):
            self.client_demo.with_user(self.car_service_user).unlink()

    def test_03_car_service_user_worker_access_rights(self):
        # Create
        with self.assertRaises(AccessError):
            self.env['car.service.worker'].with_user(self.car_service_user).create({
                'name': 'Bart',
                'surname': 'Simpson',
                'birth_date': '2000-05-25',
                'address': 'Demo str., Apt. 100',
                'passport': 'AAA222333',
            })
        # Write
        with self.assertRaises(AccessError):
            self.worker_demo.with_user(self.car_service_user).write({
                'name': 'Bart',
                'surname': 'Simpson',
            })
        # Unlink
        with self.assertRaises(AccessError):
            self.worker_demo.with_user(self.car_service_user).unlink()

    def test_04_car_service_user_car_make_access_rights(self):
        # Create
        with self.assertRaises(AccessError):
            self.env['car.service.client.car.make'].with_user(
                self.car_service_user
            ).create({
                'name': 'Nissan',
            })
        # Write
        with self.assertRaises(AccessError):
            self.car_make_demo.with_user(self.car_service_user).write({
                'name': 'Nissan',
            })
        # Unlink
        with self.assertRaises(AccessError):
            self.car_make_demo.with_user(self.car_service_user).unlink()

    def test_05_car_service_user_car_color_access_rights(self):
        # Create
        with self.assertRaises(AccessError):
            self.env['car.service.client.car.color'].with_user(
                self.car_service_user
            ).create({
                'name': 'Purple demo',
                'technical_code': 'Demo code 222',
            })
        # Write
        with self.assertRaises(AccessError):
            self.car_color_demo.with_user(self.car_service_user).write({
                'name': 'WHITE',
            })
        # Unlink
        with self.assertRaises(AccessError):
            self.car_color_demo.with_user(self.car_service_user).unlink()

    def test_06_car_service_user_client_car_access_rights(self):
        # Create
        with self.assertRaises(AccessError):
            self.env['car.service.client.car'].with_user(
                self.car_service_user
            ).create({
                'client_id': self.client_demo.id,
                'make_id': self.car_make_demo.id,
                'color_id': self.car_color_demo.id,
                'model': 'X6',
                'number': 'Test2222',
            })
        # Write
        with self.assertRaises(AccessError):
            self.client_car_demo.with_user(self.car_service_user).write({
                'model': 'X6',
            })
        # Unlink
        with self.assertRaises(AccessError):
            self.client_car_demo.with_user(self.car_service_user).unlink()

    def test_07_car_service_user_service_category_access_rights(self):
        # Create
        with self.assertRaises(AccessError):
            self.env['car.service.service.category'].with_user(
                self.car_service_user
            ).create({
                'name': 'Test category',
            })
        # Write
        with self.assertRaises(AccessError):
            self.service_category_demo.with_user(
                self.car_service_user
            ).write({
                'name': 'Test category',
            })
        # Unlink
        with self.assertRaises(AccessError):
            self.service_category_demo.with_user(
                self.car_service_user
            ).unlink()

    def test_08_car_service_user_service_access_rights(self):
        # Create
        with self.assertRaises(AccessError):
            self.env['car.service.service'].with_user(self.car_service_user).create({
                'name': 'Test service',
                'price': 10_000,
                'category_id': self.service_category_demo.id,
            })
        # Write
        with self.assertRaises(AccessError):
            self.service_demo.with_user(
                self.car_service_user
            ).write({
                'name': 'Test service',
            })
        # Unlink
        with self.assertRaises(AccessError):
            self.service_demo.with_user(self.car_service_user).unlink()

    def test_09_car_service_user_provided_service_access_rights(self):
        # Create
        with self.assertRaises(AccessError):
            self.env['car.service.provided.service'].with_user(
                self.car_service_user
            ).create({
                'client_id': self.client_demo.id,
                'car_id': self.client_car_demo.id,
                'service_id': self.service_demo.id,
                'worker_id': self.worker_demo.id,
            })
        # Write
        with self.assertRaises(AccessError):
            test_worker = self.env['car.service.worker'].create({
                'name': 'Worker',
                'surname': 'Test',
                'birth_date': '2002-08-16',
                'address': 'Demo str., Apt. 220',
                'passport': 'BBB111222',
            })
            self.service_demo.with_user(self.car_service_user).write({
                'worker_id': test_worker.id,
            })
        # Unlink
        with self.assertRaises(AccessError):
            self.invoice_demo.unlink()
            self.provided_service_demo.with_user(self.car_service_user).unlink()

    def test_10_car_service_user_invoice_access_rights(self):
        # Write
        with self.assertRaises(AccessError):
            test_client = self.env['car.service.client'].create({
                'name': 'Bart',
                'surname': 'Simpson',
            })
            test_client_car = self.env['car.service.client.car'].create({
                'client_id': test_client.id,
                'make_id': self.car_make_demo.id,
                'color_id': self.car_color_demo.id,
                'model': 'X1000',
                'number': 'TEST1010',
            })
            test_provided_service = self.env['car.service.provided.service'].create({
                'client_id': test_client.id,
                'car_id': test_client_car.id,
                'service_id': self.service_demo.id,
                'worker_id': self.worker_demo.id,
            })
            self.service_demo.with_user(
                self.car_service_user
            ).write({
                'client_id': test_client.id,
                'service_ids': [(6, 0, [test_provided_service.id])],
            })
        # Unlink
        with self.assertRaises(AccessError):
            self.invoice_demo.with_user(self.car_service_user).unlink()
        # Create
        with self.assertRaises(AccessError):
            self.invoice_demo.unlink()
            self.env['car.service.invoice'].with_user(self.car_service_user).create({
                'client_id': self.client_demo.id,
                'service_ids': [(6, 0, [self.provided_service_demo.id])],
            })
