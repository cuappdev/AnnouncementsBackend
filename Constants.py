import json

INVALID_DATE_ERROR = json.dumps({"success": False, "error": "Please input a valid date of the form 'y/m/d'"})

INVALID_ANNOUNCEMENT_ERROR = json.dumps({"success": False, "error": "No announcement with that id exists"})

INVALID_REQUEST_BODY_ERROR = json.dumps({"success": False, "error": "Invalid Request Body"})

SUCCESSFUL_RESPONSE = json.dumps({"success": True})

INVALID_APP_ERROR = json.dumps({"success": False, "error": "Invalid App Identifier(s)"})

VALID_APPS = ["pollo", "eatery", "transit", "uplift"]
