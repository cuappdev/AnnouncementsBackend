import json

INVALID_DATE_ERROR = json.dumps({"success": False, "error": "Please input a valid date of the form 'mm/dd/yyyy'"})
INVALID_ANNOUNCEMENT_ID_ERROR = json.dumps({"success": False, "error": "No announcement with that id exists"})
INVALID_REQUEST_BODY_ERROR = json.dumps({"success": False, "error": "Invalid Request Body"})
SUCCESSFUL_RESPONSE = json.dumps({"success": True})
INVALID_APP_NAME_ERROR = json.dumps({"success": False, "error": "Invalid App Identifier(s)"})
EDITABLE_ANNOUNCEMENT_FIELDS = [
    "body",
    "cta_action",
    "cta_text",
    "expiration_date",
    "image_url",
    "included_apps",
    "subject",
    "start_date",
]
VALID_APPS = ["pollo", "eatery", "transit", "uplift"]
