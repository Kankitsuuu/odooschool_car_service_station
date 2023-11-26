from odoo.tests.common import TransactionCase


class TestCommon(TransactionCase):

    def setUp(self):
        super(TestCommon, self).setUp()
        self.group_car_service_user = self.env.ref(
            'os_car_service.group_car_service_user'
        )
        self.group_car_service_worker = self.env.ref(
            'os_car_service.group_car_service_worker'
        )
        self.group_car_service_admin = self.env.ref(
            'os_car_service.group_car_service_admin'
        )
        self.car_service_user = self.env['res.users'].create({
            'name': 'Car Service User',
            'login': 'car_service_user',
            'groups_id': [
                (4, self.env.ref('base.group_user').id),
                (4, self.group_car_service_user.id),
            ]
        })
        self.car_service_worker = self.env['res.users'].create({
            'name': 'Car Service Worker',
            'login': 'car_service_worker',
            'groups_id': [
                (4, self.env.ref('base.group_user').id),
                (4, self.group_car_service_worker.id),
            ]
        })
        self.car_service_admin = self.env['res.users'].create({
            'name': 'Car Service Admin',
            'login': 'car_service_admin',
            'groups_id': [
                (4, self.env.ref('base.group_user').id),
                (4, self.group_car_service_admin.id),
            ]
        })
        self.client_demo = self.env['car.service.client'].create({
            'name': 'Client',
            'surname': 'Demo',
        })
        self.worker_demo = self.env['car.service.worker'].create({
            'name': 'Worker',
            'surname': 'Demo',
            'birth_date': '2001-04-26',
            'address': 'Demo str., Apt. 54',
            'passport': 'AAA111222',
        })
        self.car_make_demo = self.env['car.service.client.car.make'].create({
            'name': 'Demo make',
        })
        self.car_color_demo = self.env['car.service.client.car.color'].create({
            'name': 'Demo color',
            'technical_code': 'Demo code',
        })
        self.client_car_demo = self.env['car.service.client.car'].create({
            'client_id': self.client_demo.id,
            'make_id': self.car_make_demo.id,
            'color_id': self.car_color_demo.id,
            'model': 'Demo car model',
            'number': 'Demo1111',
        })
        self.service_category_demo = self.env['car.service.service.category'].create({
            'name': 'Demo service category',
        })
        self.service_demo = self.env['car.service.service'].create({
            'name': 'Demo service',
            'price': 100,
            'category_id': self.service_category_demo.id,
        })
        self.provided_service_demo = self.env['car.service.provided.service'].create({
            'client_id': self.client_demo.id,
            'car_id': self.client_car_demo.id,
            'service_id': self.service_demo.id,
            'worker_id': self.worker_demo.id,
        })
        self.invoice_demo = self.env['car.service.invoice'].create({
            'client_id': self.client_demo.id,
            'service_ids': [(6, 0, [self.provided_service_demo.id])],
        })
