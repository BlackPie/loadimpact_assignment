from rest_framework.exceptions import APIException


class MissedParameterException(APIException):
    status_code = 422
    default_detail = 'One or more required parameters are empty'
    default_code = 'missed_parameter'


class WrongParameterException(APIException):
    status_code = 422
    default_detail = "Wrong parameter's type"
    default_code = "wrong_parameter"
