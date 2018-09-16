import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class MaintanenceSchemeTestCase(APITestCase):
    def test_post(self):
        data = {
            "DM_capacity": 20,
            "DE_capacity": 8,
            "data_centers": [
                {"name": "Paris", "servers": 20},
                {"name": "Stockholm", "servers": 62}
            ]
        }
        expected_output = {
            'DE': 8,
            'DM_data_center': "Paris"
        }
        url = reverse("maintenance:maintenance_scheme")
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')

        self.assertEquals(response.json(), expected_output)

    def test_post_empty_parameter(self):
        data = {
            "DE_capacity": 9,
            "data_centers": [
                {"name": "Paris", "servers": 20},
                {"name": "Stockholm", "servers": 62}
            ]
        }
        url = reverse("maintenance:maintenance_scheme")
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')

        self.assertTrue(response.exception)
        self.assertEquals(response.json()['detail'], 'One or more required parameters are empty')
        self.assertEquals(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_post_wrong_parameter_type(self):
        data = {
            "DM_capacity": 'eleven',
            "DE_capacity": 9,
            "data_centers": [
                {"name": "Paris", "servers": 20},
                {"name": "Stockholm", "servers": 62}
            ]
        }
        url = reverse("maintenance:maintenance_scheme")
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')

        self.assertTrue(response.exception)
        self.assertEquals(response.json()['detail'], 'DM_capacity has to be a positive integer')
        self.assertEquals(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_post_not_positive_servers(self):
        data = {
            "DM_capacity": 11,
            "DE_capacity": 9,
            "data_centers": [
                {"name": "Paris", "servers": 0},
                {"name": "Stockholm", "servers": 62}
            ]
        }
        url = reverse("maintenance:maintenance_scheme")
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')

        self.assertTrue(response.exception)
        self.assertEquals(response.json()['detail'], 'Servers field has to be a positive integer')
        self.assertEquals(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_post_not_unique_names(self):
        data = {
            "DM_capacity": 11,
            "DE_capacity": 9,
            "data_centers": [
                {"name": "Paris", "servers": 10},
                {"name": "Paris", "servers": 62}
            ]
        }
        url = reverse("maintenance:maintenance_scheme")
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')

        self.assertTrue(response.exception)
        self.assertEquals(response.json()['detail'], 'City names have to be unique')
        self.assertEquals(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)