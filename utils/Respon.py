import json


def response_success(data=None):
    return json.dumps({"status_message": "", "status_error": 0, "data" : data},default=str)

def response_error(data=None):
    return json.dumps({"status_message": "Failure Request", "status_error": 1, "data" : data},default=str)

def response_socket(message='connected',status=0,data=None):
    return json.dumps({"status_message": message, "status_socket": status, "data" : data},default=str)
