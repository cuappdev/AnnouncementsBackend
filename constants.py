import json

INVALID_ANNOUNCEMENT_ID_ERROR = json.dumps({"success": False, "error": "No announcement with that id exists"})
INVALID_APP_NAME_ERROR = json.dumps({"success": False, "error": "Invalid app identifier(s)"})
INVALID_DATE_ERROR = json.dumps({"success": False, "error": "Please input a valid date of the form 'mm/dd/yyyy'"})
INVALID_REQUEST_BODY_ERROR = json.dumps({"success": False, "error": "Invalid request body"})
INVALID_REQUEST_TOKEN_ERROR = json.dumps({"success": False, "error": "Invalid access token"})
MISSING_REQUEST_TOKEN_ERROR = json.dumps({"success": False, "error": "Missing access token"})
SUCCESSFUL_RESPONSE = json.dumps({"success": True})

EDITABLE_ANNOUNCEMENT_FIELDS = [
    "body",
    "cta_action",
    "cta_button_color",
    "cta_text",
    "expiration_date",
    "image_height",
    "image_url",
    "image_width",
    "included_apps",
    "subject",
    "start_date",
]
VALID_APPS = ["pollo", "eatery", "transit", "uplift", "coursegrab"]
