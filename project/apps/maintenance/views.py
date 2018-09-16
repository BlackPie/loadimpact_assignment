from rest_framework.views import APIView
from rest_framework.response import Response

from project.apps.maintenance.utils import get_maintenance_scheme
from project.apps.maintenance.exceptions import MissedParameterException, WrongParameterException


class MaintenanceSchemeView(APIView):
    def post(self, *args, **kwargs):
        de_capacity = self.request.data.get('DE_capacity', None)
        dm_capacity = self.request.data.get('DM_capacity', None)
        data_centers = self.request.data.get('data_centers', None)

        if not all((dm_capacity, de_capacity, data_centers)):
            raise MissedParameterException()

        if not isinstance(de_capacity, int) or not de_capacity:
            raise WrongParameterException("DE_capacity has to be a positive integer")
        if not isinstance(dm_capacity, int) or not de_capacity:
            raise WrongParameterException("DM_capacity has to be a positive integer")
        if not isinstance(data_centers, list) or not len(data_centers):
            raise WrongParameterException("DM_capacity has to be a non-empty list")

        for data_center in data_centers:
            if not isinstance(data_center['servers'], int) or not data_center['servers']:
                raise WrongParameterException("Servers field has to be a positive integer")

        city_names = [x['name'] for x in data_centers]
        if not len(city_names) == len(set(city_names)):
            raise WrongParameterException("City names have to be unique")

        de_count, dm_data_center = get_maintenance_scheme(de_capacity, dm_capacity, data_centers)
        data = {
            "DE": de_count,
            "DM_data_center": dm_data_center,
        }
        return Response(data)
