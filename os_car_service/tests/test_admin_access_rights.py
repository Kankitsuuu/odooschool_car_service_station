from odoo.tests import tagged
from .common import TestCommon


@tagged('post_install', '-at_install', 'access', 'admin_access', 'car_service')
class TestAdminAccessRights(TestCommon):

    def test_01_car_service_admin_models_read(self):
        self.client_demo.with_user(self.car_service_admin).read()
        self.worker_demo.with_user(self.car_service_admin).read()
        self.car_make_demo.with_user(self.car_service_admin).read()
        self.car_color_demo.with_user(self.car_service_admin).read()
        self.client_car_demo.with_user(self.car_service_admin).read()
        self.service_category_demo.with_user(self.car_service_admin).read()
        self.service_demo.with_user(self.car_service_admin).read()
        self.provided_service_demo.with_user(self.car_service_admin).read()
        self.invoice_demo.with_user(self.car_service_admin).read()

    def test_02_car_service_admin_client_access_rights(self):
        # Create
        test_client = self.env['car.service.client'].with_user(
            self.car_service_admin
        ).create({
            'name': 'Bart',
            'surname': 'Simpson',
        })
        # Write
        test_client.with_user(self.car_service_admin).write({
            'name': 'Harry',
            'surname': 'Potter',
        })
        # Unlink
        test_client.with_user(self.car_service_admin).unlink()

    def test_03_car_service_admin_worker_access_rights(self):
        # Create
        test_worker = self.env['car.service.worker'].with_user(
            self.car_service_admin
        ).create({
            'name': 'Bart',
            'surname': 'Simpson',
            'birth_date': '2000-01-01',
            'address': 'Demo str., Apt. 1',
            'passport': 'BBB222333',
        })
        # Write
        test_worker.with_user(self.car_service_admin).write({
            'name': 'Harry',
            'surname': 'Potter',
        })
        # Unlink
        test_worker.with_user(self.car_service_admin).unlink()

    def test_04_car_service_admin_car_make_access_rights(self):
        # Create
        test_car_make = self.env['car.service.client.car.make'].with_user(
            self.car_service_admin
        ).create({
            'name': 'Test make',
        })
        # Write
        test_car_make.with_user(
            self.car_service_admin
        ).write({
            'name': 'Test make change',
        })
        # Unlink
        test_car_make.with_user(self.car_service_admin).unlink()

    def test_05_car_service_admin_car_color_access_rights(self):
        # Create
        test_car_color = self.env['car.service.client.car.color'].with_user(
            self.car_service_admin
        ).create({
            'name': 'Test color',
            'technical_code': 'Test code222',
        })
        # Write
        test_car_color.with_user(
            self.car_service_admin
        ).write({
            'name': 'Test color change',
        })
        # Unlink
        test_car_color.with_user(self.car_service_admin).unlink()

    def test_06_car_service_admin_client_car_access_rights(self):
        # Create
        test_car = self.env['car.service.client.car'].with_user(
            self.car_service_admin
        ).create({
            'client_id': self.client_demo.id,
            'make_id': self.car_make_demo.id,
            'color_id': self.car_color_demo.id,
            'model': 'Test car model',
            'number': 'TEST0505',
        })
        # Write
        test_car.with_user(self.car_service_admin).write({
            'model': 'Test car model change',
        })
        # Unlink
        test_car.with_user(self.car_service_admin).unlink()

    def test_07_car_service_admin_service_category_access_rights(self):
        # Create
        test_service_category = self.env['car.service.service.category'].with_user(
            self.car_service_admin
        ).create({
            'name': 'Test service category',
        })
        # Write
        test_service_category.with_user(self.car_service_admin).write({
            'name': 'Test service category change',
        })
        # Unlink
        test_service_category.with_user(self.car_service_admin).unlink()

    def test_08_car_service_admin_service_access_rights(self):
        # Create
        test_service = self.env['car.service.service'].with_user(
            self.car_service_admin
        ).create({
            'name': 'Test service',
            'price': 150,
            'category_id': self.service_category_demo.id,
        })
        # Write
        test_service.with_user(self.car_service_admin).write({
            'name': 'Test service change',
        })
        # Unlink
        test_service.with_user(self.car_service_admin).unlink()

    def test_09_car_service_admin_provided_service_access_rights(self):
        # Create
        test_provided_service = self.env['car.service.provided.service'].with_user(
            self.car_service_admin
        ).create({
            'client_id': self.client_demo.id,
            'car_id': self.client_car_demo.id,
            'service_id': self.service_demo.id,
            'worker_id': self.worker_demo.id,
        })
        # Write
        test_worker = self.env['car.service.worker'].create({
            'name': 'Worker',
            'surname': 'Test',
            'birth_date': '2002-08-16',
            'address': 'Demo str., Apt. 220',
            'passport': 'BBB111222',
        })
        test_provided_service.with_user(self.car_service_admin).write({
            'worker_id': test_worker.id,
        })
        # Unlink
        test_provided_service.with_user(self.car_service_admin).unlink()

    def test_10_car_service_admin_invoice_access_rights(self):
        # Unlink
        self.invoice_demo.with_user(self.car_service_admin).unlink()

        # Create
        test_invoice = self.env['car.service.invoice'].with_user(
            self.car_service_admin
        ).create({
            'client_id': self.client_demo.id,
            'service_ids': [(6, 0, [self.provided_service_demo.id])],
        })
        # Write
        test_client = self.env['car.service.client'].create({
            'name': 'Bart',
            'surname': 'Simpson',
        })
        test_client_car = self.env['car.service.client.car'].create({
            'client_id': test_client.id,
            'make_id': self.car_make_demo.id,
            'color_id': self.car_color_demo.id,
            'model': 'X1010',
            'number': 'TEST1010',
        })
        test_provided_service = self.env['car.service.provided.service'].create({
            'client_id': test_client.id,
            'car_id': test_client_car.id,
            'service_id': self.service_demo.id,
            'worker_id': self.worker_demo.id,
        })
        test_invoice.with_user(self.car_service_admin).write({
            'client_id': test_client.id,
            'service_ids': [(6, 0, [test_provided_service.id])],
        })
