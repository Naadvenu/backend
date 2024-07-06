#models/response_model.py
def create_response(message, status_code, status, data=None):
    response = {
        "message": message,
        "status": status,
        "status_code": status_code
    }
    if data:
        response["data"] = data
    return response