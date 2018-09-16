import copy
import random
import string
import time

from django.test import tag, TestCase

from project.apps.maintenance import utils


class GetMaintenanceSchemeTestCase(TestCase):
    def test_get_maintenance_scheme_zero_leftover(self):
        dm_capacity = 20
        de_capacity = 8
        data_centers = [
            {'name': 'Paris', 'servers': 20},
            {'name': 'Stockholm', 'servers': 62}
        ]
        de_count, city = utils.get_maintenance_scheme(de_capacity, dm_capacity, data_centers)

        self.assertEquals(de_count, 8)
        self.assertEquals(city, 'Paris')

    def test_get_maintenance_scheme_de_bigger_than_dm(self):
        dm_capacity = 6
        de_capacity = 10
        data_centers = [
            {'name': 'Paris', 'servers': 30},
            {'name': 'Stockholm', 'servers': 66}
        ]
        de_count, city = utils.get_maintenance_scheme(de_capacity, dm_capacity, data_centers)

        self.assertEquals(de_count, 9)
        self.assertEquals(city, 'Stockholm')

    def test_get_maintenance_scheme_server_count_less_than_dm(self):
        dm_capacity = 12
        de_capacity = 7
        data_centers = [
            {'name': 'Berlin', 'servers': 11},
            {'name': 'Stockholm', 'servers': 21}
        ]
        de_count, city = utils.get_maintenance_scheme(de_capacity, dm_capacity, data_centers)

        self.assertEquals(de_count, 3)
        self.assertEquals(city, 'Berlin')

    def test_get_maintenance_scheme_server_count_less_than_dm_and_de(self):
        dm_capacity = 12
        de_capacity = 7
        data_centers = [
            {'name': 'Berlin', 'servers': 6},
            {'name': 'Stockholm', 'servers': 21}
        ]
        de_count, city = utils.get_maintenance_scheme(de_capacity, dm_capacity, data_centers)

        self.assertEquals(de_count, 3)
        self.assertIn(city, ('Stockholm', 'Berlin'))


class PerfomanceTestCase(TestCase):
    @tag("perfomance")
    def test_perfomance(self):
        dm_capacity = random.randint(1, 15)
        de_capacity = random.randint(1, 15)
        data_centers = list()

        for i in range(50):
            for j in range(30):
                name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
                servers = random.randint(1, 100)
                data_centers.append({'name': name, 'servers': servers})

            data_centers_copy = copy.deepcopy(data_centers)
            start = time.clock()
            de_count1, city1 = utils.get_maintenance_scheme(de_capacity, dm_capacity, data_centers_copy)
            print('Basic:  ', time.clock() - start)

            data_centers_copy = copy.deepcopy(data_centers)
            start = time.clock()
            de_count2, city2 = utils.get_maintenance_scheme_system_of_equations(de_capacity, dm_capacity, data_centers_copy)
            print('Equations:  ', time.clock() - start)

            data_centers_copy = copy.deepcopy(data_centers)
            start = time.clock()
            de_count3, city3 = utils.get_maintenance_scheme_pulp_optimization(de_capacity, dm_capacity, data_centers_copy)
            print('PuLP:  ', time.clock() - start)
            print(' ')

            if de_count1 != de_count3 or de_count1 != de_count2:
                print("Answers dont match")
                print("1:  ", de_count1, city1)
                print("2:  ", de_count2, city2)
                print("3:  ", de_count3, city3)
